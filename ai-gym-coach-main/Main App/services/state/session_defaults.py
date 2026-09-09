import streamlit as st


def initial_session_defaults():
    defaults = {
        "reps": 0,
        "target_sets": 0,
        "reps_per_set": 0,
        "sets_completed": 0,
        "current_set_reps": 0,
        "workout_complete": False,
        "last_notified_sets_completed": 0,
        "last_notified_workout_complete": False,
        "last_saved_sets_completed": 0,
        "set_cycle_started_at": 0.0,
        "last_exercise_type": "Squats",

        # Workout plan (set before starting)
        "workout_started": False,
        "plan_exercise": "Squats",
        "plan_sets": 3,
        "plan_reps": 10,

        # Common Angles
        "knee_angle": 0,
        "back_angle": 0,
        "elbow_angle": 0,
        "front_knee_angle": 0,
        "torso_angle": 0,

        # Status fields
        "depth_status": "N/A",
        "body_alignment": "N/A",
        "hip_status": "N/A",
        "shoulder_status": "N/A",
        "swing_status": "N/A",
        "extension_status": "N/A",
        "back_arch_status": "N/A",
        "balance_status": "N/A",

        # Automatic Rest Timer
        "is_resting": False,
        "rest_started_at": 0.0,
        "rest_duration": 45,
        "configured_rest_duration": 45,

        # Workout Session Tracking & Reports
        "workout_started_at": 0.0,
        "correct_form_reps": 0,
        "last_session_report": None,

        # Hackathon Innovations: Live XP Combo & Velocity Fatigue Engine
        "combo_streak": 0,
        "max_combo_streak": 0,
        "combo_multiplier": 1.0,
        "live_xp": 0,
        "last_rep_timestamp": 0.0,
        "rep_durations": [],
        "current_rep_velocity": 0.0,
        "baseline_rep_velocity": 0.0,
        "velocity_drop_pct": 0.0,
        "fatigue_detected": False,
        "total_fatigue_events": 0,
        "last_form_status": "OPTIMAL",
    }

    for key, value in defaults.items():
        if key not in st.session_state:
            st.session_state[key] = value
