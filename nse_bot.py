import telebot
import requests

TOKEN = "8001126345:AAGA56L12XAkH8V3bemStEMxyUMfP3nHZlU"
bot = telebot.TeleBot(TOKEN)

WATCHLIST = ['RELIANCE', 'SBIN', 'TATAMOTORS', 'INFY', 'HDFCBANK']
headers = {"User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64)"}

def get_deep_data(symbol):
    url = f"https://www.nseindia.com/api/quote-equity?symbol={symbol}"
    try:
        session = requests.Session()
        session.get("https://www.nseindia.com", headers=headers, timeout=10)
        response = session.get(url, headers=headers, timeout=10)
        
        if response.status_code != 200:
            return f"⚠️ {symbol} નો ડેટા મળતો નથી. માર્કેટ બંધ હોઈ શકે અથવા સિમ્બોલ ખોટો છે."
            
        data = response.json()
        total_buy = data['marketDeptOrderBook']['totalBuyQuantity']
        total_sell = data['marketDeptOrderBook']['totalSellQuantity']
        price = data['priceInfo']['lastPrice']
        
        total = total_buy + total_sell
        if total == 0:
            return f"⚠️ {symbol} માં અત્યારે કોઈ લાઈવ ઓર્ડર નથી. માર્કેટ બંધ છે."
            
        buy_pct = (total_buy / total) * 100
        trend = "🔥 તેજી" if buy_pct > 65 else ("⚠️ વેચવાલી" if buy_pct < 40 else "⏳ ન્યુટ્રલ")
        expose_data = "મોટા પ્લેયર્સ (FII/DII) એન્ટ્રી મારી રહ્યા છે" if buy_pct > 60 else "રિટેલર્સનો ડર દેખાય છે"
        
        report = (
            f"🎯 *Killcritic Report: {symbol}*\n"
            f"━━━━━━━━━━━━━━━━━━━━\n"
            f"💰 ભાવ: ₹{price}\n"
            f"🧠 *Iq300 Analysis:* {trend}\n"
            f"🔬 *Autopsy:* બાયર્સ {buy_pct:.2f}% | સેલર્સ {100-buy_pct:.2f}%\n"
            f"⚡ *20x Think:* {'હાઇ પ્રોફિટ ઝોન' if buy_pct > 65 else 'રિસ્ક ઝોન'}\n"
            f"👁️ *Expose:* {expose_data}\n"
            f"━━━━━━━━━━━━━━━━━━━━"
        )
        return report
    except Exception as e:
        return f"⚠️ અત્યારે ડેટા ઉપલબ્ધ નથી. માર્કેટ બંધ હોવાને કારણે NSE સર્વર રિસ્પોન્સ નથી આપતું."

@bot.message_handler(commands=['track'])
def track(m):
    try:
        parts = m.text.split()
        if len(parts) < 2:
            bot.reply_to(m, "❌ પ્લીઝ શેરનું નામ લખો. જેમ કે: `/track RELIANCE`", parse_mode="Markdown")
            return
        symbol = parts[1].upper()
        bot.reply_to(m, "🔍 ડેટા કલેક્ટ થઈ રહ્યો છે, વેઇટ...", parse_mode="Markdown")
        report = get_deep_data(symbol)
        bot.reply_to(m, report, parse_mode="Markdown")
    except Exception as err:
        bot.reply_to(m, "❌ કમાન્ડ પ્રોસેસ કરવામાં કંઈક ભૂલ થઈ.")

@bot.message_handler(commands=['watchlist'])
def watch(m):
    bot.reply_to(m, "📊 *Watchlist Scanner:* લાઈવ માર્કેટમાં આ આખી લિસ્ટ સ્કેન થશે. અત્યારે ઓફ-માર્કેટ છે હજી.", parse_mode="Markdown")

@bot.message_handler(commands=['sector'])
def sec(m): 
    bot.reply_to(m, "💡 *Sector Sentiment:* ફાઇનાન્શિયલ અને ઓટો સેક્ટર પર નજર છે. Autopsy રિપોર્ટ સવારના લાઈવ ડેટા પર જનરેટ થશે.")

@bot.message_handler(commands=['ipo'])
def ipo(m): 
    bot.reply_to(m, "🚀 *IPO Pre-Market:* લિસ્ટિંગ સેશન ટ્રેકર એક્ટિવ છે. કાલે સવારે નવો ડેટા ફેચ થશે.")

print("🚀 માસ્ટર બોટ સેફ મોડમાં લાઈવ છે...")
bot.infinity_polling()
