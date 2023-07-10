![Webcam Mouse Controller with Blink Detection](/screenshot_mouse_web.png?raw=true "Webcam Mouse Controller with Blink Detection")
# Webcam Mouse Controller with Blink Detection

This Python program utilizes computer vision techniques and facial landmark detection to control the mouse cursor using face movements and detect blinks for mouse clicks. By tracking the user's face through the webcam, it maps the face movements to mouse movements and interprets eye blinks as mouse clicks.

## Features

- Control the mouse cursor using face movements.
- Detect eye blinking.
- Detect hand closing as left click. Try to Pop the Bubbles!

## Requirements

- Python 3.x
- OpenCV (`pip install opencv-python`)
- dlib (`pip install dlib`)
- pyautogui (`pip install pyautogui`)

## Usage

1. Clone the repository or download the files.
2. Install the required Python libraries (OpenCV, dlib, pyautogui) using pip.
3. Download the `shape_predictor_68_face_landmarks.dat` file and place it in the same directory as the script.
   - Download from: http://dlib.net/files/shape_predictor_68_face_landmarks.dat.bz2
4. Run the `webcam_mouse_controller.py` script.
5. Adjust the sensitivity constants (`MOUSE_SPEED`, `VERTICAL_SCALE`) in the script if needed.
6. Look into the webcam to control the mouse cursor.
7. Blink with your left eye to perform a left-click.
8. Blink with your right eye to perform a right-click.
9. Press 'q' to quit the program.

## How It Works

1. The program accesses the webcam using OpenCV.
2. It detects faces in the video feed using dlib's frontal face detector.
3. Facial landmarks are detected using dlib's shape predictor, specifically targeting the eye regions.
4. Eye aspect ratio (EAR) is calculated based on the eye landmarks to detect blinks.
5. Face movements are mapped to mouse movements by tracking the center of the face.
6. When a left eye blink is detected, it counters up.
7. When a right eye blink is detected, it counters up.
8. The mouse cursor is moved based on the face movements.
9. Use close hands to emulate mouse click.

## Limitations

- The program relies on accurate face detection and tracking, which may be affected by factors such as lighting conditions, facial occlusions, or head movements.
- Eye blink detection accuracy may vary depending on individual eye characteristics, such as eye shape or eyelid visibility.
- The program does not provide advanced mouse functionalities like scrolling or drag-and-drop.

## Applications

- Hands-free mouse control: The program enables individuals with limited mobility to control the mouse cursor using facial movements and blinks, offering an alternative input method.
- Novelty and experimentation: It can be used for fun experiments or demonstrations to explore computer vision, facial landmark detection, and human-computer interaction concepts.

## Acknowledgments

The face detection and facial landmark detection are powered by the following libraries:

- OpenCV - https://opencv.org/
- dlib - http://dlib.net/

## License

This project is licensed under the Boost Software License 1.0. See the [LICENSE](LICENSE) file for details.i

