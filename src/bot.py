import config
import netboxz
import telebot
import time
import subprocess
import models


def auth(handler):
    def wrapper_handler(message):
        try:
            chat = models.Chat.select().where(id=message.chat.id).get()
        except models.Chat.DoesNotExist:
            return

        print(message.chat.id)
        handler(message)

    return wrapper_handler

bot = telebot.TeleBot(config.token)

@bot.message_handler(commands=["temp"])
@auth
def get_temp(message):
    bot.send_message(message.chat.id, "Front 1: {}C\nFront 2: {}C\nBack: {}C".format(netboxz.temp(1), netboxz.temp(2), netboxz.temp(3)))

@bot.message_handler(commands=["squeue"])
@auth
def get_queue(message):
    res = subprocess.run(['squeue', '-o', '%.5i %.9P %.8j %.8u %.2t %.10M %.1D'], stdout=subprocess.PIPE)
    bot.send_message(message.chat.id, "<pre>{}</pre>".format(res.stdout.decode('utf-8')), parse_mode="HTML")

if __name__ == '__main__':
     bot.polling(none_stop=True, interval=5, timeout=20)
