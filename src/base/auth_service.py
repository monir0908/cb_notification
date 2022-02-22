from typing import Dict

from aiohttp import ClientSession

from configs import AUTH_HOST


async def decode(token: str) -> Dict:
    url: str = f'{AUTH_HOST}/api/v1.0/system/users/decode-token'
    headers = {
        'Authorization': token
    }
    async with ClientSession() as client:
        async with client.get(url=url, headers=headers) as resp:
            if resp.status == 200:
                return await resp.json()
            return dict()
