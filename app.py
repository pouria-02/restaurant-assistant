import streamlit as st
from langchain_google_genai import ChatGoogleGenerativeAI
from langchain_core.messages import HumanMessage
import os

# API Key
api_key = os.environ.get("GOOGLE_API_KEY")

# مدل Google Gemini
MODEL_NAME = "gemini-2.0-flash-exp"
llm = ChatGoogleGenerativeAI(model=MODEL_NAME, api_key=api_key)

# منوی نمونه با دسته‌بندی و عکس
menu = {
    "فست فود": {
        "پیتزا مارگاریتا": {
            "desc": "خمیر نازک، سس گوجه‌فرنگی، پنیر موتزارلا، ریحان تازه",
            #"img": "margharita.jpeg"
        },
        "پیتزا پپرونی": {
            "desc": "خمیر نازک، سس گوجه‌فرنگی، پنیر موتزارلا، پپرونی",
            "img": "https://pizzamaruusa.com/wp-content/uploads/2016/01/Pepperoni-Pizza.jpg"
        },
        "برگر کلاسیک": {
            "desc": "گوشت گوساله، نان برگر، پنیر چدار، کاهو، گوجه، سس مخصوص",
            #"img": "burger.jpg"
        },
    },
    "صبحانه": {
        "املت سبزیجات": {
            "desc": "تخم مرغ، فلفل دلمه‌ای، گوجه، سبزیجات تازه",
            #"img": "omelette.jpg"
        },
        "پنکیک با عسل": {
            "desc": "آرد، شیر، تخم مرغ، عسل، کره",
            #"img": "pancake.jpg"
        },
    },
    "قهوه": {
        "کاپوچینو": {
            "desc": "اسپرسو، شیر کف دار، شکلات پودر",
            #"img": "cappuccino.jpg"
        },
        "لاته": {
            "desc": "اسپرسو، شیر بخار داده شده",
            #"img": "latte.jpg"
        },
    },
    "پیش غذا": {
        "سالاد سزار": {
            "desc": "کاهو رومی، مرغ گریل‌شده، پنیر پارمزان، کروتون، سس سزار",
            #"img": "caesar.jpg"
        },
        "سالاد یونانی": {
            "desc": "کاهو، گوجه، خیار، زیتون، پنیر فتا، روغن زیتون",
            #"img": "greek.jpg"
        },
    }
}

# دستیار رستوران
def restaurant_assistant(question):
    system_prompt = (
        "تو یه دستیار رستوران هستی و با لحنی صمیمی با مشتری‌ها صحبت می‌کنی. "
        "فقط درباره‌ی غذاهای منوی زیر جواب بده. "
        "اگر سوال ربطی به منو یا مواد تشکیل‌دهنده‌ی غذاها نداشت، با خوشرویی بگو: "
        "«من فقط درباره‌ی منو می‌تونم کمکت کنم :)»\n\n"
        "اگر کاربر درباره‌ی مواد تشکیل‌دهنده‌ی هر غذا پرسید، "
        "با لحن دوستانه درباره اون ماده توضیح بده، خواصش رو بگو و اگر قابل درست کردن در خونه هست، "
        "به طور خلاصه روش تهیه‌ش رو هم بگو.\n\n"
        f"منو:\n{menu}"
    )
    msg = [HumanMessage(content=f"{system_prompt}\n\nسؤال مشتری: {question}")]
    response = llm.invoke(msg)
    return response.content

# ===== CSS برای واکنش‌گرایی و زیبایی =====
st.markdown("""
<style>
div.block-container {
    padding: 2rem 3rem;
    max-width: 95%;
}
.food-card {
    display: flex;
    align-items: center;
    margin-bottom: 15px;
    padding: 10px;
    border-bottom: 1px solid #ddd;
    border-radius: 8px;
}
.food-img {
    width: 100px;
    height: 100px;
    border-radius: 10px;
    margin-right: 15px;
    object-fit: cover;
    box-shadow: 0 4px 8px rgba(0,0,0,0.2);
}
.food-info {
    flex-grow: 1;
}
.food-name {
    color: #ff6600;
    font-size: 18px;
    font-weight: bold;
}
.food-ingredients {
    font-size: 14px;
    color: #444;
}
</style>
""", unsafe_allow_html=True)

# ===== UI =====
st.markdown("<h1 style='text-align: center; color: #ff6600;'>🍽️ منوی رستوران نمونه</h1>", unsafe_allow_html=True)

# Tabs برای دسته‌ها
tabs = st.tabs(list(menu.keys()))

for i, category in enumerate(menu.keys()):
    with tabs[i]:
        st.subheader(f"📋 {category}")
        for dish, info in menu[category].items():
            st.markdown(f"""
            <div class='food-card'>
                <img src='{info["img"]}' class='food-img'>
                <div class='food-info'>
                    <div class='food-name'>{dish}</div>
                    <div class='food-ingredients'>{info["desc"]}</div>
                </div>
            </div>
            """, unsafe_allow_html=True)

# سوال و جواب AI
st.markdown("---")
st.subheader("💬 بپرس از دستیار رستوران!")
question = st.text_input("سؤال خود را بنویس یا بپرس:")
if question:
    answer = restaurant_assistant(question)
    st.markdown(
        f"""
        <div style='background-color: white; color: black; padding: 15px; border-radius: 10px; font-size:15px;'>
            <strong>🍳 پاسخ دستیار:</strong><br>{answer}
        </div>
        """,
        unsafe_allow_html=True
    )
