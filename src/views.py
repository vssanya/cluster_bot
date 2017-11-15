from aiohttp import web

import models


async def job_status_post(request):
    token = request.query.get('token', None)
    if token is None:
        return web.Response(status=404)

    try:
        user = models.User.select().where(models.User.token == token).get()
    except models.User.DoesNotExist:
        return web.Response(status=404)

    job_id = request.match_info['job_id']
    data = await request.json()

    job_status = models.JobStatus.create(job_id=job_id, user=user, status=data['status'])
    return web.Response()
