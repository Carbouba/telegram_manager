from rest_framework import serializers
from .models import Dialog, Profile
class DialogSerializer(serializers.ModelSerializer):
    class Meta:
        model = Dialog
        fields = [
            'telegram_id', 'name', 'archived', 'unread_count',
            'id','message', 'is_group', 'is_channel', 'last_message_date'
        ]

class ProfileSerializer(serializers.ModelSerializer):
    class Meta:
        model = Profile
        fields = [
            'first_name', 'last_name', 'username', 'phone', 'user_id'
        ]

