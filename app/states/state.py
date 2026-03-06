from aiogram.fsm.state import StatesGroup, State

class CustomerRegister(StatesGroup):
    phone_number_sharing = State()


class MenuState(StatesGroup):
    view_all_cars = State()