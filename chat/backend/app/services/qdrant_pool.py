from ..config import settings
from qdrant_client import QdrantClient
import logging
import threading
import queue
from contextlib import contextmanager
from datetime import datetime
import time
from typing import Optional

# Set up logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

class QdrantConnectionPool:
    _instance = None
    _lock = threading.Lock()
    _pool = None
    _last_health_check = None
    _health_check_interval = 60  # seconds
    _timeout = settings.QDRANT_TIMEOUT  # Ensure this is set to a higher value if needed
    
    def __init__(self):
        self._pool = queue.Queue(maxsize=settings.QDRANT_POOL_SIZE)
        self._active_connections = 0
        self._total_connections = 0
        self._failed_connections = 0
        self.initialize_pool()

    def initialize_pool(self):
        """Initialize the connection pool"""
        for _ in range(settings.QDRANT_POOL_SIZE):
            self._add_connection()

    def _add_connection(self) -> Optional[QdrantClient]:
        """Create and add a new connection to the pool"""
        try:
            client = QdrantClient(
                host=settings.QDRANT_HOST,
                port=settings.QDRANT_PORT,
                timeout=self._timeout,
                prefer_grpc=True
            )
            # Test connection
            client.get_collections()
            self._pool.put(client)
            self._total_connections += 1
            return client
        except Exception as e:
            logger.error(f"Failed to create Qdrant connection: {e}")
            self._failed_connections += 1
            return None

    def _check_connection_health(self, client: QdrantClient) -> bool:
        """Check if connection is healthy"""
        try:
            client.get_collections()
            return True
        except Exception:
            return False

    def _health_check(self):
        """Perform health check on all connections"""
        if (not self._last_health_check or 
            time.time() - self._last_health_check > self._health_check_interval):
            with self._lock:
                size = self._pool.qsize()
                for _ in range(size):
                    client = self._pool.get()
                    if not self._check_connection_health(client):
                        logger.warning("Unhealthy connection detected, creating new one")
                        client.close()
                        client = self._add_connection()
                    if client:
                        self._pool.put(client)
                self._last_health_check = time.time()

    @classmethod
    def get_instance(cls):
        """Get singleton instance with double-checked locking"""
        if cls._instance is None:
            with cls._lock:
                if cls._instance is None:
                    cls._instance = cls()
        return cls._instance

    @contextmanager
    def get_client(self):
        """Get client from pool with context manager"""
        client = None
        try:
            self._health_check()
            client = self._pool.get(timeout=settings.QDRANT_POOL_TIMEOUT)
            self._active_connections += 1
            yield client
        except queue.Empty:
            logger.error("Connection pool timeout - no available connections")
            raise RuntimeError("No available database connections")
        finally:
            if client:
                self._active_connections -= 1
                self._pool.put(client)

    def get_pool_stats(self):
        """Get pool statistics"""
        return {
            "total_connections": self._total_connections,
            "active_connections": self._active_connections,
            "available_connections": self._pool.qsize(),
            "failed_connections": self._failed_connections,
            "last_health_check": self._last_health_check
        } 