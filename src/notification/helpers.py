import logging
import os
from typing import Tuple

import aiohttp

from configs import push_service


async def subscription(fcm, tokens, topic_name):
    try:
        result = push_service.subscribe_registration_ids_to_topic(tokens, topic_name)
        return result
    except Exception as err:
        logging.error(err)
        return False


async def unsubscription(fcm, tokens, topic_name):
    try:
        result = push_service.unsubscribe_registration_ids_from_topic(tokens, topic_name)
        return result
    except Exception:
        return False



# def get_topic(topic, to=None):
#     if topic == 'only_evaly_user':
#         topic = ''
#     else:
#         to = '' if type(None) == type(to) else '_' + to
#     return f'{APP_ENV}_{topic}{to}'
