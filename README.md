# 🚖 Toshkent-Paxtobod Taxi Bot

Telegram taxi bot aiogram 3.x va Python 3.10 uchun.

## Xususiyatlar

### Mijozlar uchun:
- ✅ Yo'nalish tanlash (Toshkent ↔ Paxtobod)
- ✅ Yo'lovchilar soni yoki pochta
- ✅ Kontakt va joylashuv ulashish
- ✅ Buyurtma tarixini saqlash

### Shopirlar uchun:
- ✅ Shopir sifatida ro'yxatdan o'tish
- ✅ To'liq ism, telefon, mashina ma'lumotlari
- ✅ Mashina rasmini yuklash
- ✅ Admin tomonidan tasdiqlash tizimi

### Admin uchun:
- ✅ Barcha buyurtmalarni real-time ko'rish
- ✅ Shopir arizalarini tasdiqlash/rad etish
- ✅ Ikki guruhga avtomatik xabar yuborish
- ✅ SQLite database bilan ma'lumotlarni saqlash

## O'rnatish

### 1. Python va Virtual Environment

```bash
# Python 3.10 o'rnatilganligini tekshiring
python --version

# Virtual environment yarating
python -m venv venv

# Aktivlashtiring
source venv/bin/activate  # Linux/Mac
# yoki
venv\Scripts\activate  # Windows
```

### 2. Dependencies o'rnatish

```bash
pip install -r requirements.txt
```

### 3. Bot sozlash

1. **Bot yarating:**
   - @BotFather ga `/newbot` buyrug'ini yuboring
   - Bot nomini va username kiriting
   - Token olasiz (masalan: `1234567890:ABCdefGHIjklMNOpqrsTUVwxyz`)

2. **User ID ni aniqlang:**
   - @userinfobot ga o'zingizni ID'ingizni so'rang
   - Bu sizning admin ID'ingiz bo'ladi

3. **Guruh ID larini oling:**
   - Botni ikkita guruhga admin qiling
   - @userinfobot ni guruhlarga qo'shing va guruh ID larini oling
   - Guruh ID lari minus (-) bilan boshlanadi (masalan: `-1001234567890`)

4. **`.env` faylini sozlang:**

```bash
cp .env.example .env
nano .env  # yoki istalgan text editor
```

`.env` fayliga quyidagilarni kiriting:

```env
BOT_TOKEN=1234567890:ABCdefGHIjklMNOpqrsTUVwxyz
ADMIN_USER_ID=123456789
GROUP_1_ID=-1001234567890
GROUP_2_ID=-1001234567891
```

## Ishga tushirish

```bash
python bot.py
```

Bot muvaffaqiyatli ishga tushsa, konsolda "Bot ishga tushdi!" xabari chiqadi.

## Bot ishlashi

### Mijoz tomonidan buyurtma berish:

1. `/start` buyrug'i - Botni ishga tushirish
2. "🚖 Taksi Chaqarish" tugmasini bosish
3. Yo'nalishni tanlash (Toshkent ↔ Paxtobod)
4. Yo'lovchilar sonini tanlash yoki pochta
5. Telefon raqamini ulashish
6. Joylashuvni yuborish
7. Buyurtma qabul qilinadi va guruhlarga yuboriladi

### Shopir sifatida ro'yxatdan o'tish:

1. "🚕 Shopir Bo'lish" tugmasini bosish
2. To'liq ismni kiritish
3. Telefon raqamini kiritish
4. Mashina rusumini kiritish (Nexia, Cobalt va h.k.)
5. Mashina raqamini kiritish (01 A 1234 BC)
6. Mashina rasmini yuborish
7. Admin tasdiqlashini kutish

### Admin funktsiyalari:

- Buyurtmalar avtomatik ikki guruhga va adminga yuboriladi
- Shopir arizalari adminga yuboriladi
- Admin "✅ Tasdiqlash" yoki "❌ Rad etish" tugmalarini bosadi
- Shopirga natija haqida xabar yuboriladi

## Fayl tuzilishi

```
taxi_bot/
├── bot.py              # Asosiy bot fayl
├── config.py           # Konfiguratsiya va environment variables
├── database.py         # Database funksiyalari
├── handlers.py         # Barcha handlerlar va callback'lar
├── states.py           # FSM (State Machine) states
├── keyboards.py        # Keyboard layouts
├── requirements.txt    # Python dependencies
├── .env.example       # Environment variables namunasi
├── .env               # Sizning konfiguratsiyangiz (git'ga qo'shilmaydi)
└── README.md          # Bu fayl
```

## Database

Bot SQLite database ishlatadi (`taxi_bot.db`):

- **users** - Foydalanuvchilar ma'lumotlari
- **orders** - Buyurtmalar tarixi
- **drivers** - Shopirlar va ularning statuslari

## Muammolarni hal qilish

### Bot ishga tushmayapti:
- `.env` faylida token to'g'ri kiritilganligini tekshiring
- Internet aloqangizni tekshiring
- Bot tokenini @BotFather dan qayta oling

### Guruhlarga xabar kelmayapti:
- Botni guruh adminlariga qo'shganingizni tekshiring
- Guruh ID larini to'g'ri kiritganingizni tekshiring (minus bilan)
- Botga "Send Messages" ruxsatini berganingizni tekshiring

### Admin tasdiqlash ishlamayapti:
- ADMIN_USER_ID to'g'ri kiritilganligini tekshiring
- User ID ni @userinfobot orqali qayta tekshiring

## Texnologiyalar

- **Python 3.10+**
- **aiogram 3.x** - Telegram Bot API framework
- **aiosqlite** - Async SQLite database
- **python-dotenv** - Environment variables

## Litsenziya

MIT License

## Muallif

Toshkent-Paxtobod Taxi Bot - 2024
