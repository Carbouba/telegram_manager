# core/views.py

from rest_framework import viewsets
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework import status

from core.models import Dialog, Profile
from core.serializers import DialogSerializer, ProfileSerializer
from .telegram_client import (
    run_telegram,
    sync_dialogs,
    archive_dialog,
    unarchive_dialog,
    delete_dialog,
    mark_as_read,
    sync_profile
)


class UserProfileViewSet(viewsets.ModelViewSet):
    queryset = Profile.objects.all()
    serializer_class = ProfileSerializer

    @action(detail=False, methods=['post', 'get'])
    def sync_user_profile(self, request):
        try:
            run_telegram(sync_profile())

            profile = Profile.objects.first()

            if not profile:
                return Response({'error': 'Profil introuvable'}, status=status.HTTP_404_NOT_FOUND)

            serializer = self.get_serializer(profile)

            return Response(serializer.data, status=status.HTTP_200_OK)
        except Exception as e:
            return Response({'error': str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)


class DialogViewSet(viewsets.ModelViewSet):
    queryset = Dialog.objects.all().order_by('-id')
    serializer_class = DialogSerializer

    # 1. Synchroniser
    @action(detail=False, methods=['post', 'get'])
    def sync(self, request):
        try:
            run_telegram(sync_dialogs())
            return Response({'status': 'Synchronisation terminée avec succès'})
        except Exception as e:
            return Response({'error': str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

    # 2. Marquer comme lu
    @action(detail=True, methods=['post'])
    def mark_read(self, request, pk=None):
        dialog = self.get_object()
        run_telegram(mark_as_read(dialog.telegram_id))

        dialog.unread_count = 0
        dialog.save()

        return Response({'status': f'"{dialog.name}" marqué comme lu'})

    # 3. Archiver
    @action(detail=True, methods=['post'])
    def archive(self, request, pk=None):
        dialog = self.get_object()
        run_telegram(archive_dialog(dialog.telegram_id))

        dialog.archived = True
        dialog.save()

        return Response({'status': f'"{dialog.name}" archivé avec succès'})

    # 4. Désarchiver
    @action(detail=True, methods=['post'])
    def unarchive(self, request, pk=None):
        dialog = self.get_object()
        run_telegram(unarchive_dialog(dialog.telegram_id))

        dialog.archived = False
        dialog.save()

        return Response({'status': f'"{dialog.name}" désarchivé avec succès'})

    # 5. Supprimer
    @action(detail=True, methods=['post'])
    def delete(self, request, pk=None):
        dialog = self.get_object()
        run_telegram(delete_dialog(dialog.telegram_id))

        dialog.delete()

        return Response({'status': f'"{dialog.name}" supprimé avec succès'})
