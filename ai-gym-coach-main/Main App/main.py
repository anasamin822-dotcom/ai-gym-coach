import sys
from pathlib import Path

# Guarantee MainApp directory is in sys.path for robust imports across all environments
MAINAPP_DIR = Path(__file__).resolve().parent
if str(MAINAPP_DIR) not in sys.path:
    sys.path.insert(0, str(MAINAPP_DIR))

import streamlit as st
import os
import time
import pandas as pd
from services.auth.login_wall import render_login_wall
from services.state.session_defaults import initial_session_defaults
from services.config.workout_config import EXERCISE_OPTIONS
from services.ui.style_loader import load_css, inject_local_font, inject_webrtc_styles
from services.persistence.exercise_repository import init_db
from streamlit_webrtc import webrtc_streamer, WebRtcMode
from services.vision.exercise_video_processor import VideoProcessorClass
from services.tracking.metrics import sync_metrics_update
from services.persistence.exercise_repository import get_users_exercises
from groq import Groq
from services.coaching.llm import LLMCoach
from services.coaching.tts import TextToSpeech
from services.coaching.voice_pipeline import VoicePipeline, autoplay_audio
from services.ui.bmi_diet_view import render_bmi_diet_planner

  
def main():
    st.set_page_config(
        page_icon="🏋️‍♀️",
        page_title="AI Real-time GYM Coach",
        initial_sidebar_state="expanded",
        layout="centered"
    )

    css_path = MAINAPP_DIR / "static" / "style.css"
    font_path = MAINAPP_DIR / "static" / "AdobeClean.otf"
    load_css(str(css_path))
    inject_local_font(str(font_path), "AdobeClean")

    init_db()

    if not render_login_wall():
        return 

    initial_session_defaults()

    if "voice_pipeline" not in st.session_state:
        try:
            api_key = os.environ.get("GROQ_API_KEY", "")

            if not api_key and hasattr(st, "secrets") and "GROQ_API_KEY" in st.secrets:
                api_key = st.secrets["GROQ_API_KEY"]
            
            groq_client = Groq(api_key=api_key)
            llm_coach = LLMCoach(groq_client)
            tts = TextToSpeech()
            st.session_state.voice_pipeline = VoicePipeline(llm_coach, tts)
        except Exception as e:
            st.session_state.voice_pipeline = None

    workout_started = st.session_state.get("workout_started", False)
    
    with st.sidebar:
        st.title("🏋️‍♂️ Apna AI Coach")

        if st.session_state.username:
            st.caption(f"👤 Login as {st.session_state.username}")

        st.divider()

        st.subheader("Workout Plan")

        if not workout_started:
            plan_exercise = st.selectbox("Exercise", options=EXERCISE_OPTIONS, key="plan_exercise")

            plan_sets = st.number_input("Sets", min_value=0, max_value=50, key="plan_sets", step=1)

            plan_reps = st.number_input("Reps per Set", min_value=0, max_value=50, key="plan_reps", step=1)

            st.markdown("")

            start_session_button = st.button("Start Workout", width="stretch", key="start_session_button")

            if start_session_button:
                st.session_state.exercise_type = plan_exercise
                st.session_state.target_sets = int(plan_sets)
                st.session_state.reps_per_set = int(plan_reps)
                st.session_state.reps = 0
                st.session_state.workout_started = True
                st.session_state.set_cycle_started_at = time.time()
                st.session_state.last_saved_sets_completed = 0

                if st.session_state.voice_pipeline:
                    result = st.session_state.voice_pipeline.process_event(
                        event="workout_started",
                        exercise=plan_exercise,
                        metrics={}
                    )
                    
                    if result:
                        st.session_state.audio_to_play, st.session_state.coach_feedback = result

                st.session_state.last_notified_sets_completed = 0
                st.session_state.last_notified_workout_complete = False
                st.rerun()
        else:
            exercise = st.session_state.get("exercise_type")
            sets = st.session_state.get("target_sets")
            reps = st.session_state.get("reps_per_set")

            st.info(f"**{exercise}** -- {sets} Sets / {reps} Reps")

            end_session_button = st.button("End Workout", key="end_session_button", width="stretch")

            if end_session_button:
                st.session_state.workout_started = False
                
                if st.session_state.voice_pipeline:
                    result = st.session_state.voice_pipeline.process_event(
                        event="workout_completed",
                        exercise=exercise,
                        metrics={}
                    )
                    if result:
                        st.session_state.audio_to_play, st.session_state.coach_feedback = result

                st.rerun()

        if workout_started:
            st.divider()

            exercise = st.session_state.get("exercise_type")
            total_reps = st.session_state.get("reps")
            current_set_reps = st.session_state.get("current_set_reps")
            reps_per_set = st.session_state.get("reps_per_set")
            sets_completed = st.session_state.get("sets_completed")
            target_sets = st.session_state.get("target_sets")

            st.subheader("Progress")

            st.metric("Total Reps", f"{total_reps}")
            st.metric("Current Set Reps", f"{current_set_reps} / {reps_per_set}")
            st.metric("Sets Completed", f"{sets_completed} / {target_sets}")

            st.divider()

            if exercise == "Squats":
                st.subheader("Squat Metrics")
                st.metric("Knee Angle", f"{st.session_state.knee_angle}°")
                st.metric("Back Angle", f"{st.session_state.back_angle}°")
                st.metric("Depth Status", st.session_state.depth_status)

            elif exercise == "Push-ups":
                st.subheader("Push-up Metrics")
                st.metric("Elbow Angle", f"{st.session_state.elbow_angle}°")
                st.metric("Body Alignment", st.session_state.body_alignment)
                st.metric("Hip Position", st.session_state.hip_status)

            elif exercise == "Biceps Curls (Dumbbell)":
                st.subheader("Curl Metrics")
                st.metric("Elbow Angle", f"{st.session_state.elbow_angle}°")
                st.metric("Shoulder Stability", st.session_state.shoulder_status)
                st.metric("Swing Detection", st.session_state.swing_status)

            elif exercise == "Shoulder Press":
                st.subheader("Shoulder Press Metrics")
                st.metric("Elbow Angle", f"{st.session_state.elbow_angle}°")
                st.metric("Arm Extension", st.session_state.extension_status)
                st.metric("Back Arch", st.session_state.back_arch_status)

            elif exercise == "Lunges":
                st.subheader("Lunge Metrics")
                st.metric("Front Knee Angle", f"{st.session_state.front_knee_angle}°")
                st.metric("Torso Angle", f"{st.session_state.torso_angle}°")
                st.metric("Balance Status", st.session_state.balance_status)

    st.markdown(
        """
        <div style="margin-bottom: 20px;">
            <div class="gym-hero-badge">
                <span class="gym-status-dot"></span> AI BIOMECHANICAL VISION ENGINE ONLINE
            </div>
            <h1 style="margin: 0; font-size: 2.3rem; font-weight: 900; letter-spacing: -0.02em;">
                ⚡ APNA AI GYM COACH
            </h1>
            <p style="color: #94A3B8; font-size: 1.02rem; margin-top: 6px; margin-bottom: 0;">
                Real-time 33-Point Pose Tracking • Biomechanical Form Verification • Certified Workout & Diet Planner
            </p>
        </div>
        """,
        unsafe_allow_html=True
    )
 
    if st.session_state.get("audio_to_play"):
        autoplay_audio(st.session_state.audio_to_play)

    if st.session_state.get("coach_feedback"):
        st.markdown("")
        st.success(f"🤖 **Coach:** {st.session_state.coach_feedback}")

    tab_workout, tab_diet, tab_history = st.tabs([
        "🏋️‍♂️ Live Workout & AI Coach",
        "🥗 BMI & Diet Planner",
        "📈 Workout History"
    ])

    with tab_workout:
        if not workout_started:
            st.markdown(
                """
                <div style="
                    background: linear-gradient(145deg, rgba(14, 20, 34, 0.9) 0%, rgba(8, 12, 22, 0.95) 100%);
                    border: 1px solid rgba(0, 245, 155, 0.3);
                    border-radius: 16px;
                    padding: 38px 28px;
                    text-align: center;
                    box-shadow: 0 14px 40px rgba(0, 0, 0, 0.55);
                    margin: 24px 0;
                ">
                    <div style="font-size: 3.5rem; margin-bottom: 10px;">🏋️‍♂️</div>
                    <h2 style="color: #FFFFFF; font-size: 1.65rem; margin-bottom: 8px; font-weight: 800;">
                        AI WORKOUT ARENA • READY
                    </h2>
                    <p style="color: #94A3B8; font-size: 1.02rem; max-width: 620px; margin: 0 auto 24px auto;">
                        Choose your exercise and target reps in the sidebar, then click <strong style="color: #00F59B;">Start Workout</strong> to activate camera telemetry and voice coaching.
                    </p>
                    <div style="display: flex; justify-content: center; flex-wrap: wrap; gap: 10px;">
                        <span style="background: rgba(0, 245, 155, 0.08); border: 1px solid rgba(0, 245, 155, 0.3); color: #00F59B; padding: 7px 15px; border-radius: 8px; font-size: 0.88rem; font-weight: 600;">🦵 Squats</span>
                        <span style="background: rgba(0, 245, 155, 0.08); border: 1px solid rgba(0, 245, 155, 0.3); color: #00F59B; padding: 7px 15px; border-radius: 8px; font-size: 0.88rem; font-weight: 600;">💪 Push-ups</span>
                        <span style="background: rgba(0, 245, 155, 0.08); border: 1px solid rgba(0, 245, 155, 0.3); color: #00F59B; padding: 7px 15px; border-radius: 8px; font-size: 0.88rem; font-weight: 600;">🏋️ Biceps Curls</span>
                        <span style="background: rgba(0, 245, 155, 0.08); border: 1px solid rgba(0, 245, 155, 0.3); color: #00F59B; padding: 7px 15px; border-radius: 8px; font-size: 0.88rem; font-weight: 600;">🎯 Shoulder Press</span>
                        <span style="background: rgba(0, 245, 155, 0.08); border: 1px solid rgba(0, 245, 155, 0.3); color: #00F59B; padding: 7px 15px; border-radius: 8px; font-size: 0.88rem; font-weight: 600;">🏃 Lunges</span>
                    </div>
                </div>
                """,
                unsafe_allow_html=True,
            )
        else:
            context = webrtc_streamer(
                key="exercise-analysis",
                mode=WebRtcMode.SENDRECV,
                video_processor_factory=VideoProcessorClass,
                rtc_configuration={
                    "iceServers": [
                        {"urls": ["stun:stun.l.google.com:19302"]},
                        {"urls": ["stun:stun1.l.google.com:19302"]},
                        {"urls": ["stun:stun2.l.google.com:19302"]},
                        {"urls": ["stun:global.stun.twilio.com:3478"]}
                    ]
                },
                media_stream_constraints={
                    "video": True,
                    "audio": False
                },
                async_processing=True
            )

            sync_metrics_update(context)

            if context.state.playing:
                time.sleep(0.25)
                st.rerun()

            inject_webrtc_styles()

    with tab_diet:
        render_bmi_diet_planner()

    with tab_history:
        st.markdown("#### Your Workout History")

        user_id = st.session_state.get("user_id", 0)

        if isinstance(user_id, int):
            history_rows = get_users_exercises(user_id)

            arr = [
                {
                    "Exercise": row['exercise_name'],
                    "Reps": row['reps'],
                    "Sets": row['sets'],
                    "Time (sec)": row['time'],
                    "Date": row['created_at']
                }
                for row in history_rows
            ]

            df = pd.DataFrame(arr)

            if not df.empty:
                df["Date"] = pd.to_datetime(df["Date"]).dt.date
                agg_df = df.groupby(["Exercise", "Date"]).agg({
                    "Reps": 'sum',
                    "Sets": "sum",
                    "Time (sec)": "sum"
                }).reset_index()
                agg_df.index += 1
                st.table(agg_df, border="horizontal")
            else:
                st.info("No workout history found.")


if __name__ == "__main__":
    main()
    