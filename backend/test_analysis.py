from backend.ai_engine import ai_engine
import unittest

class TestStudyPlan(unittest.TestCase):
    def test_generate_study_plan(self):
        subjects = [
            {
                "id": 1,
                "name": "Math",
                "topics": [{"id": 101, "name": "Algebra"}]
            }
        ]
        mistakes = [{"topic_id": 101, "question": "Q1"}]
        plan = ai_engine.generate_study_plan(subjects, mistakes)
        self.assertIn("### Your Personalized Study Plan", plan)
        self.assertIn("- **Algebra**: You've made 1 mistake(s) here recently.", plan)

if __name__ == "__main__":
    unittest.main()
