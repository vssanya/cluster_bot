import logging

from aiohttp import web
import telebot

import config
import tasks

import views


def setup_routes(app):
    app.router.add_post(r'/job/{job_id:\d+}/status', views.job_status_post)
    app.router.add_post(r'/job/{job_id:\d+}/message', views.job_message_post)

async def start_background_tasks(app):
    app['check_cluster_temp'] = app.loop.create_task(tasks.check_cluster_temp(app))
    #app['check_swap_usage'] = app.loop.create_task(tasks.check_swap_usage(app))
    app['start_group_message'] = app.loop.create_task(tasks.start_group_message(app))

async def cleanup_background_tasks(app):
    app['check_cluster_temp'].cancel()
    await app['check_cluster_temp']

    #app['check_swap_usage'].cancel()
    #await app['check_swap_usage']

    app['start_group_message'].cancel()
    await app['start_group_message']

app = web.Application()
logging.basicConfig(level=logging.DEBUG)
setup_routes(app)

app['bot'] = telebot.TeleBot(config.token)

app.on_startup.append(start_background_tasks)
app.on_cleanup.append(cleanup_background_tasks)

web.run_app(app, host=config.host, port=config.port)
