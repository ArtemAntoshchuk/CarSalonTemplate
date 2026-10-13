from aiogram import Bot, Dispatcher
from app.handlers.main_menu import router as main_menu_router
from app.handlers.car_handler import router as car_handler_router
from app.config import Config


bot = Bot(token=Config.BOT_TOKEN)
dp = Dispatcher()
dp.include_routers(main_menu_router, car_handler_router)

async def main():
    await dp.start_polling(bot)

