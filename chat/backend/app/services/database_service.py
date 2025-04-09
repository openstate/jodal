from fastapi import Depends
from sqlalchemy.orm import Session
from ..database import get_db

class DatabaseService:
    def __init__(self, db: Session = Depends(get_db)):
        self.db = db
