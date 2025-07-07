import streamlit as st
import requests
from datetime import datetime
from url import BASE_URL


def render_profile_page():
    st.markdown("<h2 style='text-align: center; color: white;'>👤 Your Profile</h2>", unsafe_allow_html=True)
    st.markdown("###")

    token = st.session_state.get("token")
    if not token:
        st.error("❌ You must be logged in to view your profile.")
        return

    try:
        res = requests.get(f"{BASE_URL}/profile?token={token}")
        res.raise_for_status()
        profile = res.json()
    except Exception:
        st.error("🚫 Failed to load profile data.")
        return

    name = profile.get("name", "")
    username = profile.get("username", "")
    email = profile.get("email", "")
    age = profile.get("age", "")
    gender = profile.get("gender", "")
    phone = profile.get("phone", "")
    created_at = datetime.fromisoformat(profile["created_at"]).strftime("%b %d, %Y")

    # Profile Card
    st.markdown(f"""
    <div style="
        background-color: #1f1f2e;
        padding: 25px;
        border-radius: 15px;
        color: white;
        width: 100%;
        max-width: 600px;
        margin: auto;
        box-shadow: 0 0 10px rgba(0,0,0,0.3);
    ">
        <h3 style="margin-top: 0;">🙋‍♀️ {name.title()}</h3>
        <p><strong>👤 Username:</strong> {username}</p>
        <p><strong>📧 Email:</strong> {email}</p>
        <p><strong>📱 Phone:</strong> {phone}</p>
        <p><strong>🎂 Age:</strong> {age}</p>
        <p><strong>🚻 Gender:</strong> {gender.capitalize()}</p>
        <p><strong>🕓 Joined:</strong> {created_at}</p>
    </div>
    """, unsafe_allow_html=True)
