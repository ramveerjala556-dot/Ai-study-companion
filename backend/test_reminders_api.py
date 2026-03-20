import requests
import datetime
import time

def test_reminders_api():
    base_url = "http://localhost:8000"

    # 1. Create a subject
    resp = requests.post(f"{base_url}/subjects/", json={"name": "History"})
    subject = resp.json()
    subject_id = subject["id"]

    # 2. Create a topic
    resp = requests.post(f"{base_url}/subjects/{subject_id}/topics/", json={"name": "French Revolution"})
    topic = resp.json()
    topic_id = topic["id"]

    # 3. Create an exam schedule
    exam_date = (datetime.datetime.utcnow() + datetime.timedelta(days=3)).isoformat()
    resp = requests.post(f"{base_url}/schedules/", json={
        "subject_id": subject_id,
        "topic_id": topic_id,
        "scheduled_date": exam_date,
        "is_exam": True
    })

    # 4. Create a quiz with mistakes
    resp = requests.post(f"{base_url}/quizzes/", json={
        "topic_id": topic_id,
        "score": 0,
        "total_questions": 1,
        "mistakes": [{
            "question": "Who was the king?",
            "incorrect_answer": "Louis XIV",
            "correct_answer": "Louis XVI",
            "explanation": "Louis XVI was the last king of France.",
            "topic_id": topic_id
        }]
    })

    # 5. Check reminders
    resp = requests.get(f"{base_url}/ai/reminders/")
    reminders = resp.json()

    print(f"Found {len(reminders)} reminders")
    for r in reminders:
        print(f"Type: {r['type']}")
        print(f"Message: {r['message'][:100]}...")

    assert any(r["type"] == "exam_reminder" for r in reminders)
    assert any(r["type"] == "study_suggestion" for r in reminders)
    print("Test passed!")

if __name__ == "__main__":
    # Restart server to pick up changes
    import subprocess
    subprocess.run(["pkill", "-f", "uvicorn"])
    server = subprocess.Popen(["uvicorn", "backend.main:app", "--port", "8000"])
    time.sleep(3)
    try:
        test_reminders_api()
    finally:
        server.terminate()
