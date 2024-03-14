import cv2
import mediapipe as mp
#from controller import Controller
import pyautogui


class Controller:
    prev_hand = None
    right_clicked = False
    left_clicked = False
    double_clicked = False
    dragging = False
    hand_Landmarks = None
    little_finger_down = None
    little_finger_up = None
    index_finger_down = None
    index_finger_up = None
    middle_finger_down = None
    middle_finger_up = None
    ring_finger_down = None
    ring_finger_up = None
    Thump_finger_down = None 
    Thump_finger_up = None
    all_fingers_down = None
    all_fingers_up = None
    index_finger_within_Thumb_finger = None
    middle_finger_within_Thumb_finger = None
    little_finger_within_Thumb_finger = None
    ring_finger_within_Thumb_finger = None
    screen_width, screen_height = pyautogui.size()
    lerp_factor = 0.2 


    def update_fingers_status():
        Controller.little_finger_down = Controller.hand_Landmarks.landmark[20].y > Controller.hand_Landmarks.landmark[17].y
        Controller.little_finger_up = Controller.hand_Landmarks.landmark[20].y < Controller.hand_Landmarks.landmark[17].y
        Controller.index_finger_down = Controller.hand_Landmarks.landmark[8].y > Controller.hand_Landmarks.landmark[5].y
        Controller.index_finger_up = Controller.hand_Landmarks.landmark[8].y < Controller.hand_Landmarks.landmark[5].y
        Controller.middle_finger_down = Controller.hand_Landmarks.landmark[12].y > Controller.hand_Landmarks.landmark[9].y
        Controller.middle_finger_up = Controller.hand_Landmarks.landmark[12].y < Controller.hand_Landmarks.landmark[9].y
        Controller.ring_finger_down = Controller.hand_Landmarks.landmark[16].y > Controller.hand_Landmarks.landmark[13].y
        Controller.ring_finger_up = Controller.hand_Landmarks.landmark[16].y < Controller.hand_Landmarks.landmark[13].y
        Controller.Thump_finger_down = Controller.hand_Landmarks.landmark[4].y > Controller.hand_Landmarks.landmark[13].y
        Controller.Thump_finger_up = Controller.hand_Landmarks.landmark[4].y < Controller.hand_Landmarks.landmark[13].y
        Controller.all_fingers_down = Controller.index_finger_down and Controller.middle_finger_down and Controller.ring_finger_down and Controller.little_finger_down
        Controller.all_fingers_up = Controller.index_finger_up and Controller.middle_finger_up and Controller.ring_finger_up and Controller.little_finger_up
        Controller.index_finger_within_Thumb_finger = Controller.hand_Landmarks.landmark[8].y > Controller.hand_Landmarks.landmark[4].y and Controller.hand_Landmarks.landmark[8].y < Controller.hand_Landmarks.landmark[2].y
        Controller.middle_finger_within_Thumb_finger = Controller.hand_Landmarks.landmark[12].y > Controller.hand_Landmarks.landmark[4].y and Controller.hand_Landmarks.landmark[12].y < Controller.hand_Landmarks.landmark[2].y
        Controller.little_finger_within_Thumb_finger = Controller.hand_Landmarks.landmark[20].y > Controller.hand_Landmarks.landmark[4].y and Controller.hand_Landmarks.landmark[20].y < Controller.hand_Landmarks.landmark[2].y
        Controller.ring_finger_within_Thumb_finger = Controller.hand_Landmarks.landmark[16].y > Controller.hand_Landmarks.landmark[4].y and Controller.hand_Landmarks.landmark[16].y < Controller.hand_Landmarks.landmark[2].y
    
    def lerp(start, end, t):
        """
        Linearly interpolates between start and end points based on t parameter.

        :param start: The start value (e.g., x or y position).
        :param end: The end value (e.g., x or y position).
        :param t: The interpolation parameter (0 <= t <= 1).
        :return: The interpolated value.
        """
        return (1 - t) * start + t * end

    def get_position(hand_x_position, hand_y_position):
        old_x, old_y = pyautogui.position()
        target_x = int(hand_x_position * Controller.screen_width)
        target_y = int(hand_y_position * Controller.screen_height)

        # Apply linear interpolation between the current cursor position and the target position
        current_x = Controller.lerp(old_x, target_x, Controller.lerp_factor)
        current_y = Controller.lerp(old_y, target_y, Controller.lerp_factor)

        # Ensure the cursor stays within the screen bounds
        threshold = 5
        if current_x < threshold:
            current_x = threshold
        elif current_x > Controller.screen_width - threshold:
            current_x = Controller.screen_width - threshold
        if current_y < threshold:
            current_y = threshold
        elif current_y > Controller.screen_height - threshold:
            current_y = Controller.screen_height - threshold

        return (int(current_x), int(current_y))
        
    def cursor_moving():
        point = 9
        current_x, current_y = Controller.hand_Landmarks.landmark[point].x ,Controller.hand_Landmarks.landmark[point].y
        x, y = Controller.get_position(current_x, current_y)
        cursor_freezed = Controller.all_fingers_up and Controller.Thump_finger_down
        if not cursor_freezed:
            pyautogui.moveTo(x, y, duration = 0)
    
    def detect_zoomming():
        zoomming = Controller.index_finger_up and Controller.middle_finger_up and Controller.ring_finger_down and Controller.little_finger_down
        window = .05
        index_touches_middle = abs(Controller.hand_Landmarks.landmark[8].x - Controller.hand_Landmarks.landmark[12].x) <= window
        zoomming_out = zoomming and index_touches_middle
        zoomming_in = zoomming and not index_touches_middle
        
        if zoomming_out:
            pyautogui.keyDown('ctrl')
            pyautogui.scroll(-50)
            pyautogui.keyUp('ctrl')
            print("Zooming Out")

        if zoomming_in:
            pyautogui.keyDown('ctrl')
            pyautogui.scroll(50)
            pyautogui.keyUp('ctrl')
            print("Zooming In")
    
    def detect_dragging():
        if not Controller.dragging and Controller.all_fingers_down:
            pyautogui.mouseDown(button = "left")
            Controller.dragging = True
            print("Dragging")
        elif not Controller.all_fingers_down:
            pyautogui.mouseUp(button = "left")
            Controller.dragging = False

cap = cv2.VideoCapture(0)

mpHands = mp.solutions.hands
hands = mpHands.Hands()
mpDraw = mp.solutions.drawing_utils

while True:
   success, img = cap.read()
   img = cv2.flip(img, 1)

   imgRGB = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
   results = hands.process(imgRGB)

   if results.multi_hand_landmarks:
        Controller.hand_Landmarks = results.multi_hand_landmarks[0]
        mpDraw.draw_landmarks(img, Controller.hand_Landmarks, mpHands.HAND_CONNECTIONS)
        
        Controller.update_fingers_status()
        Controller.cursor_moving()
        Controller.detect_zoomming()
        Controller.detect_dragging()

   cv2.imshow('Hand Tracker', img)
   if cv2.waitKey(5) & 0xff == 27:
      break