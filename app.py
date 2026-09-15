import streamlit as st
import random

st.set_page_config(
    page_title="코인 투자 게임",
    page_icon="🪙",
    layout="wide"
)

# -------------------------
# 기본 설정
# -------------------------

INITIAL_MONEY = 1_000_000

COINS = {
    "BTC": 90_000_000,
    "ETH": 4_000_000,
    "SOL": 200_000,
}

# -------------------------
# 게임 데이터 초기화
# -------------------------

if "money" not in st.session_state:
    st.session_state.money = INITIAL_MONEY

if "coins" not in st.session_state:
    st.session_state.coins = {
        "BTC": 0.0,
        "ETH": 0.0,
        "SOL": 0.0,
    }

if "prices" not in st.session_state:
    st.session_state.prices = COINS.copy()

if "history" not in st.session_state:
    st.session_state.history = []


# -------------------------
# 가격 변동
# -------------------------

def update_prices():

    for coin in COINS:

        # -5% ~ +5% 랜덤 가격 변동
        change = random.uniform(-0.05, 0.05)

        st.session_state.prices[coin] *= (
            1 + change
        )

        # 가격이 너무 작아지지 않도록
        st.session_state.prices[coin] = max(
            st.session_state.prices[coin],
            1
        )


# -------------------------
# 총자산 계산
# -------------------------

def get_total_asset():

    total = st.session_state.money

    for coin in COINS:

        total += (
            st.session_state.coins[coin]
            * st.session_state.prices[coin]
        )

    return total


# -------------------------
# 화면
# -------------------------

st.title("🪙 코인 투자 게임")

st.write(
    "가상 돈으로 코인을 사고팔아 수익률을 겨루는 게임입니다."
)

st.divider()


# -------------------------
# 상단 자산 정보
# -------------------------

total_asset = get_total_asset()

profit = total_asset - INITIAL_MONEY

profit_rate = (
    profit / INITIAL_MONEY * 100
)


col1, col2, col3 = st.columns(3)

with col1:
    st.metric(
        "💵 보유 현금",
        f"{st.session_state.money:,.0f}원"
    )

with col2:
    st.metric(
        "💰 총 자산",
        f"{total_asset:,.0f}원"
    )

with col3:
    st.metric(
        "📈 수익률",
        f"{profit_rate:+.2f}%"
    )


st.divider()


# -------------------------
# 가격 업데이트
# -------------------------

if st.button(
    "🔄 시장 가격 업데이트",
    use_container_width=True
):

    update_prices()

    st.rerun()


# -------------------------
# 코인 목록
# -------------------------

st.subheader("📊 코인 시장")


for coin in COINS:

    price = st.session_state.prices[coin]

    st.write(
        f"### {coin}"
    )

    col1, col2, col3 = st.columns(3)

    with col1:

        st.metric(
            "현재 가격",
            f"{price:,.0f}원"
        )

    with col2:

        st.write(
            f"보유량: "
            f"{st.session_state.coins[coin]:.6f}"
        )

    with col3:

        value = (
            st.session_state.coins[coin]
            * price
        )

        st.write(
            f"평가금액: {value:,.0f}원"
        )

    # -------------------------
    # 거래
    # -------------------------

    col1, col2 = st.columns(2)

    with col1:

        buy_amount = st.number_input(
            f"{coin} 매수 수량",
            min_value=0.0,
            value=0.0,
            step=0.001,
            key=f"buy_{coin}"
        )

        if st.button(
            f"🟢 {coin} 매수",
            key=f"buy_button_{coin}",
            use_container_width=True
        ):

            cost = buy_amount * price

            if buy_amount <= 0:

                st.error(
                    "매수 수량을 입력하세요."
                )

            elif cost > st.session_state.money:

                st.error(
                    "현금이 부족합니다."
                )

            else:

                st.session_state.money -= cost

                st.session_state.coins[coin] += (
                    buy_amount
                )

                st.session_state.history.append(
                    f"{coin} {buy_amount:.6f} 매수"
                )

                st.success(
                    f"{coin} 매수 완료!"
                )

                st.rerun()

    with col2:

        sell_amount = st.number_input(
            f"{coin} 매도 수량",
            min_value=0.0,
            value=0.0,
            step=0.001,
            key=f"sell_{coin}"
        )

        if st.button(
            f"🔴 {coin} 매도",
            key=f"sell_button_{coin}",
            use_container_width=True
        ):

            if sell_amount <= 0:

                st.error(
                    "매도 수량을 입력하세요."
                )

            elif (
                sell_amount
                > st.session_state.coins[coin]
            ):

                st.error(
                    "보유 수량이 부족합니다."
                )

            else:

                revenue = (
                    sell_amount * price
                )

                st.session_state.money += revenue

                st.session_state.coins[coin] -= (
                    sell_amount
                )

                st.session_state.history.append(
                    f"{coin} {sell_amount:.6f} 매도"
                )

                st.success(
                    f"{coin} 매도 완료!"
                )

                st.rerun()

    st.divider()


# -------------------------
# 거래 내역
# -------------------------

st.subheader("📜 거래 내역")

if st.session_state.history:

    for item in reversed(
        st.session_state.history
    ):

        st.write(
            f"• {item}"
        )

else:

    st.info(
        "아직 거래 내역이 없습니다."
    )


# -------------------------
# 게임 초기화
# -------------------------

st.divider()

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

    st.session_state.prices = COINS.copy()

    st.session_state.history = []

    st.rerun()
