import types

from aiogram import Router
from aiogram.fsm.context import FSMContext

from app.keyboards.keyboard_service import get_keyboard
from aiogram.filters import Command, CommandStart
from aiogram.types import Message
from app.keyboards.keyboards_enum import KeyboardsVariant


router = Router()

@router.message(Command(commands=['start', 'restart']))
async def main_menu(message: Message, state: FSMContext):
    await message.answer(text="Hello👋", reply_markup=get_keyboard(KeyboardsVariant.START_KEYBOARD))

