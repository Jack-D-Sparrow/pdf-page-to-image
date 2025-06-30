from flask import Flask, request, jsonify
from pdf2image import convert_from_bytes
import requests
import base64
import io

app = Flask(__name__)

@app.route("/")
def home():
    return "PDF to Image service is running"

@app.route("/convert", methods=["POST"])
def convert_single_page():
    try:
        data = request.get_json()
        pdf_url = data.get("pdf_url")
        page_number = data.get("page_number")

        if not pdf_url or page_number is None:
            return jsonify({"error": "Missing 'pdf_url' or 'page_number'"}), 400

        response = requests.get(pdf_url)
        if response.status_code != 200:
            return jsonify({"error": "Failed to download PDF"}), 400

        images = convert_from_bytes(response.content, dpi=150, first_page=page_number, last_page=page_number)

        if not images:
            return jsonify({"error": "Page not found"}), 404

        img = images[0]
        img_bytes = io.BytesIO()
        img.save(img_bytes, format="JPEG")
        img_base64 = base64.b64encode(img_bytes.getvalue()).decode("utf-8")

        return jsonify({
            "page_number": page_number,
            "image_base64": img_base64
        })

    except Exception as e:
        return jsonify({"error": str(e)}), 500

@app.route("/info", methods=["POST"])
def get_pdf_info():
    try:
        data = request.get_json()
        pdf_url = data.get("pdf_url")

        if not pdf_url:
            return jsonify({"error": "Missing 'pdf_url'"}), 400

        response = requests.get(pdf_url)
        if response.status_code != 200:
            return jsonify({"error": "Failed to download PDF"}), 400

        images = convert_from_bytes(response.content, dpi=150)
        total_pages = len(images)

        return jsonify({
            "total_pages": total_pages
        })

    except Exception as e:
        return jsonify({"error": str(e)}), 500

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=10000)
