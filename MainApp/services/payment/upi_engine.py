import urllib.parse
import streamlit as st
from services.persistence.exercise_repository import activate_pro_subscription, calculate_subscription_status


DEFAULT_UPI_ID = "anasamin822@okhdfcbank"
DEFAULT_PAYEE_NAME = "AI Gym Coach Pro"

PLANS = {
    "pro_monthly": {
        "title": "Pro Athlete — Monthly",
        "short_title": "⭐ Pro Monthly (₹199 / 30 Days)",
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
        "short_title": "🔥 Day Pass (₹19 / 24 Hours)",
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
        "short_title": "👑 Pro Annual (₹1499 / 365 Days)",
        "price": 1499.0,
        "days": 365,
        "badge": "BEST VALUE",
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
        upi_id = str(st.secrets.get("UPI_ID", DEFAULT_UPI_ID))
    except Exception:
        upi_id = DEFAULT_UPI_ID
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


def get_qr_image_url(upi_intent: str, size: int = 200) -> str:
    encoded_data = urllib.parse.quote(upi_intent)
    return f"https://api.qrserver.com/v1/create-qr-code/?size={size}x{size}&margin=10&data={encoded_data}"


def render_upi_payment_modal(user_id: int, is_sidebar: bool = False, key_prefix: str = "main"):
    """
    Renders an interactive Cyberpunk Dynamic UPI QR Code payment drawer.
    Provides a vertical, responsive layout for sidebars (no column squishing),
    and a spacious side-by-side layout for main page tabs.
    """
    upi_id = get_upi_id()
    plan_keys = ["pro_monthly", "day_pass", "pro_annual"]
    plan_options = [PLANS[k]["short_title"] for k in plan_keys]
    label_to_key = {PLANS[k]["short_title"]: k for k in plan_keys}

    # =========================================================================
    # 1. SIDEBAR MODE (SINGLE-COLUMN, STACKED, RESPONSIVE)
    # =========================================================================
    if is_sidebar:
        st.markdown("""
            <div style="background: rgba(14, 20, 34, 0.95); border: 1px solid #00F59B; border-radius: 10px; padding: 12px; margin-bottom: 12px;">
                <div style="color: #00F59B; font-weight: 800; font-size: 11px; text-transform: uppercase;">
                    ⚡ Instant UPI Activation
                </div>
                <div style="color: #FFFFFF; font-size: 13px; font-weight: 700; margin-top: 2px;">
                    Scan with any UPI App
                </div>
            </div>
        """, unsafe_allow_html=True)

        selected_label = st.radio(
            "Select Plan:",
            options=plan_options,
            index=0,
            key=f"{key_prefix}_plan_radio",
            label_visibility="collapsed"
        )
        selected_key = label_to_key[selected_label]
        selected = PLANS[selected_key]

        txn_note = f"PRO_{user_id}_{selected_key}"
        intent_url = generate_upi_intent_url(upi_id, DEFAULT_PAYEE_NAME, selected["price"], txn_note)
        qr_url = get_qr_image_url(intent_url, size=180)

        # Centered QR Box (responsive, fits 100% inside sidebar without overflow)
        st.markdown(f"""
            <div style="background: #FFFFFF; border-radius: 12px; padding: 10px; margin: 10px auto; width: 170px; text-align: center; box-shadow: 0 4px 16px rgba(0,245,155,0.25);">
                <img src="{qr_url}" alt="QR Code" style="width: 150px; height: 150px; display: block; margin: 0 auto;" />
                <div style="color: #0A192F; font-weight: 900; font-size: 13px; margin-top: 4px;">SCAN &bull; ₹{int(selected['price'])}</div>
                <div style="color: #64748B; font-size: 9px; word-break: break-all;">{upi_id}</div>
            </div>
        """, unsafe_allow_html=True)

        st.markdown(f"""
            <div style="text-align: center; margin-bottom: 10px;">
                <a href="{intent_url}" style="background: #00F59B; color: #0A192F; font-weight: 800; font-size: 12px; padding: 7px 12px; border-radius: 6px; text-decoration: none; display: block;">
                    📱 Tap to Pay on UPI App
                </a>
            </div>
        """, unsafe_allow_html=True)

        st.caption("Enter 12-digit UPI UTR / Ref No. below:")
        utr_val = st.text_input(
            "UTR / Ref No.",
            placeholder="12-digit UTR e.g. 4238...",
            key=f"{key_prefix}_utr_input",
            label_visibility="collapsed"
        )

        if st.button("Verify & Activate Pro 🚀", key=f"{key_prefix}_verify_btn", type="primary", use_container_width=True):
            if not utr_val or len(utr_val.strip()) < 6:
                st.error("Please enter a valid 12-digit UTR number.")
            else:
                activate_pro_subscription(
                    user_id=user_id,
                    plan_name=selected["title"],
                    days=selected["days"],
                    amount=selected["price"],
                    utr_number=utr_val.strip()
                )
                st.session_state["is_pro"] = True
                st.balloons()
                st.success(f"🎉 {selected['title']} Activated!")
                st.rerun()
        return

    # =========================================================================
    # 2. MAIN PAGE / FULL-WIDTH TAB MODE
    # =========================================================================
    st.markdown("""
        <div style="background: linear-gradient(135deg, rgba(10, 25, 47, 0.95), rgba(15, 23, 42, 0.95)); border: 1px solid #00F59B; border-radius: 12px; padding: 22px; margin-bottom: 24px;">
            <div style="display: flex; align-items: center; justify-content: space-between; flex-wrap: wrap; gap: 12px;">
                <div>
                    <span style="background: rgba(0, 245, 155, 0.15); border: 1px solid #00F59B; color: #00F59B; font-size: 10px; font-weight: 800; padding: 4px 12px; border-radius: 999px; text-transform: uppercase;">
                        INSTANT DYNAMIC UPI QR GATEWAY
                    </span>
                    <h2 style="color: #FFFFFF; margin: 10px 0 4px 0; font-size: 24px; font-weight: 800;">
                        Upgrade to AI Gym Coach Pro
                    </h2>
                    <p style="color: #94A3B8; font-size: 13px; margin: 0;">
                        Instant activation via PhonePe, Google Pay, Paytm, or any Indian UPI app.
                    </p>
                </div>
                <div style="font-size: 38px;">⚡</div>
            </div>
        </div>
    """, unsafe_allow_html=True)

    # 3 Plan Selection Cards
    p_cols = st.columns(3)
    plan_state_key = f"{key_prefix}_main_plan"
    if plan_state_key not in st.session_state:
        st.session_state[plan_state_key] = "pro_monthly"

    for idx, pk in enumerate(plan_keys):
        p_info = PLANS[pk]
        is_active = st.session_state[plan_state_key] == pk
        with p_cols[idx]:
            border_col = "#00F59B" if is_active else "rgba(255, 255, 255, 0.15)"
            bg_col = "rgba(0, 245, 155, 0.08)" if is_active else "rgba(14, 20, 34, 0.7)"
            st.markdown(f"""
                <div style="border: 2px solid {border_col}; background: {bg_col}; border-radius: 12px; padding: 14px; text-align: center; margin-bottom: 8px;">
                    <div style="font-size: 10px; font-weight: 800; color: #00F59B;">{p_info['badge']}</div>
                    <div style="font-size: 16px; font-weight: 800; color: #FFFFFF; margin: 4px 0;">{p_info['title']}</div>
                    <div style="font-size: 22px; font-weight: 900; color: #00F59B;">₹{int(p_info['price'])} <span style="font-size: 11px; color: #94A3B8;">/ {p_info['days']}d</span></div>
                </div>
            """, unsafe_allow_html=True)
            if st.button(f"Select {p_info['title'].split('—')[0].strip()}", key=f"{key_prefix}_btn_{pk}", type="primary" if is_active else "secondary", use_container_width=True):
                st.session_state[plan_state_key] = pk
                st.rerun()

    selected = PLANS[st.session_state[plan_state_key]]
    txn_note = f"PRO_{user_id}_{st.session_state[plan_state_key]}"
    intent_url = generate_upi_intent_url(upi_id, DEFAULT_PAYEE_NAME, selected["price"], txn_note)
    qr_url = get_qr_image_url(intent_url, size=220)

    # 2-Column Split for Main View (with generous spacing)
    st.markdown("<div style='margin-top: 20px;'></div>", unsafe_allow_html=True)
    col_left, col_right = st.columns([1, 1.4])

    with col_left:
        st.markdown(f"""
            <div style="background: #FFFFFF; border-radius: 16px; padding: 16px; text-align: center; box-shadow: 0 8px 30px rgba(0,245,155,0.25); max-width: 230px; margin: 0 auto;">
                <img src="{qr_url}" alt="UPI QR" style="width: 198px; height: 198px; display: block; margin: 0 auto;" />
                <div style="color: #0A192F; font-weight: 900; font-size: 15px; margin-top: 6px;">SCAN TO PAY ₹{int(selected['price'])}</div>
                <div style="color: #64748B; font-size: 11px;">UPI ID: {upi_id}</div>
            </div>
        """, unsafe_allow_html=True)

        st.markdown(f"""
            <div style="text-align: center; margin-top: 12px;">
                <a href="{intent_url}" style="background: #00F59B; color: #0A192F; font-weight: 800; font-size: 13px; padding: 10px 20px; border-radius: 8px; text-decoration: none; display: inline-block;">
                    📱 Tap to Pay on UPI App
                </a>
            </div>
        """, unsafe_allow_html=True)

    with col_right:
        st.markdown(f"### 🎯 {selected['title']}")
        st.markdown(f"**Amount:** `₹{selected['price']:.0f}` &bull; **Validity:** `{selected['days']} Days`")

        for feat in selected["features"]:
            st.markdown(f"✅ <span style='color: #E2E8F0; font-size: 13.5px;'>{feat}</span>", unsafe_allow_html=True)

        st.markdown("---")
        st.markdown("<div style='font-size: 13px; color: #94A3B8; margin-bottom: 6px;'>Payment karne ke baad apna 12-digit <b>UPI Ref / UTR Number</b> enter karein:</div>", unsafe_allow_html=True)

        col_u1, col_u2 = st.columns([1.5, 1])
        with col_u1:
            utr_main = st.text_input("12-Digit UTR", placeholder="e.g. 423871928374", key=f"{key_prefix}_main_utr_input", label_visibility="collapsed")
        with col_u2:
            if st.button("Verify & Unlock", key=f"{key_prefix}_main_verify_btn", type="primary", use_container_width=True):
                if not utr_main or len(utr_main.strip()) < 6:
                    st.error("Please enter a valid 12-digit UTR.")
                else:
                    activate_pro_subscription(
                        user_id=user_id,
                        plan_name=selected["title"],
                        days=selected["days"],
                        amount=selected["price"],
                        utr_number=utr_main.strip()
                    )
                    st.session_state["is_pro"] = True
                    st.balloons()
                    st.success(f"🎉 Congratulations! {selected['title']} Activated Successfully!")
                    st.rerun()
