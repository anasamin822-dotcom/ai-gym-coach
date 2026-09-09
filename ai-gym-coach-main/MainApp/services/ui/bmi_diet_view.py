"""
Gym Trainer BMI, Diet & Routine View Component for Streamlit
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
    st.markdown("## 🏋️‍♂️ Personal Gym Trainer: BMI, Diet & Routine")
    st.caption("Apna body data dalein aur paayein ekdum certified gym trainer jaisa personalized diet aur workout schedule.")

    # Form in 2 columns
    with st.form("bmi_diet_form"):
        col1, col2 = st.columns(2)

        with col1:
            gender = st.selectbox("Gender (Ling)", ["Male", "Female"], index=0)
            age = st.number_input("Age (Umar)", min_value=12, max_value=85, value=22, step=1)
            height_cm = st.number_input("Height (cm)", min_value=100.0, max_value=230.0, value=172.0, step=0.5,
                                        help="1 foot = 30.48 cm. (Example: 5'8\" = ~173 cm)")
            weight_kg = st.number_input("Weight (kg)", min_value=30.0, max_value=200.0, value=68.0, step=0.5)

        with col2:
            activity = st.selectbox(
                "Daily Activity Level",
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
                "Primary Fitness Goal (Aapka Lakshya)",
                [
                    "Muscle Building / Lean Bulk",
                    "Fat Loss / Cutting",
                    "Weight Gain / Hard Bulking",
                    "Maintenance & General Fitness"
                ],
                index=0
            )
            diet_pref = st.selectbox(
                "Diet Preference (Khaane Ki Pasand)",
                ["Vegetarian (Shakahari)", "Non-Vegetarian"],
                index=0
            )

        submit = st.form_submit_button("🔥 Generate Trainer Plan", use_container_width=True)

    if submit:
        # Perform calculations and persist in session_state
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
        st.info("👆 Upar apna height, weight aur goal select karke **'Generate Trainer Plan'** par click karein.")
        return

    # Display Assessment
    bmi_data = plan["bmi_data"]
    targets = plan["targets"]
    tdee_data = plan["tdee_data"]

    st.markdown("---")
    st.subheader("📊 Health & BMI Assessment")

    m_col1, m_col2, m_col3, m_col4 = st.columns(4)
    with m_col1:
        st.metric("Your BMI", f"{bmi_data['bmi']}")
    with m_col2:
        st.markdown(
            f"""
            <div style="padding: 10px; border-radius: 6px; background-color: #222; border-left: 5px solid {bmi_data['badge_color']};">
                <span style="font-size: 0.85rem; color: #bbb;">Category</span><br>
                <strong style="color: {bmi_data['badge_color']}; font-size: 1.1rem;">{bmi_data['category']}</strong>
            </div>
            """,
            unsafe_allow_html=True
        )
    with m_col3:
        st.metric("Healthy Weight Range", f"{bmi_data['min_healthy_weight']} - {bmi_data['max_healthy_weight']} kg")
    with m_col4:
        st.metric("Daily Maintenance (TDEE)", f"{tdee_data['tdee']} kcal")

    st.caption(f"💡 **Trainer Tip**: {bmi_data['message']}")

    # Macro Targets
    st.markdown("---")
    st.subheader(f"🎯 Daily Nutrition Targets for: {plan['goal']}")

    n1, n2, n3, n4, n5 = st.columns(5)
    n1.metric("🔥 Target Calories", f"{targets['target_calories']} kcal")
    n2.metric("🥩 Protein", f"{targets['protein_g']} g")
    n3.metric("🍚 Carbohydrates", f"{targets['carbs_g']} g")
    n4.metric("🥑 Healthy Fats", f"{targets['fats_g']} g")
    n5.metric("💧 Water Intake", f"{targets['water_liters']} L")

    # Food Plan
    st.markdown("---")
    st.subheader(f"🥗 Full Day Gym Diet Plan ({plan['diet_pref']})")
    st.caption("Yeh diet plan proper sports nutrition principles par based hai taaki aapka muscle recovery aur energy level 100% rahe.")

    for item in plan["meals"]:
        with st.expander(f"⏰ **{item['time']}** — {item['meal']}", expanded=True):
            st.markdown(f"**🍽️ Khaane me kya lena hai:**\n\n{item['items']}")
            st.info(f"💡 **Why this meal:** {item['notes']}")

    # Gym Workout Routine
    st.markdown("---")
    st.subheader(f"💪 Weekly Gym Workout Routine ({plan['goal']})")
    st.caption("Aap in exercises ka form check karne ke liye **'Live Workout & AI Coach'** tab use kar sakte hain!")

    routine_tabs = st.tabs([d["day"] for d in plan["routine"]])
    for i, day_tab in enumerate(routine_tabs):
        day_data = plan["routine"][i]
        with day_tab:
            st.markdown(f"### 🎯 Focus: **{day_data['focus']}**")
            
            # Display formatted table of exercises
            ex_list = []
            for ex in day_data["exercises"]:
                ex_list.append({
                    "Exercise Name": ex["name"],
                    "Sets": ex["sets"],
                    "Reps": ex["reps"],
                    "Rest Time": ex["rest"]
                })
            st.table(ex_list)

    # Trainer Golden Rules
    st.markdown("---")
    st.subheader("🏆 Gym Trainer Ke 5 Golden Rules")
    for rule in TRAINER_GOLDEN_RULES:
        st.markdown(rule)

    # Optional AI Customization if Groq is available
    if "voice_pipeline" in st.session_state and st.session_state.voice_pipeline:
        st.markdown("---")
        st.subheader("🤖 Ask AI Coach for Custom Advice")
        user_query = st.text_input("Koi specific question poochhein (e.g., 'Agar mujhe gym me weakness lage to kya khana chahiye?')")
        if st.button("💬 Get AI Advice", use_container_width=True):
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
                                            "You are an elite certified gym trainer and sports nutritionist. "
                                            "Provide friendly, actionable, motivational fitness advice in a mix of Hindi and English (Hinglish). "
                                            "Keep advice realistic, scientific, and concise."
                                        )
                                    },
                                    {
                                        "role": "user",
                                        "content": f"User details: BMI {bmi_data['bmi']} ({bmi_data['category']}), Goal: {plan['goal']}, Diet: {plan['diet_pref']}. Question: {user_query}"
                                    }
                                ],
                                max_tokens=150,
                                temperature=0.5
                            )
                            st.success(f"🤖 **AI Coach:** {resp.choices[0].message.content.strip()}")
                        except Exception as e:
                            st.warning("AI coach temporary response: Stay consistent, drink plenty of water, and ensure 8 hours of sleep!")
