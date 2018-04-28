import requests
from time import sleep
import subprocess
import sys
import re
import json
import RPi.GPIO as GPIO
from datetime import datetime

URL = 'https://api.telegram.org/botYOUR_TOKEN/' # Replace YOUR_TOKEN on the token of your bot

YOUR_TELEGRAM_ID = 159619537 # Change on your Telegram id

# pin numbers
LED1 = 14
LED2 = 15
LED3 = 18

def get_last_update():
    url = URL + 'getUpdates?offset=-1'
    r = requests.get(url)

    if len(r.json()['result']) == 0:
        return None
    return r.json()['result'][0]

def send_message(chat_id, text):
    url = URL + 'sendMessage'

    data = {
        "chat_id": chat_id,
        "text": text,
        "reply_markup": {
            "keyboard": [[
                {
                    "text": "turn on",
                    "callback_data": "1"
                }],
                [{
                    "text": "turn off",
                    "callback_data": "2"
                }]
            ]
        }
    }

    requests.get(url, json=data)


def main():

    send_message(YOUR_TELEGRAM_ID, "I'm up!")

    GPIO.setwarnings(False)
    GPIO.setmode(GPIO.BCM)
    GPIO.setup(LED1, GPIO.OUT)
    GPIO.setup(LED2, GPIO.OUT)
    GPIO.setup(LED3, GPIO.OUT)

    upd = get_last_update()

    if upd:
        last_update_id = upd['update_id']
    else:
        last_update_id = 0

    print('Started')

    while True:
        sleep(1)

        upd = get_last_update()

        if upd:
            update_id = upd['update_id']
        else:
            update_id = 0


        if update_id != last_update_id:

            last_update_id = update_id

            if 'message' in upd:
                message = upd['message']
            elif 'edited_message' in upd:
                message = upd['edited_message']

            who = message['from']
            sender_id =  who['id']

            if sender_id != YOUR_TELEGRAM_ID:
                continue

            message_text = message['text']
            chat_id = message['chat']['id']

            if re.search(r'turn on', message_text, re.IGNORECASE):
                GPIO.output(LED1, 1)
                GPIO.output(LED2, 1)
                GPIO.output(LED3, 1)
            elif re.search(r'turn off', message_text, re.IGNORECASE):
                GPIO.output(LED1, 0)
                GPIO.output(LED2, 0)
                GPIO.output(LED3, 0)
            elif message_text == '/reboot':
                send_message(chat_id, 'Rebooting...')
                subprocess.call(['sudo', 'shutdown', '-r', 'now'])
            elif re.match(r'temp', message_text, re.IGNORECASE):
                proc = subprocess.Popen(['vcgencmd', 'measure_temp'], stdout=subprocess.PIPE)
                line = proc.stdout.read().decode("utf-8")
                send_message(chat_id, line)

if __name__ == '__main__':
    main()
