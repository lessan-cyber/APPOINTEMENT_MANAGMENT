from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker,declarative_base
import psycopg2
from psycopg2.extras import RealDictCursor
import time
from app.config import settings

#SQLALCHEMY_DATABASE_URL = f'postgresql://{settings.DATABASE_USERNAME}:{settings.DATABASE_PASSWORD}@{settings.DATABASE_HOSTNAME}:{settings.DATABASE_PORT}/{settings.DATABASE_NAME}'
#SQLALCHEMY_DATABASE_URL = f'postgresql://{settings.DATABASE_USERNAME}:{settings.DATABASE_PASSWORD}@{settings.DATABASE_HOSTNAME}:{settings.DATABASE_PORT}/{settings.DATABASE_NAME}'
SQLALCHEMY_DATABASE_URL = f'mysql+pymysql://{settings.DATABASE_USERNAME}:{settings.DATABASE_PASSWORD}@{settings.DATABASE_HOSTNAME}:{settings.DATABASE_PORT}/{settings.DATABASE_NAME}'
engine = create_engine(SQLALCHEMY_DATABASE_URL,
                       pool_pre_ping=True,
                       pool_recycle=3600,
                       pool_size=20,
                       max_overflow=0,
                       echo=True)
#engine = create_engine(SQLALCHEMY_DATABASE_URL)

SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

Base = declarative_base()


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


# while True:
#
#     try:
#         conn = psycopg2.connect(host=settings.DATABASE_HOSTNAME, database=settings.DATABASE_NAME, user=settings.DATABASE_USERNAME,
#                                 password=settings.DATABASE_PASSWORD, cursor_factory=RealDictCursor)
#         cursor = conn.cursor()
#         print("Database connection was succesfull BABY!")
#         break
#     except Exception as error:
#         print("Connecting to database failed")
#         print("Error: ", error)
#         time.sleep(2)
