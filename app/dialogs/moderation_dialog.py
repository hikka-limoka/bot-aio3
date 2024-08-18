from aiogram.fsm.state import StatesGroup, State
from aiogram.types import CallbackQuery, User
from aiogram_dialog import Dialog, DialogManager, Window
from aiogram_dialog.widgets.kbd import Button
from aiogram_dialog.widgets.text import Format, Const


class ModerationDialog(StatesGroup):
    main = State()


async def approve_update(c: CallbackQuery, btn: Button, manager: DialogManager):
    update_id = manager.dialog_data["update_id"]
    api = manager.middleware_data["api"]
    await api.approve_update(update_id)
    await manager.switch_to(ModerationDialog.main)


async def get_unapproved_updates(
    dialog_manager: DialogManager, event_from_user: User, **kwargs
):
    api = kwargs.get("api")
    bot = dialog_manager.middleware_data["bot"]
    updates = await api.get_unapproved_updates()

    if not updates:
        await bot.send_message(
            event_from_user.id, "No updates to approve", disable_notification=True
        )
        return

    update = updates[0]

    dialog_manager.dialog_data["update_id"] = update["id"]
    return update


ui = Dialog(
    Window(
        Format(
            "🔧 <b>{developer}</b> <a href='https://limoka.vsecoder.dev/api/module/get_diff/{id}/html'>update module</a> #{id} <code>{name}.py</code>"
        ),
        Button(Const("Approve"), id="approve_update", on_click=approve_update),
        state=ModerationDialog.main,
        getter=get_unapproved_updates,
    ),
)
