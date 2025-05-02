#!/usr/bin/env python3
"""
Database initialization script for the Dining Hall Review API
This script creates sample data for testing the API with Postman
"""
import sqlite3
import os

DB_PATH = "app.db"

if os.path.exists(DB_PATH):
    os.remove(DB_PATH)
    print(f"Deleted existing database: {DB_PATH}")
conn = sqlite3.connect(DB_PATH)
cursor = conn.cursor()

cursor.execute('''
CREATE TABLE IF NOT EXISTS users (
    id INTEGER PRIMARY KEY AUTOINCREMENT
)
''')

cursor.execute('''
CREATE TABLE IF NOT EXISTS dining_halls (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    name TEXT NOT NULL
)
''')

cursor.execute('''
CREATE TABLE IF NOT EXISTS food_items (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    name TEXT NOT NULL,
    image TEXT,
    dining_hall_id INTEGER NOT NULL,
    FOREIGN KEY (dining_hall_id) REFERENCES dining_halls (id)
)
''')

cursor.execute('''
CREATE TABLE IF NOT EXISTS reviews (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    user_id INTEGER NOT NULL,
    rating INTEGER NOT NULL,
    message TEXT,
    food_id INTEGER NOT NULL,
    dining_hall_id INTEGER NOT NULL,
    FOREIGN KEY (user_id) REFERENCES users (id),
    FOREIGN KEY (food_id) REFERENCES food_items (id),
    FOREIGN KEY (dining_hall_id) REFERENCES dining_halls (id)
)
''')

cursor.execute('''
CREATE TABLE IF NOT EXISTS review_recommended_food (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    review_id INTEGER NOT NULL,
    food_item_id INTEGER NOT NULL,
    FOREIGN KEY (review_id) REFERENCES reviews (id),
    FOREIGN KEY (food_item_id) REFERENCES food_items (id)
)
''')

print("Inserting sample data...")

cursor.execute("INSERT INTO users DEFAULT VALUES")
user_id = cursor.lastrowid
print(f"Created user with ID: {user_id}")

dining_halls = [
    "North Dining Hall",
    "South Dining Hall",
    "West Dining Hall"
]

dining_hall_ids = []
for hall in dining_halls:
    cursor.execute("INSERT INTO dining_halls (name) VALUES (?)", (hall,))
    hall_id = cursor.lastrowid
    dining_hall_ids.append(hall_id)
    print(f"Created dining hall: {hall} with ID: {hall_id}")

food_items = [
    ("Pizza", "pizza.jpeg", dining_hall_ids[0]),
    ("Biscuit", "biscuit.jpeg", dining_hall_ids[0]),  
    ("Ravioli Pasta", "ravioli_pasta.jpeg", dining_hall_ids[1]),
    ("Tofu Salad", "spicy_tofu_salad.jpeg", dining_hall_ids[1]),
    ("Ravioli", "ravioli.jpeg", dining_hall_ids[2]), 
    ("Tofu", "tofu.jpeg", dining_hall_ids[2]),
]


food_item_ids = []
for name, image, hall_id in food_items:
    cursor.execute(
        "INSERT INTO food_items (name, image, dining_hall_id) VALUES (?, ?, ?)",
        (name, image, hall_id)
    )
    item_id = cursor.lastrowid
    food_item_ids.append(item_id)
    print(f"Created food item: {name} with ID: {item_id}")

conn.commit()
conn.close()

print("\nDatabase initialization complete!")
print("You can now run the Flask app and test it with Postman.")
print("To start the Flask app, run: python app.py")