import streamlit as st
import streamlit.components.v1 as components


# ============================================================
# STREAMLIT KONFIGURATION
# ============================================================

st.set_page_config(
    page_title="Taschenrechner",
    page_icon="🧮",
    layout="centered",
    initial_sidebar_state="collapsed",
)


# ============================================================
# SESSION STATE
# ============================================================

if "display" not in st.session_state:
    st.session_state.display = "0"

if "stored_number" not in st.session_state:
    st.session_state.stored_number = None

if "operator" not in st.session_state:
    st.session_state.operator = None

if "waiting" not in st.session_state:
    st.session_state.waiting = False


# ============================================================
# HAPTIK
# ============================================================

def vibrate():
    """
    Versucht eine kurze Vibration auf Smartphones auszulösen.
    Zusätzlich gibt es einen visuellen Button-Effekt.
    """

    components.html(
        """
        <script>
        try {
            if ("vibrate" in navigator) {
                navigator.vibrate(15);
            }
        } catch (e) {}
        </script>
        """,
        height=0,
    )


# ============================================================
# ZAHLEN
# ============================================================

def press_number(number):

    vibrate()

    if st.session_state.display == "Fehler":
        st.session_state.display = "0"

    if st.session_state.waiting:

        st.session_state.display = number
        st.session_state.waiting = False

    elif st.session_state.display == "0":

        st.session_state.display = number

    else:

        st.session_state.display += number


# ============================================================
# KOMMA
# ============================================================

def press_decimal():

    vibrate()

    if st.session_state.waiting:

        st.session_state.display = "0,"
        st.session_state.waiting = False

    elif "," not in st.session_state.display:

        st.session_state.display += ","


# ============================================================
# ZAHL UMWANDELN
# ============================================================

def current_number():

    try:
        return float(
            st.session_state.display.replace(",", ".")
        )
    except:
        return 0.0


# ============================================================
# ZAHL FORMATIEREN
# ============================================================

def format_number(number):

    if number == 0:
        return "0"

    if number.is_integer():
        return str(int(number))

    text = f"{number:.10f}"

    text = text.rstrip("0").rstrip(".")

    return text.replace(".", ",")


# ============================================================
# OPERATOR
# ============================================================

def press_operator(operator):

    vibrate()

    current = current_number()

    if (
        st.session_state.stored_number is not None
        and st.session_state.operator is not None
        and not st.session_state.waiting
    ):
        calculate()

        current = current_number()

    st.session_state.stored_number = current
    st.session_state.operator = operator
    st.session_state.waiting = True


# ============================================================
# BERECHNEN
# ============================================================

def calculate():

    vibrate()

    if (
        st.session_state.stored_number is None
        or st.session_state.operator is None
    ):
        return

    first = st.session_state.stored_number
    second = current_number()
    operator = st.session_state.operator

    try:

        if operator == "+":
            result = first + second

        elif operator == "−":
            result = first - second

        elif operator == "×":
            result = first * second

        elif operator == "÷":

            if second == 0:

                st.session_state.display = "Fehler"

                st.session_state.stored_number = None
                st.session_state.operator = None
                st.session_state.waiting = True

                return

            result = first / second

        else:
            return

        st.session_state.display = format_number(result)

        st.session_state.stored_number = None
        st.session_state.operator = None
        st.session_state.waiting = True

    except:

        st.session_state.display = "Fehler"

        st.session_state.stored_number = None
        st.session_state.operator = None
        st.session_state.waiting = True


# ============================================================
# AC
# ============================================================

def clear():

    vibrate()

    st.session_state.display = "0"
    st.session_state.stored_number = None
    st.session_state.operator = None
    st.session_state.waiting = False


# ============================================================
# VORZEICHEN
# ============================================================

def change_sign():

    vibrate()

    if st.session_state.display == "0":
        return

    if st.session_state.display == "Fehler":
        clear()
        return

    if st.session_state.display.startswith("-"):

        st.session_state.display = (
            st.session_state.display[1:]
        )

    else:

        st.session_state.display = (
            "-" + st.session_state.display
        )


# ============================================================
# PROZENT
# ============================================================

def percent():

    vibrate()

    if st.session_state.display == "Fehler":
        return

    value = current_number()

    value = value / 100

    st.session_state.display = format_number(value)


# ============================================================
# CSS
# ============================================================

st.markdown(
    """
    <style>

    /* ======================================================
       GESAMTE SEITE
       ====================================================== */

    html,
    body,
    [data-testid="stAppViewContainer"] {

        background-color: #000000 !important;

    }

    [data-testid="stHeader"] {

        background-color: #000000 !important;

    }

    .main {

        background-color: #000000 !important;

    }

    .block-container {

        max-width: 430px !important;

        padding-top: 20px !important;

        padding-left: 10px !important;

        padding-right: 10px !important;

        padding-bottom: 30px !important;

    }


    /* ======================================================
       DISPLAY
       ====================================================== */

    .calculator-display {

        height: 170px;

        display: flex;

        align-items: flex-end;

        justify-content: flex-end;

        padding: 0 18px 15px 18px;

        box-sizing: border-box;

        color: #ffffff;

        background: #000000;

        font-family:

            -apple-system,

            BlinkMacSystemFont,

            "Helvetica Neue",

            Arial,

            sans-serif;

        font-size: 72px;

        font-weight: 300;

        letter-spacing: -3px;

        white-space: nowrap;

        overflow: hidden;

        text-overflow: ellipsis;

    }


    /* ======================================================
       BUTTON GRID
       ====================================================== */

    [data-testid="column"] {

        padding: 4px !important;

    }


    /* ======================================================
       ALLE BUTTONS
       ====================================================== */

    div.stButton > button {

        width: 100% !important;

        height: 82px !important;

        min-height: 82px !important;

        border: 0 !important;

        border-radius: 50% !important;

        padding: 0 !important;

        margin: 0 !important;

        font-family:

            -apple-system,

            BlinkMacSystemFont,

            "Helvetica Neue",

            Arial,

            sans-serif !important;

        font-size: 28px !important;

        font-weight: 400 !important;

        transition:

            transform 0.07s ease,

            filter 0.07s ease !important;

        box-shadow: none !important;

    }


    /* ======================================================
       BUTTON DRÜCKEN
       ====================================================== */

    div.stButton > button:active {

        transform: scale(0.88) !important;

        filter: brightness(1.35) !important;

    }


    /* ======================================================
       ZAHLEN
       ====================================================== */

    div.stButton > button[kind="secondary"] {

        background-color: #333333 !important;

        color: #ffffff !important;

    }


    div.stButton > button[kind="secondary"]:hover {

        background-color: #4a4a4a !important;

        color: #ffffff !important;

    }


    /* ======================================================
       ORANGE OPERATOR-TASTEN
       ====================================================== */

    div.stButton > button[kind="primary"] {

        background-color: #ff9500 !important;

        color: #ffffff !important;

    }


    div.stButton > button[kind="primary"]:hover {

        background-color: #ffad33 !important;

        color: #ffffff !important;

    }


    /* ======================================================
       ERSTE REIHE - FUNKTIONEN
       ====================================================== */

    .function-button button {

        background-color: #a5a5a5 !important;

        color: #000000 !important;

    }


    /* ======================================================
       MOBILE
       ====================================================== */

    @media (max-width: 500px) {

        .block-container {

            padding-left: 7px !important;

            padding-right: 7px !important;

            padding-top: 10px !important;

        }

        .calculator-display {

            height: 145px;

            font-size: 58px;

        }

        div.stButton > button {

            height: 70px !important;

            min-height: 70px !important;

            font-size: 25px !important;

        }

    }

    </style>
    """,
    unsafe_allow_html=True,
)


# ============================================================
# DISPLAY
# ============================================================

st.markdown(
    f"""
    <div class="calculator-display">
        {st.session_state.display}
    </div>
    """,
    unsafe_allow_html=True,
)


# ============================================================
# REIHE 1
# ============================================================

col1, col2, col3, col4 = st.columns(4)

with col1:

    if st.button(
        "AC",
        key="ac",
        use_container_width=True,
    ):
        clear()

with col2:

    if st.button(
        "+/−",
        key="plusminus",
        use_container_width=True,
    ):
        change_sign()

with col3:

    if st.button(
        "%",
        key="percent",
        use_container_width=True,
    ):
        percent()

with col4:

    if st.button(
        "÷",
        key="divide",
        type="primary",
        use_container_width=True,
    ):
        press_operator("÷")


# ============================================================
# REIHE 2
# ============================================================

col1, col2, col3, col4 = st.columns(4)

with col1:

    if st.button(
        "7",
        key="seven",
        use_container_width=True,
    ):
        press_number("7")

with col2:

    if st.button(
        "8",
        key="eight",
        use_container_width=True,
    ):
        press_number("8")

with col3:

    if st.button(
        "9",
        key="nine",
        use_container_width=True,
    ):
        press_number("9")

with col4:

    if st.button(
        "×",
        key="multiply",
        type="primary",
        use_container_width=True,
    ):
        press_operator("×")


# ============================================================
# REIHE 3
# ============================================================

col1, col2, col3, col4 = st.columns(4)

with col1:

    if st.button(
        "4",
        key="four",
        use_container_width=True,
    ):
        press_number("4")

with col2:

    if st.button(
        "5",
        key="five",
        use_container_width=True,
    ):
        press_number("5")

with col3:

    if st.button(
        "6",
        key="six",
        use_container_width=True,
    ):
        press_number("6")

with col4:

    if st.button(
        "−",
        key="minus",
        type="primary",
        use_container_width=True,
    ):
        press_operator("−")


# ============================================================
# REIHE 4
# ============================================================

col1, col2, col3, col4 = st.columns(4)

with col1:

    if st.button(
        "1",
        key="one",
        use_container_width=True,
    ):
        press_number("1")

with col2:

    if st.button(
        "2",
        key="two",
        use_container_width=True,
    ):
        press_number("2")

with col3:

    if st.button(
        "3",
        key="three",
        use_container_width=True,
    ):
        press_number("3")

with col4:

    if st.button(
        "+",
        key="plus",
        type="primary",
        use_container_width=True,
    ):
        press_operator("+")


# ============================================================
# REIHE 5
# ============================================================

col1, col2, col3, col4 = st.columns(4)

with col1:

    if st.button(
        "0",
        key="zero",
        use_container_width=True,
    ):
        press_number("0")

with col2:

    if st.button(
        ",",
        key="decimal",
        use_container_width=True,
    ):
        press_decimal()

with col3:
    pass

with col4:

    if st.button(
        "=",
        key="equals",
        type="primary",
        use_container_width=True,
    ):
        calculate()
