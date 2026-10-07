from rest_framework import serializers
from .models import Dialog
class DialogSerializer(serializers.ModelSerializer):
    class Meta:
        model = Dialog
        fields = [
            'telegram_id', 'name', 'archived', 'unread_count',
            'id','message', 'is_group', 'is_channel'
        ]