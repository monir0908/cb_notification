from typing import Dict

from notification.models import UserAddress


class NotificationSerializer(object):
    @staticmethod
    def format(obj: UserAddress) -> Dict:
        data = {
            'title': obj.title,
            'body': obj.body,
            'image': obj.image,
            'type': obj.type,
            'resource_info': obj.resource_info,
            'created_at': obj.created_at,
            'expired_at': obj.expired_at
        }
        return data