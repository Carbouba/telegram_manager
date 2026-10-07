from rest_framework import viewsets
import asyncio
from core.models import Dialog
from core.serializers import DialogSerializer
from .telegram_client import sync_dialogs


class DialogViewSet(viewsets.ModelViewSet):
    # asyncio.run(sync_dialogs())
    queryset = Dialog.objects.all()
    serializer_class = DialogSerializer