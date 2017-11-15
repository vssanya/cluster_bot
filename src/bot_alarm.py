import config
import netboxz
import telebot
import time


def check_temp(bot):
    for i in range(3):
        T = netboxz.temp(i+1)
        if T > config.crit_temp:
            for chat in config.white_chat_list:
                bot.send_message(chat, "Oh it's getting hot")
            break


def check_swap_usage(bot):
    bad_nodes, swap_total, swap_free = memstat.get_nodes_overusing_swap(config.node_list, config.swap_overuse_threshold)
    if len(bad_nodes) > 0:
        message = 'Warning: swap overuse detected on nodes: '
        for i in range(len(bad_nodes)):
            message += '\n' + bad_nodes[i] + ':\t'
            message += ' used {0:.1f}G of {1:.1f}G'.format(
                (swap_total[i] - swap_free[i]) / 1048576,
                swap_total[i] / 1048576)
        for chat in config.white_chat_list:
            bot.send_message(chat, message)


bot = telebot.TeleBot(config.token)


if __name__ == '__main__':
    cnt = 0
    while True:
        cnt += 1
        check_temp(bot)
        if (cnt == config.swap_update_time_multiplier):
            cnt = 0
            check_swap_usage(bot)

        time.sleep(config.temp_update_time)

