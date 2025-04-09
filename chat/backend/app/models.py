from sqlalchemy import Column, String, JSON, DateTime, ForeignKey, Integer, Text, Enum, Float, UUID
from sqlalchemy.sql import func
from .database import Base
from sqlalchemy.orm import relationship
import uuid
from datetime import datetime
from enum import Enum

class FeedbackType(Enum):
    POSITIVE = "positive"
    NEGATIVE = "negative"
    RELEVANT = "relevant"
    IRRELEVANT = "irrelevant"


class MessageFeedback(Base):
    __tablename__ = "messages_feedback"

    id = Column(Integer, primary_key=True, autoincrement=True)
    message_id = Column(Integer, ForeignKey("messages.id", ondelete="CASCADE"), nullable=False, unique=True)
    feedback_type = Column(String(10), nullable=True, default=None)
    notes = Column(String(2048), nullable=True)
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), server_default=func.now(), onupdate=func.now())

    message = relationship("Message", back_populates="feedback")

class SessionFeedback(Base):
    __tablename__ = "sessions_feedback"
    
    id = Column(Integer, primary_key=True, autoincrement=True)
    session_id = Column(String(36), ForeignKey('sessions.id'), nullable=True)
    question = Column(String(2048))
    name = Column(String(255), nullable=True)
    email = Column(String(255), nullable=True)
    created_at = Column(DateTime, default=datetime.utcnow)
    
    session = relationship("Session", back_populates="feedback", uselist=False)

class Session(Base):
    __tablename__ = "sessions"

    id = Column(String(36), primary_key=True)
    name = Column(String(255))
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), onupdate=func.now())

    messages = relationship("Message", back_populates="session", order_by="Message.sequence")
    feedback = relationship("SessionFeedback", back_populates="session")

class Message(Base):
    __tablename__ = "messages"

    id = Column(Integer, primary_key=True, autoincrement=True)
    session_id = Column(String(36), ForeignKey('sessions.id'))
    sequence = Column(Integer)
    role = Column(String(50))
    content = Column(Text)
    user_query = Column(Text, nullable=True)
    rewritten_query_for_vector_base = Column(Text, nullable=True)
    rewritten_query_for_llm = Column(Text, nullable=True)
    formatted_content = Column(Text, nullable=True)
    message_type = Column(String(50), nullable=True)
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    search_filters = Column(JSON, nullable=True)

    session = relationship("Session", back_populates="messages")
    documents = relationship(
        "Document",
        secondary="message_documents",
        back_populates="messages",
        overlaps="documents,messages"
    )
    feedback = relationship("MessageFeedback", back_populates="message", uselist=False)
    
class Document(Base):
    __tablename__ = "documents"

    id = Column(Integer, primary_key=True, autoincrement=True)
    chunk_id = Column(String(36), nullable=False)
    content = Column(Text)
    meta = Column(JSON)
    score = Column(Float)
    rerank_score = Column(Float, nullable=True)
    title = Column(String(255), nullable=True)
    url = Column(String(1024), nullable=True)
    created_at = Column(DateTime(timezone=True), server_default=func.now())

    messages = relationship(
        "Message", 
        secondary="message_documents",
        back_populates="documents",
        overlaps="documents,messages"
    )
    feedback = relationship("DocumentFeedback", back_populates="document", uselist=False)

class MessageDocument(Base):
    __tablename__ = "message_documents"

    message_id = Column(Integer, ForeignKey('messages.id'), primary_key=True)
    document_id = Column(Integer, ForeignKey('documents.id'), primary_key=True)
    created_at = Column(DateTime(timezone=True), server_default=func.now())

class DocumentFeedback(Base):
    __tablename__ = "documents_feedback"

    id = Column(Integer, primary_key=True, autoincrement=True)
    document_id = Column(Integer, ForeignKey("documents.id", ondelete="CASCADE"), nullable=False, unique=True)
    feedback_type = Column(String(10), nullable=True, default=None)
    notes = Column(String(2048), nullable=True)
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), server_default=func.now(), onupdate=func.now())

    document = relationship("Document", back_populates="feedback")
