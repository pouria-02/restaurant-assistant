import streamlit as st
from langchain_google_genai import ChatGoogleGenerativeAI
from langchain_core.messages import HumanMessage
import os

# ====== Google Gemini Setup ======
api_key = os.environ.get("GOOGLE_API_KEY")
MODEL_NAME = "gemini-2.0-flash-exp"
llm = ChatGoogleGenerativeAI(model=MODEL_NAME, api_key=api_key)

# ====== Sample Menu ======
menu = {
    "فست فود": {
        "پیتزا مارگاریتا": {"desc": "خمیر نازک، سس گوجه‌فرنگی، پنیر موتزارلا، ریحان تازه"},
        "پیتزا پپرونی": {"desc": "خمیر نازک، سس گوجه‌فرنگی، پنیر موتزارلا، پپرونی"},
        "برگر کلاسیک": {"desc": "گوشت گوساله، نان برگر، پنیر چدار، کاهو، گوجه، سس مخصوص"},
    },
    "صبحانه": {
        "املت سبزیجات": {"desc": "تخم مرغ، فلفل دلمه‌ای، گوجه، سبزیجات تازه"},
        "پنکیک با عسل": {"desc": "آرد، شیر، تخم مرغ، عسل، کره"},
    },
    "قهوه": {
        "کاپوچینو": {"desc": "اسپرسو، شیر کف دار، شکلات پودر"},
        "لاته": {"desc": "اسپرسو، شیر بخار داده شده"},
    },
    "پیش غذا": {
        "سالاد سزار": {"desc": "کاهو رومی، مرغ گریل‌شده، پنیر پارمزان، کروتون، سس سزار"},
        "سالاد یونانی": {"desc": "کاهو، گوجه، خیار، زیتون، پنیر فتا، روغن زیتون"},
    },
}

img_url = "https://raw.githubusercontent.com/pouria-02/restaurant-assistant/main/latte.jpg"

# ====== Chatbot ======
def restaurant_assistant(question):
    system_prompt = (
        "تو یه دستیار رستوران هستی و با لحنی صمیمی با مشتری‌ها صحبت می‌کنی. "
        "فقط درباره‌ی غذاهای منوی زیر جواب بده. "
        "اگر سوال ربطی به منو یا مواد تشکیل‌دهنده‌ی غذاها نداشت، با خوشرویی بگو: "
        "«من فقط درباره‌ی منو می‌تونم کمکت کنم :)»\n\n"
        f"منو:\n{menu}"
    )
    msg = [HumanMessage(content=f"{system_prompt}\n\nسؤال مشتری: {question}")]
    response = llm.invoke(msg)
    return response.content


# ====== CSS ======
st.markdown("""
<style>
body {
    background-color: #f3e7cf;
    font-family: "IRANSans", sans-serif;
}
div.block-container {
    padding: 2rem;
    max-width: 900px;
}
h1, h2, h3, h4 {
    font-family: "IRANSans", sans-serif;
}
.category-bar {
    display: flex;
    overflow-x: auto;
    gap: 10px;
    padding: 10px 0;
}
.category-button {
    background-color: white;
    color: black;
    padding: 10px 20px;
    border-radius: 20px;
    border: 2px solid #ddd;
    font-weight: bold;
    white-space: nowrap;
    cursor: pointer;
    transition: all 0.3s;
}
.category-button:hover {
    background-color: #ff6600;
    color: white;
}
.food-card {
    display: flex;
    align-items: center;
    background-color: #fff;
    border-radius: 15px;
    padding: 10px;
    margin-bottom: 15px;
    box-shadow: 0 3px 8px rgba(0,0,0,0.1);
}
.food-img {
    width: 90px;
    height: 90px;
    border-radius: 10px;
    margin-left: 15px;
    object-fit: cover;
}
.food-info {
    flex: 1;
}
.food-name {
    font-weight: bold;
    font-size: 16px;
}
.food-desc {
    color: #666;
    font-size: 14px;
    margin-bottom: 6px;
}
.food-price {
    color: #00aa55;
    font-weight: bold;
}
.select-btn {
    background-color: #fff;
    border: 1px solid #00aa55;
    color: #00aa55;
    border-radius: 8px;
    padding: 4px 10px;
    cursor: pointer;
    transition: 0.3s;
}
.select-btn:hover {
    background-color: #00aa55;
    color: white;
}
</style>
""", unsafe_allow_html=True)


# ====== UI ======
st.markdown("<h1 style='text-align:center;color:#ff6600;'>🍽️ منوی رستوران</h1>", unsafe_allow_html=True)

# Category bar
selected_category = st.selectbox("📋 لیست دسته‌بندی‌ها:", ["همه"] + list(menu.keys()))

# Horizontal category buttons
st.markdown("<div class='category-bar'>", unsafe_allow_html=True)
for cat in menu.keys():
    if st.button(cat):
        selected_category = cat
st.markdown("</div>", unsafe_allow_html=True)

# Menu display
categories = list(menu.keys()) if selected_category == "همه" else [selected_category]
for cat in categories:
    st.markdown(f"<h3 style='color:#ff6600;margin-top:20px;'>🍴 {cat}</h3>", unsafe_allow_html=True)
    for dish, info in menu[cat].items():
        st.markdown(f"""
        <div class='food-card'>
            <img src='{img_url}' class='food-img'>
            <div class='food-info'>
                <div class='food-name'>{dish}</div>
                <div class='food-desc'>{info["desc"]}</div>
                <div style='display:flex;justify-content:space-between;align-items:center;'>
                    <span class='food-price'>۱۹۸,۸۰۰ تومان</span>
                    <button class='select-btn'>انتخاب</button>
                </div>
            </div>
        </div>
        """, unsafe_allow_html=True)

# Chatbot input
st.markdown("---")
st.subheader("💬 گفت‌وگو با دستیار منو")

question = st.text_input("سؤال خود را بنویس:")
if st.button("ارسال"):
    if question.strip():
        answer = restaurant_assistant(question)
        st.markdown(
            f"<div style='background-color:#fff;padding:15px;border-radius:10px;'>{answer}</div>",
            unsafe_allow_html=True
        )
