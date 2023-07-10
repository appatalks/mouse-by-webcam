import cv2
import dlib
import pyautogui
import tkinter as tk
from tkinter import messagebox
import random
import mediapipe as mp

# Counter variables for left and right eye blinks
left_blink_counter = 0
right_blink_counter = 0

# Constants for mouse sensitivity
MOUSE_SPEED = 5
VERTICAL_SCALE = 2

# Face detection and landmark detection initialization
detector = dlib.get_frontal_face_detector()
predictor = dlib.shape_predictor("shape_predictor_68_face_landmarks.dat")  # Path to the pre-trained facial landmark model

# Hand detection initialization
hand_detector = mp.solutions.hands.Hands(
    static_image_mode=False, max_num_hands=2, min_detection_confidence=0.5
)
THRESHOLD_DISTANCE = 0.05  # Adjust this value according to your needs

class Bubble:
    def __init__(self, x, y, radius):
        self.x = x
        self.y = y
        self.radius = radius
        self.is_popped = False

    def update(self):
        self.y -= 1

    def check_collision(self, cursor_x, cursor_y):
        if not self.is_popped and distance((self.x, self.y), (cursor_x, cursor_y)) <= self.radius:
            self.is_popped = True
            self.increment_popped_counter()
            return True
        return False

    def increment_popped_counter(self):
        if self.is_popped:
            global popped_bubble_counter
            popped_bubble_counter += 1

def calculate_ear(eye_points):
    # Calculate the eye aspect ratio (EAR)
    # EAR = (|p2-p6| + |p3-p5|) / (2 * |p1-p4|)
    a = distance(eye_points[1], eye_points[5])
    b = distance(eye_points[2], eye_points[4])
    c = distance(eye_points[0], eye_points[3])
    ear = (a + b) / (2.0 * c)
    return ear

def distance(p1, p2):
    # Calculate Euclidean distance between two points
    return ((p2[0] - p1[0]) ** 2 + (p2[1] - p1[1]) ** 2) ** 0.5

def draw_eye_region(frame, eye_points):
    # Draw eye region on the frame
    for i in range(len(eye_points)):
        cv2.line(frame, eye_points[i], eye_points[(i + 1) % len(eye_points)], (0, 255, 0), 1)

# Mouse event callback function
def mouse_callback(event, x, y, flags, param):
    if event == cv2.EVENT_LBUTTONDOWN:
        # Check for collision with bubbles
        for bubble in bubbles:
            if bubble.check_collision(x, y):
                global popped_bubble_counter
                popped_bubble_counter += 1

# Webcam initialization
cap = cv2.VideoCapture(0)  # You may need to change the index (0) depending on the webcam's availability

# Constants for blink detection
EYE_AR_THRESH = 0.2  # Eye aspect ratio threshold for blink detection
EYE_AR_CONSEC_FRAMES = 3  # Number of consecutive frames for which the eye must be below the threshold to consider it as a blink
left_eye_counter = 0
right_eye_counter = 0
left_blink_detected = False
right_blink_detected = False

# Bubble variables
bubbles = []
MAX_BUBBLES = 10
MIN_RADIUS = 10
MAX_RADIUS = 30

# Counter variable for popped bubbles
popped_bubble_counter = 0

# Create a window for the webcam
cv2.namedWindow('Webcam')
# Register the mouse callback function
cv2.setMouseCallback('Webcam', mouse_callback)

# Colors for visual indicators
LEFT_CLICK_COLOR = (0, 255, 0)  # Green
RIGHT_CLICK_COLOR = (0, 0, 255)  # Red

# Main loop
try:
    while True:
        # Read webcam frame
        ret, frame = cap.read()
        if not ret:
            break

        # Flip the frame horizontally to remove mirroring
        frame = cv2.flip(frame, 1)

        # Convert frame to grayscale for face detection
        gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)

        # Perform face detection
        faces = detector(gray)

        # Iterate through detected faces
        for face in faces:
            # Detect facial landmarks
            landmarks = predictor(gray, face)
            left_eye_points = []
            right_eye_points = []

            # Extract the coordinates of the left and right eyes
            for n in range(36, 42):
                x = landmarks.part(n).x
                y = landmarks.part(n).y
                left_eye_points.append((x, y))
            for n in range(42, 48):
                x = landmarks.part(n).x
                y = landmarks.part(n).y
                right_eye_points.append((x, y))

            # Calculate eye aspect ratio (EAR) for blink detection
            left_eye_ear = calculate_ear(left_eye_points)
            right_eye_ear = calculate_ear(right_eye_points)

            # Check for left eye blink
            if left_eye_ear < EYE_AR_THRESH:
                left_eye_counter += 1
            else:
                if left_eye_counter >= EYE_AR_CONSEC_FRAMES:
                    left_blink_detected = True
                    left_blink_counter += 1  # Increment the left blink counter
                left_eye_counter = 0

            # Check for right eye blink
            if right_eye_ear < EYE_AR_THRESH:
                right_eye_counter += 1
            else:
                if right_eye_counter >= EYE_AR_CONSEC_FRAMES:
                    right_blink_detected = True
                    right_blink_counter += 1  # Increment the right blink counter
                right_eye_counter = 0

            # Perform mouse actions based on blink detection
            if left_blink_detected:
                left_blink_detected = False
            if right_blink_detected:
                right_blink_detected = False

            # Map face movements to mouse movements
            face_center_x = face.left() + (face.width() // 2)
            face_center_y = face.top() + (face.height() // 2)
            mouse_dx = (face_center_x - frame.shape[1] // 2) // MOUSE_SPEED
            mouse_dy = (face_center_y - frame.shape[0] // 2) // (MOUSE_SPEED * VERTICAL_SCALE)

            # Move the mouse cursor
            try:
                pyautogui.moveRel(mouse_dx, mouse_dy)
            except pyautogui.FailSafeException:
                # Display a pop-up message when the fail-safe is triggered
                root = tk.Tk()
                root.withdraw()
                messagebox.showinfo("Fail-Safe Triggered", "You lost!")

            # Generate new bubbles if necessary
            if len(bubbles) < MAX_BUBBLES:
                x = random.randint(0, frame.shape[1])
                y = frame.shape[0]
                radius = random.randint(MIN_RADIUS, MAX_RADIUS)
                bubbles.append(Bubble(x, y, radius))

            # Update bubbles
            for bubble in bubbles:
                bubble.update()

            # Remove popped bubbles
            bubbles = [bubble for bubble in bubbles if not bubble.is_popped]

            # Draw bubbles on the frame
            for bubble in bubbles:
                if not bubble.is_popped:
                    cv2.circle(frame, (bubble.x, bubble.y), bubble.radius, (255, 0, 0), -1)

            # Draw eye region and blink detection indicators on the frame
            draw_eye_region(frame, left_eye_points)
            draw_eye_region(frame, right_eye_points)

            # Display the blink counters
            cv2.putText(frame, "Left Eye Blinks: {}".format(left_blink_counter), (10, 30),
                        cv2.FONT_HERSHEY_SIMPLEX, 0.7, (0, 255, 0), 2)
            cv2.putText(frame, "Right Eye Blinks: {}".format(right_blink_counter), (10, 60),
                        cv2.FONT_HERSHEY_SIMPLEX, 0.7, (0, 255, 0), 2)

        # Hand detection and mouse click functionality
        rgb_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
        results = hand_detector.process(rgb_frame)

        if results.multi_hand_landmarks:
            for hand_landmarks in results.multi_hand_landmarks:
                landmarks = hand_landmarks.landmark

                thumb_tip = landmarks[mp.solutions.hands.HandLandmark.THUMB_TIP]
                index_tip = landmarks[mp.solutions.hands.HandLandmark.INDEX_FINGER_TIP]

                hand_distance = distance((thumb_tip.x, thumb_tip.y), (index_tip.x, index_tip.y))
                is_hand_closed = hand_distance < THRESHOLD_DISTANCE

                # Visual indicators for left click and right click
                if is_hand_closed:
                    if index_tip.x < thumb_tip.x:  # Left hand
                        cv2.circle(frame, (int(thumb_tip.x * frame.shape[1]), int(thumb_tip.y * frame.shape[0])),
                                   10, LEFT_CLICK_COLOR, -1)
                        # Perform left click action
                        pyautogui.click(button='left')
                    else:  # Right hand
                        cv2.circle(frame, (int(thumb_tip.x * frame.shape[1]), int(thumb_tip.y * frame.shape[0])),
                                   10, RIGHT_CLICK_COLOR, -1)
                        # Perform right click action
                        pyautogui.click(button='left')

        # Display the popped bubble count
        cv2.putText(frame, "Popped Bubbles: {}".format(popped_bubble_counter), (10, 90),
                    cv2.FONT_HERSHEY_SIMPLEX, 0.7, (0, 0, 255), 2)

        # Display the video feed
        cv2.imshow('Webcam', frame)

        # Register the mouse callback function
#        cv2.setMouseCallback('Webcam', mouse_callback)

        # Exit the loop on 'q' key press
        if cv2.waitKey(1) & 0xFF == ord('q'):
            break

except KeyboardInterrupt:
    pass

# Release the webcam and destroy windows
cap.release()
cv2.destroyAllWindows()
