
from flask import Flask, render_template, request, redirect, url_for, send_file
import qrcode
import io
import sqlite3
import base64
from datetime import datetime

app = Flask(__name__)

DATABASE = "history.db"


def init_db():
    conn = sqlite3.connect(DATABASE)
    conn.execute("""
        CREATE TABLE IF NOT EXISTS history (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            content TEXT NOT NULL,
            qr_type TEXT NOT NULL,
            created_at TEXT NOT NULL
        )
    """)
    conn.commit()
    conn.close()


def save_history(content, qr_type):
    conn = sqlite3.connect(DATABASE)
    conn.execute(
        "INSERT INTO history (content, qr_type, created_at) VALUES (?, ?, ?)",
        (content, qr_type, datetime.now().strftime("%d-%m-%Y %H:%M:%S"))
    )
    conn.commit()
    conn.close()


def get_history():
    conn = sqlite3.connect(DATABASE)
    conn.row_factory = sqlite3.Row
    records = conn.execute(
        "SELECT * FROM history ORDER BY id DESC"
    ).fetchall()
    conn.close()
    return records


def generate_qr(content):
    qr = qrcode.make(content)
    buffer = io.BytesIO()
    qr.save(buffer, format="PNG")
    return base64.b64encode(buffer.getvalue()).decode("utf-8")


init_db()


@app.route("/")
def home():
    history = get_history()
    return render_template("index.html", history=history)


@app.route("/text", methods=["GET", "POST"])
def text_qr():
    qr_image = None
    text = ""

    if request.method == "POST":
        text = request.form.get("text", "").strip()

        if text:
            qr_image = generate_qr(text)
            save_history(text, "Text")

    return render_template("text.html", qr_image=qr_image, text=text)


@app.route("/link", methods=["GET", "POST"])
def link_qr():
    qr_image = None
    link = ""

    if request.method == "POST":
        link = request.form.get("link", "").strip()

        if link.startswith(("http://", "https://")):
            qr_image = generate_qr(link)
            save_history(link, "Link")

    return render_template("link.html", qr_image=qr_image, link=link)


@app.route("/download")
def download_qr():
    content = request.args.get("content", "").strip()
    qr_type = request.args.get("type", "")

    if not content or qr_type not in ("Text", "Link"):
        return redirect(url_for("home"))

    if qr_type == "Link" and not content.startswith(("http://", "https://")):
        return redirect(url_for("home"))

    qr = qrcode.make(content)
    buffer = io.BytesIO()
    qr.save(buffer, format="PNG")
    buffer.seek(0)

    return send_file(
        buffer,
        mimetype="image/png",
        as_attachment=True,
        download_name="qr_code.png"
    )


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5050)
