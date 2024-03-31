from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker,declarative_base
from urllib.parse import quote_plus

import time
from app.config import settings

DATABASE_URI: str = f"mysql+pymysql://{settings.DATABASE_USERNAME}:%s@{settings.DATABASE_HOSTNAME}:{settings.DATABASE_PORT}/{settings.DATABASE_NAME}" % quote_plus(settings.DATABASE_PASSWORD)
engine = create_engine(DATABASE_URI,
                       pool_pre_ping=True,
                       pool_recycle=3600,
                       pool_size=20,
                       max_overflow=0,
                       echo=True)


SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

Base = declarative_base()


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


# test connection
# try:
#     engine.connect()
#     print("Successfully connected to database")
# except Exception as e:
#     print(f"Error connecting to database: {e}")