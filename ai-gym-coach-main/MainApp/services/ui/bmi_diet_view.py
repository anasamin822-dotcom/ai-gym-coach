"""
Gym Trainer BMI, Diet & Routine View Component for Streamlit
High-Impact Athletic UI for Hackathon Demonstrations
"""
import streamlit as st
from services.nutrition.nutrition_plan import (
    calculate_bmi,
    calculate_bmr_tdee,
    calculate_nutrition_targets,
    get_real_trainer_food_plan,
    get_gym_workout_routine,
    TRAINER_GOLDEN_RULES
)


def render_bmi_diet_planner():
    st.markdown(
        """
        <div style="margin-bottom: 20px;">
            <div class="gym-hero-badge">
                <span class="gym-status-dot"></span> CERTIFIED SPORTS NUTRITION PROTOCOL
            </div>
            <h2 style="margin: 0; font-size: 1.8rem; font-weight: 800;">
                🎯 PERSONAL GYM TRAINER • BMI & DIET ENGINE
            </h2>
            <p style="color: #94A3B8; font-size: 0.98rem; margin-top: 4px;">
                Enter your physical parameters to generate a customized gym-grade meal schedule and hypertrophy/fat-loss routine.
            </p>
        </div>
        """,
        unsafe_allow_html=True
    )

    # Input Form
    with st.form("bmi_diet_form"):
        col1, col2 = st.columns(2)

        with col1:
            gender = st.selectbox("Gender (Ling)", ["Male", "Female"], index=0)
            age = st.number_input("Age (Umar in Years)", min_value=12, max_value=85, value=22, step=1)
            height_cm = st.number_input("Height in cm", min_value=100.0, max_value=230.0, value=172.0, step=0.5,
                                        help="Example: 5'8\" = ~173 cm, 5'10\" = ~178 cm, 6'0\" = ~183 cm")
            weight_kg = st.number_input("Weight in kg", min_value=30.0, max_value=200.0, value=68.0, step=0.5)

        with col2:
            activity = st.selectbox(
                "Daily Activity / Workout Intensity",
                [
                    "Sedentary (No exercise / Desk job)",
                    "Lightly Active (1-3 days/week exercise)",
                    "Moderately Active (3-5 days/week gym)",
                    "Very Active (6-7 days/week intense gym)",
                    "Extremely Active (Athletic training / physical job)"
                ],
                index=2
            )
            goal = st.selectbox(
                "Primary Fitness Goal (Aapka Target)",
                [
                    "Muscle Building / Lean Bulk",
                    "Fat Loss / Cutting",
                    "Weight Gain / Hard Bulking",
                    "Maintenance & General Fitness"
                ],
                index=0
            )
            diet_pref = st.selectbox(
                "Dietary Preference",
                ["Vegetarian (Shakahari)", "Non-Vegetarian"],
                index=0
            )

        submit = st.form_submit_button("🔥 GENERATE GYM TRAINER PLAN", use_container_width=True)

    if submit:
        bmi_data = calculate_bmi(height_cm, weight_kg)
        tdee_data = calculate_bmr_tdee(gender, age, height_cm, weight_kg, activity)
        targets = calculate_nutrition_targets(tdee_data["tdee"], weight_kg, goal)
        meals = get_real_trainer_food_plan(goal, diet_pref)
        routine = get_gym_workout_routine(goal)

        st.session_state["user_plan"] = {
            "gender": gender,
            "age": age,
            "height_cm": height_cm,
            "weight_kg": weight_kg,
            "activity": activity,
            "goal": goal,
            "diet_pref": diet_pref,
            "bmi_data": bmi_data,
            "tdee_data": tdee_data,
            "targets": targets,
            "meals": meals,
            "routine": routine
        }

    plan = st.session_state.get("user_plan")
    if not plan:
        st.info("👆 Upar apna height, weight aur goal select karke **'Generate Gym Trainer Plan'** par click karein.")
        return

    bmi_data = plan["bmi_data"]
    targets = plan["targets"]
    tdee_data = plan["tdee_data"]
    bmi_val = bmi_data["bmi"]

    # BMI Gauge Visualizer
    st.markdown("---")
    st.markdown("### 📊 Biomechanical Assessment & BMI Telemetry")

    # Interactive progress indicator for BMI
    # Map BMI 15 to 35 -> 0% to 100%
    pct = max(0, min(100, int(((bmi_val - 15) / (35 - 15)) * 100)))

    st.markdown(
        f"""
        <div style="
            background: linear-gradient(145deg, rgba(16, 23, 38, 0.95) 0%, rgba(10, 15, 26, 0.98) 100%);
            border: 1px solid rgba(255, 255, 255, 0.08);
            border-radius: 14px;
            padding: 22px 24px;
            margin-bottom: 20px;
            box-shadow: 0 8px 28px rgba(0,0,0,0.4);
        ">
            <div style="display: flex; justify-content: space-between; align-items: center; margin-bottom: 12px; flex-wrap: wrap; gap: 10px;">
                <div>
                    <span style="font-size: 0.85rem; color: #94A3B8; text-transform: uppercase; letter-spacing: 0.05em; font-weight: 600;">Current Body Mass Index</span><br>
                    <span style="font-size: 2.4rem; font-weight: 900; color: #FFFFFF; letter-spacing: -0.02em;">{bmi_val}</span>
                    <span style="font-size: 1.1rem; color: #94A3B8;"> kg/m²</span>
                </div>
                <div style="text-align: right;">
                    <span style="font-size: 0.85rem; color: #94A3B8; text-transform: uppercase; font-weight: 600;">Status Category</span><br>
                    <span style="
                        display: inline-block;
                        background: {bmi_data['badge_color']}22;
                        border: 1px solid {bmi_data['badge_color']};
                        color: {bmi_data['badge_color']};
                        padding: 6px 14px;
                        border-radius: 8px;
                        font-weight: 800;
                        font-size: 1.05rem;
                        margin-top: 4px;
                    ">{bmi_data['category']}</span>
                </div>
            </div>
            <!-- Visual Spectrum Bar -->
            <div style="position: relative; margin: 18px 0 8px 0;">
                <div style="
                    height: 12px;
                    border-radius: 6px;
                    background: linear-gradient(90deg, #3498db 0%, #2ecc71 25%, #2ecc71 50%, #f39c12 75%, #e74c3c 100%);
                    width: 100%;
                "></div>
                <!-- Needle Indicator -->
                <div style="
                    position: absolute;
                    left: {pct}%;
                    top: -4px;
                    width: 4px;
                    height: 20px;
                    background: #FFFFFF;
                    box-shadow: 0 0 10px #FFFFFF;
                    border-radius: 2px;
                    transform: translateX(-50%);
                "></div>
            </div>
            <div style="display: flex; justify-content: space-between; font-size: 0.75rem; color: #64748B; font-weight: 600; margin-top: 6px;">
                <span>Underweight (&lt;18.5)</span>
                <span>Normal (18.5 - 24.9)</span>
                <span>Overweight (25 - 29.9)</span>
                <span>Obese (&ge;30)</span>
            </div>
            <div style="margin-top: 14px; padding-top: 12px; border-top: 1px solid rgba(255,255,255,0.06); color: #CBD5E1; font-size: 0.95rem;">
                💡 <strong>Coach Advice:</strong> {bmi_data['message']}
            </div>
        </div>
        """,
        unsafe_allow_html=True
    )

    col_a, col_b, col_c = st.columns(3)
    col_a.metric("Ideal Healthy Weight", f"{bmi_data['min_healthy_weight']} - {bmi_data['max_healthy_weight']} kg")
    col_b.metric("Basal Metabolic Rate (BMR)", f"{tdee_data['bmr']} kcal")
    col_c.metric("Maintenance Burn (TDEE)", f"{tdee_data['tdee']} kcal/day")

    # Macro Targets
    st.markdown("---")
    st.markdown(f"### 🎯 Daily Macronutrient Targets • **{plan['goal']}**")

    m1, m2, m3, m4, m5 = st.columns(5)
    with m1:
        st.markdown(
            f"""
            <div style="background: rgba(16, 23, 38, 0.9); border: 1px solid rgba(255, 94, 58, 0.35); border-top: 3px solid #FF5E3A; border-radius: 10px; padding: 14px; text-align: center;">
                <div style="font-size: 0.75rem; color: #94A3B8; font-weight: 700;">DAILY TARGET</div>
                <div style="font-size: 1.6rem; font-weight: 900; color: #FF5E3A; margin: 4px 0;">{targets['target_calories']}</div>
                <div style="font-size: 0.8rem; color: #CBD5E1;">Calories (kcal)</div>
            </div>
            """,
            unsafe_allow_html=True
        )
    with m2:
        st.markdown(
            f"""
            <div style="background: rgba(16, 23, 38, 0.9); border: 1px solid rgba(0, 245, 155, 0.35); border-top: 3px solid #00F59B; border-radius: 10px; padding: 14px; text-align: center;">
                <div style="font-size: 0.75rem; color: #94A3B8; font-weight: 700;">PROTEIN</div>
                <div style="font-size: 1.6rem; font-weight: 900; color: #00F59B; margin: 4px 0;">{targets['protein_g']}g</div>
                <div style="font-size: 0.8rem; color: #CBD5E1;">Muscle Recovery</div>
            </div>
            """,
            unsafe_allow_html=True
        )
    with m3:
        st.markdown(
            f"""
            <div style="background: rgba(16, 23, 38, 0.9); border: 1px solid rgba(0, 229, 255, 0.35); border-top: 3px solid #00E5FF; border-radius: 10px; padding: 14px; text-align: center;">
                <div style="font-size: 0.75rem; color: #94A3B8; font-weight: 700;">CARBS</div>
                <div style="font-size: 1.6rem; font-weight: 900; color: #00E5FF; margin: 4px 0;">{targets['carbs_g']}g</div>
                <div style="font-size: 0.8rem; color: #CBD5E1;">Workout Energy</div>
            </div>
            """,
            unsafe_allow_html=True
        )
    with m4:
        st.markdown(
            f"""
            <div style="background: rgba(16, 23, 38, 0.9); border: 1px solid rgba(255, 184, 0, 0.35); border-top: 3px solid #FFB800; border-radius: 10px; padding: 14px; text-align: center;">
                <div style="font-size: 0.75rem; color: #94A3B8; font-weight: 700;">HEALTHY FATS</div>
                <div style="font-size: 1.6rem; font-weight: 900; color: #FFB800; margin: 4px 0;">{targets['fats_g']}g</div>
                <div style="font-size: 0.8rem; color: #CBD5E1;">Hormone Balance</div>
            </div>
            """,
            unsafe_allow_html=True
        )
    with m5:
        st.markdown(
            f"""
            <div style="background: rgba(16, 23, 38, 0.9); border: 1px solid rgba(56, 189, 248, 0.35); border-top: 3px solid #38BDF8; border-radius: 10px; padding: 14px; text-align: center;">
                <div style="font-size: 0.75rem; color: #94A3B8; font-weight: 700;">HYDRATION</div>
                <div style="font-size: 1.6rem; font-weight: 900; color: #38BDF8; margin: 4px 0;">{targets['water_liters']}L</div>
                <div style="font-size: 0.8rem; color: #CBD5E1;">Daily Water</div>
            </div>
            """,
            unsafe_allow_html=True
        )

    # Meal Plan
    st.markdown("---")
    st.markdown(f"### 🥗 Gym Trainer Full-Day Meal Protocol • **{plan['diet_pref']}**")
    st.caption("Timed nutrition ensures peak glycogen levels for training and uninterrupted amino acid delivery for muscle repair.")

    for m in plan["meals"]:
        with st.expander(f"⏰ **{m['time']}** — {m['meal']}", expanded=True):
            st.markdown(f"**🍽️ Food Items:**\n{m['items']}")
            st.markdown(f"<div style='margin-top: 8px; color: #00F59B; font-size: 0.88rem;'>💡 <strong>Trainer Rationale:</strong> {m['notes']}</div>", unsafe_allow_html=True)

    # Workout Split
    st.markdown("---")
    st.markdown(f"### 💪 Weekly Gym Workout Routine • **{plan['goal']}**")
    st.caption("Use the **'Live Workout & AI Coach'** tab to verify your form during squats, push-ups, shoulder presses, curls & lunges!")

    tabs = st.tabs([d["day"] for d in plan["routine"]])
    for i, t in enumerate(tabs):
        day_info = plan["routine"][i]
        with t:
            st.markdown(f"#### 🎯 Target: <span style='color: #00F59B;'>{day_info['focus']}</span>", unsafe_allow_html=True)
            ex_rows = []
            for ex in day_info["exercises"]:
                ex_rows.append({
                    "Exercise": ex["name"],
                    "Sets": ex["sets"],
                    "Reps": ex["reps"],
                    "Rest Interval": ex["rest"]
                })
            st.table(ex_rows)

    # Trainer Rules
    st.markdown("---")
    st.markdown("### 🏆 Gym Trainer's 5 Commandments")
    for r in TRAINER_GOLDEN_RULES:
        st.markdown(
            f"""
            <div style="
                background: rgba(14, 20, 33, 0.7);
                border-left: 4px solid #00F59B;
                padding: 12px 16px;
                border-radius: 0 8px 8px 0;
                margin-bottom: 8px;
                color: #E2E8F0;
            ">
                {r}
            </div>
            """,
            unsafe_allow_html=True
        )

    # Interactive AI Coach advice
    if "voice_pipeline" in st.session_state and st.session_state.voice_pipeline:
        st.markdown("---")
        st.markdown("### 🤖 Ask AI Coach for Instant Custom Advice")
        user_query = st.text_input("Koi specific doubt poochhein (e.g. 'Gym se pehle kya khayein?', 'Leg day recovery tips?')")
        if st.button("⚡ Get Coach Advice", use_container_width=True):
            if user_query.strip():
                with st.spinner("AI Coach is analyzing..."):
                    client = st.session_state.voice_pipeline.llm.client
                    if client:
                        try:
                            resp = client.chat.completions.create(
                                model="llama-3.1-8b-instant",
                                messages=[
                                    {
                                        "role": "system",
                                        "content": (
                                            "You are an elite, certified fitness coach and sports nutritionist. "
                                            "Answer concisely in friendly, energetic Hinglish (Hindi + English). "
                                            "Give scientifically backed fitness, diet, and gym advice in 2-3 short bullet points."
                                        )
                                    },
                                    {
                                        "role": "user",
                                        "content": f"User BMI: {bmi_val} ({bmi_data['category']}), Goal: {plan['goal']}, Diet: {plan['diet_pref']}. Question: {user_query}"
                                    }
                                ],
                                max_tokens=150,
                                temperature=0.5
                            )
                            st.success(f"🤖 **AI Coach:**\n\n{resp.choices[0].message.content.strip()}")
                        except Exception:
                            st.info("Stay consistent, hit your daily protein goal, and drink 3-4 liters of water daily!")
