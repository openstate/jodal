from ..config import settings
from ..schemas import ChatMessage
from ..models import Session
from qdrant_client import QdrantClient, models
import logging
from typing import List, Dict, AsyncGenerator, Tuple
from markdown import markdown 
import os
from ..services.base_llm_service import BaseLLMService
from ..text_utils import format_content
from fastembed.sparse import SparseTextEmbedding
from qdrant_client.http import models
from ..schemas import ChatDocument, Location
import threading
import queue
from contextlib import contextmanager
from datetime import datetime, date
import time
from typing import Optional
from .qdrant_pool import QdrantConnectionPool
from sklearn.metrics.pairwise import cosine_similarity
import numpy as np
import yaml
from ..text_utils import get_formatted_date_english
# Set up logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

class QdrantService:
    DENSE_VECTORS_NAME = "text-dense"
    SPARSE_VECTORS_NAME = "text-sparse"
    
    _sparse_document_embedder = None
    _embedder_lock = threading.Lock()
    # Adjust semaphore based on available CPU cores and workers
    # Using (CPU cores * 2) as a good balance for concurrent embeddings
    _query_semaphore = threading.BoundedSemaphore(16)  
    
    # Add batch size control for optimal memory usage
    BATCH_SIZE = 32  # Process embeddings in batches
    
    
    def __init__(self, llm_service: BaseLLMService):
        self.llm_service = llm_service
        self.dense_model_name = settings.COHERE_EMBED_MODEL
        self.sparse_model_name = settings.SPARSE_EMBED_MODEL
        self.pool = QdrantConnectionPool.get_instance()
        
    @classmethod
    def get_sparse_embedder(cls):
        if cls._sparse_document_embedder is None:
            with cls._embedder_lock:
                if cls._sparse_document_embedder is None:
                    models_dir = os.path.join(os.path.dirname(os.path.dirname(__file__)), 'models')
                    try:
                        # Set num_threads based on CPU cores while leaving room for other operations
                        cls._sparse_document_embedder = SparseTextEmbedding(
                            cache_dir=models_dir,
                            model_name=settings.SPARSE_EMBED_MODEL,
                            num_threads=4  # Half of CPU cores for embedding
                        )
                    except Exception as e:
                        logger.error(f"Failed to initialize sparse embedder: {e}")
                        raise
        return cls._sparse_document_embedder
        
        
    def generate_sparse_embedding(self, query: str):
        try:
            with self._query_semaphore:
                sparse_vectors = self.get_sparse_embedder().query_embed(query)
                return next(iter(sparse_vectors), None)
        except Exception as e:
            logger.error(f"Error generating sparse embedding: {e}")
            return None

    def get_documents_by_ids(self, documents: List[ChatDocument]):
        if not documents or len(documents) == 0:
            logger.debug("No documents provided to retrieve")
            return []
        
        qdrant_document_chunk_ids = []
        for doc in documents:
            if doc and doc.chunk_id:  # Add null check
                qdrant_document_chunk_ids.append(doc.chunk_id)
                    
        if not qdrant_document_chunk_ids:
            logger.warning("No valid document IDs found.")
            return []
        
        try:
            with self.pool.get_client() as client:
                qdrant_documents = client.retrieve(
                    collection_name=settings.QDRANT_COLLECTION,
                    ids=qdrant_document_chunk_ids,
                    with_payload=True,
                )
                
                # Convert records to the expected dictionary format
                qdrant_documents_dicts = [{
                    'id': record.id,
                    'payload': record.payload,
                    'rerank_score': 0.0
                } for record in qdrant_documents]
                
                return self._prepare_documents_with_scores_and_feedback(qdrant_documents_dicts, documents)
        except Exception as e:
            logger.error(f"Error retrieving documents from Qdrant using document IDs: {e}")
            return []

    def hybrid_search(self, query, locations: List[Location] = None, date_range: List[datetime] = None) -> List[Dict]:
        
        sparse_vector = self.generate_sparse_embedding(query)
        
        try:
            # Generate dense embeddings
            dense_vector = self.llm_service.generate_dense_embedding(query)
        except Exception as e:
            logger.error(f"Error creating dense vector from query using Cohere: {e}")
            raise   
        
        # Build filter conditions
        filter_conditions = []
        
        logger.debug("Adding location filters")
        
        if locations and len(locations) > 0:
            filter_conditions.append(
                models.FieldCondition(
                    key="meta.location",
                    match=models.MatchAny(any=[location.id for location in locations])
                )
            )
        
        if date_range and len(date_range) == 2:
            filter_conditions.append(
                models.FieldCondition(
                    key="meta.published",
                    range=models.DatetimeRange(
                        gte=date_range[0].strftime("%Y-%m-%dT%H:%M:%SZ"),
                        lte=date_range[1].strftime("%Y-%m-%dT%H:%M:%SZ")
                    )
                )
            )
        
        # Combine filters if any exist
        search_filter = None
        if filter_conditions:
            search_filter = models.Filter(
                must=filter_conditions,
            )
        
        logger.info(f"Retrieving documents from Qdrant for query using hybrid search: {query}, and filters: {search_filter}")        
        
        try:            
            logger.info(f"Querying vector database with query: '{query}'")
            with self.pool.get_client() as client:
                qdrant_documents = client.query_points(
                    collection_name=settings.QDRANT_COLLECTION,
                    prefetch=[
                        models.Prefetch(
                            query=models.SparseVector(
                                indices=sparse_vector.indices,
                                values=sparse_vector.values,
                            ),
                            using=self.SPARSE_VECTORS_NAME,
                            filter=search_filter,  # Apply filter to sparse search
                            limit=settings.QDRANT_SPARSE_RETRIEVE_LIMIT
                        ),
                        models.Prefetch(
                            query=dense_vector,
                            using=self.DENSE_VECTORS_NAME,
                            filter=search_filter,  # Apply filter to dense search
                            limit=settings.QDRANT_DENSE_RETRIEVE_LIMIT
                        ),
                    ],
                    query=models.FusionQuery(fusion=models.Fusion.RRF),
                    limit=settings.QDRANT_HYBRID_RETRIEVE_LIMIT,
                    score_threshold=None,
                    with_payload=True,
                    with_vectors=True,
                    timeout=settings.QDRANT_HYBRID_SEARCH_TIMEOUT,  # Increase timeout to 120 seconds
                ).points
                
        except Exception as e:
            logger.error(f"Error retrieving documents from Qdrant using hybrid search: {e}")   
            return None
        
        if not qdrant_documents:
            logger.warning("No documents found in Qdrant")
                    
        # Convert qdrant_document_candidates to a list of dictionaries
        qdrant_documents_dicts = self._qdrant_documents_searched_to_dicts(qdrant_documents)
        
        return qdrant_documents_dicts

    def dense_vector_search(self, query):   
        logger.debug(f"Retrieving documents from Qdrant for query: {query}")

        try:
            # Generate dense embeddings
            dense_vector = self.llm_service.generate_dense_embedding(query)
        except Exception as e:
            logger.error(f"Error creating dense vector from query using Cohere: {e}")
            return None

        try:
            qdrant_documents = self.pool.get_client().search(
                query_vector=(self.DENSE_VECTORS_NAME, dense_vector),
                collection_name=settings.QDRANT_COLLECTION,            
                limit=settings.QDRANT_DENSE_RETRIEVE_LIMIT   
            )
            
            if not qdrant_documents:
                logger.warning("No documents found in Qdrant")
            
            return qdrant_documents    
        except Exception as e:
            logger.error(f"Error retrieving documents from Qdrant using dense vector search: {e}")   
            return None

    def _qdrant_documents_retrieved_to_dicts(self, qdrant_documents):
        return [
            {
                'id': candidate.id,
                'payload': candidate.payload
            }
            for candidate in qdrant_documents
        ]  
        
    def _qdrant_documents_searched_to_dicts(self, qdrant_documents):
        return [
            {
                'id': candidate.id,
                'version': candidate.version,
                'score': candidate.score,
                'payload': candidate.payload,
                'vector': candidate.vector
            }
            for candidate in qdrant_documents
        ]   

    def retrieve_relevant_documents(self, query: str, locations: List[Location] = None, date_range: List[date] = None) -> List[Dict]:          
        logger.debug(f"Retrieving relevant documents for query: {query}")
        
        # Step 1: Retrieve initial candidates with filters
        qdrant_document_candidates = self.hybrid_search(query, locations, date_range)
        
        # Check if qdrant_documents is None or empty
        if not qdrant_document_candidates:
            logger.warning("No documents retrieved from Qdrant")
            return []
               
        # Step 2: Get relevance scores
        # document_texts = [document['payload']['content'] for document in qdrant_document_candidates]
        # Extract document metadata
        qdrant_document_candidates_with_payload = [{
            'Title': doc['payload']['meta']['title'],
            'Location': doc['payload']['meta']['location_name'],
            'Published': get_formatted_date_english(doc['payload']['meta']['published']),
            'Documents type': doc['payload']['meta']['type'],
            'Data source': doc['payload']['meta']['source'],
            'Document source': BaseLLMService.get_human_readable_source(doc['payload']['meta']['source']),
            'Content': doc['payload']['content']
        } for doc in qdrant_document_candidates]
        
        document_candidates_yaml = [yaml.dump(doc, sort_keys=False) for doc in qdrant_document_candidates_with_payload] 
                
        logger.debug(f"Reranking:\n\n {document_candidates_yaml[0]}...")
        reranked_documents = self.llm_service.rerank_documents(
            query=query,
            documents=document_candidates_yaml,
            top_n=settings.RERANK_DOC_RETRIEVE_LIMIT,
            return_documents=False
        )
        
        # Initialize all documents with a default rerank score
        for candidate in qdrant_document_candidates:
            candidate['rerank_score'] = 0.0
        
        # Update scores for documents that were reranked
        for candidate, reranked_doc in zip(qdrant_document_candidates, reranked_documents.results):
            try:
                candidate['rerank_score'] = reranked_doc.relevance_score
            except AttributeError as e:
                logger.warning(f"Could not get relevance score for document: {e}")
                # Keep default score of 0.0
        
        logger.info(f"Reranked documents: {len(qdrant_document_candidates)}")
                
        # Filter out candidates with low rerank scores
        qdrant_document_candidates = [
            candidate for candidate in qdrant_document_candidates 
            if candidate.get('rerank_score', 0.0) >= settings.RERANK_RELEVANCE_THRESHOLD
        ]        
        logger.info(f"Filtered documents: {len(qdrant_document_candidates)}")

        # Return early if no documents meet the threshold
        if not qdrant_document_candidates:
            logger.warning(f"No documents met the minimum score threshold of {settings.RERANK_RELEVANCE_THRESHOLD}")
            return []
        
        # Step 3: Compute similarity matrix
        dense_embeddings = [candidate['vector']['text-dense'] for candidate in qdrant_document_candidates]
        similarity_matrix = cosine_similarity(dense_embeddings)    
            
        # Step 4: Apply MMR
        logger.info(f"Applying MMR to {len(qdrant_document_candidates)} documents, to remove most similar documents, and keep {settings.MMR_DOC_RETRIEVE_LIMIT} documents")
        relevance_scores = [candidate.get('rerank_score', 0.0) for candidate in qdrant_document_candidates]
        diversified_candidates = self._mmr(
            documents=qdrant_document_candidates,
            query_embedding=dense_embeddings,
            relevance_scores=relevance_scores,
            similarity_matrix=similarity_matrix,
            lambda_param=settings.MMR_DOC_LAMBDA_PARAM,
            top_n=settings.MMR_DOC_RETRIEVE_LIMIT
        )
            
        return self.prepare_documents(diversified_candidates)
    
    def prepare_documents(self, qdrant_documents):
        return [self._prepare_document_dict(doc) for doc in qdrant_documents]

    def _prepare_documents_with_scores_and_feedback(self, qdrant_documents, documents: List[ChatDocument]):
        # Create a dictionary mapping document IDs to their scores
        score_map = {str(doc.chunk_id): doc.score for doc in documents}
        rerank_score_map = {str(doc.chunk_id): doc.rerank_score for doc in documents}
        feedback_map = {str(doc.chunk_id): doc.feedback for doc in documents}
        chunk_id_map = {str(doc.chunk_id): doc.id for doc in documents}
        
        return [
            self._prepare_document_dict(
                doc, 
                score_map.get(str(doc['id']), 0), 
                rerank_score_map.get(str(doc['id']), 0),
                feedback_map.get(str(doc['id']), None), 
                chunk_id_map.get(str(doc['id']), None)
            ) for doc in qdrant_documents
        ]
    
    def reorder_documents_by_publication_date(self, documents: List[Dict]):
        # Filter out ChatDocument instances and convert them to the expected format
        formatted_documents = []
        for doc in documents:
            if isinstance(doc, ChatDocument):
                # Skip ChatDocument instances as they don't contain publication dates
                continue
            formatted_documents.append(doc)
        
        return sorted(formatted_documents, key=lambda x: x['data']['published'], reverse=True)
    
    def _get_best_url(self, doc):
        url = ""
        if doc['payload']['meta']['doc_url']:
            url = doc['payload']['meta']['doc_url']
        elif doc['payload']['meta']['url']:
            url = doc['payload']['meta']['url'] 
        return url
    
    def _prepare_document_dict(self, doc, score=None, rerank_score=None, feedback=None, id=None):
        """Helper method to prepare a single document dictionary"""
        
        return {
            'id': id,  
            'chunk_id': doc['id'],
            'score': score if score is not None else doc['score'],
            'rerank_score': rerank_score if rerank_score is not None else doc['rerank_score'],
            'feedback': feedback,
            'data': {
                'source_id': doc['payload']['meta']['source_id'],
                'url': self._get_best_url(doc),
                'title': doc['payload']['meta']['title'],
                'location': doc['payload']['meta']['location'],
                'location_name': doc['payload']['meta']['location_name'],
                # 'modified': doc['payload']['meta']['modified'],
                'published': doc['payload']['meta']['published'],
                'type': doc['payload']['meta']['type'],
                'source': doc['payload']['meta']['source'],
                # 'page_number': doc.payload['meta']['page_number'],
                # 'page_count': doc['payload']['meta']['page_count'],
                'content': doc['payload']['content']
            }
        }
        
    def _mmr(self, documents, query_embedding, relevance_scores, similarity_matrix, lambda_param=0.7, top_n=10):
        selected = []
        candidate_indices = list(range(len(documents)))
        
        # Normalize relevance scores
        relevance_scores = np.array(relevance_scores)
        if relevance_scores.max() > relevance_scores.min():
            relevance_scores = (relevance_scores - relevance_scores.min()) / (relevance_scores.max() - relevance_scores.min())
        else:
            relevance_scores = np.ones_like(relevance_scores)

        while len(selected) < top_n and candidate_indices:
            mmr_scores = []
            for idx in candidate_indices:
                # Relevance to the query
                relevance = relevance_scores[idx]
                
                # Max similarity to already selected documents
                if selected:
                    sim_to_selected = max([similarity_matrix[idx][sel_idx] for sel_idx in selected])
                else:
                    sim_to_selected = 0
                
                # Calculate MMR score
                mmr_score = lambda_param * relevance - (1 - lambda_param) * sim_to_selected
                mmr_scores.append((mmr_score, idx))
            
            # Select the document with the highest MMR score
            mmr_scores.sort(reverse=True)
            selected_idx = mmr_scores[0][1]
            selected.append(selected_idx)
            candidate_indices.remove(selected_idx)
        
        # Return the selected documents
        return [documents[idx] for idx in selected]