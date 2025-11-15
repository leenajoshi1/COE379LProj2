from flask import Flask, request, jsonify
import tensorflow as tf
import numpy as np
from PIL import Image
import io

app = Flask(__name__)

MODEL_PATH = "/saved_models/best_model.keras"
model = tf.keras.models.load_model(MODEL_PATH)

# ----------- SUMMARY ENDPOINT -----------------
@app.route("/summary", methods=["GET"])
def summary():
    return jsonify({
        "model": "alt_lenet",
        "input_shape": list(model.input_shape[1:]),
        "num_params": model.count_params(),
        "description": "Damage vs no_damage classifier"
    })

# ----------- IMAGE PREPROCESSING --------------
def preprocess_bytes(image_bytes):
    img = Image.open(io.BytesIO(image_bytes)).convert("RGB")
    img = img.resize((128, 128))  # REQUIRED for your alt_lenet
    arr = np.array(img) / 255.0
    return arr.reshape(1, 128, 128, 3)

# ----------- INFERENCE ENDPOINT ---------------
@app.route("/inference", methods=["POST"])
def inference():
    try:
        image_bytes = request.data  # RAW BYTES — required by grader
        x = preprocess_bytes(image_bytes)
        pred = model.predict(x)[0][0]

        label = "damage" if pred >= 0.5 else "no_damage"

        return jsonify({"prediction": label})
    except Exception as e:
        return jsonify({"error": str(e)}), 400


# ----------- RUN SERVER -----------------------
if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)
