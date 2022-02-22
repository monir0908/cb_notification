import asyncio
import logging
from typing import Dict

from aiohttp import web
from aiohttp.web import Application, json_response, run_app
from aiohttp.web_request import Request
from aiohttp.web_response import Response

import aio_pika
import aioredis
from aiohttp_middlewares import cors_middleware
from aiohttp_middlewares.cors import DEFAULT_ALLOW_HEADERS
from mongoengine import connect, disconnect

from configs import DEBUG, RABBITMQ_URL, REDIS_HOST, CORS_ALLOW_ORIGINS, push_service
from configs.db import init_db_conn
from middleware import renderer, auth_middleware
from notification.urls import notification_routes


loop = asyncio.get_event_loop()

logger = logging.getLogger(__name__)


async def health_check(request: Request) -> Response:
    data: Dict = {
        'message': 'jmr notification service',
        'data': {
            'request_method': request.method.lower(),
        }
    }
    return json_response(data=data, status=200)


async def on_start_up(application: Application):
    try:
        logger.info('mongodb connection started')
        application['db'] = init_db_conn(loop=loop)
        logger.info('mongodb connection completed')
        logger.info('redis connection started')
        application['redis'] = await aioredis.create_redis_pool(REDIS_HOST)
        logger.info('redis connection done')
        application['rabbitmq'] = await aio_pika.connect_robust(RABBITMQ_URL, loop=loop)
        logger.info('rabbitmq connection done')
        application['fcm'] = push_service
    except (ConnectionError, Exception):
        logger.info('trying to establish connection after 2 sec')
        await asyncio.sleep(2)


async def on_app_close(application: Application):
    try:
        _ = application['db']
        disconnect(alias='default')
        logger.info('mongodb connection disconnected')
        application['redis'].close()
        await application['redis'].wait_closed()
        logger.info('redis connection disconnected')
        application['rabbitmq'].close()
        logger.info('rabbitmq connection disconnected')
    except (Exception, ConnectionError) as e:
        logger.info(f'trying to reconnect: {e}')


app = Application(
    middlewares=[
        renderer,
        auth_middleware,
        cors_middleware(
            allow_all=True,
            allow_headers=DEFAULT_ALLOW_HEADERS + ('SECRET-KEY',),
            origins=CORS_ALLOW_ORIGINS,
        ),
    ]
)

app.on_startup.append(on_start_up)
app.on_shutdown.append(on_app_close)
if DEBUG:
    logging.basicConfig(level=logging.DEBUG)

app.add_routes([web.get('/api/health', health_check)])
app.add_routes(notification_routes)

if not DEBUG:
    run_app(app=app, port=3000)
