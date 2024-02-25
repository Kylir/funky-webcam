import cv2
import numpy as np

# Load the PNG image with transparency (alpha channel)
heart_img = cv2.imread('heart.png', cv2.IMREAD_UNCHANGED)
heart_alpha = heart_img[:, :, 3] / 255.0
heart_color = heart_img[:, :, :3]

# Open webcam
cap = cv2.VideoCapture(2)

while True:
    ret, frame = cap.read()
    if not ret:
        break

    # Define where to place the heart image on the frame (top-left corner)
    y1, y2 = 50, 50 + heart_img.shape[0]
    x1, x2 = 50, 50 + heart_img.shape[1]

    # Resize heart image to fit designated area
    heart_resized_color = cv2.resize(heart_color, (x2 - x1, y2 - y1))
    heart_resized_alpha = cv2.resize(heart_alpha, (x2 - x1, y2 - y1))

    # Extract the region of interest (ROI) from the frame
    roi = frame[y1:y2, x1:x2]

    # Blend the heart image with the ROI based on alpha channel
    for c in range(0, 3):
        roi[:, :, c] = (heart_resized_alpha * heart_resized_color[:, :, c] +
                        (1 - heart_resized_alpha) * roi[:, :, c])

    # Put the modified ROI back into the original frame
    frame[y1:y2, x1:x2] = roi

    # Display the frame
    cv2.imshow('Webcam with Heart', frame)

    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

cap.release()
cv2.destroyAllWindows()