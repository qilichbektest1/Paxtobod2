from aiogram.fsm.state import State, StatesGroup


class OrderStates(StatesGroup):
    """States for order creation"""
    SELECT_DIRECTION = State()
    SELECT_PASSENGERS = State()
    REQUEST_CONTACT = State()
    REQUEST_LOCATION = State()


class DriverStates(StatesGroup):
    """States for driver registration"""
    FULL_NAME = State()
    PHONE = State()
    CAR_MODEL = State()
    CAR_NUMBER = State()
    CAR_PHOTO = State()
