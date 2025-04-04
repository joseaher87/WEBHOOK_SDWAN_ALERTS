
from fastapi import FastAPI, Request
from webexteamssdk import WebexTeamsAPI
import os

def send_message(message):
    TOKEN = os.environ.get('WEBEX_TOKEN')
    recipient = 'recipient ID from webex teams group'
    webex = WebexTeamsAPI(TOKEN)
    webex.messages.create(markdown=message,roomId=recipient)
    print(f'Message sent!')

app = FastAPI()

@app.post('/webhook')
async def webhook(request: Request):

    try:
        payload = await request.json()
        message = payload.get("message")
        values = payload.get("values")[0]
        systemip = values.get("system-ip")
        color = values.get("color")
        hostname = values.get("host-name")
        siteid = values.get("site-id")
        severity = payload.get("severity")

        webex_message = f'*** {message} ***\nSeverity: {severity}\nSite: {siteid}\nHostname: {hostname}\nSystem IP: {systemip}\nColor: {color}'
        _ = send_message(webex_message)

    except Exception as e:
        webex_message = str(payload)
        _ = send_message(webex_message)

        print(e)