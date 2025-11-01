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
    # ... ( restaurant_assistant function remains unchanged ) ...
    # منو برای پرامپت دستیار باید به‌روزرسانی شود تا آیتم‌های جدید را منعکس کند
    menu_for_prompt = {
        "نوشیدنی گرم": {"موکا مخصوص": {}, "کاپوچینو": {}, "لاته وانیلی": {}, "قهوه دمی": {}, "هات چاکلت": {}, "اسپرسو سینگل": {}, "قهوه ترک": {}},
        "فست فود": {"پیتزا مارگاریتا": {}, "برگر کلاسیک": {}, "ساندویچ ژامبون": {}, "سیب زمینی سرخ کرده": {}, "پیتزا پپرونی": {}, "سالاد سزار": {}, "لازانیا": {}},
        "چای و دمنوش": {"چای سبز": {}, "چای سیاه ارل گری": {}, "دمنوش بابونه": {}, "دمنوش زنجبیل": {}, "چای مراکشی": {}, "دمنوش میوه‌ای": {}, "چای ماسالا": {}},
        "میلکشیک‌ها": {"شکلات": {}, "توت فرنگی": {}, "وانیل": {}, "کارامل نمکی": {}, "قهوه": {}, "موز": {}, "نارگیل": {}}
    }
    
    system_prompt = (
        "تو یه دستیار رستوران هستی و با لحنی صمیمی با مشتری‌ها صحبت می‌کنی. "
        "فقط درباره‌ی غذاهای منوی زیر جواب بده. "
        "اگر سوال ربطی به منو یا مواد تشکیل‌دهنده‌ی غذاها نداشت، با خوشرویی بگو: "
        "«من فقط درباره‌ی منو می‌تونم کمکت کنم :)»\n\n"
        "اگر کاربر درباره‌ی مواد تشکیل‌دهنده‌ی هر غذا پرسید، "
        "با لحن دوستانه درباره اون ماده توضیح بده، خواصش رو بگو و اگر قابل درست کردن در خونه هست، "
        "به طور خلاصه روش تهیه‌ش رو هم بگو.\n\n"
        f"منو:\n{menu_for_prompt}"
    )
    msg = [HumanMessage(content=f"{system_prompt}\n\nسؤال مشتری: {question}")]
    response = llm.invoke(msg)
    return response.content

# --- منوی نمونه و آیکون‌ها (با آیتم‌های جدید) ---
menu = {
    "نوشیدنی گرم": {
        "موکا مخصوص": {
            "size_mid": {"desc": "ترکیب دوشات اسپرسو، شکلات داغ و خامه", "price": "۱۹۸,۸۰۰", "img": "https://raw.githubusercontent.com/pouria-02/restaurant-assistant/main/capp.jpg"},
            "size_large": {"desc": "ترکیب دوشات اسپرسو، شکلات داغ و خامه", "price": "۲۲۸,۸۰۰", "img": "https://raw.githubusercontent.com/pouria-02/restaurant-assistant/main/capp.jpg"}
        },
        "کاپوچینو": {
            "size_mid": {"desc": "اسپرسو، شیر کف دار، شکلات پودر", "price": "۱۶۵,۰۰۰", "img": "https://raw.githubusercontent.com/pouria-02/restaurant-assistant/main/capp.jpg"},
        },
        "لاته وانیلی": {
            "size_mid": {"desc": "اسپرسو، شیر داغ و عصاره وانیل", "price": "۱۸۰,۰۰۰", "img": "https://raw.githubusercontent.com/pouria-02/restaurant-assistant/main/capp.jpg"},
        },
        "قهوه دمی": {
            "size_mid": {"desc": "قهوه تک‌خاستگاه با روش دم‌آوری انتخابی", "price": "۱۵۵,۰۰۰", "img": "https://raw.githubusercontent.com/pouria-02/restaurant-assistant/main/capp.jpg"},
        },
        "هات چاکلت": {
            "size_mid": {"desc": "ترکیب ویژه شکلات و شیر گرم", "price": "۱۷۰,۰۰۰", "img": "https://raw.githubusercontent.com/pouria-02/restaurant-assistant/main/capp.jpg"},
        },
        "اسپرسو سینگل": {
            "size_mid": {"desc": "یک شات اسپرسوی غلیظ و تازه", "price": "۱۱۰,۰۰۰", "img": "https://raw.githubusercontent.com/pouria-02/restaurant-assistant/main/capp.jpg"},
        },
        "قهوه ترک": {
            "size_mid": {"desc": "قهوه سنتی ترک با پخت روی ماسه", "price": "۱۲۰,۰۰۰", "img": "https://raw.githubusercontent.com/pouria-02/restaurant-assistant/main/capp.jpg"},
        },
    },
    "فست فود": {
        "پیتزا مارگاریتا": {"mid": {"desc": "خمیر نازک، سس گوجه‌فرنگی، پنیر موتزارلا، ریحان تازه", "price": "۲۵۰,۰۰۰", "img": "https://raw.githubusercontent.com/pouria-02/restaurant-assistant/main/margharita.jpeg"}},
        "برگر کلاسیک": {"mid": {"desc": "گوشت ۱۲۰ گرمی، کاهو، گوجه، سس مخصوص", "price": "۲۱۰,۰۰۰", "img": "https://raw.githubusercontent.com/pouria-02/restaurant-assistant/main/Pepperoni.jpg"}},
        "ساندویچ ژامبون": {"mid": {"desc": "ژامبون گوشت و مرغ، پنیر، کاهو", "price": "۱۸۰,۰۰۰", "img": "https://raw.githubusercontent.com/pouria-02/restaurant-assistant/main/omellete.jpg"}},
        "سیب زمینی سرخ کرده": {"mid": {"desc": "سیب زمینی بلژیکی با سس سیر", "price": "۹۰,۰۰۰", "img": "https://raw.githubusercontent.com/pouria-02/restaurant-assistant/main/margharita.jpeg"}},
        "پیتزا پپرونی": {"mid": {"desc": "پپرونی، پنیر موتزارلا، سس تند", "price": "۲۷۰,۰۰۰", "img": "https://raw.githubusercontent.com/pouria-02/restaurant-assistant/main/Pepperoni.jpg"}},
        "سالاد سزار": {"mid": {"desc": "کاهو، مرغ گریل، سس سزار، کروتان", "price": "۱۷۵,۰۰۰", "img": "https://raw.githubusercontent.com/pouria-02/restaurant-assistant/main/omellete.jpg"}},
        "لازانیا": {"mid": {"desc": "لایه‌های خمیر، گوشت، پنیر، سس بشامل", "price": "۲۳۰,۰۰۰", "img": "https://raw.githubusercontent.com/pouria-02/restaurant-assistant/main/margharita.jpeg"}},
    },
    "چای و دمنوش": {
        "چای سبز": {"mid": {"desc": "چای سبز با عطر ملایم", "price": "۷۰,۰۰۰", "img": "https://raw.githubusercontent.com/pouria-02/restaurant-assistant/main/omellete.jpg"}},
        "چای سیاه ارل گری": {"mid": {"desc": "چای سیاه با اسانس برگاموت", "price": "۷۵,۰۰۰", "img": "https://raw.githubusercontent.com/pouria-02/restaurant-assistant/main/omellete.jpg"}},
        "دمنوش بابونه": {"mid": {"desc": "آرامش‌بخش و تسکین‌دهنده اعصاب", "price": "۸۰,۰۰۰", "img": "https://raw.githubusercontent.com/pouria-02/restaurant-assistant/main/omellete.jpg"}},
        "دمنوش زنجبیل": {"mid": {"desc": "گرم‌کننده و تقویت‌کننده سیستم ایمنی", "price": "۸۵,۰۰۰", "img": "https://raw.githubusercontent.com/pouria-02/restaurant-assistant/main/omellete.jpg"}},
        "چای مراکشی": {"mid": {"desc": "ترکیب چای سبز، نعنا و شکر (به انتخاب شما)", "price": "۹۵,۰۰۰", "img": "https://raw.githubusercontent.com/pouria-02/restaurant-assistant/main/omellete.jpg"}},
        "دمنوش میوه‌ای": {"mid": {"desc": "ترکیبی از میوه‌های خشک و طبیعی", "price": "۸۵,۰۰۰", "img": "https://raw.githubusercontent.com/pouria-02/restaurant-assistant/main/omellete.jpg"}},
        "چای ماسالا": {"mid": {"desc": "چای سیاه با ادویه‌های گرم و شیر", "price": "۱۲۰,۰۰۰", "img": "https://raw.githubusercontent.com/pouria-02/restaurant-assistant/main/omellete.jpg"}},
    },
    "میلکشیک‌ها": {
        "شکلات": {"mid": {"desc": "میلکشیک شکلاتی با تکه‌های شکلات", "price": "۱۵۰,۰۰۰", "img": "https://raw.githubusercontent.com/pouria-02/restaurant-assistant/main/Pepperoni.jpg"}},
        "توت فرنگی": {"mid": {"desc": "ترکیب شیر، بستنی و توت فرنگی تازه", "price": "۱۶۰,۰۰۰", "img": "https://raw.githubusercontent.com/pouria-02/restaurant-assistant/main/Pepperoni.jpg"}},
        "وانیل": {"mid": {"desc": "میلکشیک کلاسیک وانیلی", "price": "۱۴۵,۰۰۰", "img": "https://raw.githubusercontent.com/pouria-02/restaurant-assistant/main/Pepperoni.jpg"}},
        "کارامل نمکی": {"mid": {"desc": "بستنی، شیر و سس کارامل نمکی خانگی", "price": "۱۷۰,۰۰۰", "img": "https://raw.githubusercontent.com/pouria-02/restaurant-assistant/main/Pepperoni.jpg"}},
        "قهوه": {"mid": {"desc": "ترکیب اسپرسو، شیر و بستنی وانیلی", "price": "۱۶۵,۰۰۰", "img": "https://raw.githubusercontent.com/pouria-02/restaurant-assistant/main/Pepperoni.jpg"}},
        "موز": {"mid": {"desc": "ترکیب موز تازه، شیر و بستنی", "price": "۱۵۵,۰۰۰", "img": "https://raw.githubusercontent.com/pouria-02/restaurant-assistant/main/Pepperoni.jpg"}},
        "نارگیل": {"mid": {"desc": "میلکشیک با شیر نارگیل و تکه‌های نارگیل", "price": "۱۷۵,۰۰۰", "img": "https://raw.githubusercontent.com/pouria-02/restaurant-assistant/main/Pepperoni.jpg"}},
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
    /* رنگ کرمی تیره‌تر و گرم‌تر */
    background-color: #FBEEC8; 
}

/* رنگ مشکی برای عنوان دستیار رستوران (st.subheader) */
h3 {
    color: #000000 !important;
}

/* 🟢 استایل دهی باکس ورودی دستیار 🟢 */
.stTextInput > div > div {
    /* پس‌زمینه هم‌رنگ پس‌زمینه کلی اپلیکیشن */
    background-color: #FBEEC8; 
    /* بوردر سبز همرنگ قیمت‌ها */
    border: 2px solid #2ECC71 !important; 
    border-radius: 0.5rem; 
    box-shadow: none !important;
}

/* رنگ خاکستری برای لیبل (سوال خود را بنویسید...) */
.stTextInput > label {
    color: #555555 !important; 
    font-weight: normal !important;
}

/* رنگ متن ورودی (متنی که تایپ می‌شود) */
.stTextInput > div > div > input {
    color: #000000 !important; 
    background-color: #FBEEC8 !important; 
}


/* 🟢 استایل دهی دکمه ارسال فرم (submit button) 🟢 */
.stFormSubmitButton > button {
    background-color: #2ECC71 !important; 
    color: white !important; 
    border: none !important; 
    border-radius: 20px !important; 
    padding: 8px 20px !important; 
    font-weight: bold !important;
    box-shadow: 0 4px 6px rgba(46, 204, 113, 0.4) !important;
}

/* استایل Hover برای دکمه ارسال */
.stFormSubmitButton > button:hover {
    background-color: #27ae60 !important; /* کمی تیره تر شدن در هاور */
}


/* 🟢 استایل بخش بالایی صفحه برای دسته‌بندی‌ها (بخش مهم برای نمایش افقی) 🟢 */
.category-selection-area {
    background-color: white; 
    padding: 10px 0;
    margin-bottom: 20px;
    border-radius: 20px;
    box-shadow: 0 2px 5px rgba(0,0,0,0.05);
    /* اطمینان از نمایش افقی در مرورگرهای موبایل */
    width: 100%; 
}

/* نوار دسته‌بندی افقی - این کلاس برای نمایش افقی و اسکرول در موبایل حیاتی است */
.category-bar-container {
    overflow-x: scroll; 
    white-space: nowrap; 
    padding: 0 10px 5px 10px;
    direction: rtl; 
    scrollbar-width: none; 
    -ms-overflow-style: none;
    display: flex; /* کلید نمایش افقی */
    flex-direction: row; /* کلید نمایش افقی */
}
.category-bar-container::-webkit-scrollbar { 
    display: none; 
}

/* استایل کارت‌های دسته‌بندی شبیه تصویر */
.category-card {
    display: flex; 
    flex-shrink: 0; 
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
    /* خاکستری شدن نام غذا (درخواستی قبلی) */
    color: #555555; 
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
    /* خاکستری شدن توضیحات (درخواستی قبلی) */
    font-size: 13px;
    color: #777777; 
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
    font-weight: 900; 
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

# --- منطق UI ---

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

# 📌 این بخش اکنون اطمینان می‌دهد که دسته‌بندی‌ها به‌صورت افقی و در بدنه اصلی نمایش داده می‌شوند.
st.markdown('<div class="category-selection-area">', unsafe_allow_html=True)
st.markdown('<h3 style="text-align: right; margin: 0 15px 10px 0; font-size: 16px;">لیست دسته‌بندی‌ها ⌄</h3>', unsafe_allow_html=True)

# 🟢 ساخت یک رشته HTML برای همه کارت‌ها و قرار دادن آن در یک st.markdown واحد 🟢
category_cards_html = '' 
selected_category = st.session_state.selected_category

for category in categories:
    is_selected = "selected" if category == selected_category else ""
    icon = category_icons.get(category, "❓")
    
    url_to_click = f"/?category={category}"
    
    # اضافه کردن HTML هر کارت به رشته
    category_cards_html += f"""
    <a href="{url_to_click}" target="_self" class='category-card {is_selected}'>
        <div class='category-icon'>{icon}</div>
        {category}
    </a>
    """
# 🔴 اجرای یکباره Markdown: قرار دادن همه کارت‌ها داخل یک container اصلی 🔴
st.markdown(f"""
<div class="category-bar-container">
    {category_cards_html}
</div>
""", unsafe_allow_html=True) 

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
    # باکس ورودی کرمی با بوردر سبز (تغییرات قبلی)
    question = st.text_input("سوال خود را بنویس یا بپرس:")
    # دکمه ارسال سبز با متن سفید (تغییرات قبلی)
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
