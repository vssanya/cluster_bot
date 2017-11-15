import asyncio
import time

import config
import netboxz
import models
import memstat


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


async def check_swap_usage(app):
    cnt = 0

    while True:
        cnt += 1

        if (cnt == config.swap_update_time_multiplier):
            cnt = 0

            bad_nodes, swap_total, swap_free = memstat.get_nodes_overusing_swap(config.node_list, config.swap_overuse_threshold)
            if len(bad_nodes) > 0:
                message = 'Warning: swap overuse detected on nodes: '
                for i in range(len(bad_nodes)):
                    message += '\n' + bad_nodes[i] + ':\t'
                    message += ' used {0:.1f}G of {1:.1f}G'.format(
                        (swap_total[i] - swap_free[i]) / 1048576,
                        swap_total[i] / 1048576)

                for chat in models.Chat.select().where(models.Chat.user == None):
                    app['bot'].send_message(chat.id, message)

        await asyncio.sleep(config.update_time)
