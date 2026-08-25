import cv2
import mediapipe as mp
import time

from gesture.validator import is_peace_gesture


class GestureDetector:

    def __init__(
        self,
        required_frames=15,
        timeout=10,
        camera_index=0
    ):

        self.required_frames = required_frames
        self.timeout = timeout
        self.camera_index = camera_index

        self.mp_hands = mp.solutions.hands
        self.mp_draw = mp.solutions.drawing_utils


    def detect_peace_gesture(self):
        """
        Turns on the camera and asks the user
        to perform the V / Peace gesture.

        Returns:
            True  -> Correct gesture confirmed
            False -> Wrong gesture / timeout
        """

        cap = cv2.VideoCapture(self.camera_index)

        if not cap.isOpened():
            print("ERROR: Unable to open camera.")
            return False

        correct_frames = 0
        start_time = time.time()

        print("\nCamera started.")
        print("Please show the V / Peace gesture ✌️")
        print(f"You have {self.timeout} seconds.\n")

        with self.mp_hands.Hands(
            static_image_mode=False,
            max_num_hands=1,
            min_detection_confidence=0.7,
            min_tracking_confidence=0.7
        ) as hands:

            while cap.isOpened():

                success, frame = cap.read()

                if not success:
                    print("ERROR: Unable to read camera.")
                    cap.release()
                    cv2.destroyAllWindows()
                    return False

                # Mirror the camera
                frame = cv2.flip(frame, 1)

                # Convert BGR to RGB
                rgb_frame = cv2.cvtColor(
                    frame,
                    cv2.COLOR_BGR2RGB
                )

                # Detect hand
                results = hands.process(rgb_frame)

                elapsed_time = time.time() - start_time
                remaining_time = max(
                    0,
                    self.timeout - int(elapsed_time)
                )

                gesture_correct = False

                # Hand detected
                if results.multi_hand_landmarks:

                    hand_landmarks = (
                        results.multi_hand_landmarks[0]
                    )

                    # Draw hand landmarks
                    self.mp_draw.draw_landmarks(
                        frame,
                        hand_landmarks,
                        self.mp_hands.HAND_CONNECTIONS
                    )

                    # Validate the gesture
                    gesture_correct = is_peace_gesture(
                        hand_landmarks.landmark
                    )

                    if gesture_correct:

                        correct_frames += 1

                        status = (
                            f"CORRECT GESTURE "
                            f"{correct_frames}/{self.required_frames}"
                        )

                        cv2.putText(
                            frame,
                            status,
                            (30, 50),
                            cv2.FONT_HERSHEY_SIMPLEX,
                            0.8,
                            (0, 255, 0),
                            2
                        )

                    else:

                        # Reset confirmation
                        correct_frames = 0

                        cv2.putText(
                            frame,
                            "SHOW THE V / PEACE SIGN",
                            (30, 50),
                            cv2.FONT_HERSHEY_SIMPLEX,
                            0.8,
                            (0, 0, 255),
                            2
                        )

                else:

                    correct_frames = 0

                    cv2.putText(
                        frame,
                        "NO HAND DETECTED",
                        (30, 50),
                        cv2.FONT_HERSHEY_SIMPLEX,
                        0.8,
                        (0, 0, 255),
                        2
                    )

                # Display timer
                cv2.putText(
                    frame,
                    f"Time left: {remaining_time}s",
                    (30, 90),
                    cv2.FONT_HERSHEY_SIMPLEX,
                    0.7,
                    (255, 255, 255),
                    2
                )

                # Success
                if correct_frames >= self.required_frames:

                    cv2.putText(
                        frame,
                        "GESTURE CONFIRMED!",
                        (30, 140),
                        cv2.FONT_HERSHEY_SIMPLEX,
                        1,
                        (0, 255, 0),
                        3
                    )

                    cv2.imshow(
                        "Gesture Recognition",
                        frame
                    )

                    cv2.waitKey(1000)

                    cap.release()
                    cv2.destroyAllWindows()

                    print("\nResult: TRUE")
                    return True

                # Timeout
                if elapsed_time >= self.timeout:

                    cv2.putText(
                        frame,
                        "TIMEOUT - FAILED",
                        (30, 140),
                        cv2.FONT_HERSHEY_SIMPLEX,
                        1,
                        (0, 0, 255),
                        3
                    )

                    cv2.imshow(
                        "Gesture Recognition",
                        frame
                    )

                    cv2.waitKey(1000)

                    cap.release()
                    cv2.destroyAllWindows()

                    print("\nResult: FALSE")
                    return False

                # Display frame
                cv2.imshow(
                    "Gesture Recognition",
                    frame
                )

                # Press Q to quit
                if cv2.waitKey(1) & 0xFF == ord("q"):

                    cap.release()
                    cv2.destroyAllWindows()

                    print("\nUser cancelled.")
                    return False

        cap.release()
        cv2.destroyAllWindows()

        return False