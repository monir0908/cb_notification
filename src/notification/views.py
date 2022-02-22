import logging
import os
from typing import List

from aiohttp import web
from aiohttp.web_request import Request
from aiohttp.web_response import Response

from notification.helpers import decode_token, subscription, unsubscription
from notification.serializers import NotificationSerializer
from notification.validators import get_notification_validator


# @create_country_validator
async def subscriber(request: Request) -> Response:
    request_data = await request.json()
    subscription_token = request_data.get('subscription_token')
    topic_name = request_data.get('topic_name')

    if subscription_token:
        result = await subscription(fcm=request.app['fcm'], tokens=[subscription_token],
                                        topic_name=topic_name)
        logging.info(result)
        if result:
            return web.json_response(data={'message': 'subscribed successfully'}, status=200)

        return web.HTTPBadRequest(text='subscription not created')

    return web.json_response(text='subscription not created', status=201)


async def unsubscriber(request: Request) -> Response:
    request_data = await request.json()
    unsubscription_token = request_data.get('unsubscription_token')
    topic_name = request_data.get('topic_name')

    if unsubscription_token:
        result = await unsubscription(fcm=request.app['fcm'], tokens=[unsubscription_token],
                                        topic_name=topic_name)
        if result:
            return web.json_response(data={'message': 'unsubscribed successfully'}, status=200)

    return web.json_response(text='something went wrong', status=201)


@get_notification_validator
async def get_notifications(request : Request) -> Response:
    request_data = await request.json()
    notification = get_notifications('qcoom_all_user')
    serializer = NotificationSerializer()
    resp = [serializer.format(obj=notification)]
    return web.json_response(data=resp, status=200)

