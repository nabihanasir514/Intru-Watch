# Camera and Face Recognition Utilities for IntruWatch

import cv2
import numpy as np
import pickle
from pathlib import Path
from typing import Tuple, Optional, List
from datetime import datetime


PHOTOS_DIR = Path("photos")
RECOGNIZER_DIR = Path("recognizer_data")


def ensure_directories():
    """Create necessary directories"""
    PHOTOS_DIR.mkdir(exist_ok=True)
    RECOGNIZER_DIR.mkdir(exist_ok=True)


def initialize_face_recognizer():
    """Initialize LBPH Face Recognizer"""
    return cv2.face.LBPHFaceRecognizer_create()


def get_face_cascade():
    """Load Haar Cascade for face detection"""
    cascade_path = cv2.data.haarcascades + "haarcascade_frontalface_default.xml"
    return cv2.CascadeClassifier(cascade_path)


def detect_faces(img_bgr: np.ndarray) -> Tuple[list, np.ndarray]:
    """Detect faces in an image
    
    Returns:
        Tuple of (faces_list, grayscale_image)
    """
    face_cascade = get_face_cascade()
    gray = cv2.cvtColor(img_bgr, cv2.COLOR_BGR2GRAY)
    faces = face_cascade.detectMultiScale(
        gray,
        scaleFactor=1.1,
        minNeighbors=5,
        minSize=(30, 30)
    )
    return faces, gray


def save_face_image(username: str, img_bgr: np.ndarray, photo_num: int) -> Tuple[bool, str]:
    """Save detected face image for training
    
    Args:
        username: Person's name for labeling
        img_bgr: BGR image from camera
        photo_num: Photo number (1-3 for registration)
    
    Returns:
        Tuple of (success, message)
    """
    ensure_directories()
    
    faces, gray = detect_faces(img_bgr)
    
    if len(faces) == 0:
        return False, "No face detected. Please ensure your face is clearly visible."
    
    if len(faces) > 1:
        return False, "Multiple faces detected. Please ensure only one person is in frame."
    
    # Extract and resize face region
    (x, y, w, h) = faces[0]
    face_roi = gray[y:y+h, x:x+w]
    face_roi = cv2.resize(face_roi, (200, 200))
    
    # Save with timestamp
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    filename = PHOTOS_DIR / f"{username}_{photo_num}_{timestamp}.jpg"
    cv2.imwrite(str(filename), face_roi)
    
    return True, f"Face photo {photo_num} saved successfully!"


def train_face_recognizer() -> Tuple[bool, str]:
    """Train face recognizer on all saved photos
    
    Returns:
        Tuple of (success, message)
    """
    ensure_directories()
    
    if not PHOTOS_DIR.exists():
        return False, "No photos directory found"
    
    photo_files = list(PHOTOS_DIR.glob("*.jpg"))
    if len(photo_files) == 0:
        return False, "No photos found for training"
    
    faces = []
    labels = []
    label_map = {}
    current_label = 0
    
    # Group photos by username
    user_photos = {}
    for photo_file in photo_files:
        parts = photo_file.stem.split("_")
        if len(parts) >= 2:
            username = parts[0]
            user_photos.setdefault(username, []).append(photo_file)
    
    # Process each user's photos
    for username, photo_list in user_photos.items():
        if username not in label_map:
            label_map[username] = current_label
            current_label += 1
        
        label_id = label_map[username]
        
        for photo_file in photo_list:
            img = cv2.imread(str(photo_file), cv2.IMREAD_GRAYSCALE)
            if img is not None:
                img = cv2.resize(img, (200, 200))
                faces.append(img)
                labels.append(label_id)
    
    if len(faces) == 0:
        return False, "No valid face images found"
    
    # Train recognizer
    recognizer = initialize_face_recognizer()
    recognizer.train(faces, np.array(labels))
    
    # Save model and label map
    recognizer.save(str(RECOGNIZER_DIR / "face_recognizer.yml"))
    with open(RECOGNIZER_DIR / "label_map.pkl", "wb") as f:
        pickle.dump(label_map, f)
    
    return True, f"Trained on {len(user_photos)} users with {len(faces)} photos"


def load_face_recognizer() -> Tuple[Optional[object], dict, str]:
    """Load trained face recognizer
    
    Returns:
        Tuple of (recognizer, labels_dict, message)
    """
    ensure_directories()
    
    recognizer_file = RECOGNIZER_DIR / "face_recognizer.yml"
    label_file = RECOGNIZER_DIR / "label_map.pkl"
    
    if not recognizer_file.exists() or not label_file.exists():
        return None, {}, "Face recognizer not trained yet"
    
    try:
        recognizer = initialize_face_recognizer()
        recognizer.read(str(recognizer_file))
        
        with open(label_file, "rb") as f:
            label_map = pickle.load(f)
        
        # Reverse the label map for lookup
        labels = {v: k for k, v in label_map.items()}
        
        return recognizer, labels, "Recognizer loaded successfully"
    except Exception as e:
        return None, {}, f"Error loading recognizer: {e}"


def recognize_face(img_bgr: np.ndarray, recognizer, labels: dict) -> Tuple[Optional[str], str, float]:
    """Recognize a face from image
    
    Args:
        img_bgr: BGR image from camera
        recognizer: Trained LBPH recognizer
        labels: Label ID to username mapping
    
    Returns:
        Tuple of (username or None, message, confidence)
    """
    if recognizer is None:
        return None, "Face recognizer not available", 0.0
    
    faces, gray = detect_faces(img_bgr)
    
    if len(faces) == 0:
        return None, "No face detected", 0.0
    
    if len(faces) > 1:
        return None, "Multiple faces detected", 0.0
    
    # Extract face region
    (x, y, w, h) = faces[0]
    face_roi = gray[y:y+h, x:x+w]
    face_roi = cv2.resize(face_roi, (200, 200))
    
    # Predict
    label, confidence = recognizer.predict(face_roi)
    
    # Lower confidence = better match in LBPH
    confidence_percent = max(0, 100 - confidence)
    
    if confidence < 100:  # Threshold for recognition
        username = labels.get(label, "Unknown")
        return username, f"Recognized as {username} (confidence: {confidence_percent:.1f}%)", confidence_percent
    
    return None, f"Face not recognized (confidence too low: {confidence_percent:.1f}%)", confidence_percent


def get_registered_users() -> List[str]:
    """Get list of all registered users"""
    ensure_directories()
    
    if not PHOTOS_DIR.exists():
        return []
    
    users = set()
    for photo_file in PHOTOS_DIR.glob("*.jpg"):
        parts = photo_file.stem.split("_")
        if len(parts) >= 1:
            users.add(parts[0])
    
    return sorted(list(users))


def get_user_photo_count(username: str) -> int:
    """Get number of photos for a user"""
    ensure_directories()
    
    photos = list(PHOTOS_DIR.glob(f"{username}_*.jpg"))
    return len(photos)


def delete_user_photos(username: str) -> int:
    """Delete all photos for a user
    
    Returns:
        Number of photos deleted
    """
    ensure_directories()
    
    photos = list(PHOTOS_DIR.glob(f"{username}_*.jpg"))
    count = 0
    for photo in photos:
        photo.unlink()
        count += 1
    
    return count
