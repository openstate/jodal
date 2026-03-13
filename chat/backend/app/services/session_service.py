from .database_service import DatabaseService
from ..models import Session as SessionModel, DocumentFeedback as DocumentFeedbackModel, Message, Document, MessageFeedback as MessageFeedbackModel, MessageDocument
from ..schemas import SessionCreate, ChatMessage, ChatDocument, Session, DocumentFeedback, MessageFeedback, SearchFilter, Location
from fastapi import HTTPException
import uuid
import logging  
from typing import List, Dict
from datetime import datetime
from sqlalchemy.orm import joinedload


# Set up logging
logging.basicConfig(level=logging.INFO) 
logger = logging.getLogger(__name__)

class SessionService(DatabaseService):
    def __init__(self, db):
        super().__init__(db)

    def create_session(self, session_create: SessionCreate) -> SessionModel:
        # Create the session first
        logger.info(f"Creating session with name: {session_create.name} and messages: {session_create.messages}")
        
        new_session = SessionModel(
            id=str(uuid.uuid4()),
            name=session_create.name,
            messages=self._messages_schema_to_db_model(session_create.messages)
        )
        self.db.add(new_session)
        self.db.commit()            
        self.db.refresh(new_session)
        
        return self._session_db_model_to_schema(new_session)

    def update_session_name(self, session_id: str, name: str) -> Session:
        db_session = self._get_session(session_id)
        if not db_session:
            raise HTTPException(status_code=404, detail="Session not found")
        db_session.name = name
        self.db.commit()
        self.db.refresh(db_session)
        
        return self._session_db_model_to_schema(db_session)
           
    def get_session(self, session_id: str) -> Session:
        return self._session_db_model_to_schema(self._get_session(session_id))

    def get_session_with_relations(self, session_id: str) -> Session:
        return self._session_db_model_to_schema(self._get_session_with_relations(session_id))

    def delete_session(self, session_id: str):
        db_session = self._get_session(session_id)
        if db_session is None:
            raise HTTPException(status_code=404, detail="Session not found")
        self.db.delete(db_session)
    
    def get_messages(self, session: Session) -> List[ChatMessage]:
        # Query messages with feedback relationship eagerly loaded
        messages = self.db.query(Message)\
            .filter(Message.session_id == session.id)\
            .outerjoin(MessageFeedback)\
            .options(joinedload(Message.feedback))\
            .order_by(Message.sequence)\
            .all()
        
        return self._messages_db_model_to_schema(messages)
                
    def get_documents(self, session: Session) -> List[ChatDocument]:
        # Query documents directly through message_documents relationship
        documents = self.db.query(Document)\
            .join(MessageDocument)\
            .join(Message)\
            .outerjoin(Document.feedback)\
            .filter(Message.session_id == session.id)\
            .distinct()\
            .all()
        
        return self._documents_db_model_to_schema(documents)
    
    def add_message(self, session_id: int, message: ChatMessage) -> Session:     
        db_session = self._get_session(session_id)
        db_message = self._message_schema_to_db_model(message, len(db_session.messages))
        
        logger.info(f"Adding message with search_filters: {db_message.search_filters}")
        
        db_session.messages.append(db_message)
        self.db.commit()
        self.db.refresh(db_session, ['messages'])        
  
        return self._session_db_model_to_schema(db_session)
    
    def add_and_get_message(self, session_id: int, message: ChatMessage) -> Session:     
        db_session = self._get_session(session_id)
        db_message = self._message_schema_to_db_model(message, len(db_session.messages))
        db_session.messages.append(db_message)

        self.db.commit()
        self.db.refresh(db_session, ['messages'])    
        
        logger.info(f"Added message with id: {db_message.id}")
        return self._message_db_model_to_schema(db_message)

    def add_messages(self, session_id: int, messages: List[ChatMessage]) -> Session:
        db_session = self._get_session(session_id)
        db_messages = self._messages_schema_to_db_model(messages)
        db_session.messages.extend(db_messages)
        self.db.commit()
        self.db.refresh(db_session, ['messages'])
        return self._session_db_model_to_schema(db_session)

    def update_message(self, message: ChatMessage) -> ChatMessage:
        logger.info(f"Updating message with id: {message.id} and content: {message.content}")
        db_message = self.db.query(Message)\
            .filter(Message.id == message.id)\
            .first()
                        
        if db_message is None:
            raise HTTPException(status_code=404, detail="Message not found")
        
        db_message.content = message.content
        db_message.formatted_content = message.formatted_content        
        
        self.db.commit()
        self.db.refresh(db_message)
        return self._message_db_model_to_schema(db_message)
    
    def _get_session(self, session_id: str) -> SessionModel:
        db_session = self.db.query(SessionModel)\
            .options(joinedload(SessionModel.messages))\
            .filter(SessionModel.id == session_id)\
            .first()
        if db_session is None:
            raise HTTPException(status_code=404, detail="Session not found")
        return db_session
    
    def _get_session_with_relations(self, session_id: str) -> SessionModel:
        db_session = self.db.query(SessionModel)\
            .options(
                joinedload(SessionModel.messages).joinedload(Message.feedback),
                joinedload(SessionModel.messages).joinedload(Message.documents).joinedload(Document.feedback),
                joinedload(SessionModel.feedback)
            )\
            .filter(SessionModel.id == session_id)\
            .first()
        if db_session is None:
            raise HTTPException(status_code=404, detail="Session not found")
        return db_session
    
    # Convert DB models to schemas
    def _session_db_model_to_schema(self, db_session: SessionModel) -> Session:
        return Session(
            id=db_session.id,
            name=db_session.name,
            messages=self._messages_db_model_to_schema(db_session.messages),
        )

    def _messages_db_model_to_schema(self, db_messages: List[Message]) -> List[ChatMessage]:
        return [self._message_db_model_to_schema(msg) for msg in db_messages]
    
    def _documents_db_model_to_schema(self, db_documents: List[Document]) -> List[ChatDocument]:
        return [self._document_db_model_to_schema(doc) for doc in db_documents]
    
    def _document_db_model_to_schema(self, db_document: Document) -> ChatDocument:
        if db_document is None:
            return None
        
        return ChatDocument(
            id=db_document.id,
            chunk_id=db_document.chunk_id,
            content=db_document.content,
            score=db_document.score,
            rerank_score=db_document.rerank_score,
            title=db_document.title,
            url=db_document.url,
            feedback=self._document_feedback_db_model_to_schema(db_document.feedback)
        )
        
    def _document_feedback_db_model_to_schema(self, db_feedback: DocumentFeedbackModel) -> DocumentFeedback:
        if db_feedback is None:
            return None
        
        return DocumentFeedback(
            id=db_feedback.id,
            document_id=db_feedback.document_id,
            created_at=db_feedback.created_at,
            feedback_type=db_feedback.feedback_type,
            notes=db_feedback.notes
        )
        
    def _message_feedback_db_model_to_schema(self, db_feedback: MessageFeedbackModel) -> MessageFeedback:
        if db_feedback is None:
            return None
        
        return MessageFeedback(
            id=db_feedback.id,
            message_id=db_feedback.message_id,
            created_at=db_feedback.created_at,
            feedback_type=db_feedback.feedback_type,
            notes=db_feedback.notes
        )
        
    def _message_db_model_to_schema(self, db_message: Message) -> ChatMessage:
        if db_message is None:
            return None
        
        return ChatMessage(
            id=db_message.id,
            role=db_message.role,
            message_type=db_message.message_type,
            sequence=db_message.sequence,
            content=db_message.content,
            formatted_content=db_message.formatted_content,
            user_query=db_message.user_query,
            rewritten_query_for_vector_base=db_message.rewritten_query_for_vector_base,
            rewritten_query_for_llm=db_message.rewritten_query_for_llm,
            search_filters=self._search_filters_db_model_to_schema(db_message.search_filters),
            feedback=self._message_feedback_db_model_to_schema(db_message.feedback),
            documents=self._documents_db_model_to_schema(db_message.documents)
        )
     
    def _search_filters_db_model_to_schema(self, db_search_filters: Dict) -> SearchFilter:
        if db_search_filters is None:
            return None
        
        return SearchFilter(
            locations=db_search_filters.get("locations", []),
            date_range=db_search_filters.get("date_range", []),
            rewrite_query=db_search_filters.get("rewrite_query", True)
        )
     
    # Convert schemas to DB models
    def _session_schema_to_db_model(self, session: Session) -> SessionModel:
        if session is None:
            return None
        
        return SessionModel(
            id=session.id,
            name=session.name,
            messages=self._messages_schema_to_db_model(session.messages)
        )

    def _messages_schema_to_db_model(self, messages: List[ChatMessage]) -> List[Message]:
        return [self._message_schema_to_db_model(message, i) for i, message in enumerate(messages)]
    
    def _documents_schema_to_db_model(self, documents: List[ChatDocument]) -> List[Document]:
        return [self._document_schema_to_db_model(document) for document in documents]

    def _message_schema_to_db_model(self, message: ChatMessage, sequence: int) -> Message:
        if message is None:
            return None
         
        db_message = Message(
            sequence=sequence,
            role=message.role,
            message_type=message.message_type,
            content=message.content,
            formatted_content=message.formatted_content,
            user_query=message.user_query,
            rewritten_query_for_vector_base=message.rewritten_query_for_vector_base,
            rewritten_query_for_llm=message.rewritten_query_for_llm,
            documents=self._documents_schema_to_db_model(message.documents),
        )
        
        if message.search_filters:
            db_message.search_filters = self._prepare_search_filters_for_db(message.search_filters)

        return db_message

    def _document_schema_to_db_model(self, document: ChatDocument) -> Document:
        if document is None:
            return None

        return Document(
            chunk_id=document.chunk_id,
            content=document.content,
            score=document.score,
            rerank_score=document.rerank_score,
            title=document.title,
            url=document.url,
        )        

    def _prepare_search_filters_for_db(self, search_filters: SearchFilter) -> Dict:
        if not search_filters:
            return None
        
        return {
            "locations": self._locations_to_db_model(search_filters.locations),
            "date_range": [date.isoformat() for date in search_filters.date_range] if search_filters.date_range else [],
            "rewrite_query": search_filters.rewrite_query
        }
        
    def _locations_to_db_model(self, locations: List[Location]):
        return [{"id": location.id, "name": location.name, "type": location.type} for location in locations]    