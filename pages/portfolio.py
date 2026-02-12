import streamlit as st
import requests
from url import BASE_URL



def render_portfolio_page():
    st.markdown("<h2 style='text-align: center; color: white;'>📊 Your Portfolio</h2>", unsafe_allow_html=True)
    st.markdown("###")

    token = st.session_state.get("token")
    if not token:
        token = st.text_input("🔐 Enter your login token to continue:", type="password")
        if token:
            st.session_state["token"] = token
        else:
            st.stop()

    with st.spinner("Fetching your portfolio..."):
        try:
            res = requests.get(f"{BASE_URL}/portfolio?token={token}")
            res.raise_for_status()
            response_data = res.json()
        except Exception:
            st.error("🚫 Failed to fetch data.")
            return

    if "message" in response_data and response_data["message"] == "Invalid token":
        st.error("❌ Invalid token. Please try again.")
        st.session_state.pop("token", None)
        st.rerun()

    portfolio = response_data.get("portfolio", [])
    if not portfolio:
        st.info("🧐 No holdings yet.")
        return

    total_value = 0
    total_invested = 0
    total_pl = 0

    st.markdown("## 💼 Holdings Overview")
    st.markdown("---")

    for asset in portfolio:
        coin_id = asset["coin_id"]
        quantity = asset["quantity"]
        current_price = asset["current_price"]
        avg_price = asset["avg_price"]
        profit_loss = asset["profit_loss"]
        value = quantity * current_price
        invested = quantity * avg_price
        image_url = asset.get("coin_image_url") or ""

        total_value += value
        total_invested += invested
        total_pl += profit_loss

        pl_color = "limegreen" if profit_loss >= 0 else "crimson"

        with st.container():
            st.markdown(
                f"""
                <div style="
                    border-radius: 16px;
                    background-color: #1f1f2e;
                    padding: 20px;
                    margin-bottom: 10px;
                    color: #f1f1f1;
                    box-shadow: 0 0 10px rgba(0,0,0,0.3);
                ">
                    <div style="display: flex; align-items: center; justify-content: space-between;">
                        <div style="display: flex; align-items: center;">
                            <img src="{image_url}" alt="coin" style="width: 50px; height: 50px; margin-right: 15px; border-radius: 8px;" onerror="this.style.display='none'"/>
                            <h4 style="margin: 0;">🔷 {coin_id.upper()}</h4>
                        </div>
                        <div style="color:{pl_color}; font-weight: bold;">P/L: ${profit_loss:,.2f}</div>
                    </div>
                    <div style="display: flex; justify-content: space-between; margin-top: 12px; font-size: 15px;">
                        <div>💰 <b>Current:</b> ${current_price:,.2f}</div>
                        <div>📦 <b>Qty:</b> {quantity}</div>
                        <div>📈 <b>Avg Buy:</b> ${avg_price:,.2f}</div>
                        <div>💎 <b>Value:</b> ${value:,.2f}</div>
                    </div>
                """,
                unsafe_allow_html=True
            )

            # Sell UI inside same card
            col1, col2 = st.columns([2, 1])
            with col1:
                sell_qty = st.number_input(
                    f"Sell Qty ({coin_id.upper()})",
                    min_value=0,
                    max_value=int(quantity),
                    step=1,
                    key=f"sell_qty_{coin_id}",
                    label_visibility="collapsed"
                )
            with col2:
                if st.button(f"💸 Sell", key=f"sell_{coin_id}", use_container_width=True, type='primary'):
                    if sell_qty <= 0:
                        st.toast("⚠️ Enter a valid quantity to sell.", icon="⚠️")
                    elif sell_qty > quantity:
                        st.toast(f"❌ You only own {quantity} {coin_id.upper()}.", icon="🚫")
                    else:
                        sell_url = f"{BASE_URL}/portfolio/sell?token={token}&quantity={sell_qty}&coin_id={coin_id}"
                        res = requests.post(sell_url)

                        if res.status_code == 401:
                            st.toast("❌ Invalid token. Please login again.", icon="🚫")
                        elif res.ok:
                            total_earned = sell_qty * current_price
                            st.toast(f"✅ Sold {sell_qty} {coin_id.upper()} for ${total_earned:,.2f}", icon="💰")
                            st.rerun()
                        else:
                            st.error("❌ Failed to complete sale. Please try again.")

            st.markdown("</div>", unsafe_allow_html=True)  # Close outer div

    # Portfolio Summary
    st.markdown("---")
    st.markdown("## 📊 Portfolio Summary")
    net_pl_color = "limegreen" if total_pl >= 0 else "crimson"

    st.markdown(
        f"""
        <div style="
            padding: 25px;
            border-radius: 12px;
            background-color: #141421;
            box-shadow: 0px 0px 10px rgba(0,0,0,0.3);
            font-size: 18px;
            color: #f1f1f1;
        ">
            <b>Total Invested:</b> ${total_invested:,.2f} &nbsp;&nbsp;|&nbsp;&nbsp;
            <b>Current Value:</b> ${total_value:,.2f} &nbsp;&nbsp;|&nbsp;&nbsp;
            <b>Net P/L:</b> <span style="color:{net_pl_color}; font-weight: bold;">${total_pl:,.2f}</span>
        </div>
        """,
        unsafe_allow_html=True
    )
