import streamlit as st
import requests
from url import BASE_URL



def render_wishlist_page():
    st.markdown("## 🌟 Your Wishlist")
    st.markdown("###")

    token = st.session_state.get("token")
    if not token:
        st.error("❌ You must be logged in to view your wishlist.")
        return

    res = requests.get(f"{BASE_URL}/wishlist?token={token}")
    if res.status_code != 200:
        st.error("Failed to fetch wishlist.")
        return

    wishlist_data = res.json()
    wishlist = wishlist_data.get("wishlist", [])

    if not wishlist:
        st.info("💤 Your wishlist is empty.")
        return

    for coin in wishlist:
        coin_id = coin["coin_id"]
        name = coin["name"]
        symbol = coin["symbol"]
        price = coin["price"]
        image = coin.get("coin_image_url", "")
        market_cap = coin["market_cap"]
        rank = coin["rank"]
        ath = coin["ath"]
        percent_from_ath = coin["percent_from_ath"]
        volume_24h = coin["volume_24h"]
        total_supply = coin["total_supply"]

        # Grey background card
        with st.container():
            st.markdown(
                """
                <div style="background-color: #343c57; padding: 2px; border-radius: 15px; margin-bottom: 15px;">
                """,
                unsafe_allow_html=True
            )

            col1, col2, col3, col4 = st.columns([1, 2, 2, 1])
            with col1:
                if image:
                    st.image(image, width=50)
            with col2:
                st.markdown(f"""
                <div style="color: white;">
                    <b>{name}</b> ({symbol})<br>
                    📌 Rank: {rank}<br>
                    💰 Price: ${price:,.4f}<br>
                    📈 ATH: ${ath:,.2f} ({percent_from_ath:+.2f}%)
                </div>
                """, unsafe_allow_html=True)

            with col3:
                st.markdown(f"""
                <div style="color: white;">
                    <br>
                    🔁 24h Volume: ${volume_24h:,.0f}<br>
                    📊 Market Cap: ${market_cap:,.0f}<br>
                    🪙 Total Supply: {total_supply:,}
                </div>
                """, unsafe_allow_html=True)


            with col4:
                if st.button("❌ Remove", key=f"remove_{coin_id}"):
                    remove_url = f"{BASE_URL}/wishlist/remove?token={token}&coin_id={coin_id}"
                    remove_res = requests.delete(remove_url)
                    if remove_res.status_code == 200:
                        st.toast(f"✅ Removed {symbol} from wishlist")
                        st.rerun()
                    else:
                        st.toast("❌ Failed to remove item from wishlist")
            st.markdown("</div>", unsafe_allow_html=True)
