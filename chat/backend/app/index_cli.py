import argparse
from qdrant_client import QdrantClient, models
from app.config import settings

def create_payload_index(field_name: str, field_type: str):
    """Create a payload index in Qdrant for the specified collection and field."""
    client = QdrantClient(
        url=f"http://{settings.QDRANT_HOST}:{settings.QDRANT_PORT}",
        timeout=settings.QDRANT_TIMEOUT * 2   # Increased timeout
    )
    
    try:
        if field_type == 'KEYWORD':
            print(f"Creating payload index for field '{field_name}' of type KEYWORD in collection '{settings.QDRANT_COLLECTION}'")
            result = client.create_payload_index(
                collection_name=settings.QDRANT_COLLECTION,
                field_name=field_name,
                field_schema=models.PayloadSchemaType.KEYWORD,
                wait=False
            )
            print(f"Result: {result}")
        elif field_type == 'DATETIME':
            print(f"Creating payload index for field '{field_name}' of type DATETIME in collection '{settings.QDRANT_COLLECTION}'")
            result = client.create_payload_index(
                collection_name=settings.QDRANT_COLLECTION,
                field_name=field_name,
                field_schema=models.PayloadSchemaType.DATETIME,
                wait=False
            )
            print(f"Result: {result}")
    except Exception as e:
        print(f"Error creating payload index: {str(e)}")

def delete_payload_index(field_name: str):
    """Delete a payload index in Qdrant for the specified collection and field."""
    client = QdrantClient(
        url=f"http://{settings.QDRANT_HOST}:{settings.QDRANT_PORT}",
        timeout=settings.QDRANT_TIMEOUT * 2   # Increased timeout
    )
    
    try:
        result = client.delete_payload_index(
            collection_name=settings.QDRANT_COLLECTION,
            field_name=field_name,
            wait=False
        )
        print(f"Result: {result}")
    except Exception as e:
        print(f"Error deleting payload index: {str(e)}")


def main():
    parser = argparse.ArgumentParser(description='Create or delete a payload index in Qdrant')
    
    parser.add_argument(
        '--field', 
        '-f',
        type=str,
        required=True,
        help='Name of the field to index or delete'
    )
    parser.add_argument(
        '--type',
        '-t',
        type=str,
        choices=['KEYWORD', 'DATETIME'],
        default='KEYWORD',
        help='Type of the field to index (KEYWORD or DATETIME)'
    )
    parser.add_argument(
        '--delete', 
        '-d',
        action='store_true',
        help='Delete the specified payload index instead of creating it'
    )

    args = parser.parse_args()
    
    if args.delete:
        delete_payload_index(args.field)  # Call delete function
    else:
        create_payload_index(args.field, args.type)  # Call create function

if __name__ == "__main__":
    main() 