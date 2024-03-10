import cv2
import mediapipe as mp

# Initialize MediaPipe Hands model
mp_hands = mp.solutions.hands
hands = mp_hands.Hands(static_image_mode=False,
                       max_num_hands=1,
                       min_detection_confidence=0.7)
mp_drawing = mp.solutions.drawing_utils

# Initialize the webcam
cap = cv2.VideoCapture(0)

while cap.isOpened():
    ret, frame = cap.read()
    if not ret:
        continue

    # Flip the frame horizontally for a later selfie-view display
    frame = cv2.flip(frame, 1)

    # Get the width of the frame
    frame_width = frame.shape[1]

    # Convert the frame to RGB
    rgb_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
    
    # Process the frame
    result = hands.process(rgb_frame)
    
    # Draw the hand annotations on the frame
    if result.multi_hand_landmarks:
        for hand_landmarks in result.multi_hand_landmarks:
            mp_drawing.draw_landmarks(frame, hand_landmarks, mp_hands.HAND_CONNECTIONS)
            
            # Get the index fingertip landmark
            index_fingertip = hand_landmarks.landmark[mp_hands.HandLandmark.INDEX_FINGER_TIP]
            index_finger_x = int(index_fingertip.x * frame_width)
            
            # Determine if the hand is on the right or left side
            movement = ""
            if index_finger_x < frame_width // 2:
                movement = "Moved Left"
            else:
                movement = "Moved Right"
            
            # Overlay the movement direction on the frame
            cv2.putText(frame, movement, (10, 50), cv2.FONT_HERSHEY_SIMPLEX, 1, (255, 255, 255), 2, cv2.LINE_AA)

    # Display the frame
    cv2.imshow('Virtual Gesture Map Navigation', frame)

    if cv2.waitKey(5) & 0xFF == 27:
        break

hands.close()
cap.release()
cv2.destroyAllWindows()