import random
import streamlit as st
from streamlit_autorefresh import st_autorefresh


# =========================================================
# 페이지 설정
# =========================================================

st.set_page_config(
    page_title="코인 투자 게임",
    page_icon="🪙",
    layout="wide"
)


# =========================================================
# 게임 설정
# =========================================================

INITIAL_MONEY = 1_000_000

INITIAL_PRICES = {
    "BTC": 90_000_000,
    "ETH": 4_000_000,
    "SOL": 200_000,
}

COINS = ["BTC", "ETH", "SOL"]


# =========================================================
# 세션 상태 초기화
# =========================================================

if "money" not in st.session_state:
    st.session_state.money = INITIAL_MONEY


if "coins" not in st.session_state:
    st.session_state.coins = {
        "BTC": 0,
        "ETH": 0,
        "SOL": 0,
    }


if "prices" not in st.session_state:
    st.session_state.prices = INITIAL_PRICES.copy()


if "history" not in st.session_state:
    st.session_state.history = []


# =========================================================
# 자동 새로고침
#
# auto_refresh_count는
# "자동 새로고침이 몇 번 발생했는지"를 나타냄
# =========================================================

auto_refresh_count = st_autorefresh(
    interval=1500,
    key="market_auto_refresh"
)


# =========================================================
# 마지막 자동 새로고침 번호 초기화
# =========================================================

if "last_auto_refresh_count" not in st.session_state:

    st.session_state.last_auto_refresh_count = (
        auto_refresh_count
    )


# =========================================================
# 가격 변경 함수
# =========================================================

def update_prices():

    for coin in COINS:

        # -3% ~ +3%
        change = random.uniform(
            -0.03,
            0.03
        )

        old_price = (
            st.session_state.prices[coin]
        )

        new_price = (
            old_price * (1 + change)
        )

        # 최소 가격 1원
        new_price = max(
            1,
            new_price
        )

        st.session_state.prices[coin] = (
            new_price
        )


# =========================================================
# ⭐ 핵심
#
# 자동 새로고침 카운터가 증가했을 때만
# 시장 가격을 변경한다.
#
# 따라서 버튼을 눌러 Streamlit이 다시 실행되어도
# 가격은 변경되지 않는다.
# =========================================================

if (
    auto_refresh_count
    != st.session_state.last_auto_refresh_count
):

    update_prices()

    st.session_state.last_auto_refresh_count = (
        auto_refresh_count
    )


# =========================================================
# 매수 / 매도 수량 초기화
# =========================================================

for coin in COINS:

    buy_key = f"buy_quantity_{coin}"

    sell_key = f"sell_quantity_{coin}"


    if buy_key not in st.session_state:

        st.session_state[buy_key] = 1


    if sell_key not in st.session_state:

        st.session_state[sell_key] = 1


# =========================================================
# 계산 함수
# =========================================================

def get_coin_value():

    total = 0

    for coin in COINS:

        quantity = (
            st.session_state.coins[coin]
        )

        price = (
            st.session_state.prices[coin]
        )

        total += quantity * price

    return total


def get_total_asset():

    return (
        st.session_state.money
        + get_coin_value()
    )


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
# 제목
# =========================================================

st.title("🪙 코인 투자 게임")

st.caption(
    "⚡ 시장 가격은 1.5초마다 자동으로 변합니다."
)


# =========================================================
# 현재 자산
# =========================================================

coin_value = get_coin_value()

total_asset = get_total_asset()

profit = get_profit()

profit_rate = get_profit_rate()


# =========================================================
# 자산 정보
# =========================================================

col1, col2, col3, col4 = st.columns(4)


with col1:

    st.metric(
        "💵 보유 현금",
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


for coin in COINS:

    price = (
        st.session_state.prices[coin]
    )

    quantity = (
        st.session_state.coins[coin]
    )

    value = quantity * price


    # -----------------------------------------------------
    # 코인 이름
    # -----------------------------------------------------

    st.markdown(
        f"## {coin}"
    )


    # -----------------------------------------------------
    # 가격 / 보유량 / 평가액
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
            f"{quantity:,}개"
        )


    with col3:

        st.metric(
            "평가 금액",
            f"{value:,.0f}원"
        )


    # =====================================================
    # 매수 / 매도
    # =====================================================

    buy_col, sell_col = st.columns(2)


    # =====================================================
    # 매수
    # =====================================================

    with buy_col:

        st.markdown("### 🟢 매수")


        buy_quantity = st.number_input(
            "매수 수량",
            min_value=1,
            max_value=1_000_000,
            step=1,
            format="%d",
            key=f"buy_quantity_{coin}"
        )


        buy_cost = (
            buy_quantity * price
        )


        st.write(
            f"매수 금액: "
            f"**{buy_cost:,.0f}원**"
        )


        if st.button(
            f"🟢 {coin} 매수",
            key=f"buy_button_{coin}",
            use_container_width=True
        ):

            # ---------------------------------------------
            # 현금 부족
            # ---------------------------------------------

            if buy_cost > st.session_state.money:

                st.error(
                    "현금이 부족합니다."
                )

            else:

                # -----------------------------------------
                # 현금 차감
                # -----------------------------------------

                st.session_state.money -= (
                    buy_cost
                )


                # -----------------------------------------
                # 코인 증가
                # -----------------------------------------

                st.session_state.coins[coin] += (
                    buy_quantity
                )


                # -----------------------------------------
                # 거래 기록
                # -----------------------------------------

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
                    f"{coin} "
                    f"{buy_quantity:,}개 매수 완료!"
                )


                # -------------------------------------------------
                # 중요:
                # st.rerun()을 하더라도
                # auto_refresh_count는 증가하지 않기 때문에
                # 가격은 그대로 유지된다.
                # -------------------------------------------------

                st.rerun()


    # =====================================================
    # 매도
    # =====================================================

    with sell_col:

        st.markdown("### 🔴 매도")


        sell_quantity = st.number_input(
            "매도 수량",
            min_value=1,
            max_value=1_000_000,
            step=1,
            format="%d",
            key=f"sell_quantity_{coin}"
        )


        sell_amount = (
            sell_quantity * price
        )


        st.write(
            f"매도 금액: "
            f"**{sell_amount:,.0f}원**"
        )


        if st.button(
            f"🔴 {coin} 매도",
            key=f"sell_button_{coin}",
            use_container_width=True
        ):

            # ---------------------------------------------
            # 보유 수량 확인
            # ---------------------------------------------

            if (
                sell_quantity
                > st.session_state.coins[coin]
            ):

                st.error(
                    "보유 수량이 부족합니다."
                )

            else:

                # -----------------------------------------
                # 현금 증가
                # -----------------------------------------

                st.session_state.money += (
                    sell_amount
                )


                # -----------------------------------------
                # 코인 감소
                # -----------------------------------------

                st.session_state.coins[coin] -= (
                    sell_quantity
                )


                # -----------------------------------------
                # 거래 기록
                # -----------------------------------------

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
                    f"{coin} "
                    f"{sell_quantity:,}개 매도 완료!"
                )


                st.rerun()


    st.divider()


# =========================================================
# 내 자산
# =========================================================

st.subheader("💰 내 자산")


has_coin = False


for coin in COINS:

    quantity = (
        st.session_state.coins[coin]
    )

    price = (
        st.session_state.prices[coin]
    )

    value = quantity * price


    if quantity > 0:

        has_coin = True


        col1, col2, col3 = st.columns(3)


        with col1:

            st.write(
                f"**{coin}**"
            )


        with col2:

            st.write(
                f"{quantity:,}개"
            )


        with col3:

            st.write(
                f"{value:,.0f}원"
            )


if not has_coin:

    st.info(
        "현재 보유 중인 코인이 없습니다."
    )


# =========================================================
# 거래 내역
# =========================================================

st.divider()

st.subheader("📜 거래 내역")


if not st.session_state.history:

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
            f"{icon} "
            f"**{trade['type']}** | "
            f"{trade['coin']} | "
            f"{trade['quantity']:,}개 | "
            f"{trade['price']:,.0f}원 | "
            f"{trade['amount']:,.0f}원"
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

    # -----------------------------------------------------
    # 현금
    # -----------------------------------------------------

    st.session_state.money = (
        INITIAL_MONEY
    )


    # -----------------------------------------------------
    # 코인
    # -----------------------------------------------------

    st.session_state.coins = {
        "BTC": 0,
        "ETH": 0,
        "SOL": 0,
    }


    # -----------------------------------------------------
    # 가격
    # -----------------------------------------------------

    st.session_state.prices = (
        INITIAL_PRICES.copy()
    )


    # -----------------------------------------------------
    # 거래 내역
    # -----------------------------------------------------

    st.session_state.history = []


    # -----------------------------------------------------
    # 수량
    # -----------------------------------------------------

    for coin in COINS:

        st.session_state[
            f"buy_quantity_{coin}"
        ] = 1

        st.session_state[
            f"sell_quantity_{coin}"
        ] = 1


    st.success(
        "게임이 초기화되었습니다."
    )


    st.rerun()
