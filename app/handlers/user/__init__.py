from aiogram import Router


def get_user_router() -> Router:
    from . import search, start, callback, devs, stats

    router = Router()
    router.include_router(start.router)
    router.include_router(callback.router)
    router.include_router(devs.router)
    router.include_router(stats.router)
    router.include_router(search.router)

    return router
