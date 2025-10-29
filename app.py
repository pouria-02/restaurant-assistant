import streamlit as st
from langchain_google_genai import ChatGoogleGenerativeAI
from langchain_core.messages import HumanMessage
import os
import streamlit.components.v1 as components
from tempfile import NamedTemporaryFile
import base64
import openai

# API Key ها
api_key = os.environ.get("GOOGLE_API_KEY")          # Google Gemini
openai_api_key = os.environ.get("OPENAI_API_KEY")   # Whisper

# مدل Google Gemini
MODEL_NAME = "gemini-2.0-flash-exp"
llm = ChatGoogleGenerativeAI(model=MODEL_NAME, api_key=api_key)

# منوی نمونه
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
        "تو یه دستیار رستوران هستی و با لحنی صمیمی جواب بده. "
        "فقط درباره‌ی غذاهای منو جواب بده. "
        "اگر سوال نامرتبط بود بگو: «من فقط درباره‌ی منو می‌تونم کمکت کنم :)»\n\n"
        "اگر کاربر درباره‌ی مواد تشکیل‌دهنده‌ی هر غذا پرسید، خواص و نحوه تهیه کوتاه توضیح بده.\n\n"
        f"منو:\n{menu}"
    )
    msg = [HumanMessage(content=f"{system_prompt}\n\nسؤال مشتری: {question}")]
    response = llm.invoke(msg)
    return response.content

# ===== CSS برای UI =====
st.markdown("""
<style>
div.block-container { padding: 2rem 3rem; max-width: 95%; }
h1 { line-height: 1.3; }
.food-card { padding:10px; margin-bottom:8px; border-bottom:1px solid #cccccc; }
.food-name { color: #0066cc; font-size:16px; font-weight:bold; }
.food-ingredients { font-size:14px; }
input[type=text] { width: 80%; display: inline-block; }
button#record-btn { display: inline-block; margin-left: 10px; padding: 8px 12px; }
</style>
""", unsafe_allow_html=True)

# ===== نمایش منو =====
st.markdown("<h1 style='text-align:center; color:#ff6600;'>🍽️ منوی رستوران نمونه</h1>", unsafe_allow_html=True)

tabs = st.tabs(list(menu.keys()))
for i, category in enumerate(menu.keys()):
    with tabs[i]:
        st.subheader(f"📋 {category}")
        for dish, ingredients in menu[category].items():
            st.markdown(f"""
            <div class='food-card'>
                <span class='food-name'>{dish}</span><br>
                <span class='food-ingredients'>{ingredients}</span>
            </div>
            """, unsafe_allow_html=True)

# ===== بخش سوال و جواب =====
st.markdown("---")
st.subheader("💬 پرسش و پاسخ")

# ورودی متن + دکمه ضبط ویس
st.markdown("""
<div>
<input id="text-input" type="text" placeholder="سوال خود را تایپ کنید..." />
<button id="record-btn">🎤 ضبط ویس</button>
</div>
""", unsafe_allow_html=True)

# HTML + JS برای ضبط ویس داخل مرورگر
components.html("""
<audio id="audio" controls></audio>
<script>
let chunks = [];
let mediaRecorder;
navigator.mediaDevices.getUserMedia({ audio: true }).then(stream => {
    mediaRecorder = new MediaRecorder(stream);
    mediaRecorder.ondataavailable = e => chunks.push(e.data);
    mediaRecorder.onstop = e => {
        let blob = new Blob(chunks, { 'type': 'audio/wav; codecs=MS_PCM' });
        let url = URL.createObjectURL(blob);
        document.getElementById('audio').src = url;
        const reader = new FileReader();
        reader.readAsDataURL(blob);
        reader.onloadend = function() {
            const base64data = reader.result;
            window.parent.postMessage({type:'audio', data: base64data}, '*');
        }
        chunks = [];
    };
});
document.getElementById('record-btn').onclick = () => mediaRecorder.start();
document.getElementById('record-btn').ondblclick = () => mediaRecorder.stop();
</script>
""", height=200)

# ===== نمایش پاسخ =====
# توجه: برای تکمیل کامل دریافت ویس از JS و پردازش در Python، باید Streamlit Custom Components یا st_js_state استفاده کرد.
# در حال حاضر، نسخه پایه با آپلود فایل wav ساده تره.
st.markdown("ℹ️ ضبط ویس مستقیماً داخل مرورگر در نسخه Streamlit Cloud نیاز به Component پیشرفته دارد. برای تست، می‌توانید از آپلود فایل wav استفاده کنید.")
