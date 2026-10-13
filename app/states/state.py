from aiogram.fsm.state import StatesGroup, State

class CustomerRegister(StatesGroup):
    phone_number_sharing = State()


class MenuState(StatesGroup):
    view_all_cars = State()

class CarCreatingState(StatesGroup):
    brand = State()
    model_id = State()
    price = State()
    vin = State()
    mileage = State()
    description = State()
    shifter_type_id = State()
    year_produced = State()
    color_id = State()
    #status = State()
    was_in_accident = State()
    engine_choose = State()
    engine_id = State()
    engine_name = State()
    engine_type_id = State()
    engine_gen = State()
    engine_volume = State()
    engine_horse_power = State()
    photo = State()

