from typing_extensions import Required
import uuid
from datetime import datetime

from mongoengine import (
    Document,
    StringField,
    SequenceField,
    DateTimeField,
)

from configs import COUNTRY_CODE_MAP


class Notification(Document):
    notification_type_choices = (
        'announcement',
        'offer',
        'order',
        'others',
    )
    origin_choices = (
        'ios',
        'android',
        'web',
    )
    platform_choices = (
        'cb',
    )
    country_choices = (
        'bd',
    )

    sequence = SequenceField()
    title = StringField(max_length=350, required=True)
    body = StringField(max_length=150, required=True)
    topic = StringField(max_length=150, required=True)
    resource_info = StringField(max_length=250, required=False)
    image = StringField(required=False)
    type = StringField(choices=notification_type_choices, max_length=25)
    origin = StringField(choices=origin_choices, max_length=10)
    platform = StringField(choices=platform_choices, max_length=10)
    country_code = StringField(choices=country_choices, max_length=3)
    created_at = DateTimeField(default=datetime.utcnow)
    expired_at = DateTimeField(required=True)

    meta = {
        'indexes': [
            {
                'fields': ['-created_at'],
                'name': 'notification_created_at_idx'
            }
        ],
        'collection': 'notifications',
        'db_alias': 'default',
        'ordering': ['-created_at']
    }
