import sqlite3
from flask import Flask, redirect, render_template, request, session, url_for
from werkzeug.security import generate_password_hash, check_password_hash

app = Flask(__name__)
app.secret_key = "my_secret_key_123"


def get_db_connection():
    conn = sqlite3.connect("database.db")
    conn.row_factory = sqlite3.Row
    return conn


def init_db():
    conn = get_db_connection()
    conn.execute("""
        CREATE TABLE IF NOT EXISTS users (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            username TEXT UNIQUE NOT NULL,
            password TEXT NOT NULL
        )
    """)
    conn.commit()
    conn.close()


init_db()


# الصفحة الرئيسية والكورسات 

@app.route("/")
def index():
    conn = get_db_connection()
    courses = conn.execute("SELECT * FROM courses").fetchall()
    conn.close()
    return render_template("index.html", courses=courses)


@app.route("/course/<int:course_id>")
def course_detail(course_id):
    return render_template(f"k{course_id}.html")


#تسجيل الدخول 

@app.route("/login", methods=["GET", "POST"])
def login():
    if request.method == "POST":
        username = request.form.get("username")
        password = request.form.get("password")

        conn = get_db_connection()
        user = conn.execute(
            "SELECT * FROM users WHERE username = ?", (username,)
        ).fetchone()
        conn.close()

        if user and check_password_hash(user["password"], password):
            session["user"] = user["username"]
            return redirect(url_for("index"))
        else:
            return render_template("login.html", error="اسم المستخدم أو كلمة المرور غير صحيحة")

    return render_template("login.html")


# إنشاء حساب 

@app.route("/signup", methods=["GET", "POST"])
def signup():
    if request.method == "POST":
        username = request.form.get("username")
        password = request.form.get("password")
        confirm_password = request.form.get("confirm_password")

        if password != confirm_password:
            return render_template("signup.html", error="كلمة المرور غير متطابقة")

        conn = get_db_connection()

        existing_user = conn.execute(
            "SELECT * FROM users WHERE username = ?", (username,)
        ).fetchone()

        if existing_user:
            conn.close()
            return render_template("signup.html", error="اسم المستخدم موجود مسبقاً")

        hashed_password = generate_password_hash(password)

        conn.execute(
            "INSERT INTO users (username, password) VALUES (?, ?)",
            (username, hashed_password)
        )
        conn.commit()
        conn.close()

        session["user"] = username
        return redirect(url_for("index"))

    return render_template("signup.html")


# تسجيل الخروج والحساب 

@app.route("/logout")
def logout():
    session.pop("user", None)
    return redirect(url_for("index"))


@app.route("/account")
def account():
    if not session.get("user"):
        return redirect(url_for("login"))
    return render_template("account.html", user=session.get("user"))


if __name__ == "__main__":
    app.run(debug=True)