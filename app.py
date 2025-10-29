import streamlit as st
from langchain_google_genai import ChatGoogleGenerativeAI
from langchain_core.messages import HumanMessage
import os
from tempfile import NamedTemporaryFile
import openai
import soundfile as sf

# API Key ها
api_key = os.environ.get("GOOGLE_API_KEY")
openai_api_key = os.environ.get("OPENAI_API_KEY")  # برای Whisper

# مدل Google Gemini
MODEL_NAME = "gemini-2.0-flash-exp"
llm = ChatGoogleGenerativeAI(model=MODEL_NAME, api_key=api_key)

# منوی نمونه
menu = {
    "فست فود": {"پیتزا مارگاریتا": "خمیر نازک، سس گوجه، پنیر موتزارلا، ریحان"},
    "صبحانه": {"املت سبزیجات": "تخم مرغ، سبزیجات تازه، فلفل دلمه‌ای"},
    "قهوه": {"کاپوچینو": "اسپرسو، شیر کف دار، شکلات پودر"},
}

# دستیار رستوران
def restaurant_assistant(question):
    system_prompt = (
        "تو یه دستیار رستوران هستی و با لحنی صمیمی جواب بده. "
        "فقط درباره‌ی غذاهای منو جواب بده. "
        "اگر سوال نامرتبط بود بگو: «من فقط درباره‌ی منو می‌تونم کمکت کنم :)»\n\n"
        "اگر کاربر درباره‌ی مواد تشکیل‌دهنده‌ی هر غذا پرسید، خواص و نحوه تهیه کوتاه توضیح بده.\n\n"
        f"منو:\n{menu}"
    )
    msg = [HumanMessage(content=f"{system_prompt}\n\nسؤال مشتری: {question}")]
    response = llm.invoke(msg)
    return response.content

st.title("🍽️ دستیار رستوران با ویس")
st.subheader("منو")
for cat, items in menu.items():
    st.markdown(f"**{cat}:**")
    for dish, ing in items.items():
        st.markdown(f"- {dish}: {ing}")

# ---- ورودی متن ----
st.markdown("---")
st.subheader("💬 سوال با متن")
text_question = st.text_input("سوال خود را بپرسید:")
if text_question:
    answer = restaurant_assistant(text_question)
    st.markdown(f"<div style='background-color:white;color:black;padding:10px;border-radius:10px;'>{answer}</div>", unsafe_allow_html=True)

# ---- ورودی صوتی ----
st.markdown("---")
st.subheader("🎤 سوال با ویس")
audio_file = st.file_uploader("ویس خود را آپلود کنید (wav)", type=["wav"])
if audio_file is not None:
    with NamedTemporaryFile(delete=False, suffix=".wav") as tmp_file:
        tmp_file.write(audio_file.read())
        tmp_file_path = tmp_file.name

    # تبدیل صدا به متن با Whisper
    with open(tmp_file_path, "rb") as f:
        transcript = openai.Audio.transcriptions.create(
            file=f,
            model="whisper-1",
            api_key=openai_api_key
        ).text

    st.markdown(f"**متن تبدیل شده:** {transcript}")
    answer = restaurant_assistant(transcript)
    st.markdown(f"<div style='background-color:white;color:black;padding:10px;border-radius:10px;'>{answer}</div>", unsafe_allow_html=True)
