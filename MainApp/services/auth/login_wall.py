import re
import streamlit as st
from services.auth.sms_service import send_otp, verify_otp
from services.persistence.exercise_repository import get_or_create_user_by_phone, calculate_subscription_status


def render_login_wall() -> bool:
    """
    Renders mobile-number verification screen with 7-Day Free Trial onboarding.
    Returns True if user is verified, False otherwise.
    """
    if st.session_state.get("user_id") is not None:
        return True

    st.markdown("""
        <div style="text-align: center; margin-bottom: 24px;">
            <div style="font-size: 42px;">🏋️‍♂️</div>
            <h1 style="color: #FFFFFF; font-size: 32px; font-weight: 800; margin: 4px 0;">AI Real-Time GYM Coach</h1>
            <p style="color: #94A3B8; font-size: 14px;">Real-Time Kinematic Pose Analysis & Sub-Second Voice AI</p>
            <div style="display: inline-block; background: rgba(0, 245, 155, 0.15); border: 1px solid #00F59B; color: #00F59B; padding: 6px 16px; border-radius: 999px; font-size: 12px; font-weight: 700; margin-top: 8px;">
                🎁 7-Day Free Starter Trial Included on Signup!
            </div>
        </div>
    """, unsafe_allow_html=True)

    if "auth_step" not in st.session_state:
        st.session_state["auth_step"] = "enter_phone"
    if "auth_phone" not in st.session_state:
        st.session_state["auth_phone"] = ""
    if "sandbox_otp_hint" not in st.session_state:
        st.session_state["sandbox_otp_hint"] = ""

    # STEP 1: MOBILE NUMBER INPUT
    if st.session_state["auth_step"] == "enter_phone":
        with st.form("mobile_login_form", clear_on_submit=False):
            st.markdown("#### 📱 Enter Mobile Number to Begin")
            st.caption("We will send a 6-digit verification code to your phone.")
            
            phone_input = st.text_input(
                "Mobile Number (+91)",
                placeholder="10-digit mobile number e.g. 9876543210",
                max_chars=10
            )
            submit_phone = st.form_submit_button("Send Verification OTP 🚀", use_container_width=True)

        if submit_phone:
            clean_phone = "".join(filter(str.isdigit, phone_input))
            if len(clean_phone) != 10:
                st.error("Please enter a valid 10-digit Indian mobile number.")
                return False

            res = send_otp(clean_phone)
            st.session_state["auth_phone"] = clean_phone
            st.session_state["auth_step"] = "enter_otp"
            if res.get("mode") == "sandbox":
                st.session_state["sandbox_otp_hint"] = res.get("otp")
            else:
                st.session_state["sandbox_otp_hint"] = ""
            st.rerun()

    # STEP 2: OTP VERIFICATION
    elif st.session_state["auth_step"] == "enter_otp":
        phone = st.session_state["auth_phone"]
        st.markdown(f"#### 🔐 Verify Code for +91 {phone}")
        
        if st.session_state.get("sandbox_otp_hint"):
            st.info(f"🧪 **Sandbox / Demo Mode Active:** Your OTP is `{st.session_state['sandbox_otp_hint']}` (or use Master OTP `999999`).")
        else:
            st.info(f"📲 An OTP has been sent via SMS to **+91 {phone}**.")

        with st.form("otp_verify_form", clear_on_submit=False):
            otp_input = st.text_input("6-Digit OTP", placeholder="Enter 6-digit OTP", max_chars=6)
            col_v1, col_v2 = st.columns(2)
            with col_v1:
                verify_btn = st.form_submit_button("Verify & Start 7-Day Trial", use_container_width=True, type="primary")
            with col_v2:
                back_btn = st.form_submit_button("Change Number", use_container_width=True)

        if back_btn:
            st.session_state["auth_step"] = "enter_phone"
            st.rerun()

        if verify_btn:
            if not otp_input or len(otp_input.strip()) != 6:
                st.error("Please enter a valid 6-digit OTP.")
                return False

            if verify_otp(phone, otp_input.strip()):
                user = get_or_create_user_by_phone(phone)
                st.session_state["user_id"] = user["id"]
                st.session_state["phone_number"] = phone
                st.session_state["username"] = user["username"]

                # Sync trial and subscription status
                sub_status = calculate_subscription_status(user["id"])
                st.session_state["is_pro"] = sub_status["is_pro"]
                st.session_state["trial_days_left"] = sub_status["trial_days_left"]

                st.success("✅ Phone Verified! Welcome to AI Gym Coach.")
                st.session_state["auth_step"] = "done"
                st.rerun()
            else:
                st.error("❌ Incorrect or expired OTP. Please try again or use Master OTP `999999`.")

    return False
