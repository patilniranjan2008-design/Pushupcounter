import numpy as np


def calculate_angle(a, b, c):
    a = np.array(a)
    b = np.array(b)
    c = np.array(c)

    ba = a - b
    bc = c - b

    cosine_angle = np.dot(ba, bc) / (
        np.linalg.norm(ba) * np.linalg.norm(bc)
    )

    angle = np.arccos(cosine_angle)

    return np.degrees(angle)

import cv2
import mediapipe as mp


POSE_CONNECTIONS = [
    # Face
    (0, 1),
    (1, 2),
    (2, 3),
    (3, 7),
    (0, 4),
    (4, 5),
    (5, 6),
    (6, 8),
    (9, 10),

    # Upper body
    (11, 12),

    # Left arm
    (11, 13),
    (13, 15),
    (15, 17),
    (15, 19),
    (15, 21),

    # Right arm
    (12, 14),
    (14, 16),
    (16, 18),
    (16, 20),
    (16, 22),

    # Torso
    (11, 23),
    (12, 24),
    (23, 24),

    # Left leg
    (23, 25),
    (25, 27),
    (27, 29),
    (27, 31),

    # Right leg
    (24, 26),
    (26, 28),
    (28, 30),
    (28, 32),
]


# Create the MediaPipe Pose Landmarker
BaseOptions = mp.tasks.BaseOptions
PoseLandmarker = mp.tasks.vision.PoseLandmarker
PoseLandmarkerOptions = mp.tasks.vision.PoseLandmarkerOptions
VisionRunningMode = mp.tasks.vision.RunningMode

options = PoseLandmarkerOptions(
    base_options=BaseOptions(
        model_asset_path="models/pose_landmarker_full.task"
    ),
    running_mode=VisionRunningMode.IMAGE
)

landmarker = PoseLandmarker.create_from_options(options)

# Open webcam
cap = cv2.VideoCapture(0)

counter = 0
stage = None

while True:
    success, frame = cap.read()

    if not success:
        print("Could not access the camera.")
        break

    # OpenCV uses BGR, MediaPipe expects RGB
    rgb_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)

    # Convert frame into a MediaPipe image
    mp_image = mp.Image(
        image_format=mp.ImageFormat.SRGB,
        data=rgb_frame
    )

    # Detect the pose
    results = landmarker.detect(mp_image)
    if results.pose_landmarks:

        landmarks = results.pose_landmarks[0]

        shoulder = [landmarks[11].x, landmarks[11].y]
        elbow = [landmarks[13].x, landmarks[13].y]
        wrist = [landmarks[15].x, landmarks[15].y]
        hip = [landmarks[23].x, landmarks[23].y]

        angle = calculate_angle(shoulder, elbow, wrist)

        body_angle = np.degrees(
            np.arctan2(
                hip[1] - shoulder[1],
                hip[0] - shoulder[0]
            )
        )

        print(f"Elbow angle: {angle:.1f}°")
        print(f"Body angle: {body_angle:.1f}°")

        if body_angle < 60:

            if angle > 150:
                 if stage == "down":
                     counter += 1

                 stage = "up"

            elif angle < 135:
                 stage = "down"
 
        print(f"Stage: {stage} | Reps: {counter}")

    if results.pose_landmarks:
        left_elbow = results.pose_landmarks[0][13]
        right_elbow = results.pose_landmarks[0][14]

        print(
            f"Left elbow: x={left_elbow.x:.2f}, y={left_elbow.y:.2f}"
        )
        print(
            f"Right elbow: x={right_elbow.x:.2f}, y={right_elbow.y:.2f}"
        )
    
    # Draw landmarks and skeleton
    if results.pose_landmarks:

        landmarks = results.pose_landmarks[0]

       # Draw dots
        for landmark in landmarks:
            x = int(landmark.x * frame.shape[1])
            y = int(landmark.y * frame.shape[0])

            cv2.circle(frame, (x, y), 5, (0, 215, 255), -1)

       # Draw lines
        for start_id, end_id in POSE_CONNECTIONS:

            start = landmarks[start_id]
            end = landmarks[end_id]

            start_point = (
                int(start.x * frame.shape[1]),
                int(start.y * frame.shape[0])
            )

            end_point = (
                int(end.x * frame.shape[1]),
                int(end.y * frame.shape[0])
            )

            cv2.line(
                frame,
                start_point,
                end_point,
                (180, 0, 255),
                 2
            )
    cv2.putText(
        frame,
        f"Reps: {counter}",
        (30, 50),
        cv2.FONT_HERSHEY_SIMPLEX,
        1,
        (0, 215, 255),
         2
    )

    cv2.putText(
        frame,
        f"Stage: {stage}",
        (30, 90),
        cv2.FONT_HERSHEY_SIMPLEX,
        1,
        (0, 215, 255),
        2
    )


    cv2.imshow("Push-Up Counter", frame)

    if cv2.waitKey(1) & 0xFF == ord("q"):
        break

cap.release()
landmarker.close()
cv2.destroyAllWindows()