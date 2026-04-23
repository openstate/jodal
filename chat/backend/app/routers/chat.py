from fastapi import APIRouter, Depends, Query
from fastapi.responses import StreamingResponse
import logging
import json
from asyncio import sleep
from ..database import get_db
from sqlalchemy.orm import Session as SQLAlchemySession
from ..services.session_service import SessionService
from ..services.cohere_service import CohereService
from ..services.base_llm_service import BaseLLMService
from ..services.litellm_service import LiteLLMService
from ..services.qdrant_service import QdrantService
from ..services.bron_service import BronService
from ..schemas import ChatMessage, ChatDocument, SessionCreate, SessionUpdate, Session, MessageRole, MessageType, SearchFilter
from ..config import settings
from typing import List, Dict, AsyncGenerator
from ..text_utils import get_formatted_date_english, format_text
import time
from datetime import date, datetime
from fastapi.responses import JSONResponse

router = APIRouter()

# Set up logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

ENVIRONMENT = settings.ENVIRONMENT

base_api_url = "/"
if ENVIRONMENT == "development":
    base_api_url = "/api/"
    
    
@router.get(base_api_url + "chat")
async def chat_endpoint(
    query: str = Query(..., description="The chat message content"),
    session_id: str = Query(None, description="The session ID"),
    locations: List[str] = Query(None, description="List of location IDs to filter by"),
    start_date: date = Query(None, description="Start date to filter by"),
    end_date: date = Query(None, description="End date to filter by"),
    rewrite_query: bool = Query(True, description="Whether to enable query rewriting"),
    db: SQLAlchemySession = Depends(get_db)
):
    try:
        # Start timer for request duration tracking
        start_time = time.time()
        
        llm_service = None
        if settings.LLM_SERVICE.lower() == "litellm":
            llm_service = LiteLLMService()
        else:
            llm_service = CohereService()
            
        qdrant_service = QdrantService(llm_service)    
        session_service = SessionService(db)
        bron_service = BronService()
        
        logger.debug(f"query: {query}")
        logger.debug(f"locations: {locations}")
        logger.debug(f"start_date: {start_date}")
        logger.debug(f"end_date: {end_date}")
        logger.debug(f"rewrite_query: {rewrite_query}")  
        
        date_range = None
        if start_date is not None and end_date is not None:
            date_range = [
                datetime.combine(start_date, datetime.min.time()),
                datetime.combine(end_date, datetime.max.time())
            ]

        locations_objects = await bron_service.get_locations_by_ids(location_ids=locations)

        logger.debug(f"location_names: {locations_objects}")
        search_filters = SearchFilter(
            locations=locations_objects,
            date_range=date_range,
            rewrite_query=rewrite_query
        )
        logger.info(f"search_filters: {search_filters}")  
       
        return StreamingResponse(
            event_generator(
                session_id, 
                query, 
                start_time, 
                session_service, 
                llm_service, 
                qdrant_service,
                search_filters
            ),
            media_type="text/event-stream",
            headers={
                "Cache-Control": "no-cache",
                "Connection": "keep-alive",
                "X-Accel-Buffering": "no",
            }
        )
    except Exception as e:
        logger.error(f"Error in chat_endpoint: {e}", exc_info=True)
        return JSONResponse(status_code=500, content={"detail": "Internal Server Error"})

async def event_generator(
    session_id: str,
    user_query: str,
    start_time: float,
    session_service: SessionService, 
    llm_service: BaseLLMService, 
    qdrant_service: QdrantService,
    search_filters: SearchFilter
):      
    # Initialize status message content
    status_content = []   
    
    # First status message
    status_msg = "Bron start met zoeken"
    status_content.append(status_msg)
    yield 'data: ' + json.dumps({
        "type": "status", 
        "role": "system", 
        "content": status_msg
    }) + "\n\n"
    await sleep(0)
    
    session = session_service.get_session_with_relations(session_id)
    user_message = llm_service.get_user_message(user_query, search_filters)
    rewritten_query_for_llm = llm_service.rewrite_query_for_llm(user_message)
        
    if len(session.messages) == 0:
        # Create new session with initial messages
        is_initial_message = True
        rag_system_message = llm_service.get_rag_system_message()
       
        # if search_filters.rewrite_query:
        user_message.user_query = user_query
        user_message.rewritten_query_for_llm = rewritten_query_for_llm
        
        rewritten_query_for_vector_base = llm_service.rewrite_query_for_vector_base(user_message)
        user_message.formatted_content = rewritten_query_for_vector_base
        user_message.rewritten_query_for_vector_base = rewritten_query_for_vector_base
        # else:
        #     user_message.formatted_content = user_query
            
        #     # new fields
        #     user_message.user_query = user_query
        #     user_message.rewritten_query_for_llm = rewritten_query_for_llm
        logger.debug(f"user_message: {user_message}")        
        session = session_service.add_messages(
            session_id=session.id,
            messages=[rag_system_message, user_message]
        )
        
    else:
        is_initial_message = False   
        
        user_message.user_query = user_query
        user_message.rewritten_query_for_llm = rewritten_query_for_llm
        
        rewritten_query_for_vector_base = llm_service.rewrite_query_with_history_for_vector_base(user_message, session.messages)
        user_message.formatted_content = rewritten_query_for_vector_base
        user_message.rewritten_query_for_vector_base = rewritten_query_for_vector_base
        
        session = session_service.add_message(
            session_id=session.id, 
            message=user_message
        )
        logger.info(f"Using existing session: {session.id}")
        
    try:        
        # Second status message
        status_msg = f"Zoekopdracht herschreven van '{user_message.user_query}' naar '{user_message.rewritten_query_for_vector_base}'"
        status_content.append(status_msg)
        yield 'data: ' + json.dumps({
            "type": "status", 
            "role": "system", 
            "content": status_msg
        }) + "\n\n"
        await sleep(0)
        
        
        yield 'data: ' + json.dumps({
            "type": "session",
            "session_id": session.id
        }) + "\n\n"
        await sleep(0)
                        
        # Third status message
        status_msg = "Documenten worden gezocht"
        status_content.append(status_msg)
        yield 'data: ' + json.dumps({
            "type": "status", 
            "role": "system", 
            "content": status_msg
        }) + "\n\n"
        await sleep(0)
        
        try: 
            # Use the formatted_content (rewritten query) from the last message
            relevant_docs = qdrant_service.retrieve_relevant_documents(
                user_message.rewritten_query_for_vector_base,
                locations=search_filters.locations,
                date_range=search_filters.date_range
            )
            logger.debug(f"Relevant documents: {relevant_docs}")
        except Exception as e:
            logger.error(f"Error retrieving documents: {e}")
            
            status_msg = "Er is een fout opgetreden bij het zoeken naar documenten"
            status_content.append(status_msg)
            yield 'data: ' + json.dumps({
                "type": "status", 
                "role": "system", 
                "content": status_msg
            }) + "\n\n"
            await sleep(0)
            return
        
        if not relevant_docs:
            status_msg = "Er konden geen relevante documenten worden gevonden"
            status_content.append(status_msg)
            yield 'data: ' + json.dumps({
                "type": "status", 
                "role": "system", 
                "content": status_msg
            }) + "\n\n"
            await sleep(0)
            return
        
        session_documents = session_service.get_documents(session)
        if not session_documents:
            combined_relevant_docs = relevant_docs
        else:
            if isinstance(session_documents[0], ChatDocument):
                combined_relevant_docs = relevant_docs
            else:
                combined_relevant_docs = relevant_docs + session_documents

        reordered_relevant_docs = qdrant_service.reorder_documents_by_publication_date(combined_relevant_docs)
                                
        yield 'data: ' + json.dumps({
            "type": "documents",
            "role": "system",
            "documents": reordered_relevant_docs
        }) + "\n\n"
        await sleep(0)
        
        relevant_docs_count = len(relevant_docs)
            
        status_msg = f"{relevant_docs_count} nieuwe documenten gevonden"
        status_content.append(status_msg)
        yield 'data: ' + json.dumps({
            "type": "status", 
            "role": "system", 
            "content": status_msg
        }) + "\n\n"
        await sleep(0)            
    

        status_msg = f"Antwoord op deze vraag wordt gegenereerd door AI: '{user_message.rewritten_query_for_llm}'"
        status_content.append(status_msg)
        yield 'data: ' + json.dumps({
            "type": "status", 
            "role": "system", 
            "content": status_msg
        }) + "\n\n"
        await sleep(0)
        
        # Save the status messages to the database
        status_message = session_service.add_and_get_message(
            session_id=session.id,
            message=ChatMessage(
                role=MessageRole.SYSTEM,
                content="\n".join(status_content),
                message_type=MessageType.STATUS
            )
        )
        
        async for response in generate_full_response(
            llm_service, 
            session_service, 
            session.messages, 
            relevant_docs, 
            is_initial_message, 
            session.id, 
            user_message,
            status_message,
            start_time
        ):
            yield 'data: ' + json.dumps(response) + "\n\n"
            await sleep(0)
 
    except Exception as e:
        logger.error(f"Error in chat_endpoint: {e}", exc_info=True)
        yield 'data: ' + json.dumps({"type": "error", "content": str(e)}) + "\n\n"
        await sleep(0)
        
    finally:            
        # Send a proper close event with data
        yield 'event: close\n\ndata: {"type": "end"}\n\n'
        await sleep(0)
        
async def generate_full_response(
    llm_service : BaseLLMService, 
    session_service: SessionService, 
    session_messages: List[ChatMessage], 
    relevant_docs: List[Dict], 
    is_initial_message: bool, 
    session_id: str, 
    user_message: ChatMessage,
    status_message: ChatMessage,
    start_time: float
):
    logger.debug(f"Generating full response for query: {user_message.content}, rewritten query: {user_message.formatted_content}")
    full_text = ""
    text_formatted_with_citations = ""
    citations = []
    
    async for event in generate_response(llm_service, session_messages, relevant_docs):
        if event["type"] == "status":
            yield {
                "type": "status",
                "role": "assistant",
                "content": event["content"],
                "content_original": event["content"],
            }
        elif event["type"] == "text":
            full_text += event["content"]
            yield {
                "type": "partial",
                "role": "assistant",
                "content": event["content"],
            }
        elif event["type"] == "citation":
            citations.append(event["content"])
            text_formatted_with_citations = format_text(full_text, citations)
            yield {
                "type": "citation",
                "role": "assistant",
                "content": text_formatted_with_citations,
                "content_original": full_text,
                "citations": citations,
            }
    
    if not full_text:
        status_msg = "\nEr konden geen relevante documenten worden gevonden om de vraag te beantwoorden"
        status_message.content += status_msg
        session_service.update_message(
            session_id=session_id,
            message=status_message
        )
        yield {
            "type": "status",
            "role": "assistant",
            "content": status_msg,
            "content_original": status_msg
        }    
    else:
        if is_initial_message:
            try:
                chat_name = llm_service.create_chat_session_name(user_message)     
                session_service.update_session_name(session_id=session_id, name=chat_name)
            except Exception as e:
                logger.error(f"Error creating session name: {e}", exc_info=True)
             
        try:      
            if text_formatted_with_citations:
                text_formatted = text_formatted_with_citations
            else:
                text_formatted = format_text(full_text, [])
                
            session_service.add_message(
                session_id=session_id,
                message=ChatMessage(                                
                    role=MessageRole.ASSISTANT,
                    message_type=MessageType.ASSISTANT_MESSAGE,
                    content=full_text,
                    formatted_content=text_formatted,                                    
                    documents = [
                        ChatDocument(
                            chunk_id=doc.get('chunk_id'),
                            score=doc.get('score'),
                            rerank_score=doc.get('rerank_score'),
                            content=doc.get('content', ''),
                            title=doc.get('title', ''),
                            url=doc.get('url', '')
                        )
                        for doc in relevant_docs
                    ]   
                )
            )
        except Exception as e:
            logger.error(f"Error updating session: {e}", exc_info=True)
                  
        status_msg = f"\nAntwoord gegenereerd in {time.time() - start_time:.2f} seconden"
        status_message.content += status_msg
        session_service.update_message(message=status_message)
        
        yield {
            "type": "status",
            "role": "system",
            "content": status_msg
        } 
        
        text_formatted_with_citations = format_text(full_text, citations)    
        session = session_service.get_session_with_relations(session_id)    
        # Remove system messages from the session
        session.messages = [msg for msg in session.messages if msg.message_type != MessageType.SYSTEM_MESSAGE]              
                         
        yield {
            "type": "full",
            "session": session.model_dump()
        }
        
async def generate_response(llm_service: BaseLLMService, messages: List[ChatMessage], relevant_docs: List[Dict]) -> AsyncGenerator[Dict, None]:        
    logger.debug(f"Generating response for messages and documents: {messages}")
        
    formatted_docs = [{     
        'id': doc['chunk_id'],   
        "data": {
            "title": doc['data']['title'],
            "snippet": doc['data']['content'],
            "publication date": get_formatted_date_english(
                doc['data']['published']
            ),
            "municipality": doc['data']['location_name'],
            "source": BaseLLMService.get_human_readable_source(
                doc['data']['source']
            ),
            "type": doc['data']['type'],
        }
    } for doc in relevant_docs]
    
    current_citation = None
    first_citation = True
    
    try:
        for event in llm_service.chat_stream(messages, formatted_docs):
            if event:
                if hasattr(event, 'type'):
                    if event.type == "content-delta":
                        if hasattr(event, 'delta') and hasattr(event.delta, 'message') and hasattr(event.delta.message, 'content'):
                            yield {
                                "type": "text",
                                "content": event.delta.message.content.text
                            }
                    elif event.type == 'citation-start':       
                        if first_citation:
                            yield {
                                "type": "status",
                                "content": "De bronnen om deze tekst te onderbouwen worden er nu bij gezocht."
                            }
                            first_citation = False
                        
                        if (hasattr(event, 'delta') and 
                            hasattr(event.delta, 'message') and 
                            hasattr(event.delta.message, 'citations')):
                            
                            document_ids = []
                            if hasattr(event.delta.message.citations, 'sources') and event.delta.message.citations.sources:
                                document_ids = [source.document.get('id') for source in event.delta.message.citations.sources if hasattr(source, 'document')]
                            
                            current_citation = {
                                'start': event.delta.message.citations.start,
                                'end': event.delta.message.citations.end,
                                'text': event.delta.message.citations.text,
                                'document_ids': document_ids
                            }
                    
                    elif event.type == 'citation-end':
                        if current_citation:
                            yield {
                                "type": "citation",
                                "content": current_citation
                            }
                            current_citation = None                    
    except GeneratorExit:
        logger.info("Generator closed by client")
        return
    except Exception as e:
        logger.error(f"Error in generate_response: {e}")
        raise
    finally:
        logger.info("Exiting generate_response")
