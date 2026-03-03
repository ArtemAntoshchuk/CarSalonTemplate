from aiogram import Router
from aiogram.filters import Command
from aiogram.fsm.context import FSMContext
from aiogram.types import Message

from app.keyboards.keyboard_service import get_keyboard
from app.keyboards.keyboards_enum import KeyboardsVariant
from app.service.car_service import get_cars_by_brand
from app.service.customer_service import customer_is_registered, register_customer
from app.states.state import CustomerRegister

router = Router()


@router.message(Command(commands=['start', 'restart']))
async def main_menu(message: Message, state: FSMContext):
    tg_id = message.from_user.id
    if await customer_is_registered(tg_id):
        await message.answer(text="Привіт👋", reply_markup=get_keyboard(KeyboardsVariant.START_KEYBOARD))
    else:
        await message.answer(text="Будь ласка зареєструйтесь:\nПоділіться номером🔽",
                             reply_markup=get_keyboard(KeyboardsVariant.PHONE_KB))
        await state.set_state(CustomerRegister.phone_number_sharing)


@router.message(CustomerRegister.phone_number_sharing)
async def register(message: Message, state: FSMContext):
    if message.contact is not None:
        tg_id = message.from_user.id
        first_name = message.from_user.first_name
        last_name = message.from_user.last_name
        phone_number = message.contact.phone_number
        await register_customer(telegram_id=tg_id, first_name=first_name, last_name=last_name,
                                phone_number=phone_number)
        await message.answer(text="Ви успішно зареєструвались!", reply_markup=get_keyboard(KeyboardsVariant.START_KEYBOARD))
    else:
        await message.answer(text="Будь ласка зареєструйтесь:\nПоділіться номером🔽",
                             reply_markup=get_keyboard(KeyboardsVariant.PHONE_KB))


@router.message(Command(commands=['allCars']))
async def show_cars(message: Message):
    cars = await get_cars_by_brand(1)
    await message.answer(text=str(cars))