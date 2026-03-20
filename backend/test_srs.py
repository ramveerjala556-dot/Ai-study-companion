from backend.ai_engine import ai_engine
import unittest

class TestSRS(unittest.TestCase):
    def test_calculate_srs_score(self):
        topic_id = 1
        quizzes = [{"topic_id": 1, "score": 8, "total_questions": 10}] # 0.8
        mistakes = []
        score = ai_engine.calculate_srs_score(topic_id, quizzes, mistakes)
        self.assertAlmostEqual(score, 0.8)

        # Add a mistake, score should drop
        mistakes = [{"topic_id": 1}]
        score_with_mistake = ai_engine.calculate_srs_score(topic_id, quizzes, mistakes)
        self.assertAlmostEqual(score_with_mistake, 0.7)

if __name__ == "__main__":
    unittest.main()
