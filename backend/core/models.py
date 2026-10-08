from django.db import models

class Dialog(models.Model):
    telegram_id = models.IntegerField()
    name = models.CharField(max_length=255)
    archived = models.BooleanField(default=False)
    unread_count = models.IntegerField(default=0)
    message = models.TextField(blank=True, null=True, default="")
    is_group = models.BooleanField(default=False)
    is_channel = models.BooleanField(default=False)
    last_message_date = models.DateTimeField(null=True, blank=True)

class Profile(models.Model):
    user_id = models.IntegerField()
    first_name = models.CharField(max_length=255)
    last_name = models.CharField(max_length=255)
    username = models.CharField(max_length=255)
    phone = models.IntegerField()
    picture = models.ImageField(blank=True, null=True)



