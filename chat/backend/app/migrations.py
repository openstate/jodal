from sqlalchemy import create_engine, text
from .config import settings
from .database import SessionLocal
from .models import Base, Session, Message, Document, MessageDocument
import json
import logging

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

def drop_new_tables(db):
    """Drop the new tables if they exist"""
    try:
        # Disable foreign key checks before dropping tables
        db.execute(text("SET FOREIGN_KEY_CHECKS=0"))
        db.execute(text("DROP TABLE IF EXISTS message_documents"))
        db.execute(text("DROP TABLE IF EXISTS messages"))
        db.execute(text("DROP TABLE IF EXISTS messages_feedback"))
        db.execute(text("DROP TABLE IF EXISTS documents"))
        db.execute(text("DROP TABLE IF EXISTS documents_feedback"))
        db.execute(text("DROP TABLE IF EXISTS sessions_feedback"))
        db.execute(text("SET FOREIGN_KEY_CHECKS=1"))
        db.commit()
        logger.info("Dropped existing tables")
    except Exception as e:
        logger.error(f"Error dropping tables: {str(e)}")
        db.rollback()

def migrate_up():
    db = SessionLocal()
    try:
        # Drop existing tables first
        drop_new_tables(db)
        
        # Create new tables with updated schema
        engine = create_engine(settings.DATABASE_URL)
        Base.metadata.create_all(bind=engine)
        db.commit()
        logger.info("Created new tables")
                # Add message_type column if it doesn't exist
        result = db.execute(text("""
            SELECT COUNT(*) 
            FROM information_schema.columns 
            WHERE table_name = 'messages' 
            AND column_name = 'message_type'
            AND table_schema = DATABASE()
        """))
        
        if result.scalar() == 0:
            db.execute(text("""
                ALTER TABLE messages 
                ADD COLUMN message_type VARCHAR(50) NULL
            """))
            db.commit()
            logger.info("Added message_type column to messages table")
        
        
        # Get all existing sessions with filter conditions
        result = db.execute(text("""
            SELECT id, name, messages, documents 
            FROM sessions 
            WHERE (messages IS NOT NULL AND messages != '[]' AND messages != '')
            AND created_at >= '2023-11-18'
            AND messages IS NOT NULL
        """))
        sessions_data = [(row.id, row.name, row.messages, row.documents) for row in result]
        db.commit()
        
        logger.info(f"Found {len(sessions_data)} valid sessions to migrate")
        
        # Process each session
        for session_id, name, messages_json, documents_json in sessions_data:
            try:
                messages = json.loads(messages_json) if messages_json else []
                documents = json.loads(documents_json) if documents_json else []
                
                logger.info(f"Processing session {session_id} with {len(messages)} messages and {len(documents)} documents")
                
                # Process documents first
                session_docs = {}  # Keep track of processed documents
                for doc in documents:
                    try:
                        chunk_id = doc.get("id")
                        if not chunk_id:
                            logger.warning(f"Skipping document without ID in session {session_id}")
                            continue
                        
                        result = db.execute(text("""
                            SELECT id FROM documents WHERE chunk_id = :chunk_id
                        """), {"chunk_id": chunk_id})
                        existing_id = result.scalar()

                        if existing_id:
                            doc_id = existing_id
                        else:
                            # Execute insert
                            db.execute(text("""
                                INSERT INTO documents (
                                    chunk_id, content, meta, score, title, url
                                ) VALUES (
                                    :chunk_id, :content, :meta, :score, :title, :url
                                ) ON DUPLICATE KEY UPDATE
                                    content = VALUES(content),
                                    meta = VALUES(meta),    
                                    score = VALUES(score),
                                    title = VALUES(title),
                                    url = VALUES(url)
                            """), {
                                "chunk_id": chunk_id,
                                "content": doc.get("content", ""),
                                "meta": json.dumps(doc.get("metadata", {})),
                                "score": float(doc.get("score", 0.0)),
                                "title": doc.get("title", ""),
                                "url": doc.get("url", "")
                            })
                            
                            result = db.execute(text("SELECT LAST_INSERT_ID()"))
                            doc_id = result.scalar()

                        db.commit()
                        session_docs[chunk_id] = doc_id  # Store mapping of chunk_id to new numeric id
                        logger.info(f"Processed document {chunk_id} with new ID {doc_id}")
                    except Exception as e:
                        logger.error(f"Error processing document {doc.get('id', 'unknown')}: {str(e)}")
                        db.rollback()
                
                # Process messages
                for idx, msg in enumerate(messages):
                    try:
                        # Insert message with auto-incrementing ID
                        result = db.execute(text("""
                            INSERT INTO messages (
                                session_id, sequence, role, content, formatted_content
                            ) VALUES (
                                :session_id, :sequence, :role, :content, :formatted_content
                            )
                        """), {
                            "session_id": session_id,
                            "sequence": idx,
                            "role": msg.get("role"),
                            "content": msg.get("content", ""),
                            "formatted_content": msg.get("formatted_content", "")
                        })
                        db.commit()
                        
                        # Get the auto-generated message ID
                        message_id = result.lastrowid
                        logger.info(f"Processed message {message_id}")
                        
                        # Link documents to message
                        if msg.get("role") == "assistant" and session_docs:
                            for chunk_id, doc_id in session_docs.items():
                                try:
                                    db.execute(text("""
                                        INSERT IGNORE INTO message_documents 
                                        (message_id, document_id)
                                        VALUES (:message_id, :document_id)
                                    """), {
                                        "message_id": message_id,
                                        "document_id": doc_id  # Using the new numeric ID
                                    })
                                    db.commit()
                                except Exception as e:
                                    logger.error(f"Error linking document {doc_id} to message {message_id}: {str(e)}")
                                    db.rollback()
                    except Exception as e:
                        logger.error(f"Error processing message {idx} for session {session_id}: {str(e)}")
                        db.rollback()

                logger.info(f"Successfully processed session {session_id}")

            except Exception as e:
                logger.error(f"Error processing session {session_id}: {str(e)}")
                db.rollback()

        # Drop old columns
        try:
            # Check if columns exist before dropping
            result = db.execute(text("""
                SELECT COUNT(*) 
                FROM information_schema.columns 
                WHERE table_name = 'sessions' 
                AND column_name IN ('messages', 'documents')
                AND table_schema = DATABASE()
            """))
            
            if result.scalar() > 0:
                db.execute(text("ALTER TABLE sessions DROP COLUMN messages"))
                db.execute(text("ALTER TABLE sessions DROP COLUMN documents"))
                db.commit()
                logger.info("Successfully dropped old columns")
        except Exception as e:
            logger.error(f"Error dropping old columns: {str(e)}")
            db.rollback()
            
        # Migrate feedback data
        result = db.execute(text("""
            SELECT id, session_id, question, name, email, created_at 
            FROM feedback
            WHERE id IS NOT NULL
        """))
        feedback_data = [(row.id, row.session_id, row.question, row.name, row.email, row.created_at) 
                        for row in result]
        
        # Drop and recreate feedback table with auto-incrementing ID
        db.execute(text("DROP TABLE IF EXISTS sessions_feedback"))
        db.execute(text("""
            CREATE TABLE sessions_feedback (
                id INT AUTO_INCREMENT PRIMARY KEY,
                session_id VARCHAR(36) CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci,
                question VARCHAR(2048) CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci,
                name VARCHAR(255) CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci,
                email VARCHAR(255) CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci,
                created_at DATETIME,
                CONSTRAINT sessions_feedback_ibfk_1 FOREIGN KEY (session_id) REFERENCES sessions (id)
            ) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci
        """))
        
        # Reinsert feedback data without the old IDs
        for _, session_id, question, name, email, created_at in feedback_data:
            db.execute(text("""
                INSERT INTO sessions_feedback (session_id, question, name, email, created_at)
                VALUES (:session_id, :question, :name, :email, :created_at)
            """), {
                "session_id": session_id,
                "question": question,
                "name": name,
                "email": email,
                "created_at": created_at
            })
            
        db.execute(text("DROP TABLE IF EXISTS feedback"))        
        db.commit()
        logger.info(f"Migrated {len(feedback_data)} feedback entries")

    except Exception as e:
        logger.error(f"Migration failed: {str(e)}")
        db.rollback()
        raise e
    finally:
        db.close()

def migrate_down():
    db = SessionLocal()
    try:
        # Remove message_type column if it exists
        result = db.execute(text("""
            SELECT COUNT(*) 
            FROM information_schema.columns 
            WHERE table_name = 'messages' 
            AND column_name = 'message_type'
            AND table_schema = DATABASE()
        """))
        
        if result.scalar() > 0:
            db.execute(text("ALTER TABLE messages DROP COLUMN message_type"))
            db.commit()
            logger.info("Removed message_type column from messages table")
            
        # Check if rollback is needed
        result = db.execute(text("""
            SELECT EXISTS (
                SELECT 1 
                FROM information_schema.columns 
                WHERE table_name = 'sessions' 
                AND column_name = 'messages'
            );
        """))
        if result.scalar():
            logger.info("Tables already in old format, skipping rollback...")
            return

        # Convert back to old format
        sessions = db.execute(text("SELECT id FROM sessions")).fetchall()
        
        # Add back the columns
        db.execute(text("ALTER TABLE sessions ADD COLUMN messages JSON"))
        db.execute(text("ALTER TABLE sessions ADD COLUMN documents JSON"))
        
        for session_row in sessions:
            session_id = session_row[0]
            
            # Get all messages for this session
            messages = db.execute(text("""
                SELECT * FROM messages 
                WHERE session_id = :session_id 
                ORDER BY sequence
            """), {"session_id": session_id}).fetchall()
            
            # Get all documents for this session using new schema
            documents = db.execute(text("""
                SELECT DISTINCT d.* 
                FROM documents d
                JOIN message_documents md ON md.document_id = d.id
                JOIN messages m ON m.id = md.message_id
                WHERE m.session_id = :session_id
            """), {"session_id": session_id}).fetchall()
            
            # Convert to old format
            messages_json = []
            for msg in messages:
                messages_json.append({
                    "role": msg.role,
                    "content": msg.content,
                    "formatted_content": msg.formatted_content
                })
            
            documents_json = []
            for doc in documents:
                documents_json.append({
                    "id": doc.chunk_id,  # Use chunk_id instead of id
                    "content": doc.content,
                    "metadata": json.loads(doc.meta) if doc.meta else {}
                })
            
            # Update session
            db.execute(text("""
                UPDATE sessions 
                SET messages = :messages,
                    documents = :documents
                WHERE id = :id
            """), {
                "id": session_id,
                "messages": json.dumps(messages_json),
                "documents": json.dumps(documents_json)
            })
        
        # Drop new tables
        db.execute(text("DROP TABLE IF EXISTS message_documents"))
        db.execute(text("DROP TABLE IF EXISTS documents"))
        db.execute(text("DROP TABLE IF EXISTS messages"))
        
        # For feedback table, we can't restore the original string IDs
        # Just ensure the table exists with string ID format
        db.execute(text("DROP TABLE IF EXISTS sessions_feedback"))
        db.execute(text("""
            CREATE TABLE sessions_feedback (
                id VARCHAR(36) CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci NOT NULL,
                session_id VARCHAR(36) CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci,
                question VARCHAR(2048) CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci,
                name VARCHAR(255) CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci,
                email VARCHAR(255) CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci,
                created_at DATETIME,
                PRIMARY KEY (id),
                KEY session_id (session_id),
                CONSTRAINT sessions_feedback_ibfk_1 FOREIGN KEY (session_id) REFERENCES sessions (id)
            ) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci
        """))
        
        db.commit()
    except Exception as e:
        logger.error(f"Migration failed: {str(e)}")
        db.rollback()
        raise e
    finally:
        db.close()

if __name__ == "__main__":
    import sys
    if len(sys.argv) > 1:
        if sys.argv[1] == "down":
            migrate_down()
        elif sys.argv[1] == "force":
            logger.info("Forcing migration...")
            drop_new_tables(SessionLocal())
            migrate_up()
    else:
        migrate_up() 