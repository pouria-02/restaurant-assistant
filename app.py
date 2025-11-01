import streamlit as st
from langchain_google_genai import ChatGoogleGenerativeAI
from langchain_core.messages import HumanMessage
import os

# --- تنظیمات اولیه و مدل Gemini (بدون تغییر) ---
# API Key
api_key = os.environ.get("GOOGLE_API_KEY")

# مدل Google Gemini
MODEL_NAME = "gemini-2.0-flash-exp"
try:
    llm = ChatGoogleGenerativeAI(model=MODEL_NAME, api_key=api_key)
except Exception:
    # در محیط محلی بدون تنظیم GOOGLE_API_KEY، این خط برای ادامه اجرای UI قرار داده می‌شود
    class MockLLM:
        def invoke(self, msg):
            return type('Response', (object,), {'content': 'من فقط درباره‌ی منو می‌تونم کمکت کنم :)'})()
    llm = MockLLM()
    
def restaurant_assistant(question):
    # ... (کد تابع restaurant_assistant بدون تغییر) ...
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

# --- منوی نمونه با ساختار شامل قیمت و سایز (بدون تغییر) ---
menu = {
    "قهوه": {
        "موکا مخصوص": {
            "size_mid": {"desc": "ترکیب دوشات اسپرسو، شکلات داغ و خامه", "price": "۱۹۸,۸۰۰", "img": "https://raw.githubusercontent.com/pouria-02/restaurant-assistant/main/capp.jpg"},
            "size_large": {"desc": "ترکیب دوشات اسپرسو، شکلات داغ و خامه", "price": "۲۲۸,۸۰۰", "img": "https://raw.githubusercontent.com/pouria-02/restaurant-assistant/main/capp.jpg"}
        },
        "کاپوچینو": {
            "size_mid": {"desc": "اسپرسو، شیر کف دار، شکلات پودر", "price": "۱۶۵,۰۰۰", "img": "https://raw.githubusercontent.com/pouria-02/restaurant-assistant/main/capp.jpg"},
        },
        "لاته": {
            "size_mid": {"desc": "اسپرسو، شیر بخار داده شده", "price": "۱۷۰,۰۰۰", "img": "https://raw.githubusercontent.com/pouria-02/restaurant-assistant/main/latte.jpg"},
        }
    },
    "فست فود": {
        "پیتزا مارگاریتا": {"mid": {"desc": "خمیر نازک، سس گوجه‌فرنگی، پنیر موتزارلا، ریحان تازه", "price": "۲۵۰,۰۰۰", "img": "https://raw.githubusercontent.com/pouria-02/restaurant-assistant/main/margharita.jpeg"}},
        "پیتزا پپرونی": {"mid": {"desc": "خمیر نازک، سس گوجه‌فرنگی، پنیر موتزارلا، پپرونی", "price": "۲۹۰,۰۰۰", "img": "https://raw.githubusercontent.com/pouria-02/restaurant-assistant/main/Pepperoni.jpg"}},
    },
    "صبحانه": {
        "املت سبزیجات": {"mid": {"desc": "تخم مرغ، فلفل دلمه‌ای، گوجه، سبزیجات تازه", "price": "۹۰,۰۰۰", "img": "https://raw.githubusercontent.com/pouria-02/restaurant-assistant/main/omellete.jpg"}},
    },
    "پیش غذا": {
        "سالاد سزار": {"mid": {"desc": "کاهو رومی، مرغ گریل‌شده، پنیر پارمزان، کروتون", "price": "۱۲۰,۰۰۰", "img": "https://raw.githubusercontent.com/pouria-02/restaurant-assistant/main/Pepperoni.jpg"}},
    }
}

# --- CSS برای استایل شبیه عکس ---
st.markdown("""
<style>
/* فونت و پس زمینه */
div.block-container {
    padding: 2rem 1rem;
    max-width: 95%;
}
.stApp {
    /* تغییر اعمال شده: رنگ کرمی ملایم */
    background-color: #FFF8E7; 
}

/* نوار دسته‌بندی افقی */
.category-bar-container {
    overflow-x: auto;
    white-space: nowrap;
    padding-bottom: 10px;
    margin-bottom: 20px;
    direction: rtl; /* برای نمایش از راست به چپ */
}

.category-button {
    display: inline-block;
    padding: 8px 15px;
    margin: 5px;
    border-radius: 20px; /* دکمه‌های گرد */
    cursor: pointer;
    font-size: 14px;
    font-weight: bold;
    text-align: center;
    color: #333;
    background-color: #e0e0e0;
    transition: background-color 0.3s, color 0.3s;
}

.category-button.selected {
    background-color: #2ECC71; /* رنگ سبز مشابه عکس */
    color: white;
    box-shadow: 0 4px 6px rgba(46, 204, 113, 0.4);
}

/* استایل آیتم منو */
.food-card-container {
    background-color: white;
    padding: 15px;
    margin-bottom: 15px;
    border-radius: 15px;
    box-shadow: 0 4px 10px rgba(0,0,0,0.05);
    display: flex;
    align-items: center;
    gap: 15px;
}

.food-img-card {
    width: 90px;
    height: 90px;
    border-radius: 10px;
    object-fit: cover;
}

.food-info-card {
    flex-grow: 1;
    display: flex;
    flex-direction: column;
}

.food-item-name {
    color: #333;
    font-size: 16px;
    font-weight: bold;
    margin-bottom: 5px;
}
.food-item-size {
    font-size: 14px;
    color: #333; /* سیاه */
    font-weight: bold;
    margin-bottom: 5px;
}
.food-item-desc {
    font-size: 13px;
    color: #777;
    margin-bottom: 8px;
}

.price-row {
    display: flex;
    justify-content: space-between;
    align-items: center;
}

.food-item-price {
    color: #FF6600; /* رنگ نارنجی برای قیمت */
    font-size: 16px;
    font-weight: bold;
    direction: rtl;
}

.order-button {
    background-color: #2ECC71; /* دکمه سبز */
    color: white;
    padding: 5px 15px;
    border-radius: 20px;
    font-size: 14px;
    font-weight: bold;
    text-align: center;
    cursor: pointer;
}

/* مخفی کردن المان‌های پیش‌فرض Streamlit که ظاهر را خراب می‌کنند */
.stRadio > label {
    display: none;
}
</style>
""", unsafe_allow_html=True)

# --- منطق UI ---

st.markdown("<h1 style='text-align: right; color: #333; font-size: 24px; margin-bottom: 20px;'>🍽️ منوی کافه نمونه</h1>", unsafe_allow_html=True)


# 1. نوار دسته‌بندی افقی
categories = list(menu.keys())
default_category = categories[0]

# استفاده از Session State برای نگهداری دسته‌بندی انتخاب شده
if 'selected_category' not in st.session_state:
    st.session_state.selected_category = default_category

# ساخت دکمه‌ها و تغییر وضعیت در Session State
st.markdown('<div class="category-bar-container">', unsafe_allow_html=True)
cols = st.columns(len(categories))
for i, category in enumerate(categories):
    # از st.button داخل یک ستون استفاده می‌کنیم
    with cols[i]:
        # is_selected = "selected" if category == st.session_state.selected_category else ""
        
        # استفاده از HTML برای دکمه و اجرای یک تابع callback برای تغییر حالت
        if st.button(category, key=f"cat_btn_{category}", help=f"نمایش دسته {category}"):
            st.session_state.selected_category = category
            st.rerun() # برای رفرش کردن صفحه و نمایش منوی جدید


st.markdown('</div>', unsafe_allow_html=True)

# 2. نمایش آیتم‌های منو بر اساس دسته‌بندی انتخاب شده
selected_category = st.session_state.selected_category
st.markdown(f"<h2 style='text-align: right; color: #333; font-size: 20px; margin-top: 20px; margin-bottom: 20px;'>{selected_category}</h2>", unsafe_allow_html=True)

if selected_category in menu:
    
    # پیمایش در غذاهای دسته انتخاب شده
    for dish, sizes in menu[selected_category].items():
        
        # پیمایش در سایزهای یک غذا
        for size_key, info in sizes.items():
            
            # تعیین نام سایز برای نمایش (مثلاً متوسط، بزرگ)
            if size_key.endswith("mid"):
                size_name = "متوسط"
            elif size_key.endswith("large"):
                size_name = "بزرگ"
            else:
                size_name = "" # برای آیتم‌هایی که سایز ندارند (مثل پیتزا)
            
            
            st.markdown(f"""
            <div class='food-card-container'>
                <img src='{info["img"]}' class='food-img-card'>
                <div class='food-info-card'>
                    <div class='food-item-name'>{dish}</div>
                    <div class='food-item-size'>{size_name}</div>
                    <div class='food-item-desc'>{info["desc"]}</div>
                    <div class='price-row'>
                        <div class='food-item-price'>{info["price"]} تومان</div>
                        <div class='order-button'>انتخاب</div>
                    </div>
                </div>
            </div>
            """, unsafe_allow_html=True)

# --- دستیار رستوران (بدون تغییر) ---
st.markdown("---")
st.subheader("💬 بپرس از دستیار رستوران!")

with st.form("chat_form"):
    question = st.text_input("سوال خود را بنویس یا بپرس:")
    submit_button = st.form_submit_button("ارسال")

    if submit_button and question.strip() != "":
        # نمایش پاسخ دستیار
        with st.spinner('دستیار در حال پاسخگویی...'):
            answer = restaurant_assistant(question)
        st.markdown(
            f"""
            <div style='background-color: white; color: black; padding: 15px; border-radius: 10px; font-size:15px; border: 1px solid #ddd;'>
                <strong>🍳 پاسخ دستیار:</strong><br>{answer}
            </div>
            """,
            unsafe_allow_html=True
        )
