from aiogram import Router


def get_user_router() -> Router:
    from . import search, start

    router = Router()
    router.include_router(start.router)
    router.include_router(search.router)

    return router
