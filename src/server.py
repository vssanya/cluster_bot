from aiohttp import web
import telebot

import config
import tasks

import views


def setup_routes(app):
    app.router.add_post(r'/job/{job_id:\d+}/status', views.job_status_post)

async def start_background_tasks(app):
    app['check_cluster_temp'] = app.loop.create_task(tasks.check_cluster_temp(app))

async def cleanup_background_tasks(app):
    app['check_cluster_temp'].cancel()
    await app['check_cluster_temp']

app = web.Application()
setup_routes(app)

app['bot'] = telebot.TeleBot(config.token)

app.on_startup.append(start_background_tasks)
app.on_cleanup.append(cleanup_background_tasks)

web.run_app(app, host="localhost", port=8080)
