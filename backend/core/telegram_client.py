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


async def ensure_connected():
    if not client.is_connected():
        await client.connect()

async def sync_dialogs():
    await ensure_connected()
    dialogs = await client.get_dialogs()

    for dialog in dialogs:
        await Dialog.objects.aupdate_or_create(
            telegram_id=dialog.id,
            defaults={
                'name': dialog.name or "Sans nom",
                'archived': bool(dialog.archived),
                'unread_count': dialog.unread_count,
                'message': dialog.message.message if dialog.message else "",
                'is_group': dialog.is_group,
                'is_channel': dialog.is_channel
            }
        )

async def archive_dialog(telegram_id):
    await ensure_connected()
    entity = await client.get_entity(telegram_id)
    await client.edit_folder(entity, 1)

async def unarchive_dialog(telegram_id):
    await ensure_connected()
    entity = await client.get_entity(telegram_id)
    await client.edit_folder(entity, 0)


async def delete_dialog(telegram_id):
    await ensure_connected()
    entity = await client.get_entity(telegram_id)
    await client.delete_dialog(entity)

async def mark_as_read(telegram_id):
    dialog = get_object_or_404(Dialog, telegram_id=telegram_id)
    entity = await client.get_entity(telegram_id)
    await client.send_read_acknowledge(entity)
