import json

from asgiref.sync import async_to_sync
from channels.exceptions import StopConsumer
from channels.generic.websocket import WebsocketConsumer
from celery.task.control import revoke

from .tasks import example_task
from .models import CeleryTask

class TaskConsumer(WebsocketConsumer):

    def connect(self):
        async_to_sync(self.channel_layer.group_add)(
            "celery_task",
            self.channel_name
        )
        self.accept()

    def disconnect(self, code):
        async_to_sync(self.channel_layer.group_discard)(
            "celery_task",
            self.channel_name
        )
        raise StopConsumer()

    # receive a socket message
    def receive(self, text_data):
        data = json.loads(text_data)
        if data.get("action") == "new_celery_task":
            self.new_celery_task(data.get("name"))
        elif data.get("action") == "cancel_celery_task":
            self.cancel_celery_task(data.get("id"))

    def celery_task_status(self, text_data):
        self.send(json.dumps({
            'message': text_data
        }))

    # cancel ongoing task
    def cancel_celery_task(self, id):
        task = CeleryTask.objects.get(pk=id)
        if task is not None:
            revoke(task.celery_task_id, terminate=True)

            task.status = "CANCELLED"
            task.save()

            async_to_sync(self.channel_layer.group_send)(f'celery_task', {
                "action": "canceled",
                "type": "celery_task_status",
                "id": f"{task.pk}",
                "name": f"{task.name}",
                "created": f"{task.created.strftime('%d %b %Y, %-H:%M:%S')}",
                "finished": "",
                "status": f"{task.status}"
            })

    # create a new task with a requested name
    def new_celery_task(self, name):
        task = CeleryTask(
            name=name,
            status="STARTED",
        )
        task.save()

        result = example_task.delay(task.pk)
        task.celery_task_id = result.id
        task.save()

        async_to_sync(self.channel_layer.group_send)(f'celery_task', {
            "action": "started",
            "type": "celery_task_status",
            "id": f"{task.pk}",
            "name": f"{task.name}",
            "created": f"{task.created.strftime('%d %b %Y, %-H:%M:%S')}",
            "finished": "",
            "status": f"{task.status}"
        })

