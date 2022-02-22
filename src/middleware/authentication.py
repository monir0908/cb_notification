import logging
from typing import List

from aiohttp import web
from aiohttp.web_exceptions import HTTPInternalServerError, HTTPMethodNotAllowed, HTTPNotFound
from aiohttp.web_request import Request

from base import decode
from configs import CORS_HEADERS

logger = logging.getLogger(__name__)

WHITELIST = {
    'GET': [
        '/',
        '/api/health',
    ],
}


@web.middleware
async def auth_middleware(request: Request, handler: web.Callable) -> web.Response:
    if request.method == 'OPTIONS':
        return web.json_response({'success': True}, status=200, headers=CORS_HEADERS)
    if not WHITELIST.get(request.method) or request.path not in WHITELIST.get(request.method):
        if not request.headers.get('Authorization'):
            return web.HTTPUnauthorized(text='auth token is missing')
        auth_header: List = request.headers['Authorization'].split(' ')
        if len(auth_header) < 2:
            return web.HTTPUnauthorized(text='invalid auth header')
        token: str = auth_header[1]
        payload = await decode(token=token)
        if not payload:
            return web.HTTPUnauthorized(text='token has expired')
        setattr(request, 'user', payload)
    try:
        response = await handler(request)
        return response
    except HTTPMethodNotAllowed:
        return web.HTTPMethodNotAllowed(text=f'{request.method} is not allowed method',
                                        allowed_methods=[], method=request.method, headers=CORS_HEADERS)
    except HTTPNotFound:
        return web.HTTPNotFound(text='requested url not found', headers=CORS_HEADERS)
    # except (HTTPInternalServerError, TypeError, ValueError) as err:
    #     logger.error(f'internal server error occurred: {err}')
    #     return web.HTTPInternalServerError(text='something went wrong', headers=CORS_HEADERS)
