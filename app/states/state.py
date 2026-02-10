from aiogram.fsm.state import StatesGroup, State

class CustomerRegister(StatesGroup):
    phone_number_sharing = State()