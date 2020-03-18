from celery import shared_task


@shared_task(name="example_task")
def hello():
    print('Hello there!')