from django.db import models

class Dialog(models.Model):
    telegram_id = models.IntegerField()
    name = models.CharField(max_length=255)
    archived = models.BooleanField(default=False)
    unread_count = models.IntegerField(default=0)
    message = models.TextField(blank=True)
    is_group = models.BooleanField(default=False)
    is_channel = models.BooleanField(default=False)

