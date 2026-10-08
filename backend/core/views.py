# core/views.py

from rest_framework import viewsets
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework import status
from asgiref.sync import async_to_sync

from core.models import Dialog
from core.serializers import DialogSerializer
from .telegram_client import (
    sync_dialogs, 
    archive_dialog, 
    unarchive_dialog, 
    delete_dialog, 
    mark_as_read
)

class DialogViewSet(viewsets.ModelViewSet):
    queryset = Dialog.objects.all()
    serializer_class = DialogSerializer

    # 1. Action de synchronisation
    @action(detail=False, methods=['post'])
    def sync(self, request):
        try:
            async_to_sync(sync_dialogs)()
            return Response(
                {'status': 'Synchronisation terminée avec succès'}, 
                status=status.HTTP_200_OK
            )
        except Exception as e:
            return Response(
                {'error': str(e)}, 
                status=status.HTTP_500_INTERNAL_SERVER_ERROR
            )

    # 2. Archiver
    @action(detail=True, methods=['post'])
    def archive(self, request, pk=None):
        dialog = self.get_object()
        async_to_sync(archive_dialog)(dialog.telegram_id)

        dialog.archived = True
        dialog.save()

        return Response({'status': f'"{dialog.name}" archivé avec succès'})

    # 3. Désarchiver
    @action(detail=True, methods=['post'])
    def unarchive(self, request, pk=None):
        dialog = self.get_object()
        async_to_sync(unarchive_dialog)(dialog.telegram_id)

        dialog.archived = False
        dialog.save()

        return Response({'status': f'"{dialog.name}" désarchivé avec succès'})

    # 4. Supprimer
    @action(detail=True, methods=['post'])
    def delete(self, request, pk=None):
        dialog = self.get_object()
        async_to_sync(delete_dialog)(dialog.telegram_id)

        dialog.delete()

        return Response({'status': f'"{dialog.name}" supprimé avec succès'})

    # 5. Marquer comme lu
    @action(detail=True, methods=['post'])
    def mark_read(self, request, pk=None):
        dialog = self.get_object()
        async_to_sync(mark_as_read)(dialog.telegram_id)

        dialog.unread_count = 0
        dialog.save()

        return Response({'status': f'"{dialog.name}" marqué comme lu'})