import time

from example.models import CeleryTask
from celery import shared_task


@shared_task(name="example_task")
def example_task(task_id):
    # simulation of the task running
    time.sleep(5)

    # task completed
    task = CeleryTask.objects.get(pk=task_id)
    task.status = "DONE"
    task.save()

    # send a channels notification
    # TODO