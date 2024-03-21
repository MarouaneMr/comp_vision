# Navigation System
This project utilizes computer vision techniques to enable map navigation through hand gestures. The system captures hand movements through a webcam and translates them into actions such as cursor movement, zooming, and dragging on a map interface.

## Requirements:
- OpenCV (4.9.0.80)
- Mediapipe (0.9.1.0)
- PyAutoGUI
- Pyhton 3.x

## Usage
1. Clone repository in your local machine
2. Intall all requirements ( pip install -r requirements.txt)
3. Run map.py
4. Ensure you give permissions to VSCode for webcam usage
5. Open any map navigator (preferably Google Earth)
6. Navigate to your favorite places!

## Hand Gestures Menu:
### Cursor movement
<img width="490" alt="Screen Shot 2024-03-21 at 4 11 46 PM" src="https://github.com/MarouaneMr/comp_vision/assets/126504470/6a507b36-7f49-4181-85ab-f392e4d1fc03">

### Zooming
#### Zooming-in
<img width="490" alt="Screen Shot 2024-03-21 at 4 11 24 PM" src="https://github.com/MarouaneMr/comp_vision/assets/126504470/8da1a43f-ca00-4711-a4b6-9af6863f6d9f">

#### Zooming-out
<img width="490" alt="Screen Shot 2024-03-21 at 4 11 36 PM" src="https://github.com/MarouaneMr/comp_vision/assets/126504470/b81b643f-8ea0-4541-b3c9-1f83857ac7f3">

### Dragging
<img width="490" alt="Screen Shot 2024-03-21 at 4 11 12 PM" src="https://github.com/MarouaneMr/comp_vision/assets/126504470/598ea242-3ab0-4580-99b3-d01ef4356814">

## Note:
- Ensure you are in a setting with proper lighting conditions for more accuracy in the hand detection

## Technical explanations and discoveries
### Hand Tracking and Landmark Detection
The core of this project relies on hand tracking and landmark detection. We utilize the MediaPipe library to detect hand landmarks accurately. Each detected hand landmark represents a key point on the hand, enabling precise tracking of hand movements and gestures.
### Cursor Control and Interpolation
To ensure smooth and natural cursor movement, we employ linear interpolation (lerp) between the current cursor position and the target position calculated based on hand landmarks. This technique helps in achieving fluid cursor movement across the screen, enhancing user experience.
### Gesture Recognition
Gesture recognition plays a vital role in interpreting user intentions from hand movements. By analyzing the relative positions of hand landmarks and finger configurations, we can identify gestures such as zooming, dragging, and cursor movement. This process involves defining thresholds and conditions for recognizing specific gestures reliably. (done in the Control class).
### Real-Time Feedback and Responsiveness
One of the key challenges in developing this system is achieving real-time feedback and responsiveness. We continuously monitor hand movements captured by the webcam and update the cursor position or perform actions promptly based on detected gestures. Optimizing the processing pipeline and minimizing latency are crucial for delivering a seamless user experience.




