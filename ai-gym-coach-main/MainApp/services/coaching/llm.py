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

        fallback_responses = {
            "workout_started": "Workout started! Focus on your form and keep a steady pace.",
            "rep_completed": "Good rep! Keep your core tight.",
            "form_warning": "Watch your form, stay balanced and controlled.",
            "workout_ended": "Great session! Excellent effort today."
        }
        default_reply = fallback_responses.get(event, "Keep going, you're doing great!")

        if not self.client:
            return default_reply

        messages = [
            {"role": "system", "content": self.system_prompt},
            *self.history[-4:],
            {"role": "user", "content": prompt}
        ]

        try:
            response = self.client.chat.completions.create(
                model="llama-3.1-8b-instant",
                messages=messages,
                temperature=0.4,
                max_tokens=60
            )
            text = response.choices[0].message.content.strip()
            self.history.append({"role": "user", "content": prompt})
            self.history.append({"role": "assistant", "content": text})
            return text
        except Exception:
            return default_reply
