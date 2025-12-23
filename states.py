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

class AdminStates(StatesGroup):
    """States for admin panel"""
    MAIN_PANEL = State()
    VIEW_ORDERS = State()
    VIEW_DRIVERS = State()
    VIEW_STATISTICS = State()
    VIEW_SETTINGS = State()
    EDIT_DAILY_LIMIT = State()
