import os
import re


def get_safe_secret(key: str, default: str = "") -> str:
    val = os.environ.get(key, "")
    if val:
        return val
    try:
        import streamlit as st
        try:
            sec_val = st.secrets.get(key, default)
            return str(sec_val) if sec_val is not None else default
        except Exception:
            return default
    except Exception:
        return default


class FitnessAIAgent:
    """
    Real-Time Conversational AI Fitness Coach & Sports Nutritionist.
    Combines Cloud Groq LPU LLM inference with a deep offline Sports Science
    Knowledge Base to ensure rich, dynamic, non-repetitive answers for any query.
    """

    def __init__(self, api_key: str = None):
        self.api_key = api_key or get_safe_secret("GROQ_API_KEY", "")
        self.client = None
        if self.api_key:
            try:
                from groq import Groq
                self.client = Groq(api_key=self.api_key)
            except Exception:
                self.client = None

    def ask(self, query: str, context: dict = None) -> str:
        query_clean = query.strip()
        if not query_clean:
            return "Apna koi fitness ya diet ka doubt poochhein, mai turant advise dunga!"

        context = context or {}
        bmi_val = context.get("bmi", "Normal")
        category = context.get("category", "Normal")
        goal = context.get("goal", "Fitness")
        diet_pref = context.get("diet_pref", "Veg")
        exercise = context.get("exercise", "General Training")

        # 1. Try Live Groq LLM Inference first
        if self.client:
            try:
                system_prompt = (
                    "You are 'Apna AI Coach', an elite Olympic strength & conditioning coach and clinical sports nutritionist. "
                    "You talk to the athlete in friendly, energetic, motivating Hinglish (Hindi + English). "
                    "Rules: "
                    "1. Give direct, practical, scientifically accurate fitness/diet advice. "
                    "2. NEVER give generic one-liners. Use 3-4 structured bullet points with emojis. "
                    "3. Factor in the user's bio-metrics: "
                    f"User BMI: {bmi_val} ({category}), Goal: {goal}, Diet: {diet_pref}, Current Exercise: {exercise}. "
                    "4. If asked about supplements (creatine, whey), give exact timing, dosage, and safety. "
                    "5. If asked about pain/injury, advise biomechanics correction and safety."
                )
                
                resp = self.client.chat.completions.create(
                    model="llama-3.1-8b-instant",
                    messages=[
                        {"role": "system", "content": system_prompt},
                        {"role": "user", "content": query_clean}
                    ],
                    max_tokens=300,
                    temperature=0.6
                )
                answer = resp.choices[0].message.content.strip()
                if len(answer) > 20:
                    return answer
            except Exception:
                pass  # Fall through to Sports Science Knowledge Engine

        # 2. Advanced Contextual Sports Science Reasoning Engine (Offline / Standalone)
        return self._generate_contextual_advice(query_clean, context)

    def _generate_contextual_advice(self, query: str, ctx: dict) -> str:
        q = query.lower()
        goal = ctx.get("goal", "Maintain").lower()
        diet = ctx.get("diet_pref", "Veg").lower()
        bmi = ctx.get("bmi", 22.0)

        # Topic 1: Pre-workout food / timing
        if any(w in q for w in ["pre workout", "pehle kya khaye", "workout se pehle", "energy", "pre-workout", "subah kya khaye"]):
            if "veg" in diet:
                meals = "1-2 Kela (Banana) + 1 spoon Peanut Butter, ya Brown bread pe Peanut butter, ya 1 cup Dalia/Oats"
            else:
                meals = "2 Boiled Eggs + 1 Brown bread toast, ya 1 Banana with Black Coffee"
            return (
                f"⚡ **Pre-Workout Fuel Strategy (Goal: {ctx.get('goal', 'Workout')}):**\n\n"
                f"• **Timing Window:** Workout shuru karne se 45-60 minute pehle khayein taaki stomach heavy na lage.\n"
                f"• **Best Pre-Workout Meal ({diet.title()}):** {meals}. Yeh fast-digesting complex carbs aapko continuous stamina denge.\n"
                f"• **Instant Energy Boost:** Workout se 20 minute pehle bina cheeni wali Black Coffee piyein (Natural Caffeine focus aur strength 15% badha deta hai).\n"
                f"• **Hydration Check:** Workout se pehle 400-500ml paani zaroor piyein taaki muscle cramps na aayein!"
            )

        # Topic 2: Post-workout food & recovery
        if any(w in q for w in ["post workout", "baad me kya", "workout ke baad", "post-workout", "recovery"]):
            protein_sources = "1 scoop Whey Protein + 1 Kela ya Paneer/Tofu bhurji + Roti" if "veg" in diet else "1 scoop Whey Protein + 3 Boiled Eggs / Chicken Breast + Rice"
            return (
                f"🔥 **Post-Workout Anabolic Recovery Protocol:**\n\n"
                f"• **Anabolic Window (Within 45 mins):** Workout ke dauran muscle fibers break hote hain, unhe repair karne ke liye fast protein + glycogen chahiye.\n"
                f"• **Recommended Post-Workout:** {protein_sources}.\n"
                f"• **Carbs are Crucial:** Sirf protein mat lo, saath me thoda carbohydrate (Rice/Banana) zaroor lo taaki glycogen restore ho aur protein muscle synthesis me jaye.\n"
                f"• **Electrolyte Balance:** Thoda sa nimbu paani with a pinch of rock salt piyein taaki sweat se nikle minerals replenish ho sakein."
            )

        # Topic 3: Creatine
        if "creatine" in q:
            return (
                "💊 **Creatine Monohydrate Complete Guide:**\n\n"
                "• **Dosage:** Rozana **3 se 5 grams** Creatine Monohydrate lein. Kisi loading phase ki zaroorat nahi hai.\n"
                "• **Best Timing:** Workout ke turant baad apne post-workout shake ya kisi carb drink ke saath lena best absorb hota hai.\n"
                "• **How it works:** Yeh aapke muscles me ATP (cellular energy) recharge karta hai, jisse 2-3 extra reps aur explosive power milti hai.\n"
                "• **Golden Rule:** Creatine lete waqt din bhar me **3.5 se 4.5 Liters paani** zaroor piyein taaki zero dehydration aur full muscle volumization mile!"
            )

        # Topic 4: Whey Protein & Supplements
        if any(w in q for w in ["whey", "protein powder", "supplement", "bcaa", "mass gainer"]):
            return (
                f"🥤 **Protein & Supplement Blueprint ({ctx.get('goal', 'General')}):**\n\n"
                f"• **Daily Target:** Apne body weight ka **1.6g se 2.0g per kg** total protein target rakhein.\n"
                f"• **Whey Protein Timing:** Sabse best time post-workout hota hai ya subah breakfast me jab body ko fast absorption chahiye.\n"
                f"• **Mass Gainer Warning:** Agar goal lean muscle hai, toh sugar-loaded mass gainers avoid karein; normal Whey + Oats + Peanut butter shake banayein.\n"
                f"• **Essential Supplements:** Bas 2 core supplements kafi hain: **Whey Protein** (diet complete karne ke liye) aur **Creatine Monohydrate 3g** (power ke liye)."
            )

        # Topic 5: Muscle Building / Biceps / Chest / Hypertrophy
        if any(w in q for w in ["bicep", "chest", "muscle", "hypertrophy", "size kaise", "growth", "shoulder"]):
            return (
                f"💪 **Hypertrophy & Muscle Growth Strategy:**\n\n"
                f"• **Progressive Overload:** Har hafte ya toh 1 rep badhayein ya 1-2 kg weight badhayein. Bina overload ke muscle adapt nahi karta.\n"
                f"• **Rep Range:** Pure strength ke liye 6-8 reps, aur muscle fullness/size ke liye 10-14 reps controlled tempo (2 sec down, 1 sec explosive up) lagayein.\n"
                f"• **Weekly Volume:** Har muscle group ko hafte me **2 baar train karein** (total 12-16 working sets per week per muscle).\n"
                f"• **Mind-Muscle Connection:** Heavy jhatke (momentum) maarne ke bajaye joint ko squeeze karein — hamare WebRTC camera HUD me elbow/knee angle check karte rahein!"
            )

        # Topic 6: Fat Loss / Belly Fat / Cutting
        if any(w in q for w in ["fat loss", "belly fat", "wazan kam", "pet", "cut", "cardio", "calories"]):
            return (
                f"🎯 **Targeted Fat Loss Protocol (BMI: {bmi}):**\n\n"
                f"• **Caloric Deficit:** Apne maintenance calories se 300-400 calories kam khayein. Spot reduction (sirf pet ki charbi kam karna) scientifically possible nahi hai, overall body fat drop hoga.\n"
                f"• **Weight Training First:** Fat loss me cardio se pehle weights uthayein taaki muscle preserve rahe aur body tight bane, loose nahi.\n"
                f"• **10,000 Steps Daily (NEAT):** Roz 8,000 se 10,000 steps chalein — yeh bina muscle lose kiye 300+ calories burn karta hai.\n"
                f"• **High Protein & Fiber:** Har meal me protein aur green veggies rakhein taaki bhookh kam lage aur cravings control me rahein."
            )

        # Topic 7: Joint Pain / Knee / Shoulder / Injury
        if any(w in q for w in ["dard", "pain", "knee", "chot", "injury", "shoulder", "back", "kamar"]):
            return (
                "🩹 **Biomechanical Safety & Joint Relief:**\n\n"
                "• **Immediate Action:** Agar sharp ya shooting pain hai, toh us exercise ko turant pause karein; dull muscle burn normal hai, joint pain nahi!\n"
                "• **Squats Knee Check:** Squats me knee toes se aage nahi balki toes ki line me bahar ki taraf honi chahiye (>90 degree safe depth).\n"
                "• **Bench Press Shoulder Check:** Elbows ko 90 degree bahar flare mat karein, 45-75 degree angle par tuck rakhein rotator cuff bachane ke liye.\n"
                "• **Warm-up Routine:** Heavy sets se pehle 5 minute dynamic stretches aur rotator cuff / hip mobility zaroor karein."
            )

        # Topic 8: Vegetarian Protein Sources
        if any(w in q for w in ["veg protein", "shakahari", "vegetarian", "soya", "paneer", "daal", "tofu"]):
            return (
                "🥗 **Top High-Protein Vegetarian Sources (Indian Diet):**\n\n"
                "• **Soya Chunks (52g Protein/100g):** Sabse sasta aur highest protein source. 50g soya chunks = ~26g protein.\n"
                "• **Low Fat Paneer (18-20g/100g):** Slow-digesting casein protein jo overnight muscle repair me help karta hai.\n"
                "• **Sprouts, Chana & Daal Combo:** Daal + Rice ya Chana + Roti combine karein taaki complete essential amino acid profile bane.\n"
                "• **Greek Yogurt / Hung Curd:** 1 bowl (~150g) me 12-15g high quality protein aur gut probiotics milte hain."
            )

        # Topic 9: General / Dynamic Fallback
        return (
            f"🤖 **Personalized Coach Insights for '{query}':**\n\n"
            f"• **Form & Cadence:** Exercise karte waqt eccentric phase (weight niche aana) ko slow (2-3 sec) rakhein aur concentric ko powerful rakhein.\n"
            f"• **Caloric Target for {goal.title()}:** Aapke BMI ({bmi}) ke mutabik daily protein intake ko prioritize karein aur processed sugar bilkul cut karein.\n"
            f"• **Sleep & Recovery:** Growth Hormone sabse zyada deep sleep me release hota hai — 7 se 8 ghante ki uninterrupted sleep zaroor lein.\n"
            f"• **Live AI Feedback:** Workout shuru karte waqt sidebar se exercise select karein taaki hamara WebRTC pose tracker aapke har rep ko real-time correct kare!"
        )
