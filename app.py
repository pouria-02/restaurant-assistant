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

# --- منوی نمونه و آیکون‌ها (بدون تغییر) ---
menu = {
    "نوشیدنی گرم": {
        "موکا مخصوص": {
            "size_mid": {"desc": "ترکیب دوشات اسپرسو، شکلات داغ و خامه", "price": "۱۹۸,۸۰۰", "img": "https://raw.githubusercontent.com/pouria-02/restaurant-assistant/main/capp.jpg"},
            "size_large": {"desc": "ترکیب دوشات اسپرسو، شکلات داغ و خامه", "price": "۲۲۸,۸۰۰", "img": "https://raw.githubusercontent.com/pouria-02/restaurant-assistant/main/capp.jpg"}
        },
        "کاپوچینو": {
            "size_mid": {"desc": "اسپرسو، شیر کف دار، شکلات پودر", "price": "۱۶۵,۰۰۰", "img": "https://raw.githubusercontent.com/pouria-02/restaurant-assistant/main/capp.jpg"},
        },
    },
    "فست فود": {
        "پیتزا مارگاریتا": {"mid": {"desc": "خمیر نازک، سس گوجه‌فرنگی، پنیر موتزارلا، ریحان تازه", "price": "۲۵۰,۰۰۰", "img": "https://raw.githubusercontent.com/pouria-02/restaurant-assistant/main/margharita.jpeg"}},
    },
    "چای و دمنوش": {
        "چای سبز": {"mid": {"desc": "چای سبز با عطر ملایم", "price": "۷۰,۰۰۰", "img": "https://raw.githubusercontent.com/pouria-02/restaurant-assistant/main/omellete.jpg"}},
    },
    "میلکشیک‌ها": {
        "شکلات": {"mid": {"desc": "میلکشیک شکلاتی", "price": "۱۵۰,۰۰۰", "img": "https://raw.githubusercontent.com/pouria-02/restaurant-assistant/main/Pepperoni.jpg"}},
    }
}

category_icons = {
    "نوشیدنی گرم": "☕",
    "فست فود": "🍔",
    "چای و دمنوش": "🍵",
    "میلکشیک‌ها": "🥤"
}

# --- CSS برای استایل جدید ---
st.markdown("""
<style>
/* فونت و پس زمینه */
div.block-container {
    padding: 2rem 1rem;
    max-width: 95%;
}
.stApp {
    background-color: #FFF4D6; /* رنگ کرمی گرم‌تر */
}
/* بخش بالایی صفحه برای دسته‌بندی‌ها */
.category-selection-area {
    background-color: white; 
    padding: 10px 0;
    margin-bottom: 20px;
    border-radius: 20px;
    box-shadow: 0 2px 5px rgba(0,0,0,0.05);
}

/* نوار دسته‌بندی افقی */
.category-bar-container {
    overflow-x: scroll; /* اسکرول افقی */
    white-space: nowrap;
    padding: 0 10px 5px 10px;
    direction: rtl; /* برای نمایش از راست به چپ */
    scrollbar-width: none; 
    -ms-overflow-style: none;
    display: flex; /* تضمین نمایش افقی */
}
.category-bar-container::-webkit-scrollbar { 
    display: none; 
}

/* استایل کارت‌های دسته‌بندی شبیه تصویر */
.category-card {
    /* تغییر مهم: inline-flex برای نمایش کنار هم */
    display: inline-flex; 
    flex-shrink: 0; /* جلوگیری از کوچک شدن کارت‌ها */
    flex-direction: column;
    align-items: center;
    justify-content: center;
    width: 85px; 
    height: 85px;
    margin: 0 5px;
    border-radius: 15px;
    cursor: pointer;
    text-align: center;
    transition: all 0.2s;
    background-color: #f0f0f0; 
    border: 1px solid #e0e0e0;
    text-decoration: none;
    color: #333;
    font-size: 13px;
    font-weight: bold;
    padding-top: 10px;
}

.category-card:hover {
    box-shadow: 0 4px 8px rgba(0,0,0,0.1);
}

/* استایل کارت فعال/انتخاب شده (رنگ سبز شاداب) */
.category-card.selected {
    background-color: #2ECC71; 
    color: white;
    border-color: #2ECC71;
    box-shadow: 0 4px 8px rgba(46, 204, 113, 0.5);
}

.category-icon {
    font-size: 30px; 
    margin-bottom: 5px;
    filter: invert(0); 
}
.category-card.selected .category-icon {
    filter: invert(1);
}


/* استایل آیتم منو (بدون تغییر) */
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
    color: #333;
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
    color: #2ECC71; 
    font-size: 16px;
    font-weight: bold;
    direction: rtl;
}

.order-button {
    background-color: #2ECC71;
    color: white;
    padding: 5px 15px;
    border-radius: 20px;
    font-size: 14px;
    font-weight: bold;
    text-align: center;
    cursor: pointer;
}
</style>
""", unsafe_allow_html=True)

# --- منطق UI (بدون تغییر) ---

st.markdown("<h1 style='text-align: right; color: #333; font-size: 24px; margin-bottom: 20px;'>🍽️ منوی کافه نمونه</h1>", unsafe_allow_html=True)

# 1. نوار دسته‌بندی افقی
categories = list(menu.keys())
default_category = categories[0]

if 'selected_category' not in st.session_state:
    st.session_state.selected_category = default_category

query_params = st.query_params

if "category" in query_params:
    selected_from_url = query_params["category"]
    if selected_from_url in categories:
        st.session_state.selected_category = selected_from_url
        del st.query_params["category"]

st.markdown('<div class="category-selection-area">', unsafe_allow_html=True)
st.markdown('<h3 style="text-align: right; margin: 0 15px 10px 0; font-size: 16px;">لیست دسته‌بندی‌ها ⌄</h3>', unsafe_allow_html=True)
st.markdown('<div class="category-bar-container">', unsafe_allow_html=True)

selected_category = st.session_state.selected_category

for category in categories:
    is_selected = "selected" if category == selected_category else ""
    icon = category_icons.get(category, "❓")
    
    # استفاده از لینک HTML برای تغییر query parameter
    url_to_click = f"/?category={category}"
    
    st.markdown(f"""
    <a href="{url_to_click}" target="_self" class='category-card {is_selected}'>
        <div class='category-icon'>{icon}</div>
        {category}
    </a>
    """, unsafe_allow_html=True)

st.markdown('</div>', unsafe_allow_html=True)
st.markdown('</div>', unsafe_allow_html=True)


# 2. نمایش آیتم‌های منو بر اساس دسته‌بندی انتخاب شده
st.markdown(f"<h2 style='text-align: right; color: #333; font-size: 20px; margin-top: 20px; margin-bottom: 20px;'>{selected_category}</h2>", unsafe_allow_html=True)

if selected_category in menu:
    
    for dish, sizes in menu[selected_category].items():
        for size_key, info in sizes.items():
            
            if size_key.endswith("mid"):
                size_name = "متوسط"
            elif size_key.endswith("large"):
                size_name = "بزرگ"
            else:
                size_name = "" 
            
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
