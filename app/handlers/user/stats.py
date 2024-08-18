from aiogram import Router
from aiogram.filters import Command
from aiogram.types import Message

router = Router()


@router.message(Command(commands=["stats"]))
async def stats_handler(message: Message, api):
    count = await api.get_users_count()
    modules = len(await api.get_all_modules())

    await message.answer(
        f"📊 <b>Number of bot users -</b> <code>{count}</code>\n"
        f"📦 <b>Number of modules -</b> <code>{modules}</code>"
    )
