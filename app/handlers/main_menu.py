from aiogram import F
from aiogram import Router
from aiogram.filters import Command
from aiogram.fsm.context import FSMContext
from aiogram.types import Message, CallbackQuery

from app.handlers.utility_handler import update_car, display_car
from app.keyboards.keyboard_service import get_keyboard
from app.keyboards.keyboards_enum import KeyboardsVariant
from app.service.car_service import get_count_of_cars
from app.service.customer_service import customer_is_registered, register_customer
from app.states.state import CustomerRegister, MenuState

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


'''
     Message template:
     
     Image(one ore three)
     Base info
     |<Prev           |       Next> |
     |Add to favorites| More Details|
     |           More photo         |
'''

@router.message(F.text=="Подивитися всі машини🚗")
# async def show_cars(message: Message):
#     cars = await get_cars_by_brand(1)
#     await message.answer(text=str(cars))
async def show_cars(message: Message, state: FSMContext):
    #Set state for viewing all cars
    await state.set_state(MenuState.view_all_cars)
    #                     key = value
    await state.update_data(page=1)
    await display_car(message=message, state=state)

# NAVIGATION REGION
@router.callback_query(F.data=="next", MenuState.view_all_cars)
async def switch_to_next_cars(callback: CallbackQuery, state: FSMContext):
    state_data = await state.get_data()
    page = state_data["page"]
    # max page = count of cars
    if page < await get_count_of_cars():
        page += 1
    else:
        page = 1

    await state.update_data(page=page)
    await update_car(message=callback.message, state=state)


@router.callback_query(F.data == "prev", MenuState.view_all_cars)
async def switch_to_prev_cars(callback: CallbackQuery, state: FSMContext):
    state_data = await state.get_data()
    page = state_data["page"]
    # max page = count of cars
    if page > 1:
        page -= 1
    else:
        page = await get_count_of_cars()

    await state.update_data(page=page)
    await update_car(message=callback.message, state=state)


# async def display_car(message: Message, state: FSMContext):
#     car_dto = await get_car_dto(state)
#     user_tg_id = message.from_user.id
#     await state.update_data(user_tg_id = user_tg_id)
#     customer = await get_customer_by_tg_id(user_tg_id)
#
#     short_info = get_short_info(car_dto)
#     if await get_favorite_by_car_id_and_customer_id(car_dto.id, customer.id):
#         await message.answer_photo(caption=short_info, reply_markup=get_keyboard(KeyboardsVariant.NAVI_KB_FAVOURITES), photo=car_dto.main_photo_tg_id)
#     else:
#         await message.answer_photo(caption=short_info, reply_markup=get_keyboard(KeyboardsVariant.NAVI_KB),photo=car_dto.main_photo_tg_id)
#
#
# # @router.callback_query(F.data=="next", state=MenuState.view_fa_cars)
#
# async def update_car(message: Message, state: FSMContext):
#     car_dto = await get_car_dto(state)
#     data = await state.get_data()
#     user_tg_id = data["user_tg_id"]
#     customer = await get_customer_by_tg_id(user_tg_id)
#     short_info = get_short_info(car_dto)
#     main_photo = InputMediaPhoto(media=car_dto.main_photo_tg_id, caption=short_info)
#     if await get_favorite_by_car_id_and_customer_id(car_dto.id, customer.id):
#         await message.edit_media(media=main_photo, reply_markup=get_keyboard(KeyboardsVariant.NAVI_KB_FAVOURITES))
#     else:
#         await message.edit_media(media=main_photo, reply_markup=get_keyboard(KeyboardsVariant.NAVI_KB))


# @router.message()
# async def add_photo(message: Message, state: FSMContext):
#     photos = [InputMediaPhoto(media="pass", caption="abobaaaa"), InputMediaPhoto(media="AgACAgIAAxkBAAN6acLjrq3--iuoeTexAY0BioKfDuwAApAbaxtFCBhKJns0sy9dfRcBAAMCAAN3AAM6BA", caption="hahaha")]
#     #await message.answer(text=message.photo[-1].file_id)
#     await message.answer_media_group(media=photos)

