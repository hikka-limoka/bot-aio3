from aiogram import Router
from aiogram.filters import Command
from aiogram.types import Message

router = Router()


@router.message(Command(commands=["devs"]))
async def cmd_devs(message: Message, api):
    devs = await api.get_devs()

    text = "👥 <b>Developers:</b>\n\n"

    for dev in devs:
        text += f"◽️ <i>@{dev['username']}</i> - {dev['git']}\n"

    await message.answer(text, disable_web_page_preview=True)
