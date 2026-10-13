
from flask import Flask, render_template, request
import qrcode
import io
import base64

app = Flask(__name__)


@app.route("/", methods=["GET", "POST"])
def home():
    qr_image = None
    text = ""

    if request.method == "POST":
        text = request.form.get("text", "").strip()

        if text:
            qr = qrcode.make(text)

            buffer = io.BytesIO()
            qr.save(buffer, format="PNG")

            qr_image = base64.b64encode(
                buffer.getvalue()
            ).decode("utf-8")

    return render_template(
        "index.html",
        qr_image=qr_image,
        text=text
    )


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5050)
