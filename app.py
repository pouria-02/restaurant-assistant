# app.py
import streamlit as st
from langchain_google_genai import ChatGoogleGenerativeAI
from langchain_core.messages import HumanMessage
import os
import socket
import qrcode
from PIL import Image
from io import BytesIO

# -----------------------
# 🧠 تنظیمات API
# -----------------------
os.environ["GOOGLE_API_KEY"] = "AIzaSyCU2qgTdtZrzUXHWwO4vpXpCSefftxcdiA"  # 🔹 اینجا کلید Gemini API رو بذار
MODEL_NAME = "gemini-2.0-flash-exp"
llm = ChatGoogleGenerativeAI(model=MODEL_NAME)

# -----------------------
# 🍽️ منوی رستوران
# -----------------------
menu = {
    "پیتزا مارگاریتا": "خمیر نازک، سس گوجه‌فرنگی، پنیر موتزارلا، ریحان تازه",
    "برگر کلاسیک": "گوشت گوساله، نان برگر، پنیر چدار، کاهو، گوجه، سس مخصوص",
    "سالاد سزار": "کاهو رومی، مرغ گریل‌شده، پنیر پارمزان، کروتون، سس سزار",
    "پاستا آلفردو": "پاستا، سس خامه‌ای، مرغ، قارچ، پنیر پارمزان",
}

# -----------------------
# 💬 تابع پاسخ‌دهنده
# -----------------------
def restaurant_assistant(question):
    system_prompt = (
        "تو یک دستیار رستوران هستی و فقط درباره‌ی غذاهای منوی زیر پاسخ می‌دهی. "
        "اگر کاربر درباره‌ی یک غذا سؤال پرسید، فقط مواد تشکیل‌دهنده آن را بگو. "
        "اگر درباره‌ی مواد تشکیل‌دهنده سؤال پرسید، خواص آن را توضیح بده و اگر قابل تهیه در خانه است، "
        "به طور خلاصه روش تهیه‌اش را هم بگو. "
        "اگر سؤال هیچ ارتباطی با منو یا مواد تشکیل‌دهنده نداشت، بگو: "
        "«لطفاً فقط درباره‌ی منو سؤال بفرمایید.»\n\n"
        f"منو:\n{menu}"
    )

    msg = [HumanMessage(content=f"{system_prompt}\n\nسؤال مشتری: {question}")]
    res = llm.invoke(msg)
    return res.content

# -----------------------
# 🌐 گرفتن IP سیستم
# -----------------------
def get_local_ip():
    try:
        s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        s.connect(("8.8.8.8", 80))
        ip = s.getsockname()[0]
        s.close()
        return ip
    except Exception:
        return "localhost"

# -----------------------
# 🎨 رابط کاربری Streamlit
# -----------------------
st.set_page_config(page_title="🍕 دستیار منوی رستوران", layout="wide")
st.title("🍽️ دستیار رستوران هوشمند")

col1, col2 = st.columns([1, 2])

with col1:
    st.subheader("📋 منوی رستوران")
    for dish, ingredients in menu.items():
        st.markdown(f"**{dish}**: {ingredients}")

with col2:
    st.subheader("💬 سوال خود را بپرسید")
    question = st.text_input("سؤال شما:")

    if question:
        with st.spinner("در حال پاسخگویی..."):
            answer = restaurant_assistant(question)
            st.success(f"🤖 پاسخ: {answer}")

# -----------------------
# 📱 QR Code و آدرس دسترسی
# -----------------------
local_ip = get_local_ip()
app_url = "https://restaurant-assistant-wne4pww28hatw2fgiqxpj8.streamlit.app/"

st.divider()
st.subheader("📱 دسترسی از گوشی یا دستگاه دیگر")

qr = qrcode.QRCode(box_size=5, border=1)
qr.add_data(app_url)
qr.make(fit=True)
img = qr.make_image(fill_color="black", back_color="white")
buf = BytesIO()
img.save(buf)
st.image(Image.open(buf), caption=f"اسکن کنید یا آدرس زیر را باز کنید:\n{app_url}")
