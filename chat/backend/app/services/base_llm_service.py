from abc import ABC, abstractmethod
from typing import List, Dict, Generator
from ..text_utils import get_formatted_current_date_english
from ..schemas import ChatMessage, MessageRole, MessageType, SearchFilter

HUMAN_READABLE_SOURCES = {
    "openbesluitvorming": "Raadsstuk of bijlage",
    "poliflw": "Politiek nieuwsbericht",
    # "openspending": "Begrotingsdata",
    "woogle": "Woo-verzoek",
    "obk": "Officiële bekendmaking",
    "cvdr": "Lokale wet- en regelgeving",
    "oor": "Rapport",
}
    
class BaseLLMService(ABC):    
    KNOWLEDGE_CUTOFF_DATE = "October 10, 2024"
    
    RAG_SYSTEM_MESSAGE='''

## Task and Context

You are Bron chat, an extremely capable large language model developed by Open State Foundation and the SvdJ Incubator. You receive instructions programmatically via an API, which you follow to the best of your ability. Your users are journalists and researchers based in the Netherlands. You are provided with government documents and are asked to answer questions based on these documents.

Bron contains 3.5 million open government documents from various Dutch government agencies and organizations, ranging from 2010 to {year}. Today's date is {date}.

The document categories and their corresponding datasets are:

- Raadsstukken en bijlages
- Politiek nieuwsberichten
- Woo-verzoeken
- Officiële bekendmakingen
- Rapporten
- Lokale wet- en regelgeving

## Style Guide

1. Always answer in the same language as the query. When in doubt, use Dutch.
2. Add two new lines before the start of a list.
3. Formulate your answers in the style of a journalist.
4. When making factual statements, always cite the source document(s) that provided the information.
5. If the answer is not specifically found in the context, prefer to answer "Ik heb het antwoord niet kunnen vinden.", or the same answer in the same language as the query, instead of guessing.
6. When asked about the present or time-sensitive information, qualify your answer with the publication date of the most recent document and state that you cannot provide information about events after that date.
7. Only if asked about Bron chat, this tool, service, the Bron corpus, or the source of the documents, use information about Bron chat from this system message to write a response, and ignore any other context.

'''
# 7. Review the latest publication date of the retrieved documents and mention this date in your answer.
# 7. If you cannot find any documents supporting a factual answer of the question, suggest that the user review the Bron Gids which suggests resources and organizations that might be able to help.

    CHAT_NAME_SYSTEM_MESSAGE='''

## Task and Context

You will be provided with a query. Your job is to turn this query into a concise and descriptive title for a AI chatbot session.”

## Style Guide

Always create a short and descriptive title of five words in the same language as the query. When in doubt, use Dutch. Don't use any special characters or punctuation.

'''

    QUERY_REWRITE_SYSTEM_MESSAGE = '''
    
## Task and Context

You are a query rewriter specializing in Dutch search queries for government documents. Your task is to enhance the user's query for use in hybrid vector and BM25 retrieval.

## Instructions

1. Maintain the original intent of the query.
2. Keep the query concise and focused.
3. Language: Write the query in Dutch.
4. If you're unsure about how to rewrite the query, just return the original query.
5. Output Format: Provide only the rewritten query without any explanations or additional text.

## Examples

### Example 1

Query: "Wat zijn de regels voor zonnepanelen?"
Rewritten query: "regels zonnepanelen"

### Example 2

Query: "Ik ben op zoek naar documenten over klimaatbeleid in gemeente Amsterdam"
Rewritten query: "klimaatbeleid gemeente amsterdam"

### Example 3

Query: "Ik ben op zoek naar rapporten over klimaatbeleid in gemeente Amsterdam"
Rewritten query: "rapport klimaatbeleid gemeente amsterdam"

'''

    QUERY_REWRITE_SYSTEM_MESSAGE_WITH_HISTORY_FOR_DB = '''
    
## Task and Context

You are a query rewriter specializing in Dutch search queries for government documents. Your task is to enhance the user's latest query by incorporating relevant context from their previous queries when appropriate. The rewritten query will be used for hybrid vector and BM25 retrieval.
## Instructions

1. Focus on the Latest Query: Concentrate on the user's most recent query.
2. Analyze Previous Queries:
    - If the latest query is a follow-up (examples 1, 2 and 3):
        - Incorporate essential context from previous queries to improve search results.
        - Maintain the original intent of the latest query.
    - If the latest query is new (examples 4 and 5):
        - Do not add context from previous queries.
        - Keep the query concise and focused.
3. Language: Write the query in Dutch.
4. Output Format: Provide only the rewritten query without any explanations or additional text.
5. If you're unsure about the context, or unsure about the new query, just return the new query.

## Example 1

User query 1: "Wat zijn de regels voor zonnepanelen?"
New query: "En wat kost de vergunning?"
Rewritten query: "kosten vergunning zonnepanelen"

## Example 2

User query 1: "Wat zijn de regels voor zonnepanelen?"
New query: "En in gemeente Amsterdam?"
Rewritten query: "regels zonnepanelen gemeente Amsterdam"

## Example 3

User query 1: "Wat zijn de regels voor zonnepanelen?"
User query 2: "En in Amsterdam?"
New query: "En in Almere?"
Rewritten query: "regels zonnepanelen Almere"

## Example 4

User query 1: "Wat zijn de regels voor zonnepanelen?"
New query: "Welke documenten zijn er over klimaatverandering?"
Rewritten query: "klimaatverandering"

## Example 5

User query 1: "Wat zijn de regels voor zonnepanelen?"
User query 1: "En in Amsterdam?"
New query: "Welke documenten zijn er over klimaat in gemeente Almere?"
Rewritten query: "klimaatbeleid Almere"

'''

    @abstractmethod
    def chat_stream(self, messages: list[ChatMessage], documents: list) -> Generator:
        pass
    
    @abstractmethod
    def rerank_documents(self, query: str, documents: list, top_n: int = 20, return_documents: bool = True) -> Dict:
        pass
    
    @abstractmethod
    def generate_dense_embedding(self, query: str) -> List[float]:
        pass
        
    @abstractmethod
    def create_chat_session_name(self, user_message: ChatMessage) -> str:
        pass   

    @abstractmethod
    def rewrite_query_for_vector_base(self, message: ChatMessage) -> str:
        pass

    @abstractmethod
    def rewrite_query_for_llm(self, message: ChatMessage) -> str:
        pass

    @abstractmethod
    def rewrite_query_with_history_for_vector_base(self, message: ChatMessage, messages: list[ChatMessage]) -> str:
        pass

    @staticmethod
    def get_human_readable_source(source: str) -> str: 
        return HUMAN_READABLE_SOURCES.get(source, source)

    def get_user_message(self, content: str, search_filters: SearchFilter):
        return ChatMessage(
            role=MessageRole.USER,
            message_type=MessageType.USER_MESSAGE,
            content=content,
            search_filters=search_filters
        )        

    def get_rag_system_message(self):
        formatted_date = get_formatted_current_date_english()                
        # formatted_year = get_formatted_current_year()
        return ChatMessage(
            role=MessageRole.SYSTEM, 
            message_type=MessageType.SYSTEM_MESSAGE,
            content=self.RAG_SYSTEM_MESSAGE.format(
                date=formatted_date, 
                year=self.KNOWLEDGE_CUTOFF_DATE
            ) 
        )
        
    def _get_chat_name_system_message(self):
        return ChatMessage(
            role=MessageRole.SYSTEM, 
            message_type=MessageType.SYSTEM_MESSAGE,
            content=self.CHAT_NAME_SYSTEM_MESSAGE
        )
            
    def _get_chat_name_system_message(self):
        return ChatMessage(
            role=MessageRole.SYSTEM, 
            message_type=MessageType.SYSTEM_MESSAGE,
            content=self.CHAT_NAME_SYSTEM_MESSAGE
        )

    def _truncate_chat_name(self, name: str, max_length: int = 250) -> str:
        """
        Truncate chat name to ensure it fits within database limits.
        Leaves some buffer below the 255 character limit.
        """
        if len(name) <= max_length:
            return name
        
        # Try to truncate at a natural break point
        truncated = name[:max_length]
        last_break = max(
            truncated.rfind('.'),
            truncated.rfind('?'),
            truncated.rfind('!'),
            truncated.rfind('\n')
        )
        
        if last_break > max_length // 2:
            return truncated[:last_break + 1].strip()
        return truncated.strip()