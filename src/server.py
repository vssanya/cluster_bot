from aiohttp import web
import telebot

import config
import tasks

from models import User, Job


async def job_status_post(request):
    job_id = request.match_info['job_id']
    data = await request.json()

    try:
        user = User.select().where(User.token==data.get('token', '')).get() 
    except User.DoesNotExist:
        return web.Resource(status=404)

    job, created = Job.get_or_create(id=data['job_id'], user=user)
    job.status = data['status']
    job.save()

    return web.Response(text='', status=200)

def setup_routes(app):
    res = app.router.add_resource(r'/job/{job_id:\d+}/status')
    res.add_router('POST', job_status_post)

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
