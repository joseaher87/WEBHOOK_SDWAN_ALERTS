# Webhook Testing

All devices are reachable

## Ubuntu Server

     10.1.1.100

## vManage

     https://10.1.1.200:44040/
     ssh 10.1.1.200:44040

## Routers

SSH

     Router1: 10.1.1.150:
     

## credentials

     user01
     P@ssword01

## Start Webhook Server

Connect to ubuntu server via SSH

Move to the Scripts Folder

     cd scripts

Activate the virtual environment

     source venv/bin/activate

Start the webhook service

     uvicorn webhook:app --host 0.0.0.0

## Test Webhook Service

### Laptop Test

Open your laptop terminal and send the following commands

     ping  10.1.1.100

     curl -X POST http://10.1.1.100:8000/webhook \
          -H "Content-Type: application/json" \
          -d '{"message": "Hello, webhook LAPTOP!"}'

Expect result is ping should be succesful and you should get a webex message

### vManage Test

connect to vmanage SSH and test from CLI terminal

     ping  10.1.1.100

for CURL you need to move to vmanage shell

     vshell

Once on the shell send the CURL command

     curl -X POST http://10.1.1.100:8000/webhook \
          -H "Content-Type: application/json" \
          -d '{"message": "Hello, webhook! VMANAGE"}'

Expect result is ping should be succesful and you should get a webex message

### Verify Notification Settings on vManage

On vManage GUI go to Adminstration > Settings

Go to Alarm Notifications and click on edit

Verify the service is enabled

Click on Cancel

### Verify Alarm Notification Config on vManage

On vManage GUI go to Monitor > Logs

Click on Alarm Notifications

Create or edit the existing Notification Rule "TEST NOTIFICATION"

Confirm is set to all severity levels and the alarm name is "BFD TLOC DOWN" (You can customize it).

Scroll down to the WebHook section and verify URL

     http://10.1.1.100:8000/webhook

Configure user and password for webhook.

Scroll down to the Select Devices and confirm the routers are added


### Alarm Notification Test

Connect to Router01 router via ssh (HUB Router) and reload the device

     reload

After a few seconds you should receive the webex messages

### Verify script code

Go back to the server and end the Webhook service by doing a CTRL + C

To se the script on the terminal use the command

    cat webhook.py

You will see the following code

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



Note: "replace recipient ID from webex teams group" for your own recipient from a webex group.