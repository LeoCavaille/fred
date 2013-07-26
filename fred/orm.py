from sqlalchemy.ext.declarative import declarative_base

Base = declarative_base()

from sqlalchemy import Column, String, DateTime

class Changes(Base):
    __tablename__ = 'changes'
    nameversion = Column(String(100), unique=True, primary_key=True)
    name = Column(String(100))
    version = Column(String(50))
    suite = Column(String(50))
    created_at = Column(DateTime)
