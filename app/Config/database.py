from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from app.Config.application import BASEDIR

#SQLALCHEMY_DATABASE_URL = 'sqlite:///'+BASEDIR+'../../Sqlite.db'
SQLALCHEMY_DATABASE_URL = f"postgresql://rkvxqcpddhclhs:14726f38b69d3a9a952901f345a3f0eda56d90be9b3c9b5c8973eff514e0b1c9@ec2-54-225-203-79.compute-1.amazonaws.com:5432/d2qprvgu3mfhtt"
engine = create_engine(
    SQLALCHEMY_DATABASE_URL,
)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

Base = declarative_base()
