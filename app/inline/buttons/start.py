from aiogram.utils.keyboard import InlineKeyboardBuilder
from aiogram.types import InlineKeyboardButton

def start():
    builder = InlineKeyboardBuilder()

    builder.add(InlineKeyboardButton(
        text="Add/Remove Repo",
        url="https://t.me/vsecoder"
    ))

    builder.add(InlineKeyboardButton(
        text="Report broken module",
        url="https://t.me/vsecoder"
    ))

    builder.add(InlineKeyboardButton(
        text="Changelog",
        url="https://t.me/limokanews"
    ))

    builder.adjust(1)

    return builder.as_markup()