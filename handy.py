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

print(f"Width: {width} pixels")
print(f"Height: {height} pixels")

# Create a fake webcam device (replace 'video1' with your device's name)
fake_webcam = pyfakewebcam.FakeWebcam('/dev/video4', width, height)

while cap.isOpened():
    success, image = cap.read()
    if not success:
        continue

    # Convert the BGR image to RGB.
    image = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)

    # Process the image and track the hands.
    results = hands.process(image)

    # Convert back to BGR for OpenCV.
    #image = cv2.cvtColor(image, cv2.COLOR_RGB2BGR)
    
    # Draw the hand annotations on the image.
    if results.multi_hand_landmarks:
        for hand_landmarks in results.multi_hand_landmarks:
            mp_drawing.draw_landmarks(image, hand_landmarks, mp_hands.HAND_CONNECTIONS)

    # Display the image.
    #cv2.imshow('Hand Tracking', image)

    # Send the image to the fake webcam
    fake_webcam.schedule_frame(image)

    # Exit if ESC if pressed
    # if cv2.waitKey(5) & 0xFF == 27:
    #     break

cap.release()
cv2.destroyAllWindows()
