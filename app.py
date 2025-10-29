import streamlit as st
from langchain_google_genai import ChatGoogleGenerativeAI
from langchain_core.messages import HumanMessage
import os

# API Key
api_key = os.environ.get("GOOGLE_API_KEY")

# مدل Google Gemini
MODEL_NAME = "gemini-2.0-flash-exp"
llm = ChatGoogleGenerativeAI(model=MODEL_NAME, api_key=api_key)

# منوی نمونه با دسته‌بندی
menu = {
    "فست فود": {
        "پیتزا مارگاریتا": "خمیر نازک، سس گوجه‌فرنگی، پنیر موتزارلا، ریحان تازه",
        "پیتزا پپرونی": "خمیر نازک، سس گوجه‌فرنگی، پنیر موتزارلا، پپرونی",
        "برگر کلاسیک": "گوشت گوساله، نان برگر، پنیر چدار، کاهو، گوجه، سس مخصوص",
    },
    "صبحانه": {
        "املت سبزیجات": "تخم مرغ، فلفل دلمه‌ای، گوجه، سبزیجات تازه",
        "پنکیک با عسل": "آرد، شیر، تخم مرغ، عسل، کره",
    },
    "قهوه": {
        "کاپوچینو": "اسپرسو، شیر کف دار، شکلات پودر",
        "لاته": "اسپرسو، شیر بخار داده شده",
    },
    "پیش غذا": {
        "سالاد سزار": "کاهو رومی، مرغ گریل‌شده، پنیر پارمزان، کروتون، سس سزار",
        "سالاد یونانی": "کاهو، گوجه، خیار، زیتون، پنیر فتا، روغن زیتون",
    }
}

# دستیار رستوران
def restaurant_assistant(question):
    system_prompt = (
        "تو یک دستیار رستوران هستی. فقط درباره‌ی غذاهای منوی زیر پاسخ بده. "
        "اگر سؤال ربطی به منو یا مواد تشکیل‌دهنده‌ی آن‌ها نداشت، بگو: "
        "«لطفا فقط درباره‌ی منو سوال بفرمایید.»\n\n"
        "اگر کاربر درباره‌ی مواد تشکیل‌دهنده‌ی هر غذا پرسید، "
        "در مورد آن ماده توضیح بده، خواصش را بگو و اگر قابل تهیه در خانه است، "
        "به طور خلاصه روش تهیه‌اش را هم توضیح بده.\n\n"
        f"منو:\n{menu}"
    )
    msg = [HumanMessage(content=f"{system_prompt}\n\nسؤال مشتری: {question}")]
    response = llm.invoke(msg)
    return response.content

# ===== CSS برای واکنش‌گرایی و فاصله =====
st.markdown("""
<style>
div.block-container {
    padding: 2rem 3rem;
    max-width: 95%;
}
h1 {
    line-height: 1.3;
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
        for dish, ingredients in menu[category].items():
            st.markdown(f"""
            <div style='padding:10px; margin-bottom:8px; border-bottom:1px solid #cccccc;'>
                <span style='color: #0066cc; font-size:16px; font-weight:bold;'>{dish}</span><br>
                <span style='font-size:14px;'>{ingredients}</span>
            </div>
            """, unsafe_allow_html=True)

# سوال و جواب AI
st.markdown("---")
st.subheader("💬 پرسش و پاسخ")
question = st.text_input("سوال خود را بپرسید:")
if question:
    answer = restaurant_assistant(question)
    st.markdown(
        f"<div style='background-color: #f0f0f0; padding: 15px; border-radius: 10px; font-size:15px;'>"
        f"**پاسخ دستیار:**<br>{answer}</div>",
        unsafe_allow_html=True
    )
