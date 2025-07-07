import streamlit as st
import sys
import os

# Add project root to path
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

# 🔐 Redirect if not logged in
if not st.session_state.get("logged_in") or "token" not in st.session_state:
    st.warning("You must be logged in to access the dashboard.")
    st.switch_page("main.py")  # change this if your file is named differently
    st.stop()

# ✅ Now safe to use session data
token = st.session_state.token

# ✅ Import internal app pages
import requests
from pages.portfolio import render_portfolio_page
from pages.wishlist import render_wishlist_page
from pages.transactions import render_transactions_page
from pages.profile import render_profile_page

from url import BASE_URL


def fetch_coins():
    requests.get(f"{BASE_URL}/refresh-dashboard")
    res = requests.get(f"{BASE_URL}/coins")
    return res.json()

def safe_format_number(value, decimals=2):
    """Safely format a number, handling None values"""
    if value is None:
        return "N/A"
    else:
        if decimals == 0:
            return f"{value:,.0f}"
        else:
            return f"{value:,.{decimals}f}"

def safe_format_percentage(value, decimals=1):
    """Safely format a percentage, handling None values"""
    if value is None:
        return "N/A"
    else:
        return f"{value:.{decimals}f}%"

def inject_css():
    st.markdown("""
    <style>
    /* Hide default MPA sidebar from Streamlit */
    [data-testid="stSidebarNav"] {
        display: none !important;
    }
    </style>
""", unsafe_allow_html=True)
    st.markdown("""
    <style>
    /* Hide the radio circle */
    .stRadio > div[role="radiogroup"] > label > div:first-child {
        display: none !important;
    }

    /* Style the entire label like a sidebar nav item */
    .stRadio > div[role="radiogroup"] > label {
        display: block;
        padding: 12px;
        border-radius: 8px;
        color: #E2E8F0;  /* light text */
        background-color: transparent;
        transition: all 0.2s ease;
        font-weight: 900;
        font-size: 20px;
    }

    /* Hover effect */
    .stRadio > div[role="radiogroup"] > label:hover {
        background-color: #2D3948;  /* subtle dark hover */
        color: #fff;
    }

    </style>
""", unsafe_allow_html=True)

    st.markdown("""
        <style>
            /* Hide Streamlit default elements */
            .stApp > header {visibility: hidden;}
            .stApp > div:first-child {padding-top: 0;}
            /* Main container */
            .main .block-container {
                padding-top: 2rem;
                max-width: 1400px;
            }
            /* Custom card styling */
            .crypto-card {
                background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
                border-radius: 16px;
                padding: 2px;
                box-shadow: 0 8px 32px rgba(0,0,0,0.1);
                transition: all 0.3s ease;
            }
            .crypto-card:hover {
                transform: translateY(-8px);
                box-shadow: 0 16px 48px rgba(0,0,0,0.15);
            }
            .coin-header {
                display: flex;
                align-items: center;
                justify-content: space-between;
                margin-bottom: 16px;
                padding-bottom: 12px;
                border-bottom: 2px solid #f0f0f0;
            }
            .coin-title {
                font-size: 20px;
                font-weight: 700;
                color: #2d3748;
                margin: 0;
            }
            .coin-symbol {
                font-size: 14px;
                color: #718096;
                font-weight: 500;
            }
            .price-display {
                background: linear-gradient(135deg, #667eea, #764ba2);
                color: white;
                padding: 6px;
                border-radius: 8px;
                text-align: center;
                margin-bottom: 6px;
            }
            .price-label {
                font-size: 12px;
                opacity: 0.9;
            }
            .price-amount {
                font-size: 26px;
                font-weight: 800;
            }
            .stats-container {
            display: grid;
            grid-template-columns: 1fr 1fr;
            gap: 6px;
            margin-bottom: 10px;
            }
            .stat-box {
                background: #f8fafc;
                border-radius: 8px;
                padding: 6px;
                border-left: 3px solid #667eea;
            }
            .stat-title {
                font-size: 12px;
                color: #718096;
                font-weight: 600;
                text-transform: uppercase;
                letter-spacing: 0.5px;
                margin-bottom: 3px;
            }
            .stat-number {
                font-size: 16px;
                font-weight: 700;
                color: #2d3748;
                margin: 0;
            }
            .positive { color: #48bb78; }
            .negative { color: #f56565; }
            .rank-indicator {
                background: linear-gradient(135deg, #667eea, #764ba2);
                color: white;
                padding: 6px 12px;
                border-radius: 20px;
                font-size: 12px;
                font-weight: 600;
            .main .block-container {
            max-width: 1600px;  /* or even 1800px */
            padding: 1rem 2rem;
            }
            }
        </style>
    """, unsafe_allow_html=True)
    
def get_user_balance(token, base_url):
    """
    Fetch user balance from the API
    """
    try:
        response = requests.get(f"{base_url}/wallet?token={token}")
        if response.ok:
            return response.json().get("balance", 0), True  # Return balance and success status
        else:
            return 0, False  # Return 0 balance and failure status
    except Exception as e:
        st.error(f"Error fetching balance: {str(e)}")
        return 0, False

def render_coin_card(coin, token):
    coin_name = coin.get('name', 'Unknown Coin')
    coin_symbol = coin.get('symbol', 'N/A')
    coin_price = coin.get('price', 0)
    coin_rank = coin.get('rank', 'N/A')
    coin_id = coin.get('coin_id', '')
    coin_image = coin.get('coin_image_url', '')
    ath_formatted = safe_format_number(coin.get('ath', 0), 2)
    percent_from_ath = coin.get('percent_from_ath')
    percent_formatted = safe_format_percentage(percent_from_ath)
    market_cap_formatted = safe_format_number(coin.get('market_cap', 0), 0)
    volume_formatted = safe_format_number(coin.get('volume_24h', 0), 0)
    price_formatted = safe_format_number(coin_price, 2)
    total_supply_formatted = safe_format_number(coin.get('total_supply', 0), 0)
    ath_color_class = "positive" if percent_from_ath is not None and percent_from_ath >= 0 else "negative"

    with st.container():
        st.markdown('<div class="crypto-card">', unsafe_allow_html=True)
        st.markdown('<div class="card-inner">', unsafe_allow_html=True)
        # Top section
        st.markdown(f"""
            <div style="display: flex; justify-content: space-between; align-items: center; margin-bottom: 12px;">
                <div>
                    <h3 style="margin: 0; font-size: 22px;">{coin_name}</h3>
                    <p style="margin: 0; color: #999; font-size: 16px;">{coin_symbol}</p>
                </div>
                <div>
                    <img src="{coin_image}" width="42">
                </div>
            </div>
        """, unsafe_allow_html=True)
        # Price display
        st.markdown(f"""
            <div class="price-display">
                <div class="price-label">Current Price</div>
                <div class="price-amount">${price_formatted}</div>
            </div>
        """, unsafe_allow_html=True)
        # Stats
        st.markdown(f"""
            <div class="stats-container">
                <div class="stat-box">
                    <div class="stat-title">Rank</div>
                    <div class="stat-number">#{coin_rank}</div>
                </div>
                <div class="stat-box">
                    <div class="stat-title">Total Supply</div>
                    <div class="stat-number">{total_supply_formatted}</div>
                </div>
                <div class="stat-box">
                    <div class="stat-title">ATH</div>
                    <div class="stat-number">${ath_formatted}</div>
                </div>
                <div class="stat-box">
                    <div class="stat-title">% from ATH</div>
                    <div class="stat-number {ath_color_class}">{percent_formatted}</div>
                </div>
                <div class="stat-box">
                    <div class="stat-title">Market Cap</div>
                    <div class="stat-number">${market_cap_formatted}</div>
                </div>
                <div class="stat-box">
                    <div class="stat-title">24h Volume</div>
                    <div class="stat-number">${volume_formatted}</div>
                </div>
            </div>
        """, unsafe_allow_html=True)
        # Buy section
        col1, col2, col3 = st.columns([3, 1, 1])
        with col1:
            quantity = st.number_input(
                f"Qty ({coin_symbol})", 
                key=f"qty_{coin_id}", 
                min_value=1, 
                step=1, 
                format="%d",
                label_visibility='collapsed'
            )
        with col2:
            if st.button("Buy", key=f"buy_{coin_id}", use_container_width=True, type='primary'):
                wallet_url = f'{BASE_URL}/wallet?token={token}'
                wallet_res = requests.get(wallet_url)

                if wallet_res.status_code == 401:
                    st.toast("❌ Invalid token. Please login again.", icon="🚫")
                elif wallet_res.ok:
                    wallet_data = wallet_res.json()
                    balance = wallet_data.get("balance", 0.0)
                    total_cost = quantity * coin_price

                    if total_cost > balance:
                        st.toast(
                            f"Insufficient balance. You need ${total_cost:,.2f}",
                            icon="⚠️"
                        )
                    else:
                        buy_url = f'{BASE_URL}/portfolio/buy?token={token}&quantity={quantity}&coin_id={coin_id}'
                        res = requests.post(buy_url)

                        if res.ok:
                            result = res.json()
                            st.toast(f"Bought {quantity} {coin_symbol} for ${total_cost:,.2f}", icon="✅")
                        else:
                            st.error("❌ Failed to complete purchase. Please try again.")
                else:
                    st.toast("❌ Something went wrong. Try again.", icon="🚫")
        with col3:
            if st.button("★", key=f"wishlist_{coin_id}", use_container_width=True, type='primary', help="Add to wishlist"):
                wishlist_url = f'{BASE_URL}/wishlist/add?token={token}&coin_id={coin_id}'
                wishlist_res = requests.post(wishlist_url)
                if wishlist_res.status_code == 200:
                    st.toast("✨ Added to Wishlist!")
                else:
                    st.toast("❌ Failed to add to Wishlist.", icon="⚠️")
        st.markdown('</div></div>', unsafe_allow_html=True)


def main():
    # 🔐 Redirect if not logged in
    if not st.session_state.get("logged_in") or "token" not in st.session_state:
        st.warning("You must be logged in to access the dashboard.")
        st.switch_page("main.py")  # change this if your file is named differently
        st.stop()

    # ✅ Now safe to use session data
    token = st.session_state.token

    st.set_page_config(
        page_title="Crypto Dashboard",
        layout="wide",
        page_icon="💹"
    )

    if "balance" not in st.session_state:
        balance, is_valid = get_user_balance(token, BASE_URL)
        if is_valid:
            st.session_state.balance = balance
        else:
            st.error("❌ Failed to fetch balance. Token may be invalid.")
            for key in list(st.session_state.keys()):
                del st.session_state[key]
            st.rerun()
            return
    else:
        balance = st.session_state.balance

    inject_css()

    col1, col2 = st.columns([3, 1])
    with col1:
        st.markdown(f"# CryptoSim")
        st.caption('It all starts here!')
    with col2:
        st.write('')
        if st.button(f"**Balance: ${balance:,.2f}**", key="refresh_balance", help="Refresh balance"):
            with st.spinner("Refreshing balance..."):
                balance, is_valid = get_user_balance(token, BASE_URL)
                if is_valid:
                    st.session_state.balance = balance
                    st.success("Balance refreshed!")
                    st.rerun()
                else:
                    st.error("❌ Failed to refresh balance. Token may be invalid.")
                    for key in list(st.session_state.keys()):
                        del st.session_state[key]
                    st.rerun()

    st.markdown("---")

    with st.sidebar:
        st.header('CryptoSim')
        st.markdown("---")
        page = st.radio("", ["Dashboard", "Portfolio", "Wishlist", 'Transactions', 'Profile'])
        st.markdown("---")
        st.markdown(f"**Current Balance: ${balance:,.2f}**")
        if st.button("Logout"):
            for key in list(st.session_state.keys()):
                del st.session_state[key]
            st.rerun()

    if page == "Dashboard":
        st.markdown("<h2 style='text-align: center; color: white;'>Dashboard</h2>", unsafe_allow_html=True)
        st.markdown("###")
        try:
            coins = fetch_coins(token) if 'token' in fetch_coins.__code__.co_varnames else fetch_coins()
            for i in range(0, len(coins), 4):
                cols = st.columns(4)
                for j, col in enumerate(cols):
                    if i + j < len(coins):
                        with col:
                            render_coin_card(coins[i + j], token)
        except Exception as e:
            st.error(f"Failed to load cryptocurrency data: {str(e)}")
            st.info("💡 Please check your internet connection or try refreshing the page.")
    elif page == 'Portfolio':
        render_portfolio_page()
    elif page == 'Wishlist':
        render_wishlist_page()
    elif page == 'Transactions':
        render_transactions_page()
    elif page == 'Profile':
        render_profile_page()
    else:
        st.warning(f"⚙️ `{page}` page is under construction.")

# Utility functions expected to be defined elsewhere in the same file or imported
# def inject_css(): ...
# def fetch_coins(token): ...
# def render_coin_card(...): ...
# def get_user_balance(token, base_url): ...

if __name__ == "__main__":
    main()