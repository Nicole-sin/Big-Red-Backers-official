# setup_test_data.py

from db import DatabaseDriver

def run():
    db = DatabaseDriver()
    db.create_tables()

    print("Inserting sample data...")

    user_id = db.create_user()
    print(f"Created user with ID: {user_id}")

    dining_hall_ids = []
    halls = ["North Dining Hall", "South Dining Hall", "West Dining Hall"]
    for hall in halls:
        db.cursor.execute("INSERT INTO dining_halls (name) VALUES (?)", (hall,))
        dining_hall_ids.append(db.cursor.lastrowid)
        print(f"Created dining hall: {hall} with ID: {db.cursor.lastrowid}")

    food_items = [
        ("Pizza", "pizza.jpeg", dining_hall_ids[0]),
        ("Biscuit", "biscuit.jpeg", dining_hall_ids[0]),
        ("Ravioli Pasta", "ravioli_pasta.jpeg", dining_hall_ids[1]),
        ("Tofu Salad", "spicy_tofu_salad.jpeg", dining_hall_ids[1]),
        ("Ravioli", "ravioli.jpeg", dining_hall_ids[2]),
        ("Tofu", "tofu.jpeg", dining_hall_ids[2]),
    ]

    for name, image, hall_id in food_items:
        db.cursor.execute(
            "INSERT INTO food_items (name, image, dining_hall_id) VALUES (?, ?, ?)",
            (name, image, hall_id)
        )
        print(f"Created food item: {name}")

    db.commit()
    print("Sample data loaded successfully.")
