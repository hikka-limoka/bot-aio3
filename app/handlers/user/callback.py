from aiogram import Router, F, Bot
from aiogram.types import CallbackQuery

router = Router()


@router.callback_query(F.data.startswith("install:"))
async def install_module_handler(query: CallbackQuery, bot: Bot, api):
    module_id = query.data.split(":")[1]
    await query.answer("Downloading...")
    await bot.send_message(
        query.from_user.id,
        (
            f'<span class="tg-spoiler">#install:{module_id}</span>\n\n'
            "❗️ If you watched this message a long time ago, download this:\n"
            "<code>.dlm https://raw.githubusercontent.com/hikka-limoka/module/main/Limoka.py</code>\n"
            "And try again."
        ),
        disable_notification=True,
    )
    await api.download_module(query.from_user.id, module_id)
