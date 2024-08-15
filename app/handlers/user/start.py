from aiogram import Router
from aiogram.filters import CommandStart
from aiogram.types import Message

import html

router = Router()


@router.message(CommandStart())
async def cmd_start(message: Message):
    first_name = message.from_user.first_name

    await message.answer(
        f"Приветствую, {html.escape(first_name)}"
        "\n<b>Напиши что-нибудь и я постараюсь это найти!</b>"
    )
