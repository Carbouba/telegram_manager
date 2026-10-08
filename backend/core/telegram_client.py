# core/telegram_client.py

import asyncio
import threading
from decouple import config
from telethon import TelegramClient
from core.models import Dialog

API_ID = config("API_ID")
API_HASH = config("API_HASH")

# 1. Création d'une boucle d'événements UNIQUE et PERMANENTE dans un thread dédié
_loop = asyncio.new_event_loop()

def _start_background_loop(loop):
    asyncio.set_event_loop(loop)
    loop.run_forever()

_thread = threading.Thread(target=_start_background_loop, args=(_loop,), daemon=True)
_thread.start()

# 2. On attache explicitement Telethon à cette boucle unique
client = TelegramClient('session', API_ID, API_HASH, loop=_loop)

# 3. Utilitaire pour exécuter n'importe quelle coroutine Telethon sur la boucle permanente
def run_telegram(coro):
    """Exécute une fonction asynchrone sur la boucle dédiée de Telethon et attend son résultat."""
    future = asyncio.run_coroutine_threadsafe(coro, _loop)
    return future.result()


# --- FONCTIONS METIER TELEGRAM ---

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
                'is_channel': dialog.is_channel,
                'last_message_date': dialog.message.date if dialog.message else None,
            }
        )

async def mark_as_read(telegram_id):
    await ensure_connected()
    entity = await client.get_entity(telegram_id)
    await client.send_read_acknowledge(entity)

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