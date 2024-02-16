import cv2

# Capture video from the webcam
cap = cv2.VideoCapture(0)

while True:
    # Read the frame
    ret, frame = cap.read()
    if not ret:
        break

    # You can process the frame here
    cv2.imshow('Frame', frame)

    # Break the loop with a specific key press (e.g., 'q')
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

# Release the capture and close any OpenCV windows
cap.release()
cv2.destroyAllWindows()
