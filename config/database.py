import os
from dotenv import load_dotenv
from sqlalchemy import create_engine
from sqlalchemy.engine import URL
from sqlalchemy.orm import sessionmaker, declarative_base

load_dotenv()

Base = declarative_base()

class DatabaseManager:
    """Singleton Database"""
    _instance = None

    def __new__(cls):
        if cls._instance is None:
            cls._instance = super(DatabaseManager, cls).__new__(cls)
            cls._instance._initialize()
        return cls._instance
    
    def _initialize(self):
        db_user = os.getenv('DB_USER')
        db_password = os.getenv('DB_PASSWORD')
        db_host = os.getenv('DB_HOST')
        db_port = os.getenv('DB_PORT')
        db_name = os.getenv('DB_NAME')

        min_conn = int(os.getenv('MIN_CONN', 5))
        max_conn = int(os.getenv('MAX_CONN', 40))

        db_url = URL.create(
            drivername="postgresql+psycopg2",
            username=db_user,
            password=db_password,
            host=db_host,
            port=db_port,
            database=db_name
        )

        self.engine = create_engine(
            db_url,
            echo=True,
            pool_size=min_conn,
            max_overflow=(max_conn - min_conn)
        )
        self.SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=self.engine)

    def get_session(self):
        """Get a database session."""
        return self.SessionLocal()
    
db = DatabaseManager()

        
