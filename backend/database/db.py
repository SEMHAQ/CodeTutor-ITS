from sqlalchemy import create_engine, Column, Integer, String, Float, DateTime, Text, JSON
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from datetime import datetime
import config

engine = create_engine(config.DATABASE_URL, connect_args={"check_same_thread": False})
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
Base = declarative_base()


class ChatHistory(Base):
    __tablename__ = "chat_history"
    id = Column(Integer, primary_key=True, index=True)
    session_id = Column(String, index=True)
    role = Column(String)
    content = Column(Text)
    mode = Column(String, default="tutor")
    timestamp = Column(DateTime, default=datetime.utcnow)


class StudentKnowledge(Base):
    __tablename__ = "student_knowledge"
    id = Column(Integer, primary_key=True, index=True)
    session_id = Column(String, index=True)
    knowledge_point = Column(String)
    mastery_level = Column(Float, default=0.0)
    attempts = Column(Integer, default=0)
    correct_attempts = Column(Integer, default=0)
    last_updated = Column(DateTime, default=datetime.utcnow)


class ExerciseRecord(Base):
    __tablename__ = "exercise_records"
    id = Column(Integer, primary_key=True, index=True)
    session_id = Column(String, index=True)
    exercise_title = Column(String)
    exercise_content = Column(Text)
    student_answer = Column(Text, nullable=True)
    is_correct = Column(Integer, nullable=True)  # 0=wrong, 1=correct, null=not submitted
    knowledge_points = Column(JSON)
    created_at = Column(DateTime, default=datetime.utcnow)


def init_db():
    Base.metadata.create_all(bind=engine)


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
