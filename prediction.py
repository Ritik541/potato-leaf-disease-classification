
import tensorflow as tf
import numpy as np
from PIL import Image
from pathlib import Path

# Project folder ka path
BASE_DIR = Path(__file__).resolve().parent

# Trained model load karna
model = tf.keras.models.load_model(
    BASE_DIR / "potato_cnn_model.keras"
)

# Class names load karna
with open(BASE_DIR / "classification_report.txt", "r") as file:
    class_names = file.read().splitlines()


# Prediction function
def predict_disease(image):

    # Image ko RGB mein convert karna
    image = image.convert("RGB")

    # Image resize karna
    image = image.resize((128, 128))

    # Image ko NumPy array banana
    image_array = np.array(image, dtype=np.float32)

    # Batch dimension add karna
    image_array = np.expand_dims(image_array, axis=0)

    # CNN model se prediction
    predictions = model.predict(image_array, verbose=0)[0]

    # Highest score ka index
    best_index = int(np.argmax(predictions))

    # Predicted disease
    predicted_class = class_names[best_index]

    # Confidence score
    confidence = float(predictions[best_index])

    return predicted_class, confidence, predictions




if __name__ == "__main__":

    image = Image.open(BASE_DIR / "leaf.JPG")

    result = predict_disease(image)

    print("Predicted Disease:", result[0])
    print("Confidence:", result[1] * 100, "%")

    print("\nAll Predictions:")

    for name, score in zip(class_names, result[2]):
        print(name, ":", round(float(score) * 100, 2), "%")
