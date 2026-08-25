from gesture.detector import GestureDetector


def perform_future_action():
    """
    Put your future action here.

    For example:
    - Unlock something
    - Start another program
    - Trigger an API
    - Move to the next step
    """

    print("Future action is being performed!")


def main():

    detector = GestureDetector(
        required_frames=15,
        timeout=10,
        camera_index=0
    )

    result = detector.detect_peace_gesture()

    print("\n-------------------------")
    print(f"FINAL BOOLEAN RESULT: {result}")
    print("-------------------------")

    if result is True:

        print("Correct gesture detected.")

        perform_future_action()

    else:

        print("Gesture validation failed.")


if __name__ == "__main__":
    main()