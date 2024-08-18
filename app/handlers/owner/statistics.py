from aiogram import Router
from aiogram.filters import Command
from aiogram.types import Message
from aiogram_dialog import DialogManager

from app.filters.is_owner import IsOwner
from app.dialogs.moderation_dialog import ModerationDialog

router = Router()


@router.message(IsOwner(is_owner=True), Command(commands=["stats"]))
async def stats_handler(message: Message, api):
    count = await api.get_users_count()

    await message.answer(
        f"📊 <b>Number of bot users -</b> <code>{count}</code>"
    )


@router.message(IsOwner(is_owner=True), Command(commands=["moderate"]))
async def moderate_handler(
    message: Message, dialog_manager: DialogManager
):
    await dialog_manager.start(ModerationDialog.main)
