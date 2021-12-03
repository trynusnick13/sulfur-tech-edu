from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from app.Config.application import BASEDIR

#SQLALCHEMY_DATABASE_URL = 'sqlite:///'+BASEDIR+'../../Sqlite.db'
SQLALCHEMY_DATABASE_URL = "postgresql://bzfivvwzdowayi:505c1ece27926e04fb7d98bc7c4451e823af4dc86040562a9ad1367c6fc43325@ec2-54-224-194-214.compute-1.amazonaws.com:5432/d842guil5376i1"
engine = create_engine(
    SQLALCHEMY_DATABASE_URL,
    connect_args={'check_same_thread': False}
)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

Base = declarative_base()
