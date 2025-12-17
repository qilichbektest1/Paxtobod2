from aiogram.types import ReplyKeyboardMarkup, KeyboardButton, InlineKeyboardMarkup, InlineKeyboardButton
from aiogram.utils.keyboard import ReplyKeyboardBuilder, InlineKeyboardBuilder


def main_menu_keyboard():
    """Main menu keyboard"""
    keyboard = ReplyKeyboardMarkup(
        keyboard=[
            [KeyboardButton(text="🚖 Taksi Chaqarish")],
            [KeyboardButton(text="🚕 Shopir Bo'lish")]
        ],
        resize_keyboard=True
    )
    return keyboard


def direction_keyboard():
    """Direction selection keyboard"""
    keyboard = ReplyKeyboardMarkup(
        keyboard=[
            [KeyboardButton(text="🚕 Toshkentdan Paxtobodga")],
            [KeyboardButton(text="🚕 Paxtoboddan Toshkentga")],
            [KeyboardButton(text="⬅️ Bekor qilish")]
        ],
        resize_keyboard=True
    )
    return keyboard


def passengers_keyboard():
    """Passengers count keyboard"""
    keyboard = ReplyKeyboardMarkup(
        keyboard=[
            [KeyboardButton(text="📦 Pochta bor")],
            [KeyboardButton(text="1"), KeyboardButton(text="2")],
            [KeyboardButton(text="3"), KeyboardButton(text="4")],
            [KeyboardButton(text="⬅️ Bekor qilish")]
        ],
        resize_keyboard=True
    )
    return keyboard


def phone_input_keyboard():
    """Phone input keyboard"""
    keyboard = ReplyKeyboardMarkup(
        keyboard=[
            [KeyboardButton(text="⬅️ Bekor qilish")]
        ],
        resize_keyboard=True
    )
    return keyboard


def location_keyboard():
    """Location request keyboard"""
    keyboard = ReplyKeyboardMarkup(
        keyboard=[
            [KeyboardButton(text="📍 Joylashuvni yuborish", request_location=True)],
            [KeyboardButton(text="⬅️ Bekor qilish")]
        ],
        resize_keyboard=True
    )
    return keyboard


def cancel_keyboard():
    """Cancel keyboard"""
    keyboard = ReplyKeyboardMarkup(
        keyboard=[
            [KeyboardButton(text="⬅️ Bekor qilish")]
        ],
        resize_keyboard=True
    )
    return keyboard


def driver_approval_keyboard(driver_id: int):
    """Keyboard for driver application approval"""
    keyboard = InlineKeyboardMarkup(
        inline_keyboard=[
            [
                InlineKeyboardButton(text="✅ Tasdiqlash", callback_data=f"approve_driver_{driver_id}"),
                InlineKeyboardButton(text="❌ Rad etish", callback_data=f"reject_driver_{driver_id}")
            ]
        ]
    )
    return keyboard
