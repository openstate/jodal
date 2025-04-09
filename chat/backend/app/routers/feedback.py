from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
import logging
from uuid import UUID
from ..database import get_db
from ..services.feedback_service import FeedbackService
from ..services.session_service import SessionService
from ..models import FeedbackType
from ..config import settings
from ..schemas import (
    MessageFeedbackCreate,
    MessageFeedbackUpdate,
    SessionFeedbackCreate,
    DocumentFeedbackCreate,
    DocumentFeedbackUpdate,
    FeedbackCreate,
    MessageFeedbackTypeRequest, 
    MessageFeedbackNotesRequest, 
    FeedbackCreateRequest, 
    DocumentFeedbackTypeRequest, 
    DocumentFeedbackNotesRequest
)

router = APIRouter()

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

ENVIRONMENT = settings.ENVIRONMENT

base_api_url = "/"
if ENVIRONMENT == "development":
    base_api_url = "/api/"
    
async def get_feedback_service(db: Session = Depends(get_db)) -> FeedbackService:
    return FeedbackService(db)

async def get_session_service(db: Session = Depends(get_db)) -> SessionService:
    return SessionService(db)

@router.post(base_api_url + "feedback/messages/type/{message_id}")
async def submit_message_feedback_type(
    message_id: int,
    feedback: MessageFeedbackTypeRequest,
    feedback_service: FeedbackService = Depends(get_feedback_service)
):
    existing_feedback = feedback_service.get_message_feedback(message_id)
    
    if existing_feedback:
        return feedback_service.update_message_feedback(
            MessageFeedbackUpdate(
                message_id=message_id,
                feedback_type=feedback.feedback_type,
                notes=""
            )
        )
    else:
        return feedback_service.create_message_feedback(
            MessageFeedbackCreate(
                message_id=str(message_id),
                feedback_type=feedback.feedback_type
            )
        )

@router.post(base_api_url + "feedback/messages/notes/{message_id}")
async def submit_message_feedback_notes(
    message_id: int,
    feedback: MessageFeedbackNotesRequest,
    feedback_service: FeedbackService = Depends(get_feedback_service)
):    
    return feedback_service.update_message_feedback(        
        MessageFeedbackUpdate(
            message_id=message_id,
            notes=feedback.notes
        )
    )

# @router.post(base_api_url + "feedback/documents/{document_id}")
# def set_document_feedback(
#     document_id: str,
#     feedback: DocumentFeedbackRequest,
#     db: Session = Depends(get_db)
# ):
#     try:
#         feedback_type = FeedbackType[feedback.feedback_type.upper()]
#         feedback_service = FeedbackService(db)
#         return feedback_service.set_document_feedback(
#             document_id=document_id,
#             feedback_type=feedback_type,
#             notes=feedback.notes
#         )
#     except KeyError:
#         raise HTTPException(
#             status_code=422,
#             detail=f"Invalid feedback type. Must be one of: {[t.name for t in FeedbackType]}"
        # )
    
@router.post(base_api_url + "feedback/documents/type/{document_id}")
async def submit_document_feedback_type(
    document_id: int,
    feedback: DocumentFeedbackTypeRequest,
    feedback_service: FeedbackService = Depends(get_feedback_service)
):
    existing_feedback = feedback_service.get_document_feedback(document_id)
    
    if existing_feedback:
        return feedback_service.update_document_feedback(
            DocumentFeedbackUpdate(
                document_id=document_id,
                feedback_type=feedback.feedback_type,
                notes=""
            )
        )
    else:
        return feedback_service.create_document_feedback(
            DocumentFeedbackCreate(
                document_id=document_id,
                feedback_type=feedback.feedback_type
            )
        )

@router.post(base_api_url + "feedback/documents/notes/{document_id}")
async def submit_document_feedback_notes(
    document_id: int,
    feedback: DocumentFeedbackNotesRequest,
    feedback_service: FeedbackService = Depends(get_feedback_service)
):
    return feedback_service.update_document_feedback(
        DocumentFeedbackUpdate(
            document_id=document_id,
            notes=feedback.notes
        )
    )


@router.post(base_api_url + "feedback/{session_id}")
def create_session_feedback(
    session_id: str,
    feedback: FeedbackCreateRequest,
    feedback_service: FeedbackService = Depends(get_feedback_service),
    session_service: SessionService = Depends(get_session_service)    
):
    session = session_service.get_session(session_id)
    if session is None:
        raise HTTPException(status_code=404, detail="Session not found")
    
    return feedback_service.create_session_feedback(
        SessionFeedbackCreate(     
            question=feedback.question,
            name=feedback.name,
            email=feedback.email,
            session_id=session_id
        )
    )
    
@router.post(base_api_url + "feedback")
def create_feedback(
    feedback: FeedbackCreateRequest,
    feedback_service: FeedbackService = Depends(get_feedback_service)    
):
    return feedback_service.create_feedback(
        FeedbackCreate(     
            question=feedback.question,
            name=feedback.name,
            email=feedback.email,
        )
    )