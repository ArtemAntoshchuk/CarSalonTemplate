from datetime import datetime

from aiogram import F
from aiogram import Router
from aiogram.fsm.context import FSMContext
from aiogram.types import Message, CallbackQuery

from app.handlers.utility_handler import update_car
from app.keyboards.keyboard_service import get_keyboard, get_kb_inline_by_list, get_kb_inline_by_list_objects
from app.keyboards.keyboards_enum import KeyboardsVariant
from app.service.brand_service import get_brands_names, get_brand_by_name
from app.service.car_service import add_car
from app.service.color_service import get_all_colors
from app.service.customer_service import get_customer_by_tg_id
from app.service.engine_service import get_all_engines, create_engine, get_all_engine_types
from app.service.favorites_service import save_to_favorites, delete_from_favorites
from app.service.models_service import get_models_by_brand
from app.service.photo_service import add_photos
from app.service.shifter_type_service import get_shifter_types_names
from app.states.state import CarCreatingState

router = Router()

import asyncio

#For test

@router.message(F.text=="Додати автомобіль🚗")
async def show_cars(message: Message, state: FSMContext):
    brands_names = await get_brands_names()
    await message.answer(text="Введіть/виберіть марку:", reply_markup=get_kb_inline_by_list(brands_names,
                                                                                            "brand",
                                                                                            2))
    await state.set_state(CarCreatingState.brand)
    await state.update_data(first_message_id = message.message_id)

#BRAND

@router.callback_query(CarCreatingState.brand)
async def brand_input(callback: CallbackQuery, state: FSMContext):
    brand_data = callback.data
    index = int(brand_data.split("_")[1])
    brands_names = await get_brands_names()
    brand = brands_names[index]


    if brand in brands_names:
        brand = await get_brand_by_name(brand)
        models = await get_models_by_brand(brand.id)
        await state.update_data(brand=brand)
        await callback.message.answer(text="Введіть/виберіть модель:", reply_markup=get_kb_inline_by_list_objects(models, 3, "model"))
        await state.set_state(CarCreatingState.model_id)
    else:
        await callback.message.answer(text="Введіть/виберіть марку:")


#MODEL

@router.callback_query(CarCreatingState.model_id)
async def model_input(callback: CallbackQuery, state: FSMContext):
    model_query = callback.data

    id = int(model_query.split("_")[1])
    await state.update_data(model_id=id)
    await state.set_state(CarCreatingState.price)
    await callback.message.answer(text="Введіть ціну: ", reply_markup=None)


#PRICE

@router.message(CarCreatingState.price)
async def price_input(message: Message, state: FSMContext):
    price_query = message.text
    try:
        price = int(price_query)
        if price > 0:
            await state.update_data(price=price)
            await state.set_state(CarCreatingState.vin)
            await message.answer("Введіть VIN:")
        else:
            await message.answer("Ціна має бути більше за 0. Введіть корректне значення.")
    except ValueError:
        await message.answer("Ціна має бути числовим значенням! Введіть корректне значення.")


#VIN

@router.message(CarCreatingState.vin)
async def vin_input(message: Message, state: FSMContext):
    vin_query = message.text
    if len(vin_query) == 17:
        await state.update_data(vin=vin_query)
        await state.set_state(CarCreatingState.mileage)
        await message.answer("Введіть пробіг:")
    else:
        await message.answer("VIN має складатися з 17 символів. Спробуйте ще раз.")

@router.message(CarCreatingState.mileage)
async def mileage_input(message: Message, state: FSMContext):
    mileage_query = message.text
    try:
        mileage = int(mileage_query)
        if mileage > 0:
            await state.update_data(mileage=mileage)
            await state.set_state(CarCreatingState.description)
            await message.answer("Введіть опис автомобіля:", reply_markup=get_keyboard(KeyboardsVariant.SKIP_CONTINUE_KB))

        else:
            await message.answer("Пробіг має бути більший за 0. Введіть корректне значення.")
    except ValueError:
        await message.answer("Пробіг має бути числовим значенням! Введіть корректне значення.")


@router.callback_query(CarCreatingState.description)
async def description_choice(callback: CallbackQuery, state: FSMContext):
    choice = callback.data
    if choice == "continue":
        await callback.message.answer("Введіть опис автомобіля:")
    else:
        await callback.message.delete()
        await callback.message.answer(text="Додайте фотографії автомобіля:", reply_markup=get_keyboard(KeyboardsVariant.PENTA_GENIUS_KB))
        await state.update_data(description=None)
        await state.set_state(CarCreatingState.photo)

@router.message(CarCreatingState.description)
async def description_input(message: Message, state: FSMContext):
    description_query = message.text
    await state.update_data(description=description_query)
    await message.answer("Додайте фотографії автомобіля:", reply_markup=get_keyboard(KeyboardsVariant.PENTA_GENIUS_KB))
    await state.set_state(CarCreatingState.photo)

@router.message(CarCreatingState.photo)
async def photo_input(message: Message, state: FSMContext):
    shifter_types_names = await get_shifter_types_names()

    if message.text == "Закінчити завантаження фото📸":
        await message.answer("Виберіть тип коробки передач:", reply_markup=get_kb_inline_by_list(shifter_types_names, "shifter_type", 3))
        await state.set_state(CarCreatingState.shifter_type_id)
        return

    data = await state.get_data()
    photo_ids = data.get("photo_ids", [])
    photo_ids.append(message.photo[-1].file_id)
    await state.update_data(photo_ids=photo_ids)


@router.callback_query(CarCreatingState.shifter_type_id)
async def shifter_type_input(callback: CallbackQuery, state: FSMContext):
    shifter_type_query = callback.data
    shifter_type_id = int(shifter_type_query.split("_")[-1])

    await state.update_data(shifter_type_id=shifter_type_id)
    await state.set_state(CarCreatingState.year_produced)
    await callback.message.answer(text="Введіть рік випуску автомобіля:", reply_markup=None)

@router.message(CarCreatingState.year_produced)
async def year_produced_input(message: Message, state: FSMContext):
    year_query = message.text
    current_year = datetime.now().year

    try:
        year = int(year_query)
        if 1900 <= year <= current_year + 1:
            await state.update_data(year_produced=year)
            await state.set_state(CarCreatingState.color_id)

            colors = await get_all_colors()

            await message.answer("Введіть колір автомобіля:", reply_markup=get_kb_inline_by_list_objects(colors, 3,
                                                                                                     "color"))
        else:
            await message.answer("Введіть справжній рік автомобіля, будь ласка.")

    except ValueError:
        await message.answer("Введіть будь ласка рік числовим значенням.")

@router.callback_query(CarCreatingState.color_id)
async def color_input(callback: CallbackQuery, state: FSMContext):
    color_query = callback.data

    color_id = int(color_query.split("_")[-1])

    await state.update_data(color_id=color_id)
    await state.set_state(CarCreatingState.was_in_accident)
    await callback.message.answer(text="Введіть чи був автомобіль у ДТП:", reply_markup=get_keyboard(KeyboardsVariant.WAS_IN_ACCIDENT_KB))

# status -> default available -> no state

@router.callback_query(CarCreatingState.was_in_accident)
async def was_in_accident_input(callback: CallbackQuery, state: FSMContext):
    was_in_accident_query = callback.data
    if was_in_accident_query == "True":
        accident = True
    else:                   #== "False":
        accident = False

    await state.update_data(was_in_accident=accident)
    await state.set_state(CarCreatingState.engine_id)

    await callback.message.answer(text="Ви хочете вибрати двигун зі списку чи сторити новий кастомний двигун?", reply_markup=get_keyboard(KeyboardsVariant.ENGINE_CUSTOM_OR_NOT))

@router.callback_query(CarCreatingState.engine_id)
async def engine_input(callback: CallbackQuery, state: FSMContext):
    if callback.data == "list":
        engines = await get_all_engines()
        await callback.message.answer(text="Оберіть двигун", reply_markup=get_kb_inline_by_list_objects(engines, 3, "engine"))
        await state.set_state(CarCreatingState.engine_choose)

    elif callback.data == "custom":
        await callback.message.answer(text="Введіть назву двигуна:", reply_markup=None)
        await state.set_state(CarCreatingState.engine_name)

@router.callback_query(CarCreatingState.engine_choose)
async def engine_choose_input(callback: CallbackQuery, state: FSMContext):
    engine_id = int(callback.data.split("_")[-1])
    await state.update_data(engine_id=engine_id)
    await finish_creating_car(callback.message, state)

@router.message(CarCreatingState.engine_name)
async def engine_name_input(message: Message, state: FSMContext):
    engine_name = message.text
    await state.update_data(engine_name=engine_name)

    engine_types = await get_all_engine_types()
    await message.answer(text="Введіть тип двигуна:", reply_markup=get_kb_inline_by_list_objects(engine_types, 3, "engine_type_id"))
    await state.set_state(CarCreatingState.engine_type_id)

@router.callback_query(CarCreatingState.engine_type_id)
async def engine_type_input(callback: CallbackQuery, state: FSMContext):
    engine_type_id = int(callback.data.split("_")[-1])
    await state.update_data(engine_type_id=engine_type_id)
    await callback.message.answer(text="Введіть покоління двигуна:")
    await state.set_state(CarCreatingState.engine_gen)

@router.message(CarCreatingState.engine_gen)
async def engine_gen_input(message: Message, state: FSMContext):
    engine_gen = message.text
    await state.update_data(engine_gen=engine_gen)
    await message.answer(text="Введіть об'єм двигуна:")
    await state.set_state(CarCreatingState.engine_volume)

@router.message(CarCreatingState.engine_volume)
async def engine_volume_input(message: Message, state: FSMContext):
    engine_volume = message.text
    try:
        engine_volume = float(engine_volume)
        if engine_volume > 0:
            await state.update_data(engine_volume=engine_volume)
            await message.answer(text="Введіть потужність двигуна (у кінських силах):")
            await state.set_state(CarCreatingState.engine_horse_power)
        else:
            raise ValueError("Об'єм двигуна має бути більшим за 0.")

    except ValueError as e:
        await message.answer(text= str(e) + " \nСпробуйте ще раз:")

@router.message(CarCreatingState.engine_horse_power)
async def engine_horse_power_input(message: Message, state: FSMContext):
    engine_horse_power = message.text
    try:
        engine_horse_power = int(engine_horse_power)
        if engine_horse_power > 0:
            await state.update_data(engine_horse_power=engine_horse_power)
            data = await state.get_data()
            engine_name = data["engine_name"]
            engine_type_id = data["engine_type_id"]
            engine_gen = data["engine_gen"]
            engine_volume = data["engine_volume"]
            engine_horse_power = data["engine_horse_power"]
            engine_id = await create_engine(engine_name=engine_name, engine_type_id=engine_type_id, engine_gen=engine_gen, engine_volume=engine_volume, engine_horse_power=engine_horse_power)
            await state.update_data(engine_id=engine_id)
            end_message = await message.answer(text="Двигун створено.")
            await finish_creating_car(message, state)
            await asyncio.sleep(3)
            await end_message.delete()
        else:
            raise ValueError("Потужність двигуна має бути більшою за 0.")
    except ValueError as e:
        await message.answer(text=str(e) + " \nСпробуйте ще раз:")



async def finish_creating_car(message, state: FSMContext):
    data = await state.get_data()
    model_id = data["model_id"]
    price = data["price"]
    vin = data["vin"]
    mileage = data["mileage"]
    description = data["description"]
    shifter_type_id = data["shifter_type_id"]
    year_produced = data["year_produced"]
    color_id = data["color_id"]
    was_in_accident = data["was_in_accident"]
    engine_id = data["engine_id"]
    photo_ids = data["photo_ids"]

    car_id = await add_car(model_id=model_id, price=price, vin=vin, mileage=mileage, description=description, shifter_type_id=shifter_type_id, year_produced=year_produced, color_id=color_id, was_in_accident=was_in_accident, engine_id=engine_id)
    await add_photos(photo_ids, car_id)
    end_message = await message.answer(text="Машину створено.")
    await delete_messages(data["first_message_id"], end_message.message_id, message)
    await state.clear()
    await message.answer(text="Машину створено.", reply_markup=get_keyboard(KeyboardsVariant.START_KEYBOARD))



async def delete_messages(first_id, last_id, message):
    messages_to_delete = list(range(last_id, first_id, -1))
    chat_id = message.chat.id
    await message.bot.delete_messages(chat_id, messages_to_delete)


@router.callback_query(F.data=="save_to_fav")
async def save_car_to_fav(callback: CallbackQuery, state: FSMContext):
    data = await state.get_data()
    car_id = data["current_car_id"]
    tg_id = callback.from_user.id
    customer = await get_customer_by_tg_id(tg_id)

    await save_to_favorites(car_id=car_id, customer_id=customer.id)
    await update_car(message=callback.message, state=state)


@router.callback_query(F.data=="delete_from_fav")
async def delete_car_from_fav(callback: CallbackQuery, state: FSMContext):
    data = await state.get_data()
    car_id = data["current_car_id"]
    tg_id = callback.from_user.id
    customer = await get_customer_by_tg_id(tg_id)

    await delete_from_favorites(car_id=car_id, customer_id=customer.id)
    await update_car(message=callback.message, state=state)