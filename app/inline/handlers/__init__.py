from aiogram import Router


def get_inline_router() -> Router:
    from . import search

    router = Router()
    router.include_router(search.router)
    return router
