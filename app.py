from flask import Flask, render_template
from app.routes import ocr_bp

app = Flask(__name__)
app.register_blueprint(ocr_bp)

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000, use_reloader=True)
