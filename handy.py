import cv2
import mediapipe as mp
import pyfakewebcam

# Initialize MediaPipe Hands.
mp_hands = mp.solutions.hands
hands = mp_hands.Hands(
    static_image_mode=False,
    max_num_hands=2,
    min_detection_confidence=0.5,
    min_tracking_confidence=0.5)

# For drawing the landmarks on the image.
mp_drawing = mp.solutions.drawing_utils

cap = cv2.VideoCapture(2)  # Capture video from the first webcam

# Get the width and height of the video frame
width = int(cap.get(cv2.CAP_PROP_FRAME_WIDTH))
height = int(cap.get(cv2.CAP_PROP_FRAME_HEIGHT))

# Create a fake webcam device (replace 'video1' with your device's name)
# fake_webcam = pyfakewebcam.FakeWebcam('/dev/video4', width, height)

# Load the PNG image with transparency (alpha channel)
heart_img = cv2.imread('heart.png', cv2.IMREAD_UNCHANGED)
heart_alpha = heart_img[:, :, 3] / 255.0
heart_color = heart_img[:, :, :3]

# Classifiers to detect face and eyes
face_cascade = cv2.CascadeClassifier(cv2.data.haarcascades + 'haarcascade_frontalface_default.xml')
eye_cascade = cv2.CascadeClassifier(cv2.data.haarcascades + 'haarcascade_eye.xml')

def displayPngInImage(im, color, alpha, x, y, w, h):
    # Define where to place the heart image on the frame (top-left corner)
    y1, y2 = y, y+h
    x1, x2 = x, x+w
    
    # y1, y2 = 50, 50 + png.shape[0]
    # x1, x2 = 50, 50 + png.shape[1]

    # Resize heart image to fit designated area
    resized_color = cv2.resize(color, (x2 - x1, y2 - y1))
    resized_alpha = cv2.resize(alpha, (x2 - x1, y2 - y1))

    # Extract the region of interest (ROI) from the frame
    roi = im[y1:y2, x1:x2]

    # Blend the heart image with the ROI based on alpha channel
    for c in range(0, 3):
        roi[:, :, c] = (resized_alpha * resized_color[:, :, c] +
                        (1 - resized_alpha) * roi[:, :, c])

    # Put the modified ROI back into the original frame
    im[y1:y2, x1:x2] = roi

while cap.isOpened():
    success, image = cap.read()
    if not success:
        continue

    # Convert the BGR image to RGB.
    image = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)

    # Process the image and track the hands.
    results = hands.process(image)

    # Convert back to BGR for OpenCV.
    image = cv2.cvtColor(image, cv2.COLOR_RGB2BGR)
    
    # Draw the hand annotations on the image.
    if results.multi_hand_landmarks:
        for hand_landmarks in results.multi_hand_landmarks:
            mp_drawing.draw_landmarks(image, hand_landmarks, mp_hands.HAND_CONNECTIONS)

    gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
    faces = face_cascade.detectMultiScale(gray, 1.1, 4)
    
    for (x, y, w, h) in faces:
        cv2.rectangle(image, (x, y), (x+w, y+h), (255, 0, 0), 2)
        roi_gray = gray[y:y+h, x:x+w]
        roi_color = image[y:y+h, x:x+w]
        eyes = eye_cascade.detectMultiScale(roi_gray)
        for (ex, ey, ew, eh) in eyes:
            cv2.rectangle(roi_color, (ex, ey), (ex+ew, ey+eh), (0, 255, 0), 2)
            displayPngInImage(image, heart_color, heart_alpha, ex, ey, ew, eh)

    # Display the image.
    cv2.imshow('Hand Tracking', image)

    # Send the image to the fake webcam
    # fake_webcam.schedule_frame(image)

    # Exit if ESC if pressed
    if cv2.waitKey(5) & 0xFF == 27:
        break

cap.release()
cv2.destroyAllWindows()
