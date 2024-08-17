from aiogram import Router
from aiogram.filters import CommandStart
from aiogram.types import Message

from app.keyboards.inline import start_keyboard

router = Router()


@router.message(CommandStart())
async def cmd_start(message: Message, api):
    uid = message.from_user.id

    if not await api.get_user(uid):
        await api.create_user(uid)

    await message.answer_photo(
        "https://raw.githubusercontent.com/hikka-limoka/stuff/main/banners/start.png",
        "<b>🍾 Modules are now in one place with easy searching!</b>\n"
        "🔎 Start searching:",
        reply_markup=start_keyboard(),
    )

    await message.answer(
        "❗️ For downloading modules, you need install socket module:\n"
        "<code>.dlm https://raw.githubusercontent.com/hikka-limoka/module/main/Limoka.py</code>\n"
        "<span class=\"tg-spoiler\">#skipIfModuleInstalled</span>"
    )
