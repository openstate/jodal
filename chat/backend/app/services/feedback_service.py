from uuid import UUID
from typing import Optional
from sqlalchemy import select, update, insert
from app.models import MessageFeedback, SessionFeedback, Document, DocumentFeedback
from app.schemas import MessageFeedbackCreate, MessageFeedbackUpdate, SessionFeedbackCreate, DocumentFeedbackCreate, DocumentFeedbackUpdate, FeedbackCreate
from .database_service import DatabaseService
from fastapi import HTTPException


class FeedbackService(DatabaseService):
    def __init__(self, db):
        super().__init__(db)

    def create_message_feedback(self, feedback: MessageFeedbackCreate) -> dict:
        new_message_feedback = MessageFeedback(
            message_id=feedback.message_id,
            feedback_type=feedback.feedback_type
        )
        
        self.db.add(new_message_feedback)        
        self.db.commit()        
        self.db.refresh(new_message_feedback)
        
        return new_message_feedback

    def update_message_feedback(
        self,
        feedback: MessageFeedbackUpdate
    ) -> dict:
        db_message_feedback = self.get_message_feedback(feedback.message_id)
        
        if db_message_feedback is None:
            raise HTTPException(status_code=404, detail="Message feedback not found")

        if feedback.feedback_type is not None:
            db_message_feedback.feedback_type = feedback.feedback_type
            
        if feedback.notes is not None:
            db_message_feedback.notes = feedback.notes

        self.db.commit()
        self.db.refresh(db_message_feedback)
        
        return db_message_feedback
    
    def get_message_feedback(self, message_id: int) -> dict:        
        return self.db.query(MessageFeedback).filter(MessageFeedback.message_id == message_id).first()

    def get_session_feedback(self, session_id: int) -> dict:
        return self.db.query(SessionFeedback).filter(SessionFeedback.session_id == session_id).first()
    
    def create_session_feedback(self, feedback: SessionFeedbackCreate) -> dict:
        new_session_feedback = SessionFeedback(
            session_id=feedback.session_id,
            question=feedback.question,
            name=feedback.name,
            email=feedback.email
        )
        
        self.db.add(new_session_feedback)        
        self.db.commit()        
        self.db.refresh(new_session_feedback)
        
        return new_session_feedback
    
    def create_feedback(self, feedback: FeedbackCreate) -> dict:        
        new_feedback = SessionFeedback(
            question=feedback.question,
            name=feedback.name,
            email=feedback.email
        )
        
        self.db.add(new_feedback)        
        self.db.commit()        
        self.db.refresh(new_feedback)
        
        return new_feedback

    def create_document_feedback(self, document_feedback: DocumentFeedbackCreate) -> dict:
        """Create new document feedback"""
        new_document_feedback = DocumentFeedback(
            document_id=document_feedback.document_id,
            feedback_type=document_feedback.feedback_type
        )
        
        self.db.add(new_document_feedback)        
        self.db.commit()        
        self.db.refresh(new_document_feedback)
        
        return new_document_feedback

    def update_document_feedback(
        self,
        feedback: DocumentFeedbackUpdate
    ) -> dict:
        """Update existing document feedback"""
        document_feedback = self.get_document_feedback(feedback.document_id)
        
        if document_feedback is None:
            raise HTTPException(status_code=404, detail="Document feedback not found")

        if feedback.feedback_type is not None:
            document_feedback.feedback_type = feedback.feedback_type
            
        if feedback.notes is not None:
            document_feedback.notes = feedback.notes

        self.db.commit()
        self.db.refresh(document_feedback)
        
        return document_feedback

    def get_document_feedback(self, document_id: int) -> dict:
        """Get document feedback by document ID"""
        return self.db.query(DocumentFeedback).filter(DocumentFeedback.document_id == document_id).first()
