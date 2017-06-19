import config
import netboxz
import telebot
import time


bot = telebot.TeleBot(config.token)

if __name__ == '__main__':
    while True:
        for i in range(3)
            T = netboxz.temp(i+1)
            if T > config.crit_temp:
                bot.send_message(config.group, "Oh it's getting hot")
                break
        time.sleep(config.update_time)
