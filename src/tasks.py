import asyncio
import time

import config
import netboxz
import models
import memstat
import subprocess

last_temp = 0

async def check_cluster_temp(app):
    while True:
        Tmax = max(map(netboxz.temp, range(1,4)))
        print('Check temp: Tmax = {}'.format(Tmax))

        if Tmax > config.crit_temp and Tmax > last_temp:
            for chat in models.Chat.select().where(models.Chat.user == None):
                app['bot'].send_message(chat.id, "Oh it's getting hot")
        last_temp = Tmax

        await asyncio.sleep(config.temp_update_time)


async def check_swap_usage(app):
    while True:
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

        await asyncio.sleep(config.mem_update_time)

async def check_disk_usage(app):
    base_folder = config.disk_usage_monitor_folder
    while True:
        data = subprocess.check_output(['du', '--max-depth=1', base_folder]).decode('utf-8').split('\n')
        stats = dict(map(lambda s: (s.split('\t')[1].replace(base_folder, ''), int(s.split('\t')[0])), [x for x in data if x != '']))
        if (stats[''] > config.disk_usage_threshold):
            message = 'Running out of space in /share: {0:0.3f}G [{1} bytes] used'.format(stats[''] / (1024 * 1024 * 1024), stats[''])
            message += '\nTop users:'
            max_len = max(list(map(lambda x: len(x), stats.keys())))
            for k, v in sorted(stats.items(), key=lambda x: x[1], reverse=True):
                if k != '':
                    message += '\n{0}  {1:0.3f}G'.format(k.ljust(max_len, ' '), v / (1024 * 1024 * 1024))

            for chat in models.Chat.select().where(models.Chat.user == None):
                app['bot'].send_message(chat.id, message)

        await asyncio.sleep(config.disk_usage_update_time)