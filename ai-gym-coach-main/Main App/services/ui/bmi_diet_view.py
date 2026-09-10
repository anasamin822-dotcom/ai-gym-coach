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

    # =========================================================================
    # REAL CONVERSATIONAL AI COACH AGENT
    # =========================================================================
    st.markdown("---")
    st.markdown("### 🤖 Ask AI Coach — Real-Time Sports Nutrition & Workout Agent")
    st.caption("Ask anything about diet timing, creatine, muscle building, fat loss, or joint safety. Powered by Sports Science AI.")

    from services.coaching.fitness_agent import FitnessAIAgent

    if "coach_chat_history" not in st.session_state:
        st.session_state["coach_chat_history"] = []

    # Quick prompt suggestion chips
    st.markdown("<div style='font-size: 12px; color: #94A3B8; margin-bottom: 6px;'>💡 Quick Topics (Click to ask instantly):</div>", unsafe_allow_html=True)
    q_col1, q_col2, q_col3, q_col4 = st.columns(4)
    quick_query = None
    with q_col1:
        if st.button("⚡ Pre-Workout Diet", key="chip_pre_workout", use_container_width=True):
            quick_query = "Gym se pehle kya khayein energy ke liye?"
    with q_col2:
        if st.button("💊 Creatine Guide", key="chip_creatine", use_container_width=True):
            quick_query = "Creatine monohydrate kab aur kitna lena chahiye?"
    with q_col3:
        if st.button("💪 Muscle Hypertrophy", key="chip_muscle", use_container_width=True):
            quick_query = "Biceps aur chest ka size kaise badhayein?"
    with q_col4:
        if st.button("🩹 Joint Pain Tips", key="chip_knee", use_container_width=True):
            quick_query = "Squats me knee pain aur shoulder dard se kaise bachein?"

    with st.form("ai_coach_chat_form", clear_on_submit=False):
        user_input_val = st.text_input(
            "Apna doubt type karein:",
            placeholder="e.g. 'Creatine kab lein?', 'Veg diet me protein kaise badhayein?', 'Belly fat loss tips'",
            value=quick_query if quick_query else "",
            key="chat_user_query"
        )
        col_c1, col_c2 = st.columns([3, 1])
        with col_c1:
            ask_submitted = st.form_submit_button("⚡ GET COACH ADVICE", type="primary", use_container_width=True)
        with col_c2:
            clear_chat = st.form_submit_button("🗑️ Clear Chat", use_container_width=True)

    if clear_chat:
        st.session_state["coach_chat_history"] = []
        st.rerun()

    query_to_process = quick_query if quick_query else (user_input_val.strip() if ask_submitted else None)

    if query_to_process:
        with st.spinner("AI Coach is formulating scientific guidance..."):
            agent = FitnessAIAgent()
            context_data = {
                "bmi": bmi_val,
                "category": bmi_data.get("category", "Normal"),
                "goal": plan.get("goal", "Fitness"),
                "diet_pref": plan.get("diet_pref", "Veg")
            }
            coach_reply = agent.ask(query_to_process, context=context_data)
            st.session_state["coach_chat_history"].append({"q": query_to_process, "a": coach_reply})

    # Render Chat History
    if st.session_state["coach_chat_history"]:
        st.markdown("#### 💬 Conversation with AI Coach:")
        for idx, chat in enumerate(reversed(st.session_state["coach_chat_history"])):
            st.markdown(f"""
                <div style="background: rgba(14, 20, 34, 0.85); border: 1px solid rgba(255,255,255,0.1); border-radius: 10px; padding: 12px 16px; margin-bottom: 8px;">
                    <div style="color: #38BDF8; font-weight: 700; font-size: 13px;">👤 You: {chat['q']}</div>
                </div>
                <div style="background: linear-gradient(135deg, rgba(16, 30, 54, 0.95), rgba(10, 25, 47, 0.98)); border: 1px solid #00F59B; border-radius: 10px; padding: 16px 20px; margin-bottom: 16px; box-shadow: 0 4px 16px rgba(0,245,155,0.15);">
                    <div style="color: #00F59B; font-weight: 800; font-size: 12px; margin-bottom: 6px;">🤖 APNA AI COACH:</div>
                    <div style="color: #F8FAFC; font-size: 14px; line-height: 1.6; white-space: pre-line;">{chat['a']}</div>
                </div>
            """, unsafe_allow_html=True)
