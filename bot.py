# main.py
import os
import logging
import re
from datetime import datetime

import requests
from bs4 import BeautifulSoup
import jdatetime
import pytz

from telegram import InlineKeyboardButton, InlineKeyboardMarkup, Update
from telegram.ext import Application, CommandHandler, CallbackQueryHandler, ContextTypes

# ---------- Logger ----------
logging.basicConfig(format="%(asctime)s - %(levelname)s - %(message)s", level=logging.INFO)
logger = logging.getLogger(__name__)

# ---------- Load token (env first, then token.txt) ----------
def load_token():
    tok = os.getenv("TOKEN")
    if tok:
        return tok.strip()
    # fallback to token.txt
    try:
        with open("token.txt", "r", encoding="utf-8") as f:
            return f.read().strip()
    except FileNotFoundError:
        logger.error("token.txt not found and TOKEN env var not set.")
        return None

TOKEN = load_token()
if not TOKEN:
    raise RuntimeError("Token not found. Set TOKEN env var or add token.txt containing the token.")

# ---------- Helpers: normalize persian/arabic digits and extract number ----------
PERSIAN_DIGITS = "۰۱۲۳۴۵۶۷۸۹"
ARABIC_DIGITS  = "٠١٢٣٤٥٦٧٨٩"

def digits_to_english(s: str) -> str:
    out = []
    for ch in s:
        if ch in PERSIAN_DIGITS:
            out.append(str(PERSIAN_DIGITS.index(ch)))
        elif ch in ARABIC_DIGITS:
            out.append(str(ARABIC_DIGITS.index(ch)))
        else:
            out.append(ch)
    return "".join(out)

def extract_first_number(s: str):
    s2 = digits_to_english(s)
    # get sequences like 12,345 or 12345 or 12345.67
    m = re.search(r"[\d]{1,3}(?:[,\.\s]\d{3})*(?:[\.\,]\d+)?|[\d]+(?:[\.\,]\d+)?", s2)
    if not m:
        return None
    num = m.group(0)
    # remove spaces and commas
    num = num.replace(" ", "").replace(",", "")
    try:
        if "." in num:
            return float(num)
        return int(num)
    except:
        try:
            return float(num)
        except:
            return None

def fmt_thousands(x):
    try:
        if isinstance(x, float):
            # round to 2 decimals
            return f"{x:,.2f}"
        return f"{int(x):,}"
    except:
        return str(x)

# ---------- TGJU scraping with multiple fallbacks ----------
HEADERS = {"User-Agent": "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/115.0 Safari/537.36"}

TGJU_BASE = "https://www.tgju.org/"

def scrape_tgju_page(path):
    url = TGJU_BASE + path
    try:
        r = requests.get(url, headers=HEADERS, timeout=10)
        r.raise_for_status()
        return BeautifulSoup(r.text, "html.parser")
    except Exception as e:
        logger.warning(f"TGJU request failed for {url}: {e}")
        return None

def get_value_from_soup(soup):
    if not soup:
        return None
    # try common selectors
    selectors = [
        "span.info-price",            # common class
        "td[data-market-row]",        # earlier structure
        "div.price",                  # fallback
        ".cPrice",                    # another guess
    ]
    for sel in selectors:
        try:
            node = soup.select_one(sel)
            if node and node.get_text(strip=True):
                val = extract_first_number(node.get_text(" ", strip=True))
                if val is not None:
                    return val
        except Exception:
            continue

    # fallback: search whole text for first big number
    text = soup.get_text(" ", strip=True)
    return extract_first_number(text)

def get_tgju_price_for(path):
    soup = scrape_tgju_page(path)
    val = get_value_from_soup(soup)
    return val

# ---------- Public function that returns dictionary of values ----------
def get_prices_from_tgju():
    try:
        # paths used on tgju
        doll = get_tgju_price_for("profile/price_dollar_rl")
        eur  = get_tgju_price_for("profile/price_eur")
        gold = get_tgju_price_for("profile/geram18")
        return {"dollar": doll, "euro": eur, "gold18": gold}
    except Exception as e:
        logger.error("Error in get_prices_from_tgju: %s", e)
        return {"dollar": None, "euro": None, "gold18": None}

# ---------- Fallbacks for currency using exchangerate.host ----------
def get_currency_fallback():
    try:
        # IRR per USD
        r = requests.get("https://api.exchangerate.host/latest?base=USD&symbols=IRR,EUR", timeout=8)
        j = r.json()
        irr = j.get("rates", {}).get("IRR")
        eur_per_usd = j.get("rates", {}).get("EUR")
        # For EUR in IRR, fetch base=EUR
        r2 = requests.get("https://api.exchangerate.host/latest?base=EUR&symbols=IRR", timeout=8)
        j2 = r2.json()
        irr_per_eur = j2.get("rates", {}).get("IRR")
        return {"dollar_irr": irr, "euro_irr": irr_per_eur}
    except Exception as e:
        logger.warning(f"currency fallback failed: {e}")
        return {"dollar_irr": None, "euro_irr": None}

# ---------- Compose message text (with fallbacks & formatting) ----------
def build_price_message():
    p = get_prices_from_tgju()
    msg_parts = []
    # DOLLAR
    if p["dollar"]:
        d = p["dollar"]
        msg_parts.append("💵 دلار (تجارت آزاد): {} ریال".format(fmt_thousands(d)))
    else:
        fb = get_currency_fallback().get("dollar_irr")
        if fb:
            msg_parts.append("💵 دلار (fallback): {} ریال".format(fmt_thousands(fb)))
        else:
            msg_parts.append("💵 دلار: ❌ اتصال یا خواندن ناموفق")

    # EURO
    if p["euro"]:
        e = p["euro"]
        msg_parts.append("💶 یورو: {} ریال".format(fmt_thousands(e)))
    else:
        fb = get_currency_fallback().get("euro_irr")
        if fb:
            msg_parts.append("💶 یورو (fallback): {} ریال".format(fmt_thousands(fb)))
        else:
            msg_parts.append("💶 یورو: ❌ اتصال یا خواندن ناموفق")

    # GOLD 18
    if p["gold18"]:
        g = p["gold18"]
        msg_parts.append("🥇 طلا ۱۸ عیار (هر گرم): {} ریال".format(fmt_thousands(g)))
    else:
        msg_parts.append("🥇 طلا: ❌ خواندن ناموفق")

    return "\n".join(msg_parts)

# ---------- Date and Time helpers ----------
def get_tehran_time_str():
    tz = pytz.timezone("Asia/Tehran")
    now = datetime.now(tz)
    return now.strftime("%H:%M:%S")

def get_jalali_date_str():
    # use jdatetime
    jnow = jdatetime.datetime.fromgregorian(datetime=datetime.now(pytz.timezone("Asia/Tehran")))
    return jnow.strftime("%Y/%m/%d")

# ---------- Bot Handlers ----------
async def start_handler(update: Update, context: ContextTypes.DEFAULT_TYPE):
    keyboard = [
        [InlineKeyboardButton("📅 تاریخ شمسی", callback_data="date")],
        [InlineKeyboardButton("⏰ ساعت تهران", callback_data="time")],
        [InlineKeyboardButton("💵 دلار", callback_data="usd")],
        [InlineKeyboardButton("💶 یورو", callback_data="eur")],
        [InlineKeyboardButton("🥇 طلا (۱۸ عیار)", callback_data="gold")],
        [InlineKeyboardButton("🎲 تاس", callback_data="dice")],
        [InlineKeyboardButton("😂 جوک", callback_data="joke")],
        [InlineKeyboardButton("💡 انگیزشی", callback_data="quote")],
        [InlineKeyboardButton("👨‍💻 درباره برنامه‌نویس", callback_data="about")],
    ]
    await update.message.reply_text("سلام 👋 من ربات علی اصغر درویش پور هستم.\nیک گزینه را انتخاب کن:", reply_markup=InlineKeyboardMarkup(keyboard))

async def callback_handler(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    await query.answer()
    data = query.data

    if data == "date":
        await query.edit_message_text(f"📅 تاریخ شمسی: {get_jalali_date_str()}")
    elif data == "time":
        await query.edit_message_text(f"⏰ ساعت تهران: {get_tehran_time_str()}")
    elif data == "usd" or data == "eur":
        # show currency message (both)
        msg = build_price_message()
        await query.edit_message_text(msg)
    elif data == "gold":
        msg = build_price_message()
        await query.edit_message_text(msg)
    elif data == "dice":
        import random
        await query.edit_message_text(f"🎲 نتیجه تاس: {random.randint(1,6)}")
    elif data == "joke":
        import random
        jokes = [
            "😂 یه نفر گفت: من آهنگ سازم. گفتم چرا آهنگی نمی‌سازیش؟ گفت: بلد نیستم نوت بزنم، فقط می‌زنم روی کیبورد...",
            "🤣 مراقب باش جای خواب، خواب کاراتو نگیری!",
            "😅 یکی پرسید چرا دیر اومدی؟ گفت: خواب دیدم ماشین وایستاد، تجربه شدنیه!"
        ]
        await query.edit_message_text(random.choice(jokes))
    elif data == "quote":
        import random
        quotes = ["تو قوی‌تر از چیزی هستی که فکر می‌کنی.", "هر روز شروع جدیدیه.", "با تلاش کم کم میشه کاری بزرگ کرد."]
        await query.edit_message_text(random.choice(quotes))
    elif data == "about":
        await query.edit_message_text("👨‍💻 برنامه‌نویس: علی اصغر درویش پور\nربات قیمت و ابزار کوچک")

# ---------- Main ----------
def main():
    app = Application.builder().token(TOKEN).build()

    app.add_handler(CommandHandler("start", start_handler))
    app.add_handler(CallbackQueryHandler(callback_handler))

    logger.info("Bot starting...")
    app.run_polling()

if __name__ == "__main__":
    main()
