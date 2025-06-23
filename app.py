from flask import Flask

app = Flask(__name__)

@app.route("/")
def home():
    return "PDF to Image API is working"
