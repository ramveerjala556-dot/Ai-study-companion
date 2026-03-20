import random
from typing import List, Dict

class AIEngine:
    def __init__(self):
        # In a real app, you'd initialize LLM client here
        pass

    def generate_quiz(self, topic_name: str, count: int = 5) -> List[Dict]:
        """
        Generates quiz questions. In this implementation, it uses a mock generator.
        In a production app, this would call an LLM.
        """
        questions = []
        for i in range(count):
            q = {
                "question": f"Sample question {i+1} about {topic_name}?",
                "options": ["Option A", "Option B", "Option C", "Option D"],
                "correct_answer": "Option A",
                "explanation": f"This is why Option A is correct for {topic_name}."
            }
            random.shuffle(q["options"])
            questions.append(q)
        return questions

    def analyze_mistakes(self, mistakes: List[Dict]) -> str:
        """
        Analyzes a list of mistakes and provides feedback.
        """
        if not mistakes:
            return "Great job! You haven't made any mistakes yet."

        topics_struggled = {}
        for m in mistakes:
            t_id = m.get("topic_id", "Unknown")
            topics_struggled[t_id] = topics_struggled.get(t_id, 0) + 1

        # In a real app, you'd use an LLM to generate a personalized message
        struggled_list = ", ".join([str(k) for k in topics_struggled.keys()])
        return f"It looks like you're struggling with topic(s): {struggled_list}. I recommend spending more time on these."

    def generate_study_plan(self, subjects: List[Dict], mistakes: List[Dict]) -> str:
        """
        Generates a personalized study plan based on subjects and past mistakes.
        """
        # Group mistakes by topic_id
        mistake_counts = {}
        for m in mistakes:
            tid = m.get("topic_id")
            mistake_counts[tid] = mistake_counts.get(tid, 0) + 1

        # Identify top subjects to focus on
        focus_topics = []
        for s in subjects:
            for t in s.get("topics", []):
                if mistake_counts.get(t["id"], 0) > 0:
                    focus_topics.append((t["name"], mistake_counts[t["id"]]))

        focus_topics.sort(key=lambda x: x[1], reverse=True)

        if not focus_topics:
            return "Keep it up! Your progress is excellent. Follow your current schedule."

        plan = "### Your Personalized Study Plan\n\n"
        plan += "Based on your recent performance, you should prioritize these topics:\n"
        for name, count in focus_topics[:3]:
            plan += f"- **{name}**: You've made {count} mistake(s) here recently.\n"

        plan += "\n**Next Steps:**\n1. Review the concepts for these topics.\n2. Retake quizzes for these subjects.\n3. Reach out to your AI companion if you have questions!"
        return plan

    def calculate_srs_score(self, topic_id: int, quizzes: List[Dict], mistakes: List[Dict]) -> float:
        """
        Calculates a 'Mastery Score' from 0 to 1 based on performance and recency.
        0 = Needs immediate review, 1 = Mastered.
        """
        topic_quizzes = [q for q in quizzes if q.get("topic_id") == topic_id]
        if not topic_quizzes:
            return 0.5 # Unknown

        # Basic scoring: weight score by recency
        score_sum = 0
        weight_sum = 0
        for i, q in enumerate(reversed(topic_quizzes)):
            weight = 1 / (i + 1)
            score_sum += (q["score"] / q["total_questions"]) * weight
            weight_sum += weight

        mastery = score_sum / weight_sum

        # Penalize for recent mistakes
        recent_mistakes = [m for m in mistakes if m.get("topic_id") == topic_id]
        penalty = len(recent_mistakes) * 0.1

        return max(0.0, min(1.0, mastery - penalty))

    def get_ai_response(self, user_input: str, topic_name: str = "General") -> str:
        """
        Generates a competitive and motivating AI response.
        """
        # In a real app, this would be an LLM with a specific system prompt.
        responses = [
            f"Oh, you want to learn about {topic_name}? Let's see if you can keep up with me!",
            f"Focus! {topic_name} isn't going to master itself. Ready for a challenge?",
            f"I've seen your recent scores in {topic_name}... are you even trying? Let's fix that right now.",
            f"Mastering {topic_name} is the first step to outsmarting the system. Let's get to work."
        ]
        return random.choice(responses)

    def select_challenge(self, topic_name: str) -> Dict:
        """
        Selects a challenging question for the user.
        """
        questions = self.generate_quiz(topic_name, count=1)
        challenge = questions[0]
        challenge["question"] = f"🔥 CHALLENGE: {challenge['question']}"
        return challenge

ai_engine = AIEngine()
