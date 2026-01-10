# Utilities Package for IntruWatch

from .auth import (
    hash_password,
    verify_password,
    is_valid_giki_email,
    validate_registration_number,
    validate_employee_id,
    validate_password_strength,
    sanitize_input
)

from .persistence import (
    save_pickle,
    load_pickle,
    save_json,
    load_json,
    create_backup,
    list_backups,
    restore_backup,
    save_checkins,
    load_checkins,
    save_logins,
    load_logins,
    save_guards,
    load_guards,
    save_alerts,
    load_alerts,
    save_events,
    load_events
)

from .camera import (
    initialize_face_recognizer,
    detect_faces,
    save_face_image,
    train_face_recognizer,
    load_face_recognizer,
    recognize_face,
    get_registered_users,
    get_user_photo_count,
    delete_user_photos
)

from .sorting import (
    insertion_sort,
    merge_sort,
    quick_sort,
    binary_search,
    linear_search,
    sort_reg_numbers,
    sort_by_priority,
    sort_guards_by_id,
    search_user_by_reg
)

__all__ = [
    # Auth
    'hash_password', 'verify_password', 'is_valid_giki_email',
    'validate_registration_number', 'validate_employee_id',
    'validate_password_strength', 'sanitize_input',
    
    # Persistence
    'save_pickle', 'load_pickle', 'save_json', 'load_json',
    'create_backup', 'list_backups', 'restore_backup',
    'save_checkins', 'load_checkins', 'save_logins', 'load_logins',
    'save_guards', 'load_guards', 'save_alerts', 'load_alerts',
    'save_events', 'load_events',
    
    # Camera
    'initialize_face_recognizer', 'detect_faces', 'save_face_image',
    'train_face_recognizer', 'load_face_recognizer', 'recognize_face',
    'get_registered_users', 'get_user_photo_count', 'delete_user_photos',
    
    # Sorting
    'insertion_sort', 'merge_sort', 'quick_sort',
    'binary_search', 'linear_search',
    'sort_reg_numbers', 'sort_by_priority', 'sort_guards_by_id',
    'search_user_by_reg'
]
