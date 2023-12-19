from flask import Flask, render_template, request, redirect, url_for
from flask_uploads import UploadSet, configure_uploads, IMAGES
from PIL import Image
import tensorflow as tf
from tensorflow.keras.applications.inception_v3 import InceptionV3
from tensorflow.keras.applications.inception_v3 import preprocess_input, decode_predictions
import numpy as np

app = Flask(_name_)

# Configuration for file uploads
photos = UploadSet("photos", IMAGES)
app.config["UPLOADED_PHOTOS_DEST"] = "uploads"
configure_uploads(app, photos)

# Load pre-trained InceptionV3 model
model = InceptionV3(weights="imagenet")
graph = tf.compat.v1.get_default_graph()  # TensorFlow 2.x compatibility

def process_image(image_path):
    img = Image.open(image_path)
    img = img.resize((299, 299))
    img_array = np.array(img)
    img_array = np.expand_dims(img_array, axis=0)
    img_array = preprocess_input(img_array)
    return img_array

def predict_caption(image_path):
    global graph
    with graph.as_default():
        img_array = process_image(image_path)
        predictions = model.predict(img_array)
        labels = decode_predictions(predictions)
        # Extract top prediction label
        top_label = labels[0][0][1]
        return f"This image may contain: {top_label}"

@app.route("/", methods=["GET", "POST"])
def index():
    if request.method == "POST" and "photo" in request.files:
        photo = request.files["photo"]
        if photo.filename != "":
            photo_path = f"uploads/{photo.filename}"
            photo.save(photo_path)
            caption = predict_caption(photo_path)
            return render_template("index.html", image_path=photo_path, caption=caption)
    return render_template("index.html", image_path=None, caption=None)

if _name_ == "_main_":
    app.run(debug=True)