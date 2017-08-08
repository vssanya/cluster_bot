import config
import netboxz
import telebot
import time


bot = telebot.TeleBot(config.token)

last_temp = 0

if __name__ == '__main__':
    while True:
        Tmax = max(map(netboxz.temp, range(1,4)))
        print("Tmax = ", Tmax)

        if Tmax > config.crit_temp and Tmax > last_temp:
            for chat in config.white_chat_list:
                bot.send_message(chat, "Oh it's getting hot")
        last_temp = Tmax
        time.sleep(config.update_time)
