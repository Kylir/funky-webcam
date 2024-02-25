import cv2
import mediapipe as mp

# Initialize MediaPipe Hands.
mp_hands = mp.solutions.hands
hands = mp_hands.Hands(max_num_hands=1, min_detection_confidence=0.7)

# For drawing hand landmarks on the image.
mp_drawing = mp.solutions.drawing_utils

# Open webcam
cap = cv2.VideoCapture(2)

def detect_gesture(landmarks):
    """
    Detects hand gesture based on thumb and fingertips positions.
    Returns a string indicating the gesture.
    """
    # Landmark indices for fingertips and their respective MCP (Metacarpophalangeal joints)
    tip_ids = [4, 8, 12, 16, 20]
    #mcp_ids = [3, 6, 10, 14, 18]
    mcp_ids = [1, 5, 9, 13, 17]
    
    up_count = 0  # Count of fingers that are up
    
    # Check if non-thumb fingers are up
    for i in range(1, 5):
        if landmarks[tip_ids[i]].y < landmarks[mcp_ids[i]].y:
            up_count += 1
    
    # Check if thumb is up
    if landmarks[tip_ids[0]].x < landmarks[mcp_ids[0]].x:
        up_count += 1

    # Determine gesture based on count of fingers up
    if up_count == 0:
        return "Fist"
    elif up_count == 5:
        return "Open Palm"
    elif up_count == 2 and landmarks[tip_ids[1]].y < landmarks[tip_ids[2]].y:
        return "Victory"
    else:
        return "Other"

while True:
    ret, frame = cap.read()
    if not ret:
        break

    # Convert the BGR image to RGB and process it with MediaPipe Hands
    rgb_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
    result = hands.process(rgb_frame)

    # Draw the hand annotations on the image.
    if result.multi_hand_landmarks:
        for hand_landmarks in result.multi_hand_landmarks:
            mp_drawing.draw_landmarks(frame, hand_landmarks, mp_hands.HAND_CONNECTIONS)
            # Detect gesture
            gesture = detect_gesture(hand_landmarks.landmark)
            cv2.putText(frame, gesture, (10, 50), cv2.FONT_HERSHEY_SIMPLEX, 1, (255, 0, 0), 2, cv2.LINE_AA)

    cv2.imshow('Hand Gesture Recognition', frame)

    if cv2.waitKey(5) & 0xFF == 27:
        break

cap.release()
cv2.destroyAllWindows()
