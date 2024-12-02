from flask import Flask, render_template, request, redirect, url_for, flash
import os
from tensorflow.keras.models import load_model
from tensorflow.keras.preprocessing import image
import numpy as np

app = Flask(__name__)
app.config['UPLOAD_FOLDER'] = 'uploads'
app.secret_key = 'your_secret_key'

# Load CNN model
MODEL_PATH = 'model_ikan.h5'  # Ganti dengan path ke model Anda
model = load_model(MODEL_PATH)

# Define label classes
LABELS = ['Mujahir', 'Red Devil', 'Sepat']

# Helper function for image preprocessing
def preprocess_image(img_path):
    img = image.load_img(img_path, target_size=(224, 224))  # Sesuaikan IMG_SIZE
    img_array = image.img_to_array(img) / 255.0
    img_array = np.expand_dims(img_array, axis=0)
    return img_array

@app.route("/")
def home():
    return render_template("index.html")

@app.route("/about")
def about():
    return render_template("about.html")

@app.route("/klasifikasi", methods=["GET", "POST"])
def klasifikasi():
    if request.method == "POST":
        # Cek apakah ada file yang diunggah
        if "image" not in request.files:
            flash("Tidak ada file yang diunggah.")
            return redirect(request.url)

        file = request.files["image"]
        if file.filename == "":
            flash("Pilih file sebelum mengunggah.")
            return redirect(request.url)

        if file:
            # Simpan file gambar yang diunggah
            file_path = os.path.join(app.config['UPLOAD_FOLDER'], file.filename)
            file.save(file_path)

            # Preproses gambar dan prediksi menggunakan model
            img = preprocess_image(file_path)
            predictions = model.predict(img)
            class_index = np.argmax(predictions, axis=1)[0]
            accuracy = round(np.max(predictions) * 100, 2)

            # Hasil klasifikasi
            result = {
                "jenis_ikan": LABELS[class_index],
                "akurasi": accuracy
            }

            return render_template("klasifikasi.html", result=result)

    return render_template("klasifikasi.html", result=None)

if __name__ == "__main__":
    os.makedirs(app.config['UPLOAD_FOLDER'], exist_ok=True)
    app.run(debug=True)
