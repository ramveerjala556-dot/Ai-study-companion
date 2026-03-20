from backend.ai_engine import ai_engine
import unittest

class TestAIEngine(unittest.TestCase):
    def test_generate_quiz(self):
        topic = "Python Programming"
        questions = ai_engine.generate_quiz(topic, count=3)
        self.assertEqual(len(questions), 3)
        for q in questions:
            self.assertIn("Python Programming", q["question"])
            self.assertEqual(len(q["options"]), 4)
            self.assertIn(q["correct_answer"], q["options"])
            self.assertIn("explanation", q)

    def test_analyze_mistakes(self):
        mistakes = [{"topic_id": 1, "question": "Q1", "incorrect_answer": "W1", "correct_answer": "C1", "explanation": "E1"}]
        analysis = ai_engine.analyze_mistakes(mistakes)
        self.assertIn("struggling with topic(s): 1", analysis)

if __name__ == "__main__":
    unittest.main()
