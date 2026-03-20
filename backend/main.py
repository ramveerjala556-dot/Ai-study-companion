from fastapi import FastAPI, Depends, HTTPException
from sqlalchemy.orm import Session
from typing import List
import datetime
from . import models, database, ai_engine
from pydantic import BaseModel
from fastapi.middleware.cors import CORSMiddleware

models.Base.metadata.create_all(bind=database.engine)

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

class TopicBase(BaseModel):
    name: str

class TopicCreate(TopicBase):
    pass

class Topic(TopicBase):
    id: int
    subject_id: int

    class Config:
        from_attributes = True

class SubjectBase(BaseModel):
    name: str

class SubjectCreate(SubjectBase):
    pass

class Subject(SubjectBase):
    id: int
    topics: List[Topic] = []

    class Config:
        from_attributes = True

class MistakeCreate(BaseModel):
    question: str
    incorrect_answer: str
    correct_answer: str
    explanation: str
    topic_id: int

class QuizCreate(BaseModel):
    topic_id: int
    score: int
    total_questions: int
    mistakes: List[MistakeCreate] = []

class Mistake(MistakeCreate):
    id: int
    quiz_id: int

    class Config:
        from_attributes = True

class Quiz(BaseModel):
    id: int
    topic_id: int
    score: int
    total_questions: int
    created_at: datetime.datetime
    mistakes: List[Mistake] = []

    class Config:
        from_attributes = True

class StudyScheduleCreate(BaseModel):
    subject_id: int
    topic_id: int = None
    scheduled_date: datetime.datetime
    is_exam: bool = False

class StudySchedule(StudyScheduleCreate):
    id: int
    completed: bool

    class Config:
        from_attributes = True

@app.post("/subjects/", response_model=Subject)
def create_subject(subject: SubjectCreate, db: Session = Depends(database.get_db)):
    db_subject = models.Subject(name=subject.name)
    db.add(db_subject)
    db.commit()
    db.refresh(db_subject)
    return db_subject

@app.get("/subjects/", response_model=List[Subject])
def read_subjects(skip: int = 0, limit: int = 100, db: Session = Depends(database.get_db)):
    subjects = db.query(models.Subject).offset(skip).limit(limit).all()
    return subjects

@app.post("/subjects/{subject_id}/topics/", response_model=Topic)
def create_topic_for_subject(
    subject_id: int, topic: TopicCreate, db: Session = Depends(database.get_db)
):
    db_topic = models.Topic(**topic.dict(), subject_id=subject_id)
    db.add(db_topic)
    db.commit()
    db.refresh(db_topic)
    return db_topic

@app.post("/quizzes/", response_model=Quiz)
def create_quiz(quiz: QuizCreate, db: Session = Depends(database.get_db)):
    db_quiz = models.Quiz(
        topic_id=quiz.topic_id,
        score=quiz.score,
        total_questions=quiz.total_questions
    )
    db.add(db_quiz)
    db.commit()
    db.refresh(db_quiz)

    for mistake in quiz.mistakes:
        db_mistake = models.Mistake(
            quiz_id=db_quiz.id,
            **mistake.dict()
        )
        db.add(db_mistake)
    db.commit()
    db.refresh(db_quiz)
    return db_quiz

@app.get("/quizzes/", response_model=List[Quiz])
def read_quizzes(skip: int = 0, limit: int = 100, db: Session = Depends(database.get_db)):
    return db.query(models.Quiz).offset(skip).limit(limit).all()

@app.post("/schedules/", response_model=StudySchedule)
def create_schedule(schedule: StudyScheduleCreate, db: Session = Depends(database.get_db)):
    db_schedule = models.StudySchedule(**schedule.dict())
    db.add(db_schedule)
    db.commit()
    db.refresh(db_schedule)
    return db_schedule

@app.get("/schedules/", response_model=List[StudySchedule])
def read_schedules(db: Session = Depends(database.get_db)):
    return db.query(models.StudySchedule).all()

@app.get("/ai/reminders/")
def get_reminders(db: Session = Depends(database.get_db)):
    # Find upcoming exams within 7 days
    now = datetime.datetime.now(datetime.UTC)
    next_week = now + datetime.timedelta(days=7)

    exams = db.query(models.StudySchedule).filter(
        models.StudySchedule.is_exam == True,
        models.StudySchedule.scheduled_date >= now,
        models.StudySchedule.scheduled_date <= next_week
    ).all()

    reminders = []
    for exam in exams:
        subject = db.query(models.Subject).filter(models.Subject.id == exam.subject_id).first()
        reminders.append({
            "type": "exam_reminder",
            "message": f"Smart Reminder: You have an exam in **{subject.name}** on {exam.scheduled_date.strftime('%Y-%m-%d')}! Better get studying!",
            "date": exam.scheduled_date
        })

    # Analyze mistakes for study suggestions
    mistakes = db.query(models.Mistake).all()
    if mistakes:
        subjects = db.query(models.Subject).all()
        # Convert subjects to dict for AI engine
        subject_dicts = []
        for s in subjects:
            s_dict = {"id": s.id, "name": s.name, "topics": []}
            for t in s.topics:
                s_dict["topics"].append({"id": t.id, "name": t.name})
            subject_dicts.append(s_dict)

        mistake_dicts = [{"topic_id": m.topic_id} for m in mistakes]
        study_plan = ai_engine.ai_engine.generate_study_plan(subject_dicts, mistake_dicts)
        reminders.append({
            "type": "study_suggestion",
            "message": study_plan,
            "date": now
        })

    # SRS Proactive Challenges
    quizzes = db.query(models.Quiz).all()
    quiz_dicts = [{"topic_id": q.topic_id, "score": q.score, "total_questions": q.total_questions} for q in quizzes]
    mistake_dicts = [{"topic_id": m.topic_id} for m in mistakes]

    topics = db.query(models.Topic).all()
    for topic in topics:
        mastery = ai_engine.ai_engine.calculate_srs_score(topic.id, quiz_dicts, mistake_dicts)
        if mastery < 0.4:
            reminders.append({
                "type": "proactive_challenge",
                "message": f"I noticed you're slipping on **{topic.name}**. Prove me wrong with a quick challenge!",
                "topic_id": topic.id,
                "date": now
            })

    return reminders

@app.post("/ai/quiz/generate/")
def generate_quiz(topic_id: int, db: Session = Depends(database.get_db)):
    topic = db.query(models.Topic).filter(models.Topic.id == topic_id).first()
    if not topic:
        raise HTTPException(status_code=404, detail="Topic not found")
    questions = ai_engine.ai_engine.generate_quiz(topic.name)
    return {"topic_id": topic_id, "questions": questions}

@app.get("/ai/challenge/")
def get_daily_challenge(db: Session = Depends(database.get_db)):
    # Find the weakest topic via SRS
    topics = db.query(models.Topic).all()
    if not topics:
        raise HTTPException(status_code=404, detail="No topics found")

    quizzes = db.query(models.Quiz).all()
    quiz_dicts = [{"topic_id": q.topic_id, "score": q.score, "total_questions": q.total_questions} for q in quizzes]
    mistakes = db.query(models.Mistake).all()
    mistake_dicts = [{"topic_id": m.topic_id} for m in mistakes]

    weakest_topic = None
    min_mastery = 1.1

    for topic in topics:
        mastery = ai_engine.ai_engine.calculate_srs_score(topic.id, quiz_dicts, mistake_dicts)
        if mastery < min_mastery:
            min_mastery = mastery
            weakest_topic = topic

    challenge = ai_engine.ai_engine.select_challenge(weakest_topic.name)
    challenge["topic_id"] = weakest_topic.id
    return challenge

@app.post("/ai/chat/")
def ai_chat(message: str, topic_id: int = None, db: Session = Depends(database.get_db)):
    topic_name = "General"
    if topic_id:
        topic = db.query(models.Topic).filter(models.Topic.id == topic_id).first()
        if topic:
            topic_name = topic.name

    response = ai_engine.ai_engine.get_ai_response(message, topic_name)
    return {"response": response}

@app.get("/health")
def health_check():
    return {"status": "ok"}
