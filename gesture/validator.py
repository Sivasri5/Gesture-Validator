import math


def distance(point1, point2):
    """
    Calculate Euclidean distance between two landmarks.
    """
    return math.sqrt(
        (point1.x - point2.x) ** 2
        + (point1.y - point2.y) ** 2
        + (point1.z - point2.z) ** 2
    )


def is_finger_extended(landmarks, tip_id, pip_id, mcp_id):
    """
    Checks whether a finger is extended.

    A finger is considered extended when the fingertip
    is farther from the wrist direction than the folded joints.

    For a normal upright hand, this primarily checks
    the landmark positions.
    """

    tip = landmarks[tip_id]
    pip = landmarks[pip_id]
    mcp = landmarks[mcp_id]

    # Basic extension check
    return tip.y < pip.y and pip.y < mcp.y


def is_finger_folded(landmarks, tip_id, pip_id):
    """
    Checks whether a finger is folded.
    """

    tip = landmarks[tip_id]
    pip = landmarks[pip_id]

    return tip.y > pip.y


def fingers_are_separated(landmarks):
    """
    Makes sure index and middle fingers are sufficiently
    separated to form a V shape.
    """

    index_tip = landmarks[8]
    middle_tip = landmarks[12]

    separation = distance(index_tip, middle_tip)

    # Threshold may be adjusted based on testing
    return separation > 0.05


def is_peace_gesture(landmarks):
    """
    Validates the V / Peace gesture.

    Expected:
    - Index finger extended
    - Middle finger extended
    - Ring finger folded
    - Pinky folded
    """

    index_extended = is_finger_extended(
        landmarks,
        tip_id=8,
        pip_id=6,
        mcp_id=5
    )

    middle_extended = is_finger_extended(
        landmarks,
        tip_id=12,
        pip_id=10,
        mcp_id=9
    )

    ring_folded = is_finger_folded(
        landmarks,
        tip_id=16,
        pip_id=14
    )

    pinky_folded = is_finger_folded(
        landmarks,
        tip_id=20,
        pip_id=18
    )

    fingers_separated = fingers_are_separated(landmarks)

    is_correct = (
        index_extended
        and middle_extended
        and ring_folded
        and pinky_folded
        and fingers_separated
    )

    return is_correct