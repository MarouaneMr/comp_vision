import cv2
import mediapipe as mp
import pyautogui

# Initialize MediaPipe Hands model
mp_hands = mp.solutions.hands
hands = mp_hands.Hands(static_image_mode=False,
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
        number_of_hands = len(result.multi_hand_landmarks)
        action = "Normal"

        # Check if two hands are visible
        if number_of_hands == 2:
            action = "Unzoom"
        else:
            # Analyze the first hand (assuming max_num_hands=2)
            hand_landmarks = result.multi_hand_landmarks[0]
            mp_drawing.draw_landmarks(frame, hand_landmarks, mp_hands.HAND_CONNECTIONS)

            # Determine the horizontal and vertical movements
            index_fingertip = hand_landmarks.landmark[mp_hands.HandLandmark.INDEX_FINGER_TIP]
            index_finger_x = int(index_fingertip.x * frame_width)
            index_finger_y = int(index_fingertip.y * frame_height)

            horizontal_movement = "Left" if index_finger_x < frame_width // 2 else "Right"
            vertical_movement = "Up" if index_finger_y < frame_height // 2 else "Down"
            movement = f'{horizontal_movement}, {vertical_movement}'

            # Check if the hand is likely making a fist
            tip_ids = [mp_hands.HandLandmark.INDEX_FINGER_TIP, mp_hands.HandLandmark.MIDDLE_FINGER_TIP,
                       mp_hands.HandLandmark.RING_FINGER_TIP, mp_hands.HandLandmark.PINKY_TIP]
            base_id = mp_hands.HandLandmark.WRIST

            fist_score = 0  # A measure of how many conditions are met for a fist
            base_ids = [mp_hands.HandLandmark.INDEX_FINGER_MCP, mp_hands.HandLandmark.MIDDLE_FINGER_MCP,
                        mp_hands.HandLandmark.RING_FINGER_MCP, mp_hands.HandLandmark.PINKY_MCP]

            # Check if the fingertips are close to the corresponding base of the fingers
            # Inside your loop after getting hand landmarks
            for i, tip_id in enumerate(tip_ids):
                tip = hand_landmarks.landmark[tip_id]
                base = hand_landmarks.landmark[base_ids[i]]
                
                # Convert coordinates to same scale (assuming frame dimensions are correct)
                tip_x, tip_y = tip.x * frame_width, tip.y * frame_height
                base_x, base_y = base.x * frame_width, base.y * frame_height

                # Calculate the Euclidean distance
                distance = ((tip_x - base_x) ** 2 + (tip_y - base_y) ** 2) ** 0.5

                # Adjust this distance threshold to better fit your webcam and hand size
                if distance < 0.1 :  # Adjust based on your needs
                    fist_score += 1


            if fist_score >= 4:  # Adjust based on your needs, higher for stricter detection
                action = "Zoom"
            
            # Simulate keyboard arrow key presses based on hand movement direction
            if horizontal_movement == "Left":
                pyautogui.press('left')
            elif horizontal_movement == "Right":
                pyautogui.press('right')
            
            if vertical_movement == "Up":
                pyautogui.press('up')
            elif vertical_movement == "Down":
                pyautogui.press('down')
            
            if action == "Zoom":
                pyautogui.scroll(100)
            elif action == "Unzoom":
                pyautogui.scroll(-100)
            elif action == "Normal":
                pass

            # Overlay the movement direction on the frame
            cv2.putText(frame, f'{horizontal_movement}, {vertical_movement}', (10, 50), cv2.FONT_HERSHEY_SIMPLEX, 1, (255, 255, 255), 2, cv2.LINE_AA)

    # Display the frame
    cv2.imshow('Virtual Gesture Map Navigation', frame)

    if cv2.waitKey(5) & 0xFF == 27:
        break

hands.close()
cap.release()
cv2.destroyAllWindows()