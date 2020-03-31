from django.db import models

class CeleryTask(models.Model):
    name = models.CharField(max_length=255)
    created = models.DateTimeField(auto_now_add=True)
    status = models.CharField(max_length=255, null=True, blank=True)

    def __str__(self):
        return self.name