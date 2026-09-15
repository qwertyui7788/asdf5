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
# 세션 데이터 초기화
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


# ---------------------------------------------------------
# 버튼을 눌렀을 때 가격 변경을 막기 위한 변수
# ---------------------------------------------------------

if "skip_price_update" not in st.session_state:
    st.session_state.skip_price_update = False


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
# 가격 업데이트
# =========================================================

def update_prices():

    for coin in COINS:

        # -3% ~ +3%
        change = random.uniform(
            -0.03,
            0.03
        )

        old_price = st.session_state.prices[coin]

        new_price = old_price * (1 + change)

        # 최소 가격 1원
        new_price = max(
            1,
            new_price
        )

        st.session_state.prices[coin] = new_price


# =========================================================
# 버튼 클릭 시 호출되는 함수
#
# 버튼을 눌렀을 때 가격 업데이트를 건너뛰도록 설정
# =========================================================

def prevent_price_change():

    st.session_state.skip_price_update = True


# =========================================================
# 1.5초 자동 새로고침
# =========================================================

st_autorefresh(
    interval=1500,
    key="automatic_market_refresh"
)


# =========================================================
# 가격 업데이트
#
# 중요:
# 일반 버튼을 눌러 화면이 다시 실행되었을 때는
# 가격을 변경하지 않음.
#
# 자동 새로고침일 때만 가격 변경.
# =========================================================

if st.session_state.skip_price_update:

    # 버튼 클릭 때문에 발생한 새로고침이면
    # 가격을 그대로 유지한다.
    st.session_state.skip_price_update = False

else:

    # 자동 새로고침
    update_prices()


# =========================================================
# 계산 함수
# =========================================================

def get_coin_value():

    total = 0

    for coin in COINS:

        quantity = st.session_state.coins[coin]

        price = st.session_state.prices[coin]

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

st.info(
    "💡 매수·매도·수량 조절 버튼을 눌러도 시장 가격은 변하지 않습니다."
)


# =========================================================
# 자산 계산
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
# 코인 시장
# =========================================================

st.subheader("📊 코인 시장")


for coin in COINS:

    price = st.session_state.prices[coin]

    quantity = st.session_state.coins[coin]

    value = quantity * price


    # =====================================================
    # 코인 이름
    # =====================================================

    st.markdown(
        f"## {coin}"
    )


    # =====================================================
    # 가격 / 보유량 / 평가액
    # =====================================================

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


        buy_key = f"buy_quantity_{coin}"


        buy_quantity = st.number_input(
            "매수 수량",
            min_value=1,
            step=1,
            format="%d",
            key=buy_key
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
            use_container_width=True,
            on_click=prevent_price_change
        ):

            if buy_quantity <= 0:

                st.error(
                    "매수 수량을 입력하세요."
                )

            elif buy_cost > st.session_state.money:

                st.error(
                    "현금이 부족합니다."
                )

            else:

                # -------------------------------------------------
                # 현금 차감
                # -------------------------------------------------

                st.session_state.money -= buy_cost


                # -------------------------------------------------
                # 코인 증가
                # -------------------------------------------------

                st.session_state.coins[coin] += (
                    buy_quantity
                )


                # -------------------------------------------------
                # 거래 기록
                # -------------------------------------------------

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


                st.rerun()


    # =====================================================
    # 매도
    # =====================================================

    with sell_col:

        st.markdown("### 🔴 매도")


        sell_key = f"sell_quantity_{coin}"


        sell_quantity = st.number_input(
            "매도 수량",
            min_value=1,
            step=1,
            format="%d",
            key=sell_key
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
            use_container_width=True,
            on_click=prevent_price_change
        ):

            # -------------------------------------------------
            # 보유량 검사
            # -------------------------------------------------

            if sell_quantity <= 0:

                st.error(
                    "매도 수량을 입력하세요."
                )

            elif sell_quantity > st.session_state.coins[coin]:

                st.error(
                    "보유 수량이 부족합니다."
                )

            else:

                # -------------------------------------------------
                # 현금 증가
                # -------------------------------------------------

                st.session_state.money += (
                    sell_amount
                )


                # -------------------------------------------------
                # 코인 감소
                # -------------------------------------------------

                st.session_state.coins[coin] -= (
                    sell_quantity
                )


                # -------------------------------------------------
                # 거래 기록
                # -------------------------------------------------

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


asset_exists = False


for coin in COINS:

    quantity = st.session_state.coins[coin]

    price = st.session_state.prices[coin]

    value = quantity * price


    if quantity > 0:

        asset_exists = True

        col1, col2, col3 = st.columns(3)


        with col1:

            st.write(
                f"### {coin}"
            )


        with col2:

            st.write(
                f"보유량: **{quantity:,}개**"
            )


        with col3:

            st.write(
                f"평가액: **{value:,.0f}원**"
            )


if not asset_exists:

    st.info(
        "현재 보유 중인 코인이 없습니다."
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
    use_container_width=True,
    on_click=prevent_price_change
):

    # -----------------------------------------------------
    # 현금 초기화
    # -----------------------------------------------------

    st.session_state.money = INITIAL_MONEY


    # -----------------------------------------------------
    # 코인 초기화
    # -----------------------------------------------------

    st.session_state.coins = {
        "BTC": 0,
        "ETH": 0,
        "SOL": 0,
    }


    # -----------------------------------------------------
    # 가격 초기화
    # -----------------------------------------------------

    st.session_state.prices = (
        INITIAL_PRICES.copy()
    )


    # -----------------------------------------------------
    # 거래 내역 초기화
    # -----------------------------------------------------

    st.session_state.history = []


    # -----------------------------------------------------
    # 수량 초기화
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
