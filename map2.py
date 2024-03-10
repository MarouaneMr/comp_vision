import cv2
import mediapipe as mp
import pyautogui

# Initialize MediaPipe Hands model
mp_hands = mp.solutions.hands
hands = mp_hands.Hands(static_image_mode=False,
                       max_num_hands=2,  # Allow detection of up to 2 hands for zooming gestures
                       min_detection_confidence=0.7)
mp_drawing = mp.solutions.drawing_utils

# Initialize the webcam
cap = cv2.VideoCapture(0)

while cap.isOpened():
    ret, frame = cap.read()
    if not ret:
        continue

    # Flip the frame horizontally for a later selfie-view display, and vertically if needed
    frame = cv2.flip(frame, 1)

    # Get the width and height of the frame
    frame_width, frame_height = frame.shape[1], frame.shape[0]

    # Convert the frame to RGB
    rgb_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
    
    # Process the frame
    result = hands.process(rgb_frame)
    
    # Draw the hand annotations on the frame
    if result.multi_hand_landmarks:
        for hand_landmarks in result.multi_hand_landmarks:
            mp_drawing.draw_landmarks(frame, hand_landmarks, mp_hands.HAND_CONNECTIONS)
        
        number_of_hands = len(result.multi_hand_landmarks)
        # Assume single hand for movement and fist detection
        if number_of_hands == 1:
            hand_landmarks = result.multi_hand_landmarks[0]

            # Get the index fingertip landmark for movement detection
            index_fingertip = hand_landmarks.landmark[mp_hands.HandLandmark.INDEX_FINGER_TIP]
            index_finger_x = int(index_fingertip.x * frame_width)
            index_finger_y = int(index_fingertip.y * frame_height)

            horizontal_movement = "Left" if index_finger_x < frame_width // 2 else "Right"
            vertical_movement = "Up" if index_finger_y < frame_height // 2 else "Down"
            
            # Detect fist for zoom in
            fist_detected = True
            for tip_id in [mp_hands.HandLandmark.INDEX_FINGER_TIP, mp_hands.HandLandmark.MIDDLE_FINGER_TIP,
                           mp_hands.HandLandmark.RING_FINGER_TIP, mp_hands.HandLandmark.PINKY_TIP]:
                tip = hand_landmarks.landmark[tip_id]
                mcp_id = mp_hands.HandLandmark(tip_id - 2)
                mcp = hand_landmarks.landmark[mcp_id]
                if tip.y > mcp.y:  # If any fingertip is above its MCP, it's not a fist
                    fist_detected = False
                    break
            
            # Overlay the movement direction on the frame
            movement_text = f'{horizontal_movement}, {vertical_movement}'
            cv2.putText(frame, movement_text, (10, 50), cv2.FONT_HERSHEY_SIMPLEX, 1, (255, 255, 255), 2, cv2.LINE_AA)
            
            if fist_detected:
                pyautogui.scroll(50)  # Scroll up to zoom in

        elif number_of_hands == 2:
            # Two hands detected - zoom out
            pyautogui.scroll(-50)  # Scroll down to zoom out

    # Display the frame
    cv2.imshow('Virtual Gesture Map Navigation', frame)

    if cv2.waitKey(5) & 0xFF == 27:
        break

hands.close()
cap.release()
cv2.destroyAllWindows()