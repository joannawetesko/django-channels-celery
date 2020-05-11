import time

from example.models import CeleryTask

from celery import shared_task

from asgiref.sync import async_to_sync
from channels.layers import get_channel_layer
from django.utils import timezone

import logging

@shared_task(name="example_task")
def example_task(task_id):
    # simulation of the task running
    time.sleep(10)

    # task completed
    task = CeleryTask.objects.get(pk=task_id)
    task.status = "FINISHED"
    task.finished = timezone.now()
    task.save()

    # send a channels notification
    channel_layer = get_channel_layer()
    async_to_sync(channel_layer.group_send)(f'celery_task', {
        "action": "completed",
        "type": "celery_task_status",
        "id": f"{task.pk}",
        "name": f"{task.name}",
        "created": f"{task.created.strftime('%d %b %Y, %-H:%M:%S')}",
        "finished": f"{task.finished.strftime('%d %b %Y, %-H:%M:%S')}",
        "status": f"{task.status}"
    })
    return True