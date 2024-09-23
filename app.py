import streamlit as st
import easyocr
import numpy as np
import cv2
app = Flask(__name__)
CORS(app)

print("Initializing EasyOCR Reader...")
reader = easyocr.Reader(['en'])
print("EasyOCR Reader Initialized!")

@app.route('/ocr', methods=['POST'])
def process_image():
    try:
        print("Received request at /ocr")
        if 'image' not in request.files:
            print("No image found in the request.")
            return jsonify({"error": "No image uploaded"}), 400

        file = request.files['image']
        image = np.frombuffer(file.read(), np.uint8)
        image = cv2.imdecode(image, cv2.IMREAD_COLOR)

        print("Image received and processed successfully.")
        print("Running OCR on the image...")
        result = reader.readtext(image)
        print("OCR complete.")

        # Extract only the detected text and convert to standard Python types
        detected_text = []
        for bbox, text, confidence in result:
            detected_text.append({
                "text": text,
                "confidence": float(confidence)  # Convert numpy float to Python float
            })

        print(f"Returning {len(detected_text)} results.")
        return jsonify({"detected_text": detected_text})

    except Exception as e:
        print(f"An error occurred: {e}")
        return jsonify({"error": str(e)}), 500

if __name__ == '__main__':
    print("Starting Flask server on http://localhost:3000")
    app.run(debug=True, host="0.0.0.0", port=3000, threaded=True)
