import config
import netboxz
import telebot
import time
import subprocess


def auth(handler):
    def wrapper_handler(message):
        print(message.chat.id)
        if message.chat.id in config.white_chat_list:
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
     bot.polling(none_stop=True)
