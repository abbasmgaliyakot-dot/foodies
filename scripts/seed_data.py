import asyncio
import sys
import os
sys.path.append('/app/backend')

from motor.motor_asyncio import AsyncIOMotorClient
from passlib.context import CryptContext
import uuid

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

async def seed_database():
    # Connect to MongoDB
    client = AsyncIOMotorClient(os.environ.get('MONGO_URL', 'mongodb://localhost:27017'))
    db = client[os.environ.get('DB_NAME', 'test_database')]
    
    print("Seeding database...")
    
    # Create admin user
    admin_exists = await db.users.find_one({"username": "admin"})
    if not admin_exists:
        admin_user = {
            "id": str(uuid.uuid4()),
            "username": "admin",
            "password_hash": pwd_context.hash("admin123"),
            "role": "admin"
        }
        await db.users.insert_one(admin_user)
        print("✓ Created admin user (username: admin, password: admin123)")
    else:
        print("✓ Admin user already exists")
    
    # Create staff user
    staff_exists = await db.users.find_one({"username": "staff"})
    if not staff_exists:
        staff_user = {
            "id": str(uuid.uuid4()),
            "username": "staff",
            "password_hash": pwd_context.hash("staff123"),
            "role": "staff"
        }
        await db.users.insert_one(staff_user)
        print("✓ Created staff user (username: staff, password: staff123)")
    else:
        print("✓ Staff user already exists")
    
    # Create sample tables
    table_count = await db.tables.count_documents({})
    if table_count == 0:
        tables = [
            {"id": str(uuid.uuid4()), "table_number": "T1", "capacity": 4, "status": "available", "current_order_id": None},
            {"id": str(uuid.uuid4()), "table_number": "T2", "capacity": 2, "status": "available", "current_order_id": None},
            {"id": str(uuid.uuid4()), "table_number": "T3", "capacity": 6, "status": "available", "current_order_id": None},
            {"id": str(uuid.uuid4()), "table_number": "T4", "capacity": 4, "status": "available", "current_order_id": None},
            {"id": str(uuid.uuid4()), "table_number": "T5", "capacity": 2, "status": "available", "current_order_id": None},
            {"id": str(uuid.uuid4()), "table_number": "T6", "capacity": 8, "status": "available", "current_order_id": None},
        ]
        await db.tables.insert_many(tables)
        print(f"✓ Created {len(tables)} sample tables")
    else:
        print(f"✓ Tables already exist ({table_count} tables)")
    
    # Create sample menu items
    menu_count = await db.menu_items.count_documents({})
    if menu_count == 0:
        menu_items = [
            {"id": str(uuid.uuid4()), "name": "Butter Chicken", "category": "Main Course", "price": 15.99, "description": "Creamy tomato curry"},
            {"id": str(uuid.uuid4()), "name": "Grilled Salmon", "category": "Main Course", "price": 22.99, "description": "Fresh Atlantic salmon"},
            {"id": str(uuid.uuid4()), "name": "Margherita Pizza", "category": "Main Course", "price": 12.99, "description": "Classic tomato and mozzarella"},
            {"id": str(uuid.uuid4()), "name": "Caesar Salad", "category": "Appetizers", "price": 8.99, "description": "Crispy romaine with parmesan"},
            {"id": str(uuid.uuid4()), "name": "Garlic Bread", "category": "Appetizers", "price": 5.99, "description": "Toasted with herbs"},
            {"id": str(uuid.uuid4()), "name": "Chocolate Lava Cake", "category": "Desserts", "price": 7.99, "description": "Warm chocolate cake"},
            {"id": str(uuid.uuid4()), "name": "Tiramisu", "category": "Desserts", "price": 8.99, "description": "Classic Italian dessert"},
            {"id": str(uuid.uuid4()), "name": "Coke", "category": "Beverages", "price": 2.99, "description": "Chilled soft drink"},
            {"id": str(uuid.uuid4()), "name": "Fresh Juice", "category": "Beverages", "price": 4.99, "description": "Orange or apple"},
            {"id": str(uuid.uuid4()), "name": "Coffee", "category": "Beverages", "price": 3.99, "description": "Freshly brewed"},
        ]
        await db.menu_items.insert_many(menu_items)
        print(f"✓ Created {len(menu_items)} sample menu items")
    else:
        print(f"✓ Menu items already exist ({menu_count} items)")
    
    print("\nDatabase seeded successfully!")
    print("\nLogin credentials:")
    print("  Admin - username: admin, password: admin123")
    print("  Staff - username: staff, password: staff123")
    
    client.close()

if __name__ == "__main__":
    asyncio.run(seed_database())
