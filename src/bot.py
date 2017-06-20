import config
import netboxz
import telebot
import time


bot = telebot.TeleBot(config.token)

@bot.message_handler(commands=["temp"])
def get_temp(message):
    print(message.chat.id)
    if message.chat.id in config.white_chat_list:
        bot.send_message(message.chat.id, "Front 1: {}C\nFront 2: {}C\nBack: {}C".format(netboxz.temp(1), netboxz.temp(2), netboxz.temp(3)))

if __name__ == '__main__':
     bot.polling(none_stop=True)
