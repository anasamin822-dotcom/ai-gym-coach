import urllib.parse
import streamlit as st
from services.persistence.exercise_repository import activate_pro_subscription, calculate_subscription_status


# Default Receiver UPI ID (Can be configured via st.secrets["UPI_ID"])
DEFAULT_UPI_ID = "anasamin822@okhdfcbank"
DEFAULT_PAYEE_NAME = "AI Gym Coach Pro"

PLANS = {
    "pro_monthly": {
        "title": "Pro Athlete — Monthly",
        "price": 199.0,
        "days": 30,
        "badge": "MOST POPULAR",
        "features": [
            "Unlimited Groq Sub-Second Voice Coaching",
            "1-Click Certified Clinical PDF & CSV Reports",
            "Velocity Fatigue Drop Engine (<35% alert)",
            "Personalized BMI & Indian Diet Meal Routine",
            "XP Combo Streaks & Priority Cloud Support"
        ]
    },
    "day_pass": {
        "title": "Intense Day Pass",
        "price": 19.0,
        "days": 1,
        "badge": "FLEXIBLE",
        "features": [
            "Full 24-Hour Access to All Pro Exercises",
            "Real-Time Voice Feedback Audio Pipeline",
            "Session Summary & PDF Export"
        ]
    },
    "pro_annual": {
        "title": "Pro Athlete — Annual Pass",
        "price": 1499.0,
        "days": 365,
        "badge": "BEST VALUE (Save 40%)",
        "features": [
            "365 Days Uninterrupted Pro Coaching",
            "All Current + Future Exercise Additions",
            "Exclusive Orthopedic Angle Telemetry",
            "VIP Hackathon Grand Prize Edition Access"
        ]
    }
}


def get_upi_id() -> str:
    upi_id = DEFAULT_UPI_ID
    try:
        if hasattr(st, "secrets") and "UPI_ID" in st.secrets:
            upi_id = st.secrets["UPI_ID"]
    except Exception:
        pass
    return upi_id


def generate_upi_intent_url(upi_id: str, payee_name: str, amount: float, transaction_note: str) -> str:
    params = {
        "pa": upi_id,
        "pn": payee_name,
        "am": f"{amount:.2f}",
        "cu": "INR",
        "tn": transaction_note
    }
    return f"upi://pay?{urllib.parse.urlencode(params)}"


def get_qr_image_url(upi_intent: str, size: int = 240) -> str:
    encoded_data = urllib.parse.quote(upi_intent)
    return f"https://api.qrserver.com/v1/create-qr-code/?size={size}x{size}&margin=10&data={encoded_data}"


def render_upi_payment_modal(user_id: int, key_prefix: str = "main"):
    """
    Renders an interactive Cyberpunk Dynamic UPI QR Code payment drawer.
    Uses key_prefix to guarantee unique element keys across multiple instances.
    """
    st.markdown("""
        <div style="background: linear-gradient(135deg, rgba(10, 25, 47, 0.95), rgba(15, 23, 42, 0.95)); border: 1px solid #00F59B; border-radius: 12px; padding: 20px; margin-bottom: 20px;">
            <div style="display: flex; align-items: center; justify-content: space-between;">
                <div>
                    <span style="background: rgba(0, 245, 155, 0.2); border: 1px solid #00F59B; color: #00F59B; font-size: 10px; font-weight: 800; padding: 3px 10px; border-radius: 999px; text-transform: uppercase;">
                        INSTANT UPI QR PAYWALL
                    </span>
                    <h3 style="color: #FFFFFF; margin: 8px 0 4px 0; font-size: 20px;">Unlock AI Gym Coach Pro 🚀</h3>
                    <p style="color: #94A3B8; font-size: 12px; margin: 0;">Scan with PhonePe, Google Pay, Paytm or any UPI App for Instant Activation</p>
                </div>
                <div style="font-size: 32px;">⚡</div>
            </div>
        </div>
    """, unsafe_allow_html=True)

    # Select Plan
    col_p1, col_p2, col_p3 = st.columns(3)
    
    plan_state_key = f"{key_prefix}_selected_plan"
    if plan_state_key not in st.session_state:
        st.session_state[plan_state_key] = "pro_monthly"

    with col_p1:
        is_sel = st.session_state[plan_state_key] == "day_pass"
        if st.button("🔥 Day Pass (₹19)", key=f"{key_prefix}_plan_day_pass", type="primary" if is_sel else "secondary", use_container_width=True):
            st.session_state[plan_state_key] = "day_pass"
            st.rerun()

    with col_p2:
        is_sel = st.session_state[plan_state_key] == "pro_monthly"
        if st.button("⭐ Monthly (₹199)", key=f"{key_prefix}_plan_monthly", type="primary" if is_sel else "secondary", use_container_width=True):
            st.session_state[plan_state_key] = "pro_monthly"
            st.rerun()

    with col_p3:
        is_sel = st.session_state[plan_state_key] == "pro_annual"
        if st.button("👑 Annual (₹1499)", key=f"{key_prefix}_plan_annual", type="primary" if is_sel else "secondary", use_container_width=True):
            st.session_state[plan_state_key] = "pro_annual"
            st.rerun()

    selected = PLANS[st.session_state[plan_state_key]]
    upi_id = get_upi_id()
    txn_note = f"PRO_{user_id}_{st.session_state[plan_state_key]}"
    intent_url = generate_upi_intent_url(upi_id, DEFAULT_PAYEE_NAME, selected["price"], txn_note)
    qr_url = get_qr_image_url(intent_url, size=220)

    col_qr, col_details = st.columns([1, 1.2])

    with col_qr:
        st.markdown(f"""
            <div style="text-align: center; background: #FFFFFF; padding: 12px; border-radius: 12px; box-shadow: 0 0 20px rgba(0,245,155,0.3); margin: 8px auto; width: 220px;">
                <img src="{qr_url}" alt="Dynamic UPI QR Code" style="width: 196px; height: 196px; display: block; margin: 0 auto;" />
                <div style="color: #0F172A; font-weight: 800; font-size: 13px; margin-top: 6px;">SCAN TO PAY ₹{int(selected['price'])}</div>
                <div style="color: #64748B; font-size: 10px;">UPI ID: {upi_id}</div>
            </div>
        """, unsafe_allow_html=True)
        
        # Deep links for mobile
        st.markdown(f"""
            <div style="text-align: center; margin-top: 8px;">
                <a href="{intent_url}" style="background: #00F59B; color: #0A192F; font-weight: 700; font-size: 12px; padding: 6px 14px; border-radius: 6px; text-decoration: none; display: inline-block;">
                    📱 Tap to Pay on UPI App
                </a>
            </div>
        """, unsafe_allow_html=True)

    with col_details:
        st.markdown(f"#### 🎯 {selected['title']}")
        st.markdown(f"**Amount:** `₹{selected['price']:.0f}` &bull; **Validity:** `{selected['days']} Days`")
        
        for feat in selected["features"]:
            st.markdown(f"✅ <span style='color: #E2E8F0; font-size: 13px;'>{feat}</span>", unsafe_allow_html=True)

        st.markdown("---")
        st.markdown("<div style='font-size: 12px; color: #94A3B8;'>Payment karne ke baad apna 12-digit <b>UPI Ref / UTR Number</b> niche enter karein:</div>", unsafe_allow_html=True)

        col_utr, col_btn = st.columns([1.5, 1])
        with col_utr:
            utr_input = st.text_input("12-Digit UTR / Ref No.", placeholder="e.g. 423871928374", key=f"{key_prefix}_input_utr", label_visibility="collapsed")
        
        with col_btn:
            if st.button("Verify & Unlock", key=f"{key_prefix}_btn_verify_utr", type="primary", use_container_width=True):
                if not utr_input or len(utr_input.strip()) < 6:
                    st.error("Please enter a valid UPI UTR / Reference ID.")
                else:
                    activate_pro_subscription(
                        user_id=user_id,
                        plan_name=selected["title"],
                        days=selected["days"],
                        amount=selected["price"],
                        utr_number=utr_input.strip()
                    )
                    st.session_state["is_pro"] = True
                    st.balloons()
                    st.success(f"🎉 Congratulations! {selected['title']} Activated Successfully!")
                    st.rerun()
