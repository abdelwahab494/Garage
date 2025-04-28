import sqlite3

def init_db():
    conn = sqlite3.connect('task_manager.db')
    cursor = conn.cursor()

    # إنشاء جدول current_cars
    cursor.execute('''
    CREATE TABLE current_cars (
        phone INTEGER PRIMARY KEY NOT NULL,
        client_name TEXT NOT NULL,
        car_number TEXT NOT NULL,
        car_model TEXT,
        location TEXT NOT NULL,
        car_color TEXT,
        date DATETIME NOT NULL DEFAULT current_timestamp
    )
    ''')

    # إنشاء جدول history
    cursor.execute('''
    CREATE TABLE history (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        phone INTEGER NOT NULL,
        client_name TEXT NOT NULL,
        car_number TEXT NOT NULL,
        car_model TEXT,
        location TEXT NOT NULL,
        car_color TEXT,
        date DATETIME NOT NULL DEFAULT current_timestamp
    )
    ''')

    cursor.execute('''
    CREATE TABLE requested_cars (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        phone INTEGER NOT NULL,
        car_number TEXT NOT NULL,
        location TEXT NOT NULL
    )
    ''')

    count = cursor.execute("SELECT COUNT(id) FROM requested_cars").fietchone()[0]

    conn.commit()
    conn.close()
    print("Database initialized successfully!")

if __name__ == "__main__":
    init_db()
