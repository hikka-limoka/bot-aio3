from aiogram.fsm.state import StatesGroup, State
from aiogram_dialog import Dialog, DialogManager, Window
from aiogram_dialog.widgets.text import Const
from aiogram_dialog.widgets.kbd import Button, Next, Back
from aiogram_dialog.widgets.input import MessageInput
from aiogram.types import ContentType, Message

from aiogram.types import CallbackQuery
from app.keyboards.inline import mailing_keyboard


class MailingDialog(StatesGroup):
    start = State()
    image = State()
    text = State()
    buttons = State()
    confirm = State()
    result = State()


async def image_handler(message: Message, _: MessageInput, manager: DialogManager):
    image = None
    type_ = "text"
    if getattr(message, "photo", None):
        image = message.photo[-1].file_id
        type_ = "photo"
    elif getattr(message, "video", None):
        image = message.video.file_id
        type_ = "video"
    elif getattr(message, "animation", None):
        image = message.animation.file_id
        type_ = "animation"
    manager.dialog_data["image"] = image
    manager.dialog_data["type"] = type_
    await manager.next()


async def text_handler(message: Message, _: MessageInput, manager: DialogManager):
    manager.dialog_data["text"] = message.text
    await manager.next()


async def buttons_handler(message: Message, _: MessageInput, manager: DialogManager):
    buttons = message.text.split("\n")
    buttons = [button.split("|") for button in buttons]
    buttons = [(button[0].strip(), button[1].strip()) for button in buttons]
    manager.dialog_data["buttons"] = buttons
    await manager.next()


async def get_preview(c: CallbackQuery, _: Button, manager: DialogManager):
    data = manager.dialog_data
    text = data["text"]
    image = data["image"]
    type_ = data["type"]
    buttons = data.get("buttons", [])
    bot = manager.middleware_data["bot"]
    reply_markup = mailing_keyboard(buttons)

    try:
        if type_ == "photo":
            await bot.send_photo(
                c.from_user.id, image, caption=text, reply_markup=reply_markup
            )
        elif type_ == "video":
            await bot.send_video(
                c.from_user.id, image, caption=text, reply_markup=reply_markup
            )
        elif type_ == "animation":
            await bot.send_animation(
                c.from_user.id, image, caption=text, reply_markup=reply_markup
            )
        else:
            await bot.send_message(c.from_user.id, text, reply_markup=reply_markup)
    except Exception as e:
        await bot.send_message(c.from_user.id, f"Ошибка: {e}")


async def confirm(c: CallbackQuery, _: Button, manager: DialogManager):
    data = manager.dialog_data
    text = data["text"]
    image = data["image"]
    type_ = data["type"]
    buttons = data.get("buttons", [])
    bot = manager.middleware_data["bot"]
    reply_markup = mailing_keyboard(buttons)
    api = manager.middleware_data["api"]
    #users = await api.get_all_users()
    users = [] # TODO: Replace with your own list of users
    counter = 0

    await bot.send_message(c.from_user.id, f"📨 Начал рассылку")

    for user in users:
        try:
            if type_ == "photo":
                await bot.send_photo(
                    user.telegram_id, image, caption=text, reply_markup=reply_markup
                )
            elif type_ == "video":
                await bot.send_video(
                    user.telegram_id, image, caption=text, reply_markup=reply_markup
                )
            elif type_ == "animation":
                await bot.send_animation(
                    user.telegram_id, image, caption=text, reply_markup=reply_markup
                )
            else:
                await bot.send_message(user.telegram_id, text)
            counter += 1
        except Exception:
            pass

    await bot.send_message(
        c.from_user.id, f"📨 Рассылка завершена. Отправлено {counter} сообщений"
    )
    await manager.done()


async def cancel(c: CallbackQuery, _: Button, manager: DialogManager):
    await manager.done()


ui = Dialog(
    Window(
        Const("<b>📨 Рассылка по всем пользователям (пока не работает)</b>\n"),
        Const("<i>Дальше вам будет необходимо загрузить изображение и текст</i>"),
        #Next(Const("➡️ Продолжить")),
        state=MailingDialog.start,
    ),
    Window(
        Const(
            "<b>🖼 Загрузите изображение/видео/GIF или напишите <code>пусто</code>:</b>"
        ),
        Back(Const("⬅️ Назад")),
        MessageInput(
            image_handler,
            content_types=[
                ContentType.PHOTO,
                ContentType.TEXT,
                ContentType.VIDEO,
                ContentType.ANIMATION,
            ],
        ),
        state=MailingDialog.image,
    ),
    Window(
        Const("<b>📝 Введите текст рассылки:</b>"),
        Back(Const("⬅️ Назад")),
        MessageInput(text_handler, content_types=[ContentType.TEXT]),
        state=MailingDialog.text,
    ),
    Window(
        Const("<b>⏏️ Добавьте кнопки к сообщению:</b>"),
        Const("<i>Вводите кнопки построчно в формате:</i>"),
        Const(
            "<pre><code language='example'>Кнопка 1 | https://google.com\nКнопка 2 | https://yandex.ru</code></pre>"
        ),
        Next(Const("➡️ Пропустить")),
        Back(Const("⬅️ Назад")),
        MessageInput(buttons_handler, content_types=[ContentType.TEXT]),
        state=MailingDialog.buttons,
    ),
    Window(
        Const("<b>🔍 Проверьте ваш пост</b>"),
        Const(
            "<i>Если вместо превью вы видите ошибку, нажмите <code>Отмена</code>, возможно, вы что-то сделали не так</i>"
        ),
        Button(Const("👀 Превью"), id="preview", on_click=get_preview),
        Button(Const("✅ Отправить"), id="confirm", on_click=confirm),
        Button(Const("❌ Отмена"), id="cancel", on_click=cancel),
        Back(Const("⬅️ Назад")),
        state=MailingDialog.confirm,
    ),
)
