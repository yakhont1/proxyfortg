import requests
import os

# Ссылки на источники для разных типов
HTTP_SOURCES = ["https://raw.githubusercontent.com/TheSpeedX/PROXY-List/master/http.txt"]
# Источники для MTProto и V2Ray (VLESS/Trojan)
V2RAY_SOURCES = [
    "https://raw.githubusercontent.com/freev2rayspeed/v2ray/main/v2ray.txt",
    "https://raw.githubusercontent.com/mansor427/v2ray-shahr/main/v2ray.txt"
]

def get_data(urls, limit=5):
    items = []
    for url in urls:
        try:
            r = requests.get(url, timeout=10)
            if r.status_code == 200:
                lines = [l for l in r.text.splitlines() if len(l) > 5]
                items.extend(lines[:limit])
        except: pass
    return list(set(items))

def send_to_telegram():
    token = os.environ['TELEGRAM_TOKEN']
    chat_id = os.environ['CHAT_ID']
    
    http_list = get_data(HTTP_SOURCES, 5)
    v2ray_list = get_data(V2RAY_SOURCES, 5)

    text = "🚀 **МЕГА-ПОДБОРКА ПРОКСИ** 🚀\n\n"
    
    if http_list:
        text += "🌐 **HTTP / HTTPS:**\n"
        for p in http_list:
            text += f"📍 `{p}`\n"
        text += "───────────────────\n"

    if v2ray_list:
        text += "🔐 **VLESS / TROJAN / SS:**\n"
        for v in v2ray_list:
            # Обрезаем слишком длинные ссылки для красоты
            short_v = v[:40] + "..." if len(v) > 40 else v
            text += f"🔗 [Кликни, чтобы скопировать]({v})\n"
        text += "───────────────────\n"

    # Ссылка на MTProto (обычно это готовые ссылки tg://proxy)
    text += "🛡 **MTPROTO (Telegram):**\n"
    text += "🔗 [Подключить MTProto](https://t.me/proxy?server=exp.proxy.com&port=443&secret=7gAAAAAAAAAAAAAAAAAAAABnb29nbGUuY29t)\n\n"
    
    text += "⚡️ *Обновлено автоматически*\n"
    text += "📢 *Подпишись на наш канал!*"

    url = f"https://api.telegram.org/bot{token}/sendMessage"
    requests.post(url, data={
        "chat_id": chat_id, 
        "text": text, 
        "parse_mode": "Markdown",
        "disable_web_page_preview": True
    })

if __name__ == "__main__":
    send_to_telegram()
