# chronogg_telebot
Personal Telegram bot for site chrono.gg that can automate some task 
for you. Mainly coin spinning.
Because coins are rewards for looking at site, every spin is always
accompanied with Today's sale.

Bot wont answer anyone other than configured user.

Bot will coin spin evey day, some time from 18:00-21:00 (time is random)

Bot can do this commands on demand:
- /start | /help - List of commands
- /sale - Game on sale
- /spin - Coin spin
- /balance - Show coin balance
- /update "token" - Update Authorization Token

Usage:
-
- Self run:
    - Install all requirements with **pip install -r requirements.txt**
    - Change config-example.json -> config.json and fill it
    - Run bot.py
- Docker:
  - Download settings/config-example.json
  - Change config-example.json -> config.json and fill it
  - Pull from docker hub: **docker pull fildah/chronogg_telebot**
  - Create container with connected volume to directory where is config.json

Config:
-
- chrono: token - explained lower
- bot: token - [https://core.telegram.org/bots](https://core.telegram.org/bots) and [https://telegram.me/botfather](https://telegram.me/botfather)
- bot: username - [https://telegram.me/userinfobot](https://telegram.me/userinfobot)
- bot: chat_id - [https://telegram.me/userinfobot](https://telegram.me/userinfobot)
- logging: level - 40 for ERROR only, 10 for DEBUG


Getting token from chrono.gg:
- Go to https://chrono.gg/ and login
- Press F12 on keyboard -> Go to the network tab -> Filter by XHR
- Keep the network tab open and refresh the page
- Select "account" and copy Authorization header under 
*Request Headers". It should start with "JWT". Copy whole token.

Logging: Logs are saved in settings/log.log


