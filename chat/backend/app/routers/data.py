from fastapi import APIRouter, HTTPException, Depends
import logging
from ..config import settings
from sqlalchemy.orm import Session as SQLAlchemySession
from ..database import get_db
from ..services.bron_service import BronService

router = APIRouter()

# Set up logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

ENVIRONMENT = settings.ENVIRONMENT

base_api_url = "/"
if ENVIRONMENT == "development":
    base_api_url = "/api/"


@router.get(base_api_url + "locations")
async def get_locations(db: SQLAlchemySession = Depends(get_db)):
    """Return a list of available locations"""
   
    bron_service = BronService()
    try:
        return await bron_service.get_locations()
    except Exception as e:
        logger.error(f"Error fetching locations: {e}")
        raise HTTPException(status_code=500, detail="Error fetching locations")
