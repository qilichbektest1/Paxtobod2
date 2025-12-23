import aiosqlite
from config import DATABASE_PATH


async def init_db():
    """Initialize database tables"""
    async with aiosqlite.connect(DATABASE_PATH) as db:
        # Users table
        await db.execute("""
            CREATE TABLE IF NOT EXISTS users (
                user_id INTEGER PRIMARY KEY,
                username TEXT,
                first_name TEXT,
                phone TEXT,
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
            )
        """)

        # Orders table
        await db.execute("""
            CREATE TABLE IF NOT EXISTS orders (
                order_id INTEGER PRIMARY KEY AUTOINCREMENT,
                user_id INTEGER,
                direction TEXT,
                passengers INTEGER,
                order_type TEXT,
                phone TEXT,
                location_lat REAL,
                location_lon REAL,
                status TEXT DEFAULT 'pending',
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                FOREIGN KEY (user_id) REFERENCES users(user_id)
            )
        """)

        await db.execute("""
            CREATE TABLE IF NOT EXISTS drivers (
                driver_id INTEGER PRIMARY KEY AUTOINCREMENT,
                user_id INTEGER,
                full_name TEXT,
                phone TEXT,
                car_model TEXT,
                car_number TEXT,
                photo_file_id TEXT,
                status TEXT DEFAULT 'pending',
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                FOREIGN KEY (user_id) REFERENCES users(user_id)
            )
        """)

        await db.commit()


async def add_user(user_id: int, username: str, first_name: str):
    """Add or update user in database"""
    async with aiosqlite.connect(DATABASE_PATH) as db:
        await db.execute("""
            INSERT OR REPLACE INTO users (user_id, username, first_name)
            VALUES (?, ?, ?)
        """, (user_id, username, first_name))
        await db.commit()


async def create_order(user_id: int, direction: str, passengers: int, order_type: str):
    """Create new order"""
    async with aiosqlite.connect(DATABASE_PATH) as db:
        cursor = await db.execute("""
            INSERT INTO orders (user_id, direction, passengers, order_type)
            VALUES (?, ?, ?, ?)
        """, (user_id, direction, passengers, order_type))
        await db.commit()
        return cursor.lastrowid


async def update_order_contact(order_id: int, phone: str, location_lat: float, location_lon: float):
    """Update order with contact and location"""
    async with aiosqlite.connect(DATABASE_PATH) as db:
        await db.execute("""
            UPDATE orders 
            SET phone = ?, location_lat = ?, location_lon = ?
            WHERE order_id = ?
        """, (phone, location_lat, location_lon, order_id))
        await db.commit()


async def create_driver_application(user_id: int, full_name: str, phone: str, car_model: str, car_number: str,
                                    photo_file_id: str):
    """Create new driver application"""
    async with aiosqlite.connect(DATABASE_PATH) as db:
        cursor = await db.execute("""
            INSERT INTO drivers (user_id, full_name, phone, car_model, car_number, photo_file_id, status)
            VALUES (?, ?, ?, ?, ?, ?, 'pending')
        """, (user_id, full_name, phone, car_model, car_number, photo_file_id))
        await db.commit()
        return cursor.lastrowid


async def update_driver_status(driver_id: int, status: str):
    """Update driver application status"""
    async with aiosqlite.connect(DATABASE_PATH) as db:
        await db.execute("""
            UPDATE drivers 
            SET status = ?
            WHERE driver_id = ?
        """, (status, driver_id))
        await db.commit()


async def get_driver_by_id(driver_id: int):
    """Get driver information by ID"""
    async with aiosqlite.connect(DATABASE_PATH) as db:
        async with db.execute("""
            SELECT driver_id, user_id, full_name, phone, car_model, car_number, photo_file_id, status
            FROM drivers
            WHERE driver_id = ?
        """, (driver_id,)) as cursor:
            row = await cursor.fetchone()
            if row:
                return {
                    'driver_id': row[0],
                    'user_id': row[1],
                    'full_name': row[2],
                    'phone': row[3],
                    'car_model': row[4],
                    'car_number': row[5],
                    'photo_file_id': row[6],
                    'status': row[7]
                }
            return None