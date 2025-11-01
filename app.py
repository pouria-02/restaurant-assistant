import streamlit as st
from langchain_google_genai import ChatGoogleGenerativeAI
from langchain_core.messages import HumanMessage
import os

# === API Key ===
api_key = os.environ.get("GOOGLE_API_KEY")
MODEL_NAME = "gemini-2.0-flash-exp"
llm = ChatGoogleGenerativeAI(model=MODEL_NAME, api_key=api_key)

# === Menu Data ===
menu = {
    "فست فود 🍔": {
        "پیتزا مارگاریتا": {"desc": "خمیر نازک، سس گوجه، پنیر موتزارلا، ریحان تازه", "price": "۲۴۰٬۰۰۰ تومان"},
        "پیتزا پپرونی": {"desc": "پپرونی تند، پنیر موتزارلا و خمیر نازک", "price": "۲۶۰٬۰۰۰ تومان"},
        "برگر کلاسیک": {"desc": "گوشت گوساله، نان کنجدی، سس مخصوص", "price": "۱۸۰٬۰۰۰ تومان"},
    },
    "صبحانه 🍳": {
        "املت سبزیجات": {"desc": "تخم‌مرغ، گوجه، فلفل دلمه‌ای، سبزیجات تازه", "price": "۱۳۰٬۰۰۰ تومان"},
        "پنکیک با عسل": {"desc": "پنکیک نرم با عسل طبیعی و کره", "price": "۱۵۰٬۰۰۰ تومان"},
    },
    "قهوه ☕": {
        "لاته": {"desc": "اسپرسو با شیر بخار داده‌شده", "price": "۸۰٬۰۰۰ تومان"},
        "کاپوچینو": {"desc": "اسپرسو، شیر کف‌دار و شکلات پودر", "price": "۹۰٬۰۰۰ تومان"},
    },
    "پیش‌غذا 🥗": {
        "سالاد سزار": {"desc": "کاهو رومی، مرغ گریل‌شده، سس مخصوص", "price": "۱۶۰٬۰۰۰ تومان"},
        "سالاد یونانی": {"desc": "کاهو، گوجه، خیار، زیتون و پنیر فتا", "price": "۱۴۰٬۰۰۰ تومان"},
    },
}

# === Chat Assistant ===
def restaurant_assistant(question):
    system_prompt = (
        "تو یه دستیار رستوران هستی و با لحنی صمیمی با مشتری‌ها صحبت می‌کنی. "
        "فقط درباره‌ی غذاهای منوی زیر جواب بده و اگر سوال بی‌ربط بود، بگو: "
        "«من فقط درباره‌ی منو می‌تونم کمکت کنم 🙂»\n\n"
        f"منو:\n{menu}"
    )
    msg = [HumanMessage(content=f"{system_prompt}\n\nسؤال مشتری: {question}")]
    response = llm.invoke(msg)
    return response.content

# === Page Config ===
st.set_page_config(page_title="منوی رستوران", page_icon="🍽️", layout="wide")

# === Custom CSS ===
st.markdown("""
<style>
@import url('https://cdn.fontcdn.ir/Font/Persian/Vazir/Vazir.css');

html, body, [class*="css"] {
    font-family: 'Vazir', sans-serif !important;
    background-color: #fffaf3;
    direction: rtl;
}

h1, h2, h3, h4 {
    color: #ff6600;
}

.menu-card {
    background-color: #fff;
    border-radius: 15px;
    box-shadow: 0 4px 12px rgba(0,0,0,0.1);
    padding: 20px;
    text-align: right;
    transition: 0.3s;
}
.menu-card:hover {
    transform: translateY(-4px);
    box-shadow: 0 6px 18px rgba(0,0,0,0.15);
}
.menu-img {
    width: 100%;
    border-radius: 12px;
    margin-bottom: 10px;
}
.price {
    color: #ff6600;
    font-weight: bold;
}
.select-btn {
    background-color: #ff6600;
    color: white;
    border: none;
    border-radius: 8px;
    padding: 6px 14px;
    cursor: pointer;
}
.select-btn:hover {
    background-color: #e65c00;
}
.chat-btn {
    position: fixed;
    bottom: 25px;
    left: 25px;
    background-color: #ff6600;
    color: white;
    border: none;
    border-radius: 50%;
    width: 60px;
    height: 60px;
    font-size: 26px;
    box-shadow: 0 4px 12px rgba(0,0,0,0.3);
    cursor: pointer;
    transition: 0.3s;
}
.chat-btn:hover {
    background-color: #e65c00;
    transform: scale(1.1);
}
.chat-popup {
    position: fixed;
    bottom: 100px;
    left: 25px;
    width: 340px;
    background-color: #fff;
    border-radius: 10px;
    box-shadow: 0 4px 16px rgba(0,0,0,0.25);
    display: flex;
    flex-direction: column;
    z-index: 9999;
}
.chat-header {
    background-color: #ff6600;
    color: white;
    padding: 10px;
    border-radius: 10px 10px 0 0;
    text-align: center;
    font-weight: bold;
}
.chat-body {
    padding: 10px;
    height: 300px;
    overflow-y: auto;
    font-size: 14px;
}
.chat-input {
    display: flex;
    border-top: 1px solid #ddd;
}
.chat-input input {
    flex: 1;
    padding: 8px;
    border: none;
    border-radius: 0 0 0 10px;
}
.chat-input button {
    background-color: #ff6600;
    border: none;
    color: white;
    padding: 8px 12px;
    border-radius: 0 0 10px 0;
    cursor: pointer;
}
</style>
""", unsafe_allow_html=True)

# === Main Title ===
st.markdown("<h1 style='text-align:center;'>🍽️ منوی رستوران نمونه</h1>", unsafe_allow_html=True)

# === Tabs ===
tabs = st.tabs(list(menu.keys()))
image_url = "https://raw.githubusercontent.com/pouria-02/restaurant-assistant/main/latte.jpg"

for i, category in enumerate(menu.keys()):
    with tabs[i]:
        cols = st.columns(3)
        dishes = list(menu[category].items())
        for j, (dish, info) in enumerate(dishes):
            with cols[j % 3]:
                st.markdown(f"""
                <div class='menu-card'>
                    <img src='{image_url}' class='menu-img'>
                    <h4>{dish}</h4>
                    <p>{info['desc']}</p>
                    <p class='price'>{info['price']}</p>
                    <button class='select-btn'>انتخاب</button>
                </div>
                """, unsafe_allow_html=True)

# === Floating Chatbot ===
if "chat_open" not in st.session_state:
    st.session_state.chat_open = False

chat_toggle = st.button("💬", key="chat_btn", help="چت با دستیار", use_container_width=False)

if chat_toggle:
    st.session_state.chat_open = not st.session_state.chat_open

if st.session_state.chat_open:
    st.markdown("""
    <div class='chat-popup'>
        <div class='chat-header'>🤖 گفت‌وگو با دستیار</div>
        <div class='chat-body' id='chat-body'>
            <p>سلام! درباره‌ی منو هر سوالی داری بپرس 😄</p>
        </div>
    </div>
    """, unsafe_allow_html=True)

    user_message = st.text_input("پیام شما:", key="user_input")
    if st.button("ارسال", key="send_msg"):
        if user_message.strip():
            answer = restaurant_assistant(user_message)
            st.markdown(f"""
            <div class='chat-popup'>
                <div class='chat-header'>🤖 پاسخ دستیار</div>
                <div class='chat-body'>{answer}</div>
            </div>
            """, unsafe_allow_html=True)
