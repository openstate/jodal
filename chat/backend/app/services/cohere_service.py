from ..config import settings
from cohere import ClientV2 as CohereClient
import logging
from ..schemas import ChatMessage, MessageRole, MessageType
from .base_llm_service import BaseLLMService
from typing import Generator
# Set up logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

class CohereService(BaseLLMService):    
    def __init__(self):
        self.client = CohereClient(api_key=settings.COHERE_API_KEY)
        
    def chat_stream(self, messages: list[ChatMessage], documents: list) -> Generator:
        logger.info(f"Starting chat stream with {len(messages)} messages and {len(documents)} documents...")
        
        # Filter out status messages and validate message content
        system_and_user_messages = []
        for msg in messages:
            if msg.message_type == MessageType.SYSTEM_MESSAGE:
                system_and_user_messages.append({
                    'role': msg.role,
                    'content': msg.content
                })
            elif msg.message_type == MessageType.USER_MESSAGE:
                system_and_user_messages.append({
                    'role': msg.role,
                    'content': msg.rewritten_query_for_llm
                })
        
        logger.info(f"Filtered to {len(system_and_user_messages)} valid non-status messages")
        
        max_retries = 3
        for attempt in range(max_retries):
            try:
                return self.client.chat_stream(
                    model="command-r-08-2024",
                    messages=system_and_user_messages,
                    documents=documents
                )                
            except Exception as e:
                logger.error(f"Error in chat stream (attempt {attempt + 1}): {e}")
                if attempt < max_retries - 1:
                    logger.info("Retrying...")
                else:
                    logger.error("Max retries reached. Raising exception.")
                    raise

        
    def rerank_documents(self, query: str, documents: list, top_n: int = 20, return_documents: bool = True):
        logger.info(f"Reranking {len(documents)} documents, and returning {top_n} documents...")
        
        max_retries = 3
        for attempt in range(max_retries):
            try:
                return self.client.rerank(
                    query=query,
                    documents=documents,
                    top_n=top_n,
                    model=settings.COHERE_RERANK_MODEL,
                    return_documents=return_documents
                )
            except Exception as e:
                logger.error(f"Error reranking documents (attempt {attempt + 1}): {e}")
                if attempt < max_retries - 1:
                    logger.info("Retrying...")
                else:
                    logger.error("Max retries reached. Raising exception.")
                    raise
                
    def generate_dense_embedding(self, query: str):
        logger.info(f"Generating dense embedding for query: {query}")        
        
        # HACK TO FIX COHERE'S DIACRITIC ISSUES
        # Replace diacritics with base characters using unicode normalization
        import unicodedata
        query = ''.join(c for c in unicodedata.normalize('NFKD', query)
                         if not unicodedata.combining(c))
        # END HACK
        
        max_retries = 3
        for attempt in range(max_retries):
            try:
                if settings.EMBEDDING_QUANTIZATION == "float":
                    embeddings = self.client.embed(
                        texts=[query], 
                        input_type="search_query", 
                        model=settings.COHERE_EMBED_MODEL,
                        embedding_types=["float"]
                    ).embeddings.float[0]
                    
                    logger.info("Generated dense embeddings")
                    return embeddings
                elif settings.EMBEDDING_QUANTIZATION == "uint8":
                    embeddings = self.client.embed(
                        texts=[query], 
                        input_type="search_query", 
                        model=settings.COHERE_EMBED_MODEL,
                        embedding_types=["uint8"]
                    ).embeddings.uint8[0]
                    
                    logger.info("Generated dense embeddings")
                    return embeddings
                else:
                    embeddings = self.client.embed(
                        texts=[query], 
                        input_type="search_query", 
                        model=settings.COHERE_EMBED_MODEL,
                        embedding_types=["float"]
                    ).embeddings.float[0]
                    
                    logger.info("Generated dense embeddings")
                    return embeddings
            except Exception as e:
                logger.error(f"Error generating dense embedding (attempt {attempt + 1}): {e}")
                if attempt < max_retries - 1:
                    logger.info("Retrying...")
                else:
                    logger.error("Max retries reached. Raising exception.")
                    raise
        
    def create_chat_session_name(self, user_message: ChatMessage):      
        logger.info(f"Creating chat session name for query: {user_message.content}, using rewritten query: {user_message.formatted_content}")
        
        system_message = self._get_chat_name_system_message()  
        
        response = None
        
        max_retries = 3
        for attempt in range(max_retries):
            try:
                response = self.client.chat(
                    model="command-r-08-2024",
                    messages=[
                        {
                            'role': system_message.role,
                            'content': system_message.content
                        },
                        {
                            'role': user_message.role,
                            'content': user_message.rewritten_query_for_llm
                        }
                    ],
                    temperature=0.1
                )
            except Exception as e:
                logger.error(f"Error creating chat session name (attempt {attempt + 1}): {e}")
                if attempt < max_retries - 1:
                    logger.info("Retrying...")
                else:
                    logger.error("Max retries reached. Raising exception.")
                    raise
        
        if response:
            name = response.message.content[0].text
            return self._truncate_chat_name(name)
        else:
            return None

    def rewrite_query_with_history_for_vector_base(self, message: ChatMessage, messages: list[ChatMessage]) -> str:
        logger.info("Rewriting query based on chat history...")

        # Filter out system messages and get last few messages for context
        # Get up to last 6 messages, but works with fewer messages too
        chat_history = [msg for msg in messages if msg.role == MessageRole.USER][-6:]
        
        system_message = ChatMessage(
            role="system",
            content=self.QUERY_REWRITE_SYSTEM_MESSAGE_WITH_HISTORY_FOR_DB
        )
        
        # Format chat history and new query
        history_context = "\n".join([
            f"User query {i}: {msg.user_query}" for i, msg in enumerate(chat_history, start=1)
        ])
        user_message = ChatMessage(
            role="user",
            content=f"""{history_context}
New query: {message.user_query}"""
        )
        
        max_retries = 3
        for attempt in range(max_retries):
            try:
                response = self.client.chat(
                    model="command-r-08-2024",
                    messages=[
                    {
                        'role': system_message.role,
                        'content': system_message.content
                    },
                    {
                            'role': user_message.role,
                            'content': user_message.content
                        }
                    ],
                    temperature=0.1
                )
                
                rewritten_query = response.message.content[0].text
                logger.info(f"Original query: {message.user_query}")
                logger.info(f"Rewritten query: {rewritten_query}")
                return rewritten_query
            except Exception as e:
                logger.error(f"Error rewriting query with history (attempt {attempt + 1}): {e}")
                if attempt < max_retries - 1:
                    logger.info("Retrying...")
                else:
                    logger.error("Max retries reached. Raising exception.")
                    raise
                
        return message.user_query  # Fall back to original query if rewriting fails

    def rewrite_query_for_llm(self, message: ChatMessage) -> str:       
        rewritten_query = message.content
        # Check if any location names are already in the content
        if message.search_filters.locations:
            location_names = [location.name for location in message.search_filters.locations]
            if not any(loc_name in message.content for loc_name in location_names):
                locations_str = ", of ".join(location_names) 
                rewritten_query = f"{message.content} in {locations_str}"
           
        # if message.search_filters.date_range:
        #     rewritten_query += f" van {message.search_filters.date_range[0].strftime('%d-%m-%Y')} tot {message.search_filters.date_range[1].strftime('%d-%m-%Y')}"
        
        return rewritten_query

    def rewrite_query_for_vector_base(self, message: ChatMessage) -> str:       
        system_message = ChatMessage(
            role="system",
            content=self.QUERY_REWRITE_SYSTEM_MESSAGE
        )
        user_message = ChatMessage(
            role="user",
            content=f"""Query: {message.user_query}"""
        )

        max_retries = 3
        for attempt in range(max_retries):
            try:
                response = self.client.chat(
                    model="command-r",
                    messages=[
                        {
                            'role': system_message.role,
                            'content': system_message.content
                        },
                        {
                            'role': user_message.role,
                            'content': user_message.content
                        }
                    ],
                    temperature=0.1
                )
                
                rewritten_query = response.message.content[0].text
                logger.info(f"Original query: {message.user_query}")
                logger.info(f"Rewritten query: {rewritten_query}")
                return rewritten_query
            except Exception as e:
                logger.error(f"Error rewriting query for vector base (attempt {attempt + 1}): {e}")
                if attempt < max_retries - 1:
                    logger.info("Retrying...")
                else:
                    logger.error("Max retries reached. Raising exception.")
                    raise
        return message.content  # Fall back to original query if rewriting fails