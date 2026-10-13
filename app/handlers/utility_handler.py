from aiogram.fsm.context import FSMContext
from aiogram.types import InputMediaPhoto
from aiogram.types import Message

from app.dto.dto import CarBaseInfoDTO
from app.keyboards.keyboard_service import get_keyboard
from app.keyboards.keyboards_enum import KeyboardsVariant
from app.service.car_service import get_all_cars_base_dto
from app.service.customer_service import get_customer_by_tg_id
from app.service.favorites_service import get_favorite_by_car_id_and_customer_id


async def display_car(message: Message, state: FSMContext):
    car_dto = await get_car_dto(state)
    user_tg_id = message.from_user.id
    await state.update_data(user_tg_id = user_tg_id)
    customer = await get_customer_by_tg_id(user_tg_id)

    short_info = get_short_info(car_dto)
    if await get_favorite_by_car_id_and_customer_id(car_dto.id, customer.id):
        await message.answer_photo(caption=short_info, reply_markup=get_keyboard(KeyboardsVariant.NAVI_KB_FAVOURITES), photo=car_dto.main_photo_tg_id)
    else:
        await message.answer_photo(caption=short_info, reply_markup=get_keyboard(KeyboardsVariant.NAVI_KB),photo=car_dto.main_photo_tg_id)


async def update_car(message: Message, state: FSMContext):
    car_dto = await get_car_dto(state)
    data = await state.get_data()
    user_tg_id = data["user_tg_id"]
    customer = await get_customer_by_tg_id(user_tg_id)
    short_info = get_short_info(car_dto)
    main_photo = InputMediaPhoto(media=car_dto.main_photo_tg_id, caption=short_info)
    if await get_favorite_by_car_id_and_customer_id(car_dto.id, customer.id):
        await message.edit_media(media=main_photo, reply_markup=get_keyboard(KeyboardsVariant.NAVI_KB_FAVOURITES))
    else:
        await message.edit_media(media=main_photo, reply_markup=get_keyboard(KeyboardsVariant.NAVI_KB))


async def get_car_dto(state: FSMContext) -> CarBaseInfoDTO:
    cars = await get_all_cars_base_dto()
    data = await state.get_data()
    page = data["page"]
    car = cars[page - 1]
    await save_current_car_id(car_id=car.id, state=state)
    return car

def get_short_info(car_dto: CarBaseInfoDTO):
    return f"{car_dto.brand_name} {car_dto.model_name} {car_dto.year}\n${car_dto.price}"

async def save_current_car_id(state: FSMContext, car_id: int):
    await state.update_data(current_car_id=car_id)