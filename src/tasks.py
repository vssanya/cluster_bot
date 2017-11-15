import asyncio
import config
import netboxz
import telebot
import time


last_temp = 0

async def check_cluster_temp(app):
    while True:
        print('Check temp')

        Tmax = max(map(netboxz.temp, range(1,4)))
        if Tmax > config.crit_temp and Tmax > last_temp:
            for chat in config.white_chat_list:
                app['bot'].send_message(chat, "Oh it's getting hot")
        last_temp = Tmax

        await asyncio.sleep(config.update_time)
