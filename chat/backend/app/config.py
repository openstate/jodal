import os
from pydantic_settings import BaseSettings

class Settings(BaseSettings):
    QDRANT_HOST: str = os.getenv("QDRANT_HOST", "host.docker.internal")
    QDRANT_PORT: int = int(os.getenv("QDRANT_PORT", 6333))
    DATABASE_URL: str = f"mysql://{os.getenv('MYSQL_USER')}:{os.getenv('MYSQL_PASSWORD')}@{os.getenv('MYSQL_HOST', 'mysql')}/{os.getenv('MYSQL_DATABASE')}"
    COHERE_API_KEY: str = os.getenv("COHERE_API_KEY")
    COHERE_EMBED_MODEL: str = os.getenv("COHERE_EMBED_MODEL")
    COHERE_RERANK_MODEL: str = os.getenv("COHERE_RERANK_MODEL")
    SPARSE_EMBED_MODEL: str = os.getenv("SPARSE_EMBED_MODEL")
    QDRANT_HYBRID_SEARCH_TIMEOUT: int = int(os.getenv("QDRANT_HYBRID_SEARCH_TIMEOUT"))
    EMBEDDING_QUANTIZATION: str = os.getenv("EMBEDDING_QUANTIZATION")
    QDRANT_COLLECTION: str = os.getenv("QDRANT_COLLECTION")
    
    QDRANT_SPARSE_RETRIEVE_LIMIT: int = int(os.getenv("QDRANT_SPARSE_RETRIEVE_LIMIT"))
    QDRANT_DENSE_RETRIEVE_LIMIT: int = int(os.getenv("QDRANT_DENSE_RETRIEVE_LIMIT"))
    QDRANT_HYBRID_RETRIEVE_LIMIT: int = int(os.getenv("QDRANT_HYBRID_RETRIEVE_LIMIT"))
    RERANK_DOC_RETRIEVE_LIMIT: int = int(os.getenv("RERANK_DOC_RETRIEVE_LIMIT"))
    MMR_DOC_RETRIEVE_LIMIT: int = int(os.getenv("MMR_DOC_RETRIEVE_LIMIT"))
    RERANK_RELEVANCE_THRESHOLD: float = float(os.getenv("RERANK_RELEVANCE_THRESHOLD"))    
    MMR_DOC_LAMBDA_PARAM: float = float(os.getenv("MMR_DOC_LAMBDA_PARAM"))
    
    ALLOWED_ORIGINS: str = os.getenv("ALLOWED_ORIGINS", "").split(",")
    ENVIRONMENT: str = os.getenv("ENVIRONMENT")
    # Qdrant settings
    QDRANT_POOL_SIZE: int = int(os.getenv("QDRANT_POOL_SIZE"))
    QDRANT_POOL_TIMEOUT: int = int(os.getenv("QDRANT_POOL_TIMEOUT"))
    QDRANT_TIMEOUT: int = int(os.getenv("QDRANT_TIMEOUT"))
    SENTRY_DSN: str = os.getenv("SENTRY_DSN")

    OTEL_EXPORTER_OTLP_HEADER: str = os.getenv("OTEL_EXPORTER_OTLP_HEADER")
    PHOENIX_CLIENT_HEADERS: str = os.getenv("PHOENIX_CLIENT_HEADERS")
    PHOENIX_COLLECTOR_ENDPOINT: str = os.getenv("PHOENIX_COLLECTOR_ENDPOINT")
    PHOENIX_TRACER_ENDPOINT: str = os.getenv("PHOENIX_TRACER_ENDPOINT")
    PHOENIX_PROJECT_NAME: str = os.getenv("PHOENIX_PROJECT_NAME")
    LLM_SERVICE: str = os.getenv("LLM_SERVICE", "cohere")
    
settings = Settings()
