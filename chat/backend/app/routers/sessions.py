from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session as SQLAlchemySession
from ..schemas import SessionCreate, MessageType, MessageRole
from ..services.session_service import SessionService
from ..database import get_db
from ..services.qdrant_service import QdrantService
import logging
from datetime import datetime
from ..config import settings
from ..services.cohere_service import CohereService
from ..services.litellm_service import LiteLLMService
from ..services.bron_service import BronService

router = APIRouter()

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

ENVIRONMENT = settings.ENVIRONMENT

base_api_url = "/"
if ENVIRONMENT == "development":
    base_api_url = "/api/"

@router.get(base_api_url + "sessions/{session_id}")
async def get_session(session_id: str, db: SQLAlchemySession = Depends(get_db)):
    logger.debug(f"Getting session with id: {session_id}")
    session_service = SessionService(db)

    llm_service = None
    # Use the configured LLM service
    if settings.LLM_SERVICE.lower() == "litellm":
        llm_service = LiteLLMService()
    else:
        llm_service = CohereService()
        
    qdrant_service = QdrantService(llm_service)
    bron_service = BronService()
    
    session = session_service.get_session_with_relations(session_id)    
    documents = []
    for message in session.messages:
        documents.extend(message.documents)
        
    logger.debug(f"Found {len(documents)} documents in MySQL for session {session_id}")
    
    qdrant_documents = qdrant_service.get_documents_by_ids(documents)    
    logger.info(f"Found {len(qdrant_documents)} documents in Qdrant for session {session_id}")
        
    # Remove system messages from the session
    messages = []
    for message in session.messages:
        if (message.role == MessageRole.SYSTEM and 
            (message.message_type is None or message.message_type != MessageType.STATUS)):
            continue
        
        if message.role == MessageRole.ASSISTANT:
            message.content = message.get_param("formatted_content")
            
        messages.append(message)
                   
    locations = await bron_service.get_locations()
            
    response = {
        "id": session.id,
        "name": session.name,
        "messages": messages,
        "documents": qdrant_documents,
        "locations": locations
    }
    
    return response

@router.post(base_api_url + "new_session")
async def create_session(db: SQLAlchemySession = Depends(get_db)):
    logger.debug("Creating new session")
    now = datetime.now()
    session_service = SessionService(db)
    return session_service.create_session(
        SessionCreate(
            name=f"Sessie {now.strftime('%Y-%m-%d %H:%M')}",
            messages=[], 
            documents=[]
        )
    )

@router.post(base_api_url + "sessions/{session_id}/clone")
async def clone_session(session_id: str, db: SQLAlchemySession = Depends(get_db)):
    logger.debug(f"Cloning session with id: {session_id}")
    session_service = SessionService(db)
    
    # Get the original session with messages
    original_session = session_service.get_session_with_relations(session_id)
    
    new_session = session_service.create_session(
        SessionCreate(
            name=f"Copy of {original_session.name}",
            messages=[],
            documents=[]
        )
    )
    
    # Get messages in chronological order
    sorted_messages = sorted(original_session.messages, key=lambda x: x.sequence)
    
    # Get only user messages in order
    user_messages = [msg for msg in sorted_messages if msg.role == MessageRole.USER]
    
    # Return the new session ID and the messages to replay
    return {
        "session_id": new_session.id,
        "messages": [
            {
                "content": msg.content,
                "message_type": msg.message_type
            } for msg in user_messages
        ]
    }
