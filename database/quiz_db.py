from sqlalchemy import create_engine, MetaData
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from databases import Database
from dotenv import load_dotenv
import os

# Dev purposes only
load_dotenv(".env")

# Create database credential object
USERNAME = os.getenv("DATABASE_USERNAME", None)
PSW = str(os.environ.get("DATABASE_PASSWORD", None))
HOST = str(os.environ.get("DATABASE_HOST", None))
DB = str(os.environ.get("DATABASE_NAME", None))


DATABASE_URL = f"mysql+pymysql://{USERNAME}:{PSW}@{HOST}/{DB}"
database = Database(DATABASE_URL)


# SQLAlchemy New engine
metadata = MetaData()
engine = create_engine(DATABASE_URL)

SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

Base = declarative_base()
