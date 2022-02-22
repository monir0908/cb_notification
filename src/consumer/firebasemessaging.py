import json
import logging
import os

from pyfcm import FCMNotification

from configs import push_service

push_service = FCMNotification(api_key=os.environ.get('FCM_SERVER_KEY'))

def sendNotification(body):
    data = json.loads(body)
    if data['topic'] :
        result = push_service.notify_topic_subscribers(topic_name=body['topic'], message_title=data['title'], message_body=data['body'])
        logging.info(result)

