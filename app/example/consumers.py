import json

from asgiref.sync import async_to_sync
from channels.exceptions import StopConsumer
from channels.generic.websocket import WebsocketConsumer


class TaskConsumer(WebsocketConsumer):

    def connect(self):
        async_to_sync(self.channel_layer.group_add)(
            "celery_task",
            self.channel_name
        )
        self.accept()

    def disconnect(self):
        async_to_sync(self.channel_layer.group_discard)(
            "celery_task",
            self.channel_name
        )
        raise StopConsumer()

    def receive(self, data):
        self.send(data=json.dumps({
            'message': data
        }))

    def celery_task_status(self, data):
        self.send(data=json.dumps({
            'message': data
        }))
