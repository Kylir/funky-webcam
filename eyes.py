import cv2
import mediapipe as mp
import numpy as np

# Display a png image
def displayPngInImage(im, color, alpha, center_x, center_y, w, h):
    try:
        # Define where to place the heart image on the frame (top-left corner)
        x1,x2 = center_x - int(w/2.0), center_x + int(w/2.0)
        y1,y2 = center_y - int(h/2.0), center_y + int(h/2.0)

        # Resize heart image to fit designated area
        resized_color = cv2.resize(color, (x2 - x1, y2 - y1))
        resized_alpha = cv2.resize(alpha, (x2 - x1, y2 - y1))
        # Extract the region of interest (ROI) from the frame
        roi = im[y1:y2, x1:x2]
        # Blend the image with the ROI based on alpha channel
        for c in range(0, 3):
            roi[:, :, c] = (resized_alpha * resized_color[:, :, c] +
                            (1 - resized_alpha) * roi[:, :, c])
        # Put the modified ROI back into the original frame
        im[y1:y2, x1:x2] = roi
    except:
        return


# Initialize MediaPipe Face Mesh.
mp_face_mesh = mp.solutions.face_mesh
face_mesh = mp_face_mesh.FaceMesh(min_detection_confidence=0.5, min_tracking_confidence=0.5)

# Open webcam
cap = cv2.VideoCapture(2)

# Load the PNG image with transparency (alpha channel)
heart_img = cv2.imread('./images/rnwl-icon.png', cv2.IMREAD_UNCHANGED)
heart_alpha = heart_img[:, :, 3] / 255.0
heart_color = heart_img[:, :, :3]


while cap.isOpened():
    ret, frame = cap.read()
    if not ret:
        break

    # Convert the BGR image to RGB.
    rgb_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)

    # Process the image and track the face
    results = face_mesh.process(rgb_frame)

    # Convert back to BGR for OpenCV
    bgr_frame = cv2.cvtColor(rgb_frame, cv2.COLOR_RGB2BGR)

    if results.multi_face_landmarks:
        for face_landmarks in results.multi_face_landmarks:
            # Define landmarks for right and left eye
            right_eye_indices = [160, 159, 158, 144, 145, 153]
            left_eye_indices = [385, 386, 380, 374, 373]

            # Calculate the center of the right eye
            right_eye_center = np.mean([(face_landmarks.landmark[point].x * bgr_frame.shape[1],
                                         face_landmarks.landmark[point].y * bgr_frame.shape[0])
                                        for point in right_eye_indices], axis=0)
            eye_x_right, eye_y_right = int(right_eye_center[0]), int(right_eye_center[1])

            # Calculate the center of the left eye
            left_eye_center = np.mean([(face_landmarks.landmark[point].x * bgr_frame.shape[1],
                                        face_landmarks.landmark[point].y * bgr_frame.shape[0])
                                       for point in left_eye_indices], axis=0)
            eye_x_left, eye_y_left = int(left_eye_center[0]), int(left_eye_center[1])

            # Draw circles at the center of each eye
            #cv2.circle(bgr_frame, (eye_x_right, eye_y_right), 5, (0, 255, 0), -1)
            #cv2.circle(bgr_frame, (eye_x_left, eye_y_left), 5, (0, 255, 0), -1)

            # Display hearts for the eyes
            SIZE = 60
            displayPngInImage(bgr_frame, heart_color, heart_alpha, eye_x_right, eye_y_right, SIZE, SIZE)
            displayPngInImage(bgr_frame, heart_color, heart_alpha, eye_x_left, eye_y_left, SIZE, SIZE)

    # Display the frame with facial landmarks and eye centers.
    cv2.imshow('Eyes Center Detection', bgr_frame)

    if cv2.waitKey(5) & 0xFF == 27:  # Exit loop with the ESC key.
        break

cap.release()
cv2.destroyAllWindows()
