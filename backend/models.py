from sqlalchemy import Column, Integer, String, ForeignKey, DateTime, Boolean, JSON
from sqlalchemy.orm import relationship
from .database import Base
import datetime

class User(Base):
    __tablename__ = "users"
    id = Column(Integer, primary_key=True, index=True)
    username = Column(String, unique=True, index=True)

class Subject(Base):
    __tablename__ = "subjects"
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, index=True)
    topics = relationship("Topic", back_populates="subject")

class Topic(Base):
    __tablename__ = "topics"
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, index=True)
    subject_id = Column(Integer, ForeignKey("subjects.id"))
    subject = relationship("Subject", back_populates="topics")
    quizzes = relationship("Quiz", back_populates="topic")

class Quiz(Base):
    __tablename__ = "quizzes"
    id = Column(Integer, primary_key=True, index=True)
    topic_id = Column(Integer, ForeignKey("topics.id"))
    score = Column(Integer)
    total_questions = Column(Integer)
    created_at = Column(DateTime, default=lambda: datetime.datetime.now(datetime.UTC))
    topic = relationship("Topic", back_populates="quizzes")
    mistakes = relationship("Mistake", back_populates="quiz")

class Mistake(Base):
    __tablename__ = "mistakes"
    id = Column(Integer, primary_key=True, index=True)
    quiz_id = Column(Integer, ForeignKey("quizzes.id"))
    question = Column(String)
    incorrect_answer = Column(String)
    correct_answer = Column(String)
    explanation = Column(String)
    topic_id = Column(Integer, ForeignKey("topics.id"))
    quiz = relationship("Quiz", back_populates="mistakes")

class StudySchedule(Base):
    __tablename__ = "study_schedules"
    id = Column(Integer, primary_key=True, index=True)
    subject_id = Column(Integer, ForeignKey("subjects.id"))
    topic_id = Column(Integer, ForeignKey("topics.id"), nullable=True)
    scheduled_date = Column(DateTime)
    is_exam = Column(Boolean, default=False)
    completed = Column(Boolean, default=False)
