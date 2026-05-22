import cv2
import time
import os

# ===== CHANGE THIS FOR EACH MEDICINE =====
medicine_name = "defup" \
""  # Change to "defup" or "hcqs" for those medicines
number_of_photos = 20     # How many photos to take
# =========================================

# Make sure the folder exists
folder_path = f"medicines/{medicine_name}"
if not os.path.exists(folder_path):
    os.makedirs(folder_path)
    print(f"Created folder: {folder_path}")

# Open webcam
camera = cv2.VideoCapture(0)
print("Camera warming up...")
time.sleep(2)

# Throwaway frames so camera adjusts
for i in range(5):
    camera.read()

print(f"\nReady! Taking {number_of_photos} photos of '{medicine_name}'.")
print("HOLD THE MEDICINE STRIP IN FRONT OF THE CAMERA NOW.")
print("Slowly rotate, tilt, and move it during the shoot.\n")
time.sleep(3)  # Give you 3 seconds to get ready

# Take the photos
for i in range(number_of_photos):
    success, photo = camera.read()
    if success:
        filename = f"{folder_path}/photo_{i+1}.jpg"
        cv2.imwrite(filename, photo)
        print(f"  Saved photo {i+1} of {number_of_photos}")
        time.sleep(1)  # Wait 1 second before next photo
    else:
        print(f"  Failed to capture photo {i+1}")

camera.release()
print(f"\nDone! All photos saved in {folder_path}") 
