from pydantic import BaseModel, EmailStr, field_serializer, ConfigDict
from typing import List, Dict, Optional, Any
from datetime import datetime, date
from enum import Enum

class FeedbackType(str, Enum):
    POSITIVE = "positive"
    NEGATIVE = "negative"
    RELEVANT = "relevant"
    IRRELEVANT = "irrelevant"

class MessageType(str, Enum):
    SYSTEM_MESSAGE = "system_message"
    USER_MESSAGE = "user_message"
    ASSISTANT_MESSAGE = "assistant_message"
    STATUS = "status"
    
class MessageRole(str, Enum):
    SYSTEM = "system"
    USER = "user"
    ASSISTANT = "assistant"

class DocumentFeedbackBase(BaseModel):
    document_id: int
    feedback_type: Optional[FeedbackType] = None
    notes: Optional[str] = None


class DocumentFeedback(DocumentFeedbackBase):
    id: int
    created_at: Optional[datetime] = None
    updated_at: Optional[datetime] = None

    model_config = ConfigDict(ser_json_timedelta='iso8601', from_attributes=True)
    
    @field_serializer('created_at')
    @field_serializer('updated_at')
    def serialize_dt(self, dt: datetime, _info):
        if dt:
            return dt.timestamp()
        return None
    
class DocumentBase(BaseModel):
    chunk_id: str
    content: str
    meta: Optional[Dict] = None
    score: float
    rerank_score: Optional[float] = None
    title: Optional[str] = None
    url: Optional[str] = None

class DocumentCreate(DocumentBase):
    pass

class Document(DocumentBase):
    id: int
    created_at: Optional[datetime] = None

    model_config = ConfigDict(ser_json_timedelta='iso8601', from_attributes=True)
    
    @field_serializer('created_at')
    @field_serializer('updated_at')
    def serialize_dt(self, dt: datetime, _info):
        if dt:
            return dt.timestamp()
        return None

class ChatDocument(BaseModel):
    id: Optional[int] = None
    chunk_id: str
    score: float
    rerank_score: Optional[float] = None
    content: Optional[str] = None
    title: Optional[str] = None
    url: Optional[str] = None
    feedback: Optional[DocumentFeedback] = None
    
    def __hash__(self):
        return hash(self.id)
    
    def __eq__(self, other):
        if not isinstance(other, ChatDocument):
            return False
        return self.id == other.id
    

class MessageFeedbackBase(BaseModel):
    message_id: int
    feedback_type: Optional[FeedbackType] = None
    notes: Optional[str] = None

    
class MessageFeedback(MessageFeedbackBase):
    id: int
    created_at: Optional[datetime] = None
    updated_at: Optional[datetime] = None

    model_config = ConfigDict(ser_json_timedelta='iso8601', from_attributes=True)
    
    @field_serializer('created_at')
    @field_serializer('updated_at')
    def serialize_dt(self, dt: datetime, _info):
        if dt:
            return dt.timestamp() 
        return None

class MessageFeedbackCreate(MessageFeedbackBase):
    pass


class MessageFeedbackUpdate(MessageFeedbackBase):
    pass

     
class Location(BaseModel):
    id: str
    name: str
    type: str
    
    
class SearchFilter(BaseModel):
    locations: Optional[List[Location]] = []
    date_range: Optional[List[datetime]] = []
    rewrite_query: bool = True
    
    @field_serializer('date_range')
    def serialize_dt(self, date_range: List[datetime], _info):  
        if date_range:
            return [dt.strftime("%Y-%m-%d") for dt in date_range]
        return None
  
class ChatMessage(BaseModel):
    id: Optional[int] = None
    role: MessageRole
    message_type: Optional[MessageType] = None
    sequence: Optional[int] = 0
    content: str
    formatted_content: Optional[str] = None
    user_query: Optional[str] = None
    rewritten_query_for_vector_base: Optional[str] = None
    rewritten_query_for_llm: Optional[str] = None
    feedback: Optional[MessageFeedback] = None
    documents: Optional[List[ChatDocument]] = []
    search_filters: Optional[SearchFilter] = None

    def get_param(self, param_name: str) -> Any:
        """
        Dynamically get the value of a parameter by its name.

        Args:
            param_name (str): The name of the parameter to retrieve.

        Returns:
            Any: The value of the parameter.

        Raises:
            ValueError: If the parameter does not exist in the model.
        """
        if param_name in self.model_fields:
            if param_name == "formatted_content":
                if self.formatted_content is not None and self.formatted_content != "":
                    return self.formatted_content
                else:
                    return self.content
            else:
                return getattr(self, param_name)
        else:
            raise ValueError(f"Parameter '{param_name}' does not exist in the model.")
     
        
class ChatRequest(BaseModel):
    content: str
    
    
class SessionBase(BaseModel):
    name: Optional[str] = None
    messages: List[ChatMessage] = []
    
class SessionCreate(SessionBase):
    pass


class SessionUpdate(SessionBase):
    pass


class Session(SessionBase):
    id: str
    created_at: Optional[datetime] = None
    updated_at: Optional[datetime] = None

    model_config = ConfigDict(ser_json_timedelta='iso8601', from_attributes=True)
    
    @field_serializer('created_at')
    @field_serializer('updated_at')
    def serialize_dt(self, dt: datetime, _info):
        if dt:
            return dt.timestamp()     
        return None

class FeedbackBase(BaseModel):
    id: int
    created_at: datetime
    session: Optional[Session] = None
    question: str
    name: Optional[str] = None
    email: Optional[str] = None

    model_config = ConfigDict(ser_json_timedelta='iso8601', from_attributes=True)
    
    @field_serializer('created_at')
    def serialize_dt(self, dt: datetime, _info):
        return dt.timestamp()   
        
        
class FeedbackCreateRequest(BaseModel):
    question: str
    name: Optional[str] = None
    email: Optional[str] = None

        
class FeedbackCreate(BaseModel):
    question: str
    name: Optional[str] = None
    email: Optional[str] = None
        
        
class SessionFeedbackCreate(BaseModel):
    session_id: str
    question: str
    name: Optional[str] = None
    email: Optional[str] = None


class MessageFeedbackTypeRequest(BaseModel):
    feedback_type: FeedbackType


class MessageFeedbackNotesRequest(BaseModel):
    notes: str


class DocumentFeedbackTypeRequest(BaseModel):
    feedback_type: FeedbackType


class DocumentFeedbackNotesRequest(BaseModel):
    notes: str


class DocumentFeedbackCreate(DocumentFeedbackBase):
    pass


class DocumentFeedbackUpdate(DocumentFeedbackBase):
    pass
