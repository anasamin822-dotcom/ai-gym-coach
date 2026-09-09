"""
Workout Session UI Components:
1. Automatic Rest Countdown Timer with audio transitions and Skip button.
2. Workout Summary Export Card with pure Python PDF & CSV downloads.
"""
import time
import json
import streamlit as st
import streamlit.components.v1 as components
from services.reporting.workout_report import (
    calculate_session_metrics,
    generate_workout_csv,
    generate_workout_pdf
)


def play_rest_chime():
    """Play a short athletic chime using Web Audio API in the browser."""
    components.html(
        """
        <script>
        (() => {
            try {
                const ctx = new (window.AudioContext || window.webkitAudioContext)();
                const osc = ctx.createOscillator();
                const gain = ctx.createGain();
                osc.type = 'sine';
                osc.frequency.setValueAtTime(587.33, ctx.currentTime); // D5
                osc.frequency.setValueAtTime(880, ctx.currentTime + 0.12); // A5
                gain.gain.setValueAtTime(0.3, ctx.currentTime);
                gain.gain.exponentialRampToValueAtTime(0.001, ctx.currentTime + 0.4);
                osc.connect(gain);
                gain.connect(ctx.destination);
                osc.start();
                osc.stop(ctx.currentTime + 0.4);
            } catch (e) {
                console.warn('Audio chime could not play:', e);
            }
        })();
        </script>
        """,
        height=0
    )


def render_rest_timer_overlay(render_voice_feedback_func=None):
    """
    Renders an interactive athletic countdown timer between workout sets.
    Transitions back to active workout when time expires or when Skip is clicked.
    """
    if not st.session_state.get("is_resting", False):
        return

    now_ts = time.time()
    started_at = st.session_state.get("rest_started_at", now_ts)
    duration = st.session_state.get("rest_duration", 45)
    elapsed = now_ts - started_at
    remaining = max(0, int(duration - elapsed))

    sets_done = st.session_state.get("sets_completed", 1)
    target_sets = st.session_state.get("target_sets", 3)
    next_set = sets_done + 1

    # Visual percentage for countdown
    progress_pct = max(0, min(100, int((remaining / max(1, duration)) * 100)))

    st.markdown(
        f"""
        <div style="
            background: linear-gradient(145deg, rgba(10, 15, 26, 0.95) 0%, rgba(18, 25, 42, 0.95) 100%);
            border: 2px solid #00F59B;
            border-radius: 16px;
            padding: 24px;
            text-align: center;
            box-shadow: 0 0 30px rgba(0, 245, 155, 0.25);
            margin: 16px 0 24px 0;
        ">
            <div style="display: inline-block; background: rgba(0, 245, 155, 0.15); border: 1px solid #00F59B; color: #00F59B; padding: 4px 14px; border-radius: 9999px; font-weight: 800; font-size: 0.8rem; letter-spacing: 0.08em; text-transform: uppercase; margin-bottom: 12px;">
                🧘 SET {sets_done} COMPLETED • RECOVERY INTERVAL
            </div>
            <div style="font-size: 3.6rem; font-weight: 900; color: #00F59B; letter-spacing: -0.03em; margin: 4px 0; text-shadow: 0 0 20px rgba(0,245,155,0.4);">
                {remaining}s
            </div>
            <div style="color: #E2E8F0; font-size: 1.05rem; font-weight: 600; margin-bottom: 4px;">
                Hydrate & Catch Your Breath
            </div>
            <div style="color: #94A3B8; font-size: 0.9rem; margin-bottom: 16px;">
                Next Up: <strong>Set {next_set} of {target_sets}</strong>
            </div>
            <div style="background: rgba(255,255,255,0.08); height: 8px; border-radius: 4px; overflow: hidden; width: 80%; margin: 0 auto 12px auto;">
                <div style="background: linear-gradient(90deg, #00F59B, #00E5FF); height: 100%; width: {progress_pct}%; transition: width 0.9s linear;"></div>
            </div>
        </div>
        """,
        unsafe_allow_html=True
    )

    col_t1, col_t2, col_t3 = st.columns([1, 1, 2])
    with col_t1:
        if st.button("+15s", key="btn_rest_plus_15", use_container_width=True):
            st.session_state.rest_duration = duration + 15
            st.rerun()
    with col_t2:
        if st.button("-15s", key="btn_rest_minus_15", use_container_width=True):
            st.session_state.rest_duration = max(10, duration - 15)
            st.rerun()
    with col_t3:
        skip_clicked = st.button("⚡ Skip Rest & Begin Set", key="btn_skip_rest", use_container_width=True)

    # Trigger conclusion when time finishes or user clicks Skip
    if remaining <= 0 or skip_clicked:
        st.session_state.is_resting = False
        play_rest_chime()
        if render_voice_feedback_func:
            render_voice_feedback_func(f"Rest is over! Get ready for Set {next_set}!")
        st.rerun()
    else:
        # Smooth auto-tick
        time.sleep(1)
        st.rerun()


def render_workout_summary_section(metrics: dict):
    """
    Displays an aesthetic summary card with XP badge and CSV/PDF export buttons.
    """
    if not metrics:
        return

    st.markdown(
        f"""
        <div style="
            background: linear-gradient(145deg, rgba(14, 20, 34, 0.95) 0%, rgba(8, 12, 22, 0.98) 100%);
            border: 1px solid rgba(0, 245, 155, 0.35);
            border-radius: 16px;
            padding: 28px;
            margin: 20px 0;
            box-shadow: 0 12px 36px rgba(0, 0, 0, 0.55);
        ">
            <div style="display: flex; justify-content: space-between; align-items: center; flex-wrap: wrap; gap: 12px; margin-bottom: 16px;">
                <div>
                    <span style="background: rgba(0, 245, 155, 0.12); border: 1px solid #00F59B; color: #00F59B; padding: 4px 12px; border-radius: 9999px; font-size: 0.78rem; font-weight: 800; text-transform: uppercase;">
                        WORKOUT COMPLETE
                    </span>
                    <h2 style="margin: 8px 0 2px 0; color: #FFFFFF; font-size: 1.8rem; font-weight: 800;">
                        🏆 {metrics['exercise']} Session Highlights
                    </h2>
                    <span style="color: #94A3B8; font-size: 0.9rem;">Completed on {metrics['date']}</span>
                </div>
                <div style="background: rgba(0, 245, 155, 0.1); border: 1px solid #00F59B; padding: 12px 18px; border-radius: 12px; text-align: right;">
                    <div style="font-size: 0.8rem; color: #94A3B8; font-weight: 600;">REWARD EARNED</div>
                    <div style="font-size: 1.6rem; font-weight: 900; color: #00F59B;">+{metrics['xp_earned']} XP</div>
                    <div style="font-size: 0.85rem; color: #CBD5E1; font-weight: 700;">{metrics['rank_title']}</div>
                </div>
            </div>
        </div>
        """,
        unsafe_allow_html=True
    )

    c1, c2, c3, c4 = st.columns(4)
    c1.metric("Total Reps", f"{metrics['total_reps']}")
    c2.metric("Sets Finished", f"{metrics['sets_completed']}")
    c3.metric("Avg Rep Tempo", f"{metrics['avg_tempo_sec']} s/rep")
    c4.metric("Form Accuracy", f"{metrics['form_accuracy_pct']}%")

    st.markdown("#### 📥 Export Workout Session Report")
    st.caption("Download your certified session report for offline fitness tracking, logs, or sharing.")

    csv_data = generate_workout_csv(metrics)
    pdf_data = generate_workout_pdf(metrics)

    dl_col1, dl_col2 = st.columns(2)
    with dl_col1:
        st.download_button(
            label="📊 Download Report (CSV)",
            data=csv_data,
            file_name=f"workout_{metrics['exercise'].lower().replace(' ', '_')}_{int(time.time())}.csv",
            mime="text/csv",
            use_container_width=True,
            key="btn_download_csv"
        )
    with dl_col2:
        st.download_button(
            label="📄 Download Official PDF Report",
            data=pdf_data,
            file_name=f"workout_report_{metrics['exercise'].lower().replace(' ', '_')}_{int(time.time())}.pdf",
            mime="application/pdf",
            use_container_width=True,
            key="btn_download_pdf"
        )
