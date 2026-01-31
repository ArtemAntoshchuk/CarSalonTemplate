from aiogram import Bot, Dispatcher
from app.handlers.main_menu import router as main_menu_router
from app.config import Config as conf


bot = Bot(token=conf.BOT_TOKEN)
dp = Dispatcher()
dp.include_routers(main_menu_router)

async def main():
    await dp.start_polling(bot)

