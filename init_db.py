import sqlite3

conn = sqlite3.connect("database.db")
cursor = conn.cursor()

cursor.execute("""
CREATE TABLE IF NOT EXISTS courses (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    title TEXT NOT NULL,
    description TEXT NOT NULL,
    image_url TEXT NOT NULL
)
""")


cursor.execute("DELETE FROM courses")
cursor.execute("DELETE FROM sqlite_sequence WHERE name='courses'")

courses_data = [
    (
        "Introduction to Programming",
        "The first gateway to learning programming.",
        "https://i.pinimg.com/1200x/b5/f6/a9/b5f6a9ab784b1a548416ce816fa7d01f.jpg",
    ),
    (
        "Python language",
        "A course to learn Python at a professional level.",
        "https://i.pinimg.com/736x/42/2d/8b/422d8b254521ae7162b32b0284d11569.jpg",
    ),
    (
        "Web development",
        "The best course for learning web development.",
        "https://i.pinimg.com/736x/47/3b/a6/473ba641121eae735636ce746a00e3db.jpg",
    ),
    (
        "Encryption",
        "Learn about the history of cryptography.",
        "https://i.pinimg.com/736x/ff/93/4d/ff934d9c42934e4fbdeeb7a08edeb8cd.jpg",
    ),
]

cursor.executemany(
    "INSERT INTO courses (title, description, image_url) VALUES (?, ?, ?)",
    courses_data,
)
conn.commit()
conn.close()

print("--> Database setup completed successfully!")