from aiogram import Router, F, Bot
from aiogram.filters import CommandStart
from aiogram.types import Message, CallbackQuery
from aiogram.fsm.context import FSMContext

from keyboards import (
    main_menu_keyboard,
    direction_keyboard,
    passengers_keyboard,
    phone_input_keyboard,
    location_keyboard,
    cancel_keyboard,
    driver_approval_keyboard
)
from states import OrderStates, DriverStates
from database import (
    add_user,
    create_order,
    update_order_contact,
    create_driver_application,
    update_driver_status,
    get_driver_by_id
)
from config import ADMIN_USER_ID, TAXI_GROUP_ID, BOT_NAME

router = Router()


@router.message(CommandStart())
async def cmd_start(message: Message, state: FSMContext):
    """Handle /start command"""
    await state.clear()

    await add_user(
        user_id=message.from_user.id,
        username=message.from_user.username or "",
        first_name=message.from_user.first_name or ""
    )

    await message.answer(
        f"👋 Salom {message.from_user.first_name}!\n\n"
        f"{BOT_NAME} ga xush kelibsiz!\n\n"
        f"Quyidagi menyudan kerakli bo'limni tanlang:",
        reply_markup=main_menu_keyboard()
    )


@router.message(F.text == "🚖 Taksi Chaqarish")
async def order_taxi(message: Message, state: FSMContext):
    """Start taxi order process"""
    await state.set_state(OrderStates.SELECT_DIRECTION)
    await message.answer(
        "📍 Bormoqchi bo'lgan yo'nalishingizni belgilang:",
        reply_markup=direction_keyboard()
    )


@router.message(F.text == "🚕 Shopir Bo'lish")
async def become_driver(message: Message, state: FSMContext):
    """Start driver registration process"""
    await state.set_state(DriverStates.FULL_NAME)
    await message.answer(
        "🚕 Shopir bo'lish uchun ro'yxatdan o'ting!\n\n"
        "Iltimos, to'liq ismingizni kiriting:",
        reply_markup=cancel_keyboard()
    )


@router.message(DriverStates.FULL_NAME)
async def driver_full_name(message: Message, state: FSMContext):
    """Handle driver full name"""
    if message.text == "⬅️ Bekor qilish":
        await state.clear()
        await message.answer("❌ Ro'yxatdan o'tish bekor qilindi.", reply_markup=main_menu_keyboard())
        return

    await state.update_data(full_name=message.text)
    await state.set_state(DriverStates.PHONE)
    await message.answer(
        "📱 Telefon raqamingizni kiriting:\n"
        "(Masalan: +998901234567)",
        reply_markup=cancel_keyboard()
    )


@router.message(DriverStates.PHONE)
async def driver_phone(message: Message, state: FSMContext):
    """Handle driver phone"""
    if message.text == "⬅️ Bekor qilish":
        await state.clear()
        await message.answer("❌ Ro'yxatdan o'tish bekor qilindi.", reply_markup=main_menu_keyboard())
        return

    await state.update_data(phone=message.text)
    await state.set_state(DriverStates.CAR_MODEL)
    await message.answer(
        "🚗 Mashina rusumini kiriting:\n"
        "(Masalan: Nexia 3, Cobalt, Spark va h.k.)",
        reply_markup=cancel_keyboard()
    )


@router.message(DriverStates.CAR_MODEL)
async def driver_car_model(message: Message, state: FSMContext):
    """Handle driver car model"""
    if message.text == "⬅️ Bekor qilish":
        await state.clear()
        await message.answer("❌ Ro'yxatdan o'tish bekor qilindi.", reply_markup=main_menu_keyboard())
        return

    await state.update_data(car_model=message.text)
    await state.set_state(DriverStates.CAR_NUMBER)
    await message.answer(
        "🔢 Mashina raqamini kiriting:\n"
        "(Masalan: 01 A 123 BC)",
        reply_markup=cancel_keyboard()
    )

@router.message(DriverStates.CAR_NUMBER)
async def driver_car_number(message: Message, state: FSMContext):
    """Handle driver car number"""
    if message.text == "⬅️ Bekor qilish":
        await state.clear()
        await message.answer("❌ Ro'yxatdan o'tish bekor qilindi.", reply_markup=main_menu_keyboard())
        return

    await state.update_data(car_number=message.text)
    await state.set_state(DriverStates.CAR_PHOTO)
    await message.answer(
        "📸 Mashina rasmini yuboring:",
        reply_markup=cancel_keyboard()
    )


@router.message(DriverStates.CAR_PHOTO, F.photo)
async def driver_car_photo(message: Message, state: FSMContext, bot: Bot):
    """Handle driver car photo and send to admin for approval with user profile link"""
    photo_file_id = message.photo[-1].file_id
    data = await state.get_data()

    user = message.from_user
    profile_link = f"<a href='tg://user?id={user.id}'>{user.full_name}</a>"

    # Create driver application in database
    driver_id = await create_driver_application(
        user_id=user.id,
        full_name=data['full_name'],
        phone=data['phone'],
        car_model=data['car_model'],
        car_number=data['car_number'],
        photo_file_id=photo_file_id
    )

    # Prepare admin message with profile link
    admin_message = (
        f"🚕 Yangi shopir arizasi!\n\n"
        f"👤 Mijoz: {profile_link}\n"
        f"📱 Telefon: {data['phone']}\n"
        f"🚗 Mashina: {data['car_model']}\n"
        f"🔢 Raqam: {data['car_number']}\n"
        f"🆔 User ID: {user.id}\n"
        f"📋 Ariza ID: {driver_id}"
    )

    # Send photo + caption to admin
    if ADMIN_USER_ID > 0:
        await bot.send_photo(
            chat_id=ADMIN_USER_ID,
            photo=photo_file_id,
            caption=admin_message,
            parse_mode="HTML",  # 🔹 HTML ni ishlatish
            reply_markup=driver_approval_keyboard(driver_id)
        )

    # Notify driver
    await message.answer(
        "✅ Arizangiz qabul qilindi!\n\n"
        "Admin ko'rib chiqib, tez orada siz bilan bog'lanadi.",
        reply_markup=main_menu_keyboard()
    )

    await state.clear()


@router.callback_query(F.data.startswith("approve_driver_"))
async def approve_driver(callback: CallbackQuery, bot: Bot):
    """Handle driver approval"""
    driver_id = int(callback.data.split("_")[-1])

    # Update driver status
    await update_driver_status(driver_id, "approved")

    # Get driver info
    driver = await get_driver_by_id(driver_id)

    if driver:
        # Notify driver
        await bot.send_message(
            chat_id=driver['user_id'],
            text=f"🎉 Tabriklaymiz!\n\n"
                 f"Sizning arizangiz tasdiqlandi!\n"
                 f"Endi siz shopir sifatida ishlashingiz mumkin."
        )

    await callback.message.edit_caption(
        caption=callback.message.caption + "\n\n✅ Tasdiqlandi!",
        reply_markup=None
    )
    await callback.answer("✅ Shopir tasdiqlandi!")


@router.callback_query(F.data.startswith("reject_driver_"))
async def reject_driver(callback: CallbackQuery, bot: Bot):
    """Handle driver rejection"""
    driver_id = int(callback.data.split("_")[-1])

    # Update driver status
    await update_driver_status(driver_id, "rejected")

    # Get driver info
    driver = await get_driver_by_id(driver_id)

    if driver:
        # Notify driver
        await bot.send_message(
            chat_id=driver['user_id'],
            text=f"❌ Kechirasiz!\n\n"
                 f"Sizning arizangiz rad etildi.\n"
                 f"Iltimos, ma'lumotlaringizni to'g'ri to'ldiring va qayta urinib ko'ring."
        )

    await callback.message.edit_caption(
        caption=callback.message.caption + "\n\n❌ Rad etildi!",
        reply_markup=None
    )
    await callback.answer("❌ Shopir rad etildi!")


@router.message(OrderStates.SELECT_DIRECTION, F.text.in_([
    "🚕 Toshkentdan Paxtobodga",
    "🚕 Paxtoboddan Toshkentga"
]))
async def select_direction(message: Message, state: FSMContext):
    """Handle direction selection"""
    direction = message.text.replace("🚕 ", "")
    await state.update_data(direction=direction)
    await state.set_state(OrderStates.SELECT_PASSENGERS)

    await message.answer(
        "👥 Nechta yo'lovchi bor yoki 📦 pochta?",
        reply_markup=passengers_keyboard()
    )


@router.message(OrderStates.SELECT_PASSENGERS, F.text.in_([
    "📦 Pochta bor", "1", "2", "3", "4"
]))
async def select_passengers(message: Message, state: FSMContext):
    """Handle passengers/cargo selection"""
    if message.text == "📦 Pochta bor":
        order_type = "pochta"
        passengers = 0
    else:
        order_type = "people"
        passengers = int(message.text)

    await state.update_data(
        passengers=passengers,
        order_type=order_type
    )

    data = await state.get_data()
    order_id = await create_order(
        user_id=message.from_user.id,
        direction=data['direction'],
        passengers=passengers,
        order_type=order_type
    )
    await state.update_data(order_id=order_id)

    await state.set_state(OrderStates.REQUEST_CONTACT)
    await message.answer(
        "📱 Telefon raqamingizni kiriting:\n"
        "(Masalan: +998901234567)\n\n"
        "Shopir siz bilan bog'lanishi uchun kerak bo'ladi.",
        reply_markup=phone_input_keyboard()
    )


@router.message(OrderStates.REQUEST_CONTACT, F.text)
async def receive_phone(message: Message, state: FSMContext):
    """Handle phone number input"""
    if message.text == "⬅️ Bekor qilish":
        await cancel_order(message, state)
        return

    phone = message.text
    await state.update_data(phone=phone)
    await state.set_state(OrderStates.REQUEST_LOCATION)

    await message.answer(
        "📍 Endi joylashuvingizni yuboring:\n\n"
        "Bu shopirga sizni topishda yordam beradi.",
        reply_markup=location_keyboard()
    )


@router.message(OrderStates.REQUEST_LOCATION, F.location)
async def receive_location(message: Message, state: FSMContext, bot: Bot):
    """Handle location and complete order with user profile"""
    location_lat = message.location.latitude
    location_lon = message.location.longitude

    data = await state.get_data()

    await update_order_contact(
        order_id=data['order_id'],
        phone=data['phone'],
        location_lat=location_lat,
        location_lon=location_lon
    )

    # --- Foydalanuvchi profili ---
    user = message.from_user
    profile_link = f"<a href='tg://user?id={user.id}'>{user.full_name}</a>"

    # --- Foydalanuvchiga tasdiq xabari ---
    order_info = (
        f"✅ Buyurtmangiz qabul qilindi!\n\n"
        f"📍 Yo'nalish: {data['direction']}\n"
    )
    if data['order_type'] == 'pochta':
        order_info += f"📦 Turi: Pochta\n"
    else:
        order_info += f"👥 Yo'lovchilar: {data['passengers']} kishi\n"
    order_info += f"📱 Telefon: {data['phone']}\n\n"
    order_info += "🚕 Shopir siz bilan tez orada bog'lanadi!"

    await message.answer(
        order_info,
        reply_markup=main_menu_keyboard()
    )

    # --- Guruh va admin uchun xabar (profil bilan) ---
    group_message = (
        f"🚖 YANGI BUYURTMA!\n\n"
        f"👤 Mijoz: {profile_link}\n"
        f"📍 Yo'nalish: {data['direction']}\n"
    )
    if data['order_type'] == 'pochta':
        group_message += f"📦 Turi: Pochta\n"
    else:
        group_message += f"👥 Yo'lovchilar: {data['passengers']} kishi\n"
    group_message += (
        f"📱 Telefon: {data['phone']}\n"
        f"🆔 Order ID: {data['order_id']}\n"
        f"📅 Vaqt: {message.date.strftime('%Y-%m-%d %H:%M')}"
    )

    # --- Guruhga yuborish ---
    if TAXI_GROUP_ID != 0:
        try:
            await bot.send_location(
                chat_id=TAXI_GROUP_ID,
                latitude=location_lat,
                longitude=location_lon
            )
            await bot.send_message(
                chat_id=TAXI_GROUP_ID,
                text=group_message,
                parse_mode="HTML"
            )
        except Exception as e:
            print(f"Error sending to TAXI_GROUP: {e}")

    # --- Adminga yuborish ---
    if ADMIN_USER_ID != 0:
        try:
            await bot.send_location(
                chat_id=ADMIN_USER_ID,
                latitude=location_lat,
                longitude=location_lon
            )
            await bot.send_message(
                chat_id=ADMIN_USER_ID,
                text=group_message,
                parse_mode="HTML"
            )
        except Exception as e:
            print(f"Error sending to ADMIN: {e}")

    await state.clear()

    await state.clear()


@router.message(F.text == "⬅️ Bekor qilish")
async def cancel_order(message: Message, state: FSMContext):
    """Cancel current order"""
    await state.clear()
    await message.answer(
        "❌ Amal bekor qilindi.",
        reply_markup=main_menu_keyboard()
    )


@router.message()
async def unknown_message(message: Message):
    if message.chat.type != "private":
        return  # 👈 guruhda javob bermaydi

    await message.answer(
        "❓ Noma'lum buyruq. Iltimos, menyudan tanlang.",
        reply_markup=main_menu_keyboard()
    )

