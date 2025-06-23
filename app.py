from flask import Flask, request, jsonify
from pdf2image import convert_from_path
import requests
import os
import uuid

app = Flask(__name__)

@app.route("/")
def home():
    return "PDF to Image API is live"

@app.route("/convert", methods=["POST"])
def convert_pdf_to_images():
    try:
        data = request.get_json()
        pdf_url = data.get("pdf_url")

        if not pdf_url:
            return jsonify({"error": "Missing 'pdf_url' in request"}), 400

        # Download PDF
        response = requests.get(pdf_url)
        temp_pdf_path = f"temp_{uuid.uuid4()}.pdf"
        with open(temp_pdf_path, "wb") as f:
            f.write(response.content)

        # Convert to images
        output_folder = f"output_{uuid.uuid4()}"
        os.makedirs(output_folder, exist_ok=True)

        pages = convert_from_path(temp_pdf_path, dpi=200)
        image_paths = []

        for i, page in enumerate(pages, start=1):
            img_path = os.path.join(output_folder, f"{i}.png")
            page.save(img_path, "PNG")
            image_paths.append(img_path)

        # Clean up PDF
        os.remove(temp_pdf_path)

        return jsonify({
            "message": "Conversion successful",
            "images": image_paths
        })

    except Exception as e:
        return jsonify({"error": str(e)}), 500

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=10000)

