import asyncio
import config
import netboxz
import telebot
import time
import models


last_temp = 0

async def check_cluster_temp(app):
    while True:
        Tmax = max(map(netboxz.temp, range(1,4)))
        print('Check temp: Tmax = {}'.format(Tmax))

        if Tmax > config.crit_temp and Tmax > last_temp:
            for chat in models.Chat.select().where(models.Chat.user == None):
                app['bot'].send_message(chat.id, "Oh it's getting hot")
        last_temp = Tmax

        await asyncio.sleep(config.update_time)
