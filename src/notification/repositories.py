from typing import Dict, Tuple, Union

from mongoengine.errors import DoesNotExist

from notification.models import Notification
from notification.validators import get_notification_validator

@get_notification_validator
async def save_notification(request_data: Dict):
    try:
        notification = Notification()
        notification.title = request_data.get('title')
        notification.body = request_data.get('body')
        notification.topic = request_data.get('topic')
        notification.type = request_data.get('type')
        notification.resource_info = request_data.get('resource_info')
        notification.image = request_data.get('image')
        notification.origin = request_data.get('origin')
        notification.platform = request_data.get('platform')
        notification.country_code = request_data.get('country_code')
        notification.expired_at = request_data.get('expired_at')
        notification.save()
        return True, notification
    except Exception as e:
        print(f'{e.message}')
        return False, e.message

def get_all_user_addresses(topic: str) -> Tuple[bool, Union[Notification, str]]:
    try:
        notifications = Notification.objects(topic=topic)
        return True, notifications
    except DoesNotExist:
        return False, 'user does not exists'