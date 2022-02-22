from aiohttp import web

from configs import V1_PATTERNS
from notification.views import (
    subscriber,
    unsubscriber
)


notification_public_urls = [
    web.post(f'{V1_PATTERNS}/public/subscribe', subscriber),
    web.post(f'{V1_PATTERNS}/public/unsubscribe', unsubscriber),
]

provider_system_urls = [
    
]

notification_routes = notification_public_urls + provider_system_urls
