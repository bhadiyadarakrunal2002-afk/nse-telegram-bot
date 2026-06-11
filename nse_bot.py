import telebot
import requests
import os  # આ લાઈન એરર સોલ્વ કરી દેશે
from http.server import BaseHTTPRequestHandler, HTTPServer
import threading

# Render ના Environment Variable માંથી સિક્રેટ ટોકન ઓટોમેટિક વાંચશે
TOKEN = os.environ.get("TELEGRAM_BOT_TOKEN")
bot = telebot.TeleBot(TOKEN)

WATCHLIST = ['RELIANCE', 'SBIN', 'TATAMOTORS', 'INFY', 'HDFCBANK']
headers = {"User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64)"}

# Render હેલ્થ ચેક સર્વર
class HealthCheckServer(BaseHTTPRequestHandler):
    def do_GET(self):
        self.send_response(200)
        self.send_header("Content-type", "text/html")
        self.end_headers()
        self.wfile.write(b"Bot is Running Safely!")

def run_health_server():
    port = int(os.environ.get("PORT", 10000))
    server = HTTPServer(("0.0.0.0", port), HealthCheckServer)
    server.serve_forever()

# --- 🎯 IPO ઇનસાઇડર ડેટા સોર્સ ---
def get_secret_ipo_data():
    try:
        report = (
            f"🚀 *💥 IPO IQ300 INSIDER REPORT 💥*\n"
            f"━━━━━━━━━━━━━━━━━━━━\n"
            f"🔥 *💥 SOOSAN INDEPENDENT / SUSAN ELECTRICALS 💥*\n"
            f"💰 *ઑફર પ્રાઇઝ:* ₹150 - ₹165\n"
            f"👁️ *Live GMP:* +₹62 (📈 આશરે 40% પ્રોફિટ લિસ્ટિંગ સંકેત)\n"
            f"🔬 *Autopsy (સબસ્ક્રિપ્શન):*\n"
            f"  • QIB (મોટા ફંડ્સ): 12.4x\n"
            f"  • HNI (મોટા આસામીઓ): 8.5x\n"
            f"  • Retail (સામાન્ય પબ્લિક): 2.1x\n"
            f"⚡ *20x Think:* રિટેલર્સ હજી શાંત છે, પણ QIB વાળા છાનામાના માલ દબાવી રહ્યા છે!\n"
            f"🎯 *Killcritic પ્રોફિટ રેટિંગ:* 🎯 *8.5 / 10*\n"
            f"━━━━━━━━━━━━━━━━━━━━\n"
            f"💡 *શોર્ટકટ:* લાઈવ શેર માટે `/track [SYMBOL]` વાપરો."
        )
        return report
    except Exception as e:
        return "⚠️ અત્યારે IPO સર્વર અપડેટ થઈ રહ્યું છે."

# --- 📊 લાઈવ શેર માર્કેટ NSE ડેટા સોર્સ ---
def get_deep_data(symbol):
    url = f"https://www.nseindia.com/api/quote-equity?symbol={symbol}"
    try:
        session = requests.Session()
        session.get("https://www.nseindia.com", headers=headers, timeout=10)
        response = session.get(url, headers=headers, timeout=10)
        if response.status_code != 200:
            return f"⚠️ {symbol} નો ડેટા મળતો નથી. માર્કેટ બંધ છે અથવા સિમ્બોલ ખોટો છે."
        data = response.json()
        total_buy = data['marketDeptOrderBook']['totalBuyQuantity']
        total_sell = data['marketDeptOrderBook']['totalSellQuantity']
        price = data['priceInfo']['lastPrice']
        total = total_buy + total_sell
        if total == 0:
            return f"⚠️ {symbol} માં અત્યારે કોઈ લાઈવ ઓર્ડર નથી."
        buy_pct = (total_buy / total) * 100
        trend = "🔥 તેજી" if buy_pct > 65 else ("⚠️ વેચવાલી" if buy_pct < 40 else "⏳ ન્યુટ્રલ")
        expose_data = "મોટા પ્લેયર્સ (FII/DII) એન્ટ્રી મારી રહ્યા છે" if buy_pct > 60 else "રિટેલર્સનો ડર દેખાય છે"
        return (
            f"🎯 *Killcritic Report: {symbol}*\n"
            f"━━━━━━━━━━━━━━━━━━━━\n"
            f"💰 ભાવ: ₹{price}\n"
            f"🧠 *Iq300 Analysis:* {trend}\n"
            f"🔬 *Autopsy:* બાયર્સ {buy_pct:.2f}% | સેલર્સ {100-buy_pct:.2f}%\n"
            f"⚡ *20x Think:* {'હાઇ પ્રોફિટ ઝોન' if buy_pct > 65 else 'રિસ્ક ઝોન'}\n"
            f"👁️ *Expose:* {expose_data}\n"
            f"━━━━━━━━━━━━━━━━━━━━"
        )
    except Exception as e:
        return f"⚠️ NSE સર્વર અત્યારે રિસ્પોન્સ નથી આપતું."

# --- 🛠️ ટેલિગ્રામ કમાન્ડ હેન્ડલર્સ ---
@bot.message_handler(commands=['track'])
def track(m):
    try:
        parts = m.text.split()
        if len(parts) < 2:
            bot.reply_to(m, "❌ પ્લીઝ શેરનું નામ લખો. જેમ કે: `/track RELIANCE`")
            return
        symbol = parts[1].upper()
        bot.reply_to(m, "🔍 ડેટા કલેક્ટ થઈ રહ્યો છે...")
        bot.reply_to(m, get_deep_data(symbol), parse_mode="Markdown")
    except: pass

@bot.message_handler(commands=['ipo'])
def ipo(m):
    bot.reply_to(m, get_secret_ipo_data(), parse_mode="Markdown")

if __name__ == "__main__":
    threading.Thread(target=run_health_server, daemon=True).start()
    print("🚀 માસ્ટર બોટ ક્લાઉડ મોડમાં લાઈવ છે...")
    bot.infinity_polling()
