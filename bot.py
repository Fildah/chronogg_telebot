import datetime
import json
import logging
import os
import random
import time

from telegram.ext import CommandHandler
from telegram.ext import MessageHandler, Filters
from telegram.ext import Updater

from chronogg import Chrono


#  Global variable
current_path = os.path.dirname(os.path.abspath(__file__))


class Robot:
    def __init__(self, config):
        self.config = config
        self.chrono = Chrono(config['chrono']['token'])
        self.updater = Updater(token=config['bot']['token'])
        self.dispatcher = self.updater.dispatcher
        start_owner_handler = CommandHandler(
            ['start', 'help'], self.start_owner, filters=Filters.user(username=config['bot']['username']))
        self.dispatcher.add_handler(start_owner_handler)
        start_not_owner_handler = CommandHandler(
            'start', self.start_not_owner, filters=(~ Filters.user(username=config['bot']['username'])))
        self.dispatcher.add_handler(start_not_owner_handler)
        sale_handler = CommandHandler(
            'sale', self.sale, filters=Filters.user(username=config['bot']['username']))
        self.dispatcher.add_handler(sale_handler)
        spin_handler = CommandHandler(
            'spin', self.spin, filters=Filters.user(username=config['bot']['username']))
        self.dispatcher.add_handler(spin_handler)
        balance_handler = CommandHandler(
            'balance', self.balance, filters=Filters.user(username=config['bot']['username']))
        self.dispatcher.add_handler(balance_handler)
        update_handler = CommandHandler(
            'update', self.update_token, pass_args=True, filters=Filters.user(username=config['bot']['username']))
        self.dispatcher.add_handler(update_handler)
        unknown_handler = MessageHandler(
            Filters.user(username=config['bot']['username']) & (Filters.command | Filters.text), self.unknown)
        self.dispatcher.add_handler(unknown_handler)
        self.updater.job_queue.run_daily(
            self.spin_job, time=datetime.time(18, 5, 0))

    def run(self):
        self.updater.start_polling()
        return

    @staticmethod
    def start_owner(bot, update):
        bot.send_message(chat_id=update.message.chat_id, text='''Here are your commands:\n
/start | /help - List of commands
/sale - Game on sale
/spin - Coin spin
/balance - Show coin balance
/update \"token\" - Update Authorization Token
''')

    @staticmethod
    def start_not_owner(bot, update):
        bot.send_message(chat_id=update.message.chat_id,
                         text="This is private bot. If you want to know more, go to:"
                              "https://github.com/Fildah/chronogg_telebot")

    def sale(self, bot, update):
        result = self.chrono.get_sale()
        bot.send_message(chat_id=update.message.chat_id, text=result)

    def spin(self, bot, update):
        result = self.chrono.coin_spin()
        if result == 'Coin spin successful.':
            result = result + '\nCoin balance: ' + self.chrono.get_coin_balance() \
                     + '\nToday\'s deal' + self.chrono.get_sale()
        bot.send_message(chat_id=update.message.chat_id, text=result)

    def balance(self, bot, update):
        result = self.chrono.get_coin_balance()
        bot.send_message(chat_id=update.message.chat_id, text=result)

    def update_token(self, bot, update, args):
        if len(args) is not 2:
            bot.send_message(chat_id=update.message.chat_id, text='Wrong format of token. It has to start JWT.')
        elif args[0] != 'JWT':
            bot.send_message(chat_id=update.message.chat_id, text='Wrong format of token. It has to start JWT.')
        else:
            token = args[0] + ' ' + args[1]
            self.chrono.set_token(token)
            self.config['chrono']['token'] = token
            with open(current_path + '\\settings\\config.json', 'w') as json_file:
                json.dump(self.config, json_file, indent=2)
            bot.send_message(chat_id=update.message.chat_id, text='Token updated.')

    @staticmethod
    def unknown(bot, update):
        bot.send_message(chat_id=update.message.chat_id,
                         text="Sorry, I didn't understand that command. Try /start for more info.")

    def spin_job(self, bot, job):
        spin_result = self.chrono.coin_spin()
        if spin_result == 'Coin spin successful.':
            coin_balance = self.chrono.get_coin_balance()
            sale_result = self.chrono.get_sale()
            bot.send_message(chat_id=self.config['bot']['chat_id'],
                             text=spin_result + '\nCoin balance: ' + coin_balance + '\nToday\'s deal' + sale_result)
        else:
            bot.send_message(chat_id=self.config['bot']['chat_id'], text=spin_result)


if __name__ == "__main__":
    try:
        with open(os.path.join(current_path, 'settings', 'config.json'), 'r') as conf_file:
            config = json.load(conf_file)
    except IOError:
        logging.basicConfig(filename=os.path.join(current_path, 'settings', 'log.log'), filemode='a',
                            format='%(asctime)s %(levelname)s:%(message)s', level=10)
        logging.error('config.json missing or not in right format', exc_info=True)
    logging.basicConfig(filename=os.path.join(current_path, 'settings', 'log.log'), filemode='a',
                        format='%(asctime)s %(levelname)s:%(message)s', level=config['logging']['level'])
    rob = Robot(config)
    rob.run()
    pass
