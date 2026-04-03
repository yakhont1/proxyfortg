import requests
import os

# Ссылки на проверенные источники (Raw TXT списки)
SOURCES = [
    "https://raw.githubusercontent.com/TheSpeedX/PROXY-List/master/http.txt",
    "https://raw.githubusercontent.com/ShiftyTR/Proxy-List/master/http.txt"
]

def get_proxies():
    proxies = []
    for url in SOURCES:
        try:
            r = requests.get(url)
            if r.status_code == 200:
                proxies.extend(r.text.splitlines()[:5]) # Берем по 5 штук из каждого
        except:
            pass
    return list(set(proxies))

def send_to_telegram(proxy_list):
    token = os.environ['TELEGRAM_TOKEN']
    chat_id = os.environ['CHAT_ID']
    
    # Красивое оформление
    text = "🌐 **СВЕЖИЕ HTTP ПРОКСИ** 🌐\n\n"
    text += "📅 *Обновлено:* " + "только что\n"
    text += "───────────────────\n"
    for proxy in proxy_list:
        text += f"📍 `{proxy}`\n"
    text += "───────────────────\n"
    text += "⚡️ *Тип:* HTTP/S | *Анонимно:* Да\n"
    text += "📢 *Подпишись на наш канал!*"

    url = f"https://api.telegram.org/bot{token}/sendMessage"
    requests.post(url, data={"chat_id": chat_id, "text": text, "parse_mode": "Markdown"})

if __name__ == "__main__":
    p_list = get_proxies()
    if p_list:
        send_to_telegram(p_list)
