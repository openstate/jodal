import time
from typing import List
import logging
from ..config import settings
import httpx
from fastapi import HTTPException
from ..schemas import Location
# Set up logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Cache variables
locations_cache = None
locations_cache_time = 0
CACHE_EXPIRATION = 86400  # 24 hours in seconds

class BronService:    
    def __init__(self):
        pass
    
    async def _fetch_locations_data(self):
        """Fetch locations data from the external API"""
        locations_url = 'https://api.bron.live/locations/search?includes=id,name,kind&limit=999'
        response = None
        
        try:
            async with httpx.AsyncClient() as client:
                response = await client.get(locations_url)
                response.raise_for_status()  # Raise an error for bad responses
        
        except httpx.HTTPStatusError as http_error:
            logger.error('HTTP error occurred: %s', http_error)
            raise HTTPException(
                status_code=http_error.response.status_code,
                detail=f"HTTP error occurred: {http_error.response.text}"
            )
        except httpx.RequestError as request_error:
            logger.error('Request error occurred: %s', request_error)
            raise HTTPException(
                status_code=500,
                detail="Error occurred while making the request to the external API."
            )
            
        return response

    async def get_locations(self) -> List[Location]:
        """Return a list of available locations"""
        global locations_cache, locations_cache_time

        # Check if cache is still valid
        if locations_cache is not None and (time.time() - locations_cache_time) < CACHE_EXPIRATION:
            return locations_cache
                
        locations_response = await self._fetch_locations_data()  # Call the new function
                    
        hits = locations_response.json().get('hits', {}).get('hits', [])

        # Transform the data into the desired format
        locations = []
        for hit in hits:
            source = hit.get('_source', {})
            
            # Check if 'id' key exists in the source
            if 'id' not in source:
                logger.warning('Missing expected key "id" in source: %s', source)
                continue  # Skip this item if 'id' is missing

            # Skip items where id contains 'type:' or '*'
            if 'type:' in source['id'] or '*' in source['id']:
                continue

            # Use get to safely access 'kind'
            kind = source.get('kind', 'ministry')  # Default to 'ministry' if 'kind' is not present

            # Map the kind to the desired format
            if kind == 'municipality':
                kind_label = 'Gemeente'
            elif kind == 'province':
                kind_label = 'Provincie'
            elif kind == 'ministry':
                kind_label = 'Ministerie'
            else:
                kind_label = 'Ministerie'
            
            if source.get('name', '') == '':
                continue
            
            locations.append(
                Location(
                    id=source['id'],
                    name=source.get('name', ''),  # Default to 'Unnamed' if 'name' is not present
                    type=kind_label
                )
            )

        # Update cache with the original response
        locations_cache = locations  # Cache the original response
        locations_cache_time = time.time()
        
        return locations_cache
    
    async def get_locations_by_ids(self, location_ids: List[str]) -> List[Location]:
        # Use cache if available, otherwise fetch data
        if location_ids is None or len(location_ids) == 0:
            return []
        
        locations = await self.get_locations()
        
        # Create a lookup dictionary for faster access
        location_map = {location.id: location for location in locations}
        
        # Get Location objects using dictionary lookup
        filtered_locations = [location_map[loc_id] for loc_id in location_ids if loc_id in location_map]
        
        return filtered_locations
