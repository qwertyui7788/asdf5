import random
import streamlit as st
from streamlit_autorefresh import st_autorefresh


# =========================================================
# 기본 설정
# =========================================================

st.set_page_config(
    page_title="코인 투자 게임",
    page_icon="🪙",
    layout="wide"
)


# =========================================================
# 설정
# =========================================================

INITIAL_MONEY = 1_000_000

INITIAL_PRICES = {
    "BTC": 90_000_000,
    "ETH": 4_000_000,
    "SOL": 200_000,
}


# =========================================================
# 3초마다 화면 자동 새로고침
# =========================================================

st_autorefresh(
    interval=3000,
    key="coin_game_refresh"
)


# =========================================================
# 게임 데이터 초기화
# =========================================================

if "money" not in st.session_state:
    st.session_state.money = INITIAL_MONEY


if "coins" not in st.session_state:
    st.session_state.coins = {
        "BTC": 0.0,
        "ETH": 0.0,
        "SOL": 0.0,
    }


if "prices" not in st.session_state:
    st.session_state.prices = INITIAL_PRICES.copy()


if "history" not in st.session_state:
    st.session_state.history = []


# =========================================================
# 가격 변동
# =========================================================

def update_prices():

    for coin in st.session_state.prices:

        # -3% ~ +3%
        change = random.uniform(-0.03, 0.03)

        old_price = st.session_state.prices[coin]

        new_price = old_price * (1 + change)

        # 가격이 1원 아래로 내려가지 않도록
        new_price = max(1, new_price)

        st.session_state.prices[coin] = new_price


# =========================================================
# 총 코인 평가액
# =========================================================

def get_coin_value():

    total = 0

    for coin in st.session_state.coins:

        quantity = st.session_state.coins[coin]

        price = st.session_state.prices[coin]

        total += quantity * price

    return total


# =========================================================
# 총 자산
# =========================================================

def get_total_asset():

    return (
        st.session_state.money
        + get_coin_value()
    )


# =========================================================
# 수익률
# =========================================================

def get_profit():

    return (
        get_total_asset()
        - INITIAL_MONEY
    )


def get_profit_rate():

    return (
        get_profit()
        / INITIAL_MONEY
        * 100
    )


# =========================================================
# 가격 업데이트
# =========================================================

update_prices()


# =========================================================
# 제목
# =========================================================

st.title("🪙 코인 투자 게임")

st.caption(
    "가격은 3초마다 자동으로 변합니다."
)


# =========================================================
# 상단 정보
# =========================================================

coin_value = get_coin_value()

total_asset = get_total_asset()

profit = get_profit()

profit_rate = get_profit_rate()


col1, col2, col3, col4 = st.columns(4)


with col1:

    st.metric(
        "💵 현금",
        f"{st.session_state.money:,.0f}원"
    )


with col2:

    st.metric(
        "🪙 코인 평가액",
        f"{coin_value:,.0f}원"
    )


with col3:

    st.metric(
        "💰 총 자산",
        f"{total_asset:,.0f}원"
    )


with col4:

    st.metric(
        "📈 수익률",
        f"{profit_rate:+.2f}%",
        delta=f"{profit:+,.0f}원"
    )


st.divider()


# =========================================================
# 시장
# =========================================================

st.subheader("📊 코인 시장")


for coin in ["BTC", "ETH", "SOL"]:

    price = st.session_state.prices[coin]

    quantity = st.session_state.coins[coin]

    value = quantity * price


    # -----------------------------------------------------
    # 코인 제목
    # -----------------------------------------------------

    st.markdown(
        f"## {coin}"
    )


    # -----------------------------------------------------
    # 가격 정보
    # -----------------------------------------------------

    col1, col2, col3 = st.columns(3)


    with col1:

        st.metric(
            "현재 가격",
            f"{price:,.0f}원"
        )


    with col2:

        st.metric(
            "보유 수량",
            f"{quantity:.6f}"
        )


    with col3:

        st.metric(
            "평가 금액",
            f"{value:,.0f}원"
        )


    # -----------------------------------------------------
    # 매수 / 매도
    # -----------------------------------------------------

    buy_col, sell_col = st.columns(2)


    # =====================================================
    # 매수
    # =====================================================

    with buy_col:

        st.markdown("### 🟢 매수")


        buy_key = f"buy_quantity_{coin}"


        # 세션에 수량이 없으면 생성
        if buy_key not in st.session_state:
            st.session_state[buy_key] = 0.01


        buy_quantity = st.number_input(
            "매수 수량",
            min_value=0.000001,
            step=0.01,
            format="%.6f",
            key=buy_key
        )


        buy_cost = (
            buy_quantity
            * price
        )


        st.write(
            f"매수 금액: **{buy_cost:,.0f}원**"
        )


        if st.button(
            f"{coin} 매수",
            key=f"buy_button_{coin}",
            use_container_width=True
        ):

            if buy_quantity <= 0:

                st.error(
                    "수량을 입력하세요."
                )

            elif buy_cost > st.session_state.money:

                st.error(
                    "현금이 부족합니다."
                )

            else:

                st.session_state.money -= buy_cost

                st.session_state.coins[coin] += buy_quantity


                st.session_state.history.append(
                    {
                        "type": "매수",
                        "coin": coin,
                        "quantity": buy_quantity,
                        "price": price,
                        "amount": buy_cost,
                    }
                )


                st.success(
                    f"{coin} {buy_quantity:.6f}개 매수!"
                )


                # 입력창 초기화
                st.session_state[buy_key] = 0.01

                st.rerun()


    # =====================================================
    # 매도
    # =====================================================

    with sell_col:

        st.markdown("### 🔴 매도")


        sell_key = f"sell_quantity_{coin}"


        if sell_key not in st.session_state:
            st.session_state[sell_key] = 0.01


        sell_quantity = st.number_input(
            "매도 수량",
            min_value=0.000001,
            step=0.01,
            format="%.6f",
            key=sell_key
        )


        sell_amount = (
            sell_quantity
            * price
        )


        st.write(
            f"매도 금액: **{sell_amount:,.0f}원**"
        )


        if st.button(
            f"{coin} 매도",
            key=f"sell_button_{coin}",
            use_container_width=True
        ):

            if sell_quantity <= 0:

                st.error(
                    "수량을 입력하세요."
                )

            elif sell_quantity > st.session_state.coins[coin]:

                st.error(
                    "보유 수량이 부족합니다."
                )

            else:

                st.session_state.money += sell_amount

                st.session_state.coins[coin] -= sell_quantity


                st.session_state.history.append(
                    {
                        "type": "매도",
                        "coin": coin,
                        "quantity": sell_quantity,
                        "price": price,
                        "amount": sell_amount,
                    }
                )


                st.success(
                    f"{coin} {sell_quantity:.6f}개 매도!"
                )


                st.session_state[sell_key] = 0.01

                st.rerun()


    st.divider()


# =========================================================
# 내 자산
# =========================================================

st.subheader("💰 내 자산")


for coin in ["BTC", "ETH", "SOL"]:

    quantity = st.session_state.coins[coin]

    price = st.session_state.prices[coin]

    value = quantity * price


    if quantity > 0:

        col1, col2, col3 = st.columns(3)


        with col1:

            st.write(
                f"**{coin}**"
            )


        with col2:

            st.write(
                f"{quantity:.6f}개"
            )


        with col3:

            st.write(
                f"{value:,.0f}원"
            )


# =========================================================
# 거래 내역
# =========================================================

st.divider()

st.subheader("📜 거래 내역")


if len(st.session_state.history) == 0:

    st.info(
        "아직 거래 내역이 없습니다."
    )

else:

    for trade in reversed(
        st.session_state.history
    ):

        if trade["type"] == "매수":

            icon = "🟢"

        else:

            icon = "🔴"


        st.write(
            f"""
            {icon} **{trade['type']}**

            {trade['coin']} |
            {trade['quantity']:.6f}개 |
            {trade['price']:,.0f}원 |
            {trade['amount']:,.0f}원
            """
        )


# =========================================================
# 게임 초기화
# =========================================================

st.divider()

st.subheader("⚙️ 게임")


if st.button(
    "🔄 게임 초기화",
    use_container_width=True
):

    st.session_state.money = INITIAL_MONEY


    st.session_state.coins = {
        "BTC": 0.0,
        "ETH": 0.0,
        "SOL": 0.0,
    }


    st.session_state.prices = (
        INITIAL_PRICES.copy()
    )


    st.session_state.history = []


    # 매수/매도 수량도 초기화
    for coin in ["BTC", "ETH", "SOL"]:

        st.session_state[
            f"buy_quantity_{coin}"
        ] = 0.01

        st.session_state[
            f"sell_quantity_{coin}"
        ] = 0.01


    st.rerun()
