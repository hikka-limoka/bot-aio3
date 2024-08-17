from aiogram import Router


def get_dialog_router() -> Router:
    from .sample_dialog import ui as sample_dialog_ui
    from .mailing_dialog import ui as mailing_dialog_ui

    dialog_routers = Router()

    dialog_routers.include_router(sample_dialog_ui)
    dialog_routers.include_router(mailing_dialog_ui)

    return dialog_routers
