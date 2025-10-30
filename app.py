import streamlit as st
from langchain_google_genai import ChatGoogleGenerativeAI
from langchain_core.messages import HumanMessage
import os
from streamlit_webrtc import webrtc_streamer, AudioProcessorBase, WebRtcMode

import tempfile
import speech_recognition as sr

# API Key
api_key = os.environ.get("GOOGLE_API_KEY")

# مدل Google Gemini
MODEL_NAME = "gemini-2.0-flash-exp"
llm = ChatGoogleGenerativeAI(model=MODEL_NAME, api_key=api_key)

# منوی نمونه با دسته‌بندی و عکس (همون قبلی)
menu = { ... }  # از کد قبلی استفاده کن

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

# ===== UI =====
st.markdown("<h1 style='text-align: center; color: #ff6600;'>🍽️ منوی رستوران نمونه</h1>", unsafe_allow_html=True)

# نمایش منو
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

st.markdown("---")
st.subheader("💬 بپرس از دستیار رستوران!")

# ورودی متن
with st.form("chat_form"):
    text_question = st.text_input("سوال خود را بنویس یا بپرس:")
    submit_button = st.form_submit_button("ارسال")
    if submit_button and text_question.strip() != "":
        answer = restaurant_assistant(text_question)
        st.markdown(f"<div style='background-color: white; color: black; padding: 15px; border-radius: 10px;'>{answer}</div>", unsafe_allow_html=True)

st.markdown("🎤 یا میکروفون خود را استفاده کنید:")

# ضبط صوتی
webrtc_ctx = webrtc_streamer(
    key="speech-input",
    mode=WebRtcMode.SENDONLY,
    audio_receiver_size=1024,
)

if webrtc_ctx.audio_receiver:
    audio_frames = webrtc_ctx.audio_receiver.get_frames(timeout=1)
    if audio_frames:
        # ذخیره به فایل موقت
        with tempfile.NamedTemporaryFile(suffix=".wav", delete=False) as tmp_file:
            tmp_file_path = tmp_file.name
            audio_frames[0].to_file(tmp_file_path)  # اولین فریم را ذخیره می‌کنیم

        # تبدیل صوت به متن
        r = sr.Recognizer()
        with sr.AudioFile(tmp_file_path) as source:
            audio_data = r.record(source)
            try:
                voice_text = r.recognize_google(audio_data, language="fa-IR")
                st.markdown(f"**🗣️ شما گفتید:** {voice_text}")
                answer = restaurant_assistant(voice_text)
                st.markdown(f"<div style='background-color: white; color: black; padding: 15px; border-radius: 10px;'>{answer}</div>", unsafe_allow_html=True)
            except:
                st.warning("صدای شما قابل تشخیص نیست. لطفاً دوباره صحبت کنید.")
