import cv2
import numpy as np
from keras.models import load_model
import time

# Load your trained AI model and labels
print("Loading AI model...")
model = load_model("keras_model.h5", compile=False)

# Read the labels file (xtpara, defup, hcqs)
with open("labels.txt", "r") as f:
    labels = [line.strip() for line in f.readlines()]

print("Model loaded! Labels:", labels)

# Open webcam
camera = cv2.VideoCapture(0)
print("Camera warming up...")
time.sleep(2)

# Throwaway frames
for i in range(5):
    camera.read()

print("\nReady! Showing you what the AI sees...")
print("Press ENTER to identify the medicine in front of the camera.")
print("Press Ctrl+C to quit.\n")

while True:
    # Wait for user to press Enter
    input("👉 Hold medicine in front of camera, then press ENTER: ")

    # Capture photo
    success, photo = camera.read()

    if not success:
        print("Camera error. Try again.")
        continue

    # Resize photo to 224x224 (what the AI expects)
    photo_resized = cv2.resize(photo, (224, 224))

    # Normalize pixel values (AI expects numbers between -1 and 1)
    photo_array = np.array(photo_resized, dtype=np.float32)
    photo_array = (photo_array / 127.5) - 1

    # Add an extra dimension (AI expects a "batch" of photos)
    photo_batch = np.expand_dims(photo_array, axis=0)

    # Ask the AI to predict
    predictions = model.predict(photo_batch, verbose=0)

    # Find which medicine scored highest
    highest_index = np.argmax(predictions[0])
    medicine_name = labels[highest_index]
    confidence = predictions[0][highest_index] * 100

    print(f"\n🔍 AI says: {medicine_name.upper()} ({confidence:.1f}% confident)")
    print(f"   All scores: xtpara={predictions[0][0]*100:.1f}% | defup={predictions[0][1]*100:.1f}% | hcqs={predictions[0][2]*100:.1f}%\n")

camera.release() 