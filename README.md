💪 Push-Up Counter Using Computer Vision
📌 Overview
The Push-Up Counter is a real-time computer vision application built using Python, OpenCV, and MediaPipe Pose. It automatically counts push-ups by analyzing body movements and tracking key body landmarks through a camera.

The system uses elbow angle calculation and hip position monitoring to identify push-up movements and determine when a repetition is completed.

This project demonstrates how computer vision and pose estimation can be applied to fitness tracking without requiring wearable devices.

✨ Features
🎥 Real-Time Video Processing — Captures live video using a webcam.
🧍 Human Pose Estimation — Detects body landmarks using MediaPipe Pose.
📐 Elbow Angle Calculation — Analyzes elbow movement to identify push-up phases.
📏 Hip Position Tracking — Monitors hip movement and body alignment.
🔢 Automatic Rep Counting — Counts completed push-ups based on body movement.
🖥️ Live Visual Feedback — Displays pose landmarks and the repetition count on the video feed.
🛠️ Technologies Used
Python — Core programming language
OpenCV — Video capture and image processing
MediaPipe Pose — Human pose estimation and landmark detection
NumPy — Numerical calculations, if used in the implementation
⚙️ How It Works
The application detects the user's pose and analyzes movement using two important measurements.

1. Pose Detection
MediaPipe Pose detects key body landmarks, such as the shoulders, elbows, wrists, and hips, from the webcam feed.

2. Elbow Angle Calculation
The application calculates the elbow angle using the detected shoulder, elbow, and wrist landmarks. Changes in this angle help identify the lowering and raising phases of a push-up.

3. Hip Position Monitoring
The system tracks the hip landmark to monitor body position during the exercise. This information can help assess body alignment and distinguish the intended push-up movement.

4. Repetition Counting
The elbow angle and hip position are used together to identify the movement cycle. When the required conditions for a complete push-up are satisfied, the counter increments.

5. Real-Time Display
OpenCV displays the processed video, detected pose landmarks, and current push-up count.
