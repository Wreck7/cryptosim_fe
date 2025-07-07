import streamlit as st
import requests
from datetime import datetime
from url import BASE_URL


def render_transactions_page():
    st.markdown("<h2 style='text-align: center; color: white;'>📑 Transaction History</h2>", unsafe_allow_html=True)
    st.markdown("###")

    token = st.session_state.get("token")
    if not token:
        st.error("❌ Please login to view your transactions.")
        return

    # Search bar
    search = st.text_input("🔍 Search by coin name or leave empty to view all", placeholder="e.g. bitcoin, eth, solana")

    # Determine endpoint
    if search:
        st.markdown(f"Showing results for: **{search}**")
        coin_id = search.lower().replace(" ", "-")
        url = f"{BASE_URL}/coin_transactions?token={token}&coin_id={coin_id}"
    else:
        url = f"{BASE_URL}/transactions?token={token}"

    try:
        res = requests.get(url)
        res.raise_for_status()
        txs = res.json()
    except Exception:
        st.error("❌ Failed to fetch transactions.")
        return

    if not isinstance(txs, list):
        if search:
            st.warning(f"🔍 No transactions found for **{search}**.")
        else:
            st.info("🙁 No transactions found.")
        return
    
    for tx in txs:
        tx_type = tx["type"].capitalize()
        quantity = tx["quantity"]
        price = tx["price_per_unit"]
        total = tx["total_value"]
        coin = tx["coin_id"]
        date = datetime.fromisoformat(tx["created_at"]).strftime("%b %d, %Y %H:%M")

        card_color = "#1f1f2e" if tx["type"] == "buy" else "#382222"

        st.markdown(f"""
        <div style="
            background-color: {card_color};
            border-radius: 12px;
            padding: 15px 20px;
            margin-bottom: 15px;
            box-shadow: 0 0 10px rgba(0,0,0,0.3);
            color: white;
        ">
            <div style="display: flex; justify-content: space-between; align-items: center;">
                <div style="font-size: 18px;"><b>{tx_type}</b> {quantity} × {coin.upper()}</div>
                <div style="opacity: 0.7; font-size: 14px;">{date}</div>
            </div>
            <div style="margin-top: 10px;">
                💰 <b>Unit Price:</b> ${price:,.2f}<br>
                🧾 <b>Total:</b> ${total:,.2f}
            </div>
        </div>
        """, unsafe_allow_html=True)
