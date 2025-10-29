import streamlit as st
from langchain_google_genai import ChatGoogleGenerativeAI
from langchain_core.messages import HumanMessage
import os

# گرفتن API Key از Secret
api_key = os.environ.get("GOOGLE_API_KEY")

# Google Gemini
MODEL_NAME = "gemini-2.0-flash-exp"
llm = ChatGoogleGenerativeAI(model=MODEL_NAME, api_key=api_key)

# منوی نمونه
menu = {
    "پیتزا مارگاریتا": "خمیر نازک، سس گوجه‌فرنگی، پنیر موتزارلا، ریحان تازه",
    "برگر کلاسیک": "گوشت گوساله، نان برگر، پنیر چدار، کاهو، گوجه، سس مخصوص",
    "سالاد سزار": "کاهو رومی، مرغ گریل‌شده، پنیر پارمزان، کروتون، سس سزار",
    "پاستا آلفردو": "پاستا، سس خامه‌ای، مرغ، قارچ، پنیر پارمزان",
}

# تابع دستیار رستوران
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

# ===== UI مرتب =====
st.title("🍽️ دستیار رستوران")

# ستون‌ها: چپ منو، راست سوال و جواب
col1, col2 = st.columns([2, 3])

with col1:
    st.subheader("📋 منو رستوران")
    with st.expander("نمایش منو"):
        for dish, ingredients in menu.items():
            st.write(f"**{dish}**: {ingredients}")

with col2:
    st.subheader("💬 پرسش و پاسخ")
    question = st.text_input("سوال خود را بپرسید:")
    if question:
        answer = restaurant_assistant(question)
        st.markdown(f"**پاسخ دستیار:**\n\n{answer}")
