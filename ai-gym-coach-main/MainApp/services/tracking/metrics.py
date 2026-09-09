import streamlit as st
import time
from services.config.workout_config import METRICS_FIELDS
from services.persistence.exercise_repository import add_exercise


def sync_metrics_update(context):
    if not context or not hasattr(context, "state") or not context.state.playing:
        return
    
    processor = getattr(context, "video_processor", None)

    if not processor:
        return 
    
    exercise = st.session_state.get("exercise_type")

    if not exercise:
        return
    
    processor.set_exercise(exercise)
    latest_metrics = processor.get_latest_metrics()

    if not latest_metrics:
        return
    
    reps = latest_metrics.get("reps", 0)

    if reps is None:
        reps = 0
        
    old_reps = st.session_state.get("reps", 0)
    now_ts = time.time()

    # --- HACKATHON INNOVATION: Real-Time Velocity, Fatigue & XP Combo Engine ---
    if reps > old_reps:
        reps_diff = reps - old_reps
        last_rep_ts = st.session_state.get("last_rep_timestamp", 0.0)

        # 1. Rep duration & movement velocity (s/rep)
        if last_rep_ts > 0.0:
            rep_duration = max(0.5, round((now_ts - last_rep_ts) / max(1, reps_diff), 2))
        else:
            rep_duration = 2.0

        st.session_state.last_rep_timestamp = now_ts
        st.session_state.current_rep_velocity = rep_duration

        durations = st.session_state.get("rep_durations", [])
        durations.append(rep_duration)
        st.session_state.rep_durations = durations

        # 2. Muscular Fatigue & Velocity Drop Detection
        current_set_reps_now = (reps - 1) % max(1, st.session_state.get("reps_per_set", 10))
        if current_set_reps_now <= 2:
            st.session_state.baseline_rep_velocity = rep_duration
            st.session_state.fatigue_detected = False
            st.session_state.velocity_drop_pct = 0.0
        else:
            baseline = st.session_state.get("baseline_rep_velocity", rep_duration)
            if baseline > 0 and rep_duration >= (baseline * 1.35):
                drop_pct = round(((rep_duration - baseline) / baseline) * 100.0, 1)
                st.session_state.fatigue_detected = True
                st.session_state.velocity_drop_pct = drop_pct
                st.session_state.total_fatigue_events = st.session_state.get("total_fatigue_events", 0) + 1
            else:
                st.session_state.fatigue_detected = False
                st.session_state.velocity_drop_pct = 0.0

        # 3. Form Accuracy & Live XP Combo Multiplier
        is_good_form = True
        depth = str(latest_metrics.get("depth_status", ""))
        body = str(latest_metrics.get("body_alignment", ""))
        swing = str(latest_metrics.get("swing_status", ""))
        ext = str(latest_metrics.get("extension_status", ""))
        bal = str(latest_metrics.get("balance_status", ""))

        if "TOO HIGH" in depth or "NO DEPTH" in depth:
            is_good_form = False
        elif "POOR" in body or "SAGGING" in body:
            is_good_form = False
        elif "SWING" in swing:
            is_good_form = False
        elif "INCOMPLETE" in ext:
            is_good_form = False
        elif "UNBALANCED" in bal:
            is_good_form = False

        combo = st.session_state.get("combo_streak", 0)
        if is_good_form:
            combo += 1
            st.session_state.correct_form_reps = st.session_state.get("correct_form_reps", 0) + reps_diff
            st.session_state.last_form_status = "PERFECT FORM"
        else:
            combo = 0
            st.session_state.last_form_status = "FORM SLIP"

        st.session_state.combo_streak = combo
        st.session_state.max_combo_streak = max(st.session_state.get("max_combo_streak", 0), combo)

        # XP multiplier scaling
        if combo >= 8:
            multiplier = 3.0
        elif combo >= 5:
            multiplier = 2.0
        elif combo >= 3:
            multiplier = 1.5
        else:
            multiplier = 1.0

        st.session_state.combo_multiplier = multiplier
        st.session_state.live_xp = st.session_state.get("live_xp", 0) + int(10 * multiplier * reps_diff)

    # Synchronize HUD telemetry into the WebRTC video processor
    if hasattr(processor, "set_hud_telemetry"):
        processor.set_hud_telemetry(
            combo=st.session_state.get("combo_streak", 0),
            multiplier=st.session_state.get("combo_multiplier", 1.0),
            velocity=st.session_state.get("current_rep_velocity", 0.0),
            fatigue=st.session_state.get("fatigue_detected", False)
        )

    st.session_state.reps = reps

    fields = METRICS_FIELDS.get(exercise)

    if not fields:
        return 

    for key, default in fields.items():
        st.session_state[key] = latest_metrics.get(key, default)

    reps_per_set = st.session_state.get("reps_per_set", 0)
    target_sets = st.session_state.get("target_sets", 0)

    if reps is not None and reps_per_set > 0 and target_sets > 0:
        sets_completed = reps // reps_per_set
        current_set_reps = reps % reps_per_set
        workout_completed = sets_completed >= target_sets 
    else:
        sets_completed = 0
        current_set_reps = 0
        workout_completed = False

    st.session_state.sets_completed = sets_completed
    st.session_state.current_set_reps = current_set_reps
    st.session_state.workout_completed = workout_completed

    last_saved_sets = st.session_state.get("last_saved_sets_completed", 0)

    if target_sets > 0 and reps_per_set > 0 and sets_completed > last_saved_sets:
        newly_completed = sets_completed - last_saved_sets
        now_ts = time.time()
        started_at = st.session_state.get("set_cycle_started_at", now_ts)
        time_taken = now_ts - started_at
        user_id = st.session_state.get("user_id", 0)

        add_exercise(user_id, exercise, newly_completed * reps_per_set, newly_completed, time_taken)

        if st.session_state.get("voice_pipeline"):
            result = st.session_state.voice_pipeline.process_event(
                event="set_completed",
                exercise=exercise,
                metrics=latest_metrics,
            )

            if result:
                st.session_state.audio_to_play, st.session_state.coach_feedback = result

        st.session_state.set_cycle_started_at = now_ts
        st.session_state.last_saved_sets_completed = sets_completed
        st.session_state.baseline_rep_velocity = 0.0
        st.session_state.last_rep_timestamp = 0.0
        st.session_state.fatigue_detected = False

        # Trigger automatic rest interval between sets if workout is ongoing
        if not workout_completed:
            st.session_state.is_resting = True
            st.session_state.rest_started_at = now_ts
            st.session_state.rest_duration = st.session_state.get("configured_rest_duration", 45)

    if workout_completed and not st.session_state.get("last_notified_workout_complete", False):
        st.session_state.last_notified_workout_complete = True

        if st.session_state.get("voice_pipeline"):
            result = st.session_state.voice_pipeline.process_event(
                event="workout_completed",
                exercise=exercise,
                metrics=latest_metrics,
            )

            if result:
                st.session_state.audio_to_play, st.session_state.coach_feedback = result
                
    pose_detected = latest_metrics.get("pose_detected", True)
    
    if not pose_detected and st.session_state.get("voice_pipeline"):
        result = st.session_state.voice_pipeline.process_event(
            event="no_pose_detected",
            exercise=exercise,
            metrics={"issue": "No pose detected! Please step into the camera frame."},
        )
    
        if result:
            st.session_state.audio_to_play, st.session_state.coach_feedback = result

    if st.session_state.get("voice_pipeline"):
        result = st.session_state.voice_pipeline.process_event(
            event="ongoing_form_check",
            exercise=exercise,
            metrics=latest_metrics,
        )
        
        if result:
            st.session_state.audio_to_play, st.session_state.coach_feedback = result
