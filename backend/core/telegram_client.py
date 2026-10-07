import os
import django
from django.shortcuts import get_object_or_404

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'backend_api.settings')
django.setup()

from core.models import Dialog

import asyncio

from decouple import config
from telethon import TelegramClient

# Identifiant de l'application disponible depuis (my.telegram.org)
API_ID = config("API_ID")
# Clé secrète de ton application disponible aussi depuis (my.telegram.org)
API_HASH = config("API_HASH")
# Le numéros de telephone du compte Telegram (format : +22700000000)
PHONE_NUMBER = config("PHONE_NUMBER")
# Le point d'entrée, il represente la connexion à Telegram
client = TelegramClient('session', API_ID, API_HASH)


async def sync_dialogs():
    async with client:
        # Recuperation des tous les echanges, grace a la methode 'get_dialogs()',
        # elle renvoie une liste
        dialogs = await client.get_dialogs()
        for dialog in dialogs:
            db_dialog = Dialog.objects.update_or_create(telegram_id=dialog.id, name=dialog.name,
                                                        archived=dialog.archived,
                                                        unread_count=dialog.unread_count, message=dialog.message,
                                                        is_group=dialog.is_group, is_channel=dialog.is_channel)

async def archive_dialog(telegram_id):
    async with client:
        await client.edit_folder(telegram_id, 1)

async def unarchive_dialog(telegram_id):
    async with client:
        await client.edit_folder(telegram_id, 0)

async def delete_dialog(telegram_id):
    dialog = get_object_or_404(Dialog, id=telegram_id)
    async with client:
        await client.delete_dialog(dialog)
        await asyncio.sleep(5)

async def mark_as_read(telegram_id):
    dialog = get_object_or_404(Dialog, id=telegram_id)
    message = dialog.message
    async with client:
        await client.send_read_acknowledge(dialog, message)
