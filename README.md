# WEBHOOK_SDWAN_ALERTS

Webhook for SDWAN alarms notification

# INSTALLATION

Clone repository

    git clone https://github.com/joseaher87/WEBHOOK_SDWAN_ALERTS.git

Change to repository directory

    cd WEBHOOK_SDWAN_ALERTS

Create virtual environment

    python -m venv venv


Activate virtual environment

    source venv/bin/activate


install requirements

    pip install -r requirements.txt

# USE

## Ubuntu Server

     10.1.1.100

## vManage

     https://10.1.1.200
     ssh 10.1.1.200

## Routers

SSH

     Router1: 10.1.1.150
     

## credentials

     user01
     P@ssword01

## Start Webhook Server

Connect to ubuntu server via SSH

Move to the repository folder

     cd WEBHOOK_SDWAN_ALERTS

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
