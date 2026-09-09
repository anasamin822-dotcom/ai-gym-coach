from services.config.workout_config import PROMPT


class LLMCoach:
    def __init__(self, groq_client):
        self.client = groq_client
        self.history = []
        self.system_prompt = PROMPT

 def give_feedback(self, event, issue=None):
        prompt = f"Event: {event}"
        if issue:
            prompt += f" | Issue: {issue}"

        messages = [
            {"role": "system", "content": "You are an encouraging, energetic AI gym coach. Give very short, punchy 1-sentence real-time voice feedback."},
            {"role": "user", "content": prompt}
        ]

        # 1. Fallback default responses agar API fail ho
        fallback_responses = {
            "workout_started": "Workout started! Focus on your form and keep a steady pace.",
            "rep_completed": "Good rep! Keep your core tight.",
            "form_warning": "Watch your form, stay balanced and controlled.",
            "workout_ended": "Great session! Excellent effort today."
        }
        default_reply = fallback_responses.get(event, "Keep going, you're doing great!")

        # 2. Try calling Groq API safely
        try:
            # First try llama3-8b-8192, if fails fallback to safe string
            response = self.client.chat.completions.create(
                model="llama3-8b-8192",
                messages=messages,
                temperature=0.4,
                max_tokens=60
            )
            text = response.choices[0].message.content.strip()
            return text
        except Exception:
            # Agar Groq API 404 ya connection error de, app crash nahi hoga
            return default_reply
    
