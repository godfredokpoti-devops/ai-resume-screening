from sqlalchemy import Column, Integer, String
from sqlalchemy.orm import declarative_base

Base = declarative_base()

class Candidate(Base):
    __tablename__ = "candidates"

    id = Column(Integer, primary_key=True, index=True)
    resume_name = Column(String)
    ats_score = Column(Integer)
    matched_skills = Column(String)
    missing_skills = Column(String)