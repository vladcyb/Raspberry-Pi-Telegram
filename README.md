# Raspberry Pi Telegram chatbot


This is an example of a Telegram chatbot that can help you with managing your Raspberry Pi. To bypass Telegram block go to <b>proxy</b> branch.
- In Telegram create a new bot (start chat with </b>BotFather</b>)
- Download this repository on your Raspberry Pi
- Install RPi.GPIO (Python module)
- In main.py replace "YOUR_TOKEN" with the token of your bot
- Connect three LEDs to your Raspberry Pi (to 14, 15 and 18 GPIO pins, use resistors to prevent damage of you Raspberry Pi)
- Run script

Now you can send commands to your chatbot.

This chatbot supports four commands:
- <b>turn on</b> - turn on the GPIO pins
- <b>turn off</b>
- <b>/reboot</b> - reboot Raspberry Pi
- <b>temp</b> get processor temperature
To send the first two commands you can use markup keyboard
