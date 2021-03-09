import telebot
import time
import subprocess
import tabulate

import config
import netboxz
import memstat
from models import *
import slurm


def auth(handler):
    def wrapper_handler(message):
        print("Message from ", message.chat.id)
        try:
            chat = Chat.select().where(Chat.id == message.chat.id).get()
        except Chat.DoesNotExist:
            return

        handler(message, chat.user)

    return wrapper_handler

bot = telebot.TeleBot(config.token)

@bot.message_handler(commands=["job_status"])
@auth
def get_job_status(message, user):
    running_jobs = JobStatus.select().where(JobStatus.user == user and JobStatus.status > 0.0).group_by(JobStatus.job_id)

    data = []
    for job in running_jobs[-30:]:
        last_job = JobStatus.select().where(JobStatus.job_id == job.job_id).order_by(JobStatus.time.desc()).get()
        if last_job.status != 1.0 and last_job.status != 0.0:
            start_job = JobStatus.select().where(JobStatus.job_id == job.job_id).order_by(JobStatus.time.asc()).get()
            estimate_time = str((last_job.time - start_job.time)*(1/last_job.status - 1))

            job_name = slurm.get_job_name_by_id(job.job_id)
            if job_name != None:
                data.append([job.job_id, slurm.get_job_name_by_id(job.job_id), last_job.status*100, estimate_time])

    table = tabulate.tabulate(data, headers=['ID', 'Name', 'Status %', 'Est. time (h:m:s)']) 
    bot.send_message(message.chat.id, '<pre>{}</pre>'.format(table), parse_mode='HTML')

@bot.message_handler(commands=["temp"])
@auth
def get_temp(message, user):
    data = [
            ['Front 1', netboxz.temp(1)],
            ['Front 2', netboxz.temp(2)],
            ['Back'   , netboxz.temp(3)],
    ]
    table = tabulate.tabulate(data, headers=['Loc', 'Temp (C)'])
    bot.send_message(message.chat.id, '<pre>{}</pre>'.format(table), parse_mode='HTML')

@bot.message_handler(commands=["login"])
def login(message):
    try:
        chat = Chat.select().where(Chat.id == message.chat.id).get()
        bot.send_message(message.chat.id, "Already logged in")
    except Chat.DoesNotExist:
        args = message.text.split()
        if len(args) == 2:
            token = args[1]
            try:
                user = User.select().where(User.token == token).get()
            except User.DoesNotExist:
                bot.send_message(message.chat.id, "Login failed")
                return

            Chat.create(user=user, id=message.chat.id)
            bot.send_message(message.chat.id, "Login successful")
        else:
            bot.send_message(message.chat.id, "Login failed")

@bot.message_handler(commands=["squeue"])
@auth
def get_queue(message, user):
    res = subprocess.run(['squeue', '-o', '%.5i %.9P %.8j %.8u %.2t %.10M %.1D'], stdout=subprocess.PIPE)
    bot.send_message(message.chat.id, "<pre>{}</pre>".format(res.stdout.decode('utf-8')), parse_mode="HTML")

@bot.message_handler(commands=["memstat"])
@auth
def get_memstat(message, user):
    memdata = memstat.format_memdata(config.node_list)
    bot.send_message(message.chat.id, "<pre>{}</pre>".format(memdata), parse_mode="HTML")

if __name__ == '__main__':
    if False:
        from aiohttp import web

        app = web.Application()

        async def handler(request):
            if request.match_info.get('token') == bot.token:
                request_body_dict = await request.json()
                update = telebot.types.Update.de_json(request_body_dict)
                bot.process_new_updates([update])
                return web.Response()
            else:
                return web.Response(status=403)

        app.router.add_post("/bot/{token}/", handler)

        bot.remove_webhook()
        bot.set_webhook(url=config.webhook_url_base + config.webhook_url_path)

        web.run_app(app, host=config.webhook_host, port=config.webhook_port)
    else:
        import time
        #bot.delete_webhook()
        while True:
            try:
                bot.polling()
            except Exception as e:
                print(e)
                time.sleep(1)
