
from typing import Callable

from typing import Callable, Union, Dict
import functools

from aiohttp import web
from aiohttp.web_response import Response
from aiohttp.web_request import Request

async def get_notification_validator(func : Callable) -> Callable:
    @functools.wraps(func)
    async def wrapper(request: Request) -> Union[Callable, Response]:
        if not request.headers.get('Authorization'):
            return web.HTTPUnauthorized(text='auth token is missing')
        return await func(request)
    return wrapper

async def save_notificatoin_validator(func : Callable) -> Callable:
    @functools.wraps(func)
    async def wrapper(request_data : Dict) -> Union[Callable, Union[bool, str]]:
        if not request_data.get('title'):
            return False, 'notification title missing'
        elif not request_data.get('body'):
            return False, 'notification body missing'
        elif not request_data.get('topic'):
            return False, 'notification topic missing'
        elif not request_data.get('expired_at'):
            return False, 'notification expired_at missing'
        
        return await func(request_data)
    return wrapper
