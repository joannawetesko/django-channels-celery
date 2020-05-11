# Generated by Django 2.2.10 on 2020-05-11 11:45

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='CeleryTask',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=255)),
                ('created', models.DateTimeField(auto_now_add=True)),
                ('finished', models.DateTimeField(blank=True, null=True)),
                ('status', models.CharField(blank=True, max_length=255, null=True)),
                ('celery_task_id', models.CharField(blank=True, max_length=255, null=True)),
            ],
        ),
    ]