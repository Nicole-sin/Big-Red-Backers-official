import sqlite3
from sqlite3 import Error


def singleton(cls):
    instances = {}
    def getinstance():
        if cls not in instances:
            instances[cls] = cls()
        return instances[cls]

    return getinstance

@singleton
class DatabaseDriver:
    def __init__(self, db_path="app.db"):
        self.conn = None
        self.db_path = db_path
        self._connect()

    def _connect(self):
        try:
            self.conn = sqlite3.connect(self.db_path, check_same_thread=False)
            self.conn.row_factory = sqlite3.Row
            self.cursor = self.conn.cursor()
        except Error as e:
            print(f"Error connecting to database: {e}")

    def create_tables(self):
        self.cursor.execute('''
            CREATE TABLE IF NOT EXISTS users (
                id INTEGER PRIMARY KEY AUTOINCREMENT
            )
        ''')
        self.cursor.execute('''
            CREATE TABLE IF NOT EXISTS dining_halls (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                name TEXT NOT NULL
            )
        ''')
        self.cursor.execute('''
            CREATE TABLE IF NOT EXISTS food_items (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                name TEXT NOT NULL,
                image TEXT,
                dining_hall_id INTEGER NOT NULL,
                FOREIGN KEY (dining_hall_id) REFERENCES dining_halls (id)
            )
        ''')
        self.cursor.execute('''
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
        self.cursor.execute('''
            CREATE TABLE IF NOT EXISTS review_recommended_food (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                review_id INTEGER NOT NULL,
                food_item_id INTEGER NOT NULL,
                FOREIGN KEY (review_id) REFERENCES reviews (id),
                FOREIGN KEY (food_item_id) REFERENCES food_items (id)
            )
        ''')
        self.conn.commit()

    def commit(self):
        self.conn.commit()

    def close(self):
        if self.conn:
            self.conn.close()

    def create_user(self):
        self.cursor.execute("INSERT INTO users DEFAULT VALUES")
        self.conn.commit()
        return self.cursor.lastrowid

    def get_user(self, user_id):
        self.cursor.execute("SELECT * FROM users WHERE id = ?", (user_id,))
        return self.cursor.fetchone()

    def get_dining_hall(self, hall_id):
        self.cursor.execute("SELECT * FROM dining_halls WHERE id = ?", (hall_id,))
        return self.cursor.fetchone()

    def get_all_dining_halls(self):
        self.cursor.execute("SELECT * FROM dining_halls")
        halls = self.cursor.fetchall()
        result = []
        for hall in halls:
            hall_dict = dict(hall)
            self.cursor.execute(
                "SELECT * FROM food_items WHERE dining_hall_id = ?",
                (hall['id'],)
            )
            hall_dict['food_items'] = [dict(item) for item in self.cursor.fetchall()]
            result.append(hall_dict)
        return result

    def get_food_items_by_dining_hall(self, hall_id):
        self.cursor.execute(
            "SELECT * FROM food_items WHERE dining_hall_id = ?",
            (hall_id,)
        )
        return self.cursor.fetchall()

    def get_food_item(self, food_id):
        self.cursor.execute("SELECT * FROM food_items WHERE id = ?", (food_id,))
        return self.cursor.fetchone()

    def create_review(self, user_id, food_id, dining_hall_id, rating, message=""):
        self.cursor.execute(
            '''
            INSERT INTO reviews (user_id, food_id, dining_hall_id, rating, message)
            VALUES (?, ?, ?, ?, ?)
            ''',
            (user_id, food_id, dining_hall_id, rating, message)
        )
        self.conn.commit()
        return self.cursor.lastrowid

    def get_review(self, review_id):
        self.cursor.execute("SELECT * FROM reviews WHERE id = ?", (review_id,))
        return self.cursor.fetchone()

    def get_all_reviews(self):
        self.cursor.execute("SELECT * FROM reviews")
        reviews = self.cursor.fetchall()
        return [self._expand_review(dict(r)) for r in reviews]

    def get_reviews_by_user(self, user_id):
        self.cursor.execute("SELECT * FROM reviews WHERE user_id = ?", (user_id,))
        reviews = self.cursor.fetchall()
        return [self._expand_review(dict(r)) for r in reviews]

    def _expand_review(self, review_dict):
        food_item = self.get_food_item(review_dict['food_id'])
        if food_item:
            review_dict['food_item'] = {
                'id': food_item['id'],
                'name': food_item['name'],
                'image': food_item['image']
            }
        dining_hall = self.get_dining_hall(review_dict['dining_hall_id'])
        if dining_hall:
            review_dict['dining_hall'] = {
                'id': dining_hall['id'],
                'name': dining_hall['name']
            }
        review_dict['recommended_foods'] = self.get_recommended_foods_for_review(review_dict['id'])
        return review_dict

    def delete_review(self, review_id):
        self.cursor.execute("DELETE FROM review_recommended_food WHERE review_id = ?", (review_id,))
        self.cursor.execute("DELETE FROM reviews WHERE id = ?", (review_id,))
        self.conn.commit()

    def add_recommended_food(self, review_id, food_item_id):
        self.cursor.execute(
            '''
            INSERT INTO review_recommended_food (review_id, food_item_id)
            VALUES (?, ?)
            ''',
            (review_id, food_item_id)
        )
        self.conn.commit()

    def get_recommended_foods_for_review(self, review_id):
        self.cursor.execute(
            '''
            SELECT rf.food_item_id, fi.name
            FROM review_recommended_food rf
            JOIN food_items fi ON rf.food_item_id = fi.id
            WHERE rf.review_id = ?
            ''',
            (review_id,)
        )
        return [{'id': row['food_item_id'], 'name': row['name']} for row in self.cursor.fetchall()]


def create_all():
    db = DatabaseDriver()
    db.create_tables()
