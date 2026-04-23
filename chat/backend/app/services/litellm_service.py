import os
from ..config import settings
from litellm import completion, embedding, rerank
from litellm.exceptions import APIConnectionError, Timeout, APIError
import logging
from ..text_utils import get_formatted_current_date_english, get_formatted_current_year
from ..schemas import ChatMessage
from .base_llm_service import BaseLLMService
from typing import Generator
# Set up logging
logging.basicConfig(level=logging.DEBUG)
logger = logging.getLogger(__name__)

class LiteLLMService(BaseLLMService):    
    def __init__(self):
        os.environ["COHERE_API_KEY"] = settings.COHERE_API_KEY
        
    def chat_stream(self, messages: list[ChatMessage], documents: list) -> Generator:
        logger.info("Starting chat stream...")
        os.environ["COHERE_API_KEY"] = settings.COHERE_API_KEY
        
        # Flatten the documents structure
        flattened_docs = [{
            'id': doc['id'],
            'title': doc['data']['title'],
            'snippet': doc['data']['snippet'],
            'publication date': doc['data']['publication date'],
            'municipality': doc['data']['municipality'],
            'source': doc['data']['source'],
            'type': doc['data']['type']
        } for doc in documents]        
        
        system_prompt = messages[0].content
        
        # Log the messages and documents being sent
        logger.info(f"System_prompt being sent: {system_prompt}")
        logger.info(f"Messages being sent: {messages}")
        logger.info(f"Documents being sent: {flattened_docs[0]}")
        
        try:            
            return completion(
                model="cohere/command-r-plus-08-2024",
                messages=[{
                        'role': message.role, 
                        'content': message.get_param("formatted_content")
                    } for message in messages
                ],
                documents=flattened_docs,
                citation_quality="accurate",
                stream=True
            )            
                    
        except GeneratorExit:
            logger.info("Chat stream generator closed")
            return
        except APIConnectionError as e:
            logger.error(f'Chat stream connection failed: {e}')
            raise
        except Timeout as e:
            logger.error(f'Chat stream request timed out: {e}')
            raise
        except APIError as e:
            logger.error(f'Chat stream API error occurred: {e}')
            raise

    def rerank_documents(self, query: str, documents: list):
        logger.info("Reranking documents...")
        try:
            response = rerank(
                query=query,
                documents=documents,
                top_n=20,
                model=f"cohere/{settings.COHERE_RERANK_MODEL}",
                return_documents=True
            )            
            
            # Transform response to match expected format
            if hasattr(response, 'results'):
                # Create object with results attribute containing list of results
                class RerankedResult:
                    def __init__(self, index, relevance_score):
                        self.index = index
                        self.relevance_score = relevance_score
                
                transformed_response = type('RerankedResponse', (), {
                    'results': [
                        RerankedResult(
                            index=result['index'],
                            relevance_score=result['relevance_score']
                        ) for result in response.results
                    ]
                })
                
                return transformed_response
                
            return response         
        except APIConnectionError as e:
            logger.error(f'Reranking connection failed: {e}')
        except Timeout as e:
            logger.error(f'Reranking request timed out: {e}')
        except APIError as e:
            logger.error(f'Reranking API error occurred: {e}')

    def generate_dense_embedding(self, query: str):
        try:
            embedding_response = embedding(
                input=[query], 
                input_type="search_query", 
                model=f"cohere/{settings.COHERE_EMBED_MODEL}"
            )
                
            return embedding_response.data[0]['embedding']
        except APIConnectionError as e:
            logger.error(f'Embedding connection failed: {e}')
        except Timeout as e:
            logger.error(f'Embedding request timed out: {e}')
        except APIError as e:
            logger.error(f'Embedding API error occurred: {e}')         

    def create_chat_session_name(self, user_message: ChatMessage):      
        logger.info(f"Creating chat session name for query: {user_message.content}, using rewritten query: {user_message.formatted_content}")
    
        system_message = self._get_chat_name_system_message()  
        messages = [system_message, user_message]
        response = None
        
        try:
            response = completion(
                model="cohere/command-r",
                messages=[{
                    'role': message.role, 
                    'content': message.get_param("formatted_content")
                    } for message in messages
                ],
            )
        except APIConnectionError as e:
            logger.error(f'Chat name connection failed: {e}')
        except Timeout as e:
            logger.error(f'Chat name request timed out: {e}')
        except APIError as e:
            logger.error(f'Chat name API error occurred: {e}') 

        if response:
            name = response.message.content[0].text
            return self._truncate_chat_name(name)
        else:
            return None
        
    def rewrite_query_for_vector_base(self, new_message: ChatMessage) -> str:
        logger.info("Rewriting query...")
        pass
       
    def rewrite_query_for_llm(self, new_message: ChatMessage) -> str:
        logger.info("Rewriting query...")
        pass
            
    def rewrite_query_with_history_for_vector_base(self, new_message: ChatMessage, messages: list[ChatMessage]) -> str:
        logger.info("Rewriting query based on chat history...")
        
        # Filter out system messages and get last few messages for context
        # Get up to last 6 messages, but works with fewer messages too
        chat_history = [msg for msg in messages if msg.role != "system"][-6:]
        
        system_message = ChatMessage(
            role="system",
            content=self.QUERY_REWRITE_SYSTEM_MESSAGE
        )
        
        # Format chat history and new query
        history_context = "\n".join([
            f"{msg.role}: {msg.get_param('formatted_content')}" for msg in chat_history
        ])
        user_message = ChatMessage(
            role="user",
            content=f"""Chat history:
            {history_context}
            
            New query: {new_message.content}
            
            Rewrite this query to include relevant context from the chat history."""
        )
        
        try:            
            response = completion(
                model="cohere/command-r",
                messages=[{
                    'role': msg.role,
                    'content': msg.content
                } for msg in [system_message, user_message]],
                temperature=0.1
            )
            
            rewritten_query = response.message.content[0].text
            logger.info(f"Original query: {new_message.content}")
            logger.info(f"Rewritten query: {rewritten_query}")
            return rewritten_query
        except Exception as e:
            logger.error(f"Error rewriting query: {e}")
            return new_message.content  # Fall back to original query if rewriting fails