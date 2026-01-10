# Data Persistence Utilities for IntruWatch

import pickle
import json
from pathlib import Path
from typing import Any, Optional
from datetime import datetime


DATA_DIR = Path("data")
BACKUP_DIR = Path("backups")


def ensure_directories():
    """Create necessary directories if they don't exist"""
    DATA_DIR.mkdir(exist_ok=True)
    BACKUP_DIR.mkdir(exist_ok=True)


def save_pickle(data: Any, filename: str) -> bool:
    """Save data to pickle file"""
    ensure_directories()
    try:
        filepath = DATA_DIR / f"{filename}.pkl"
        with open(filepath, 'wb') as f:
            pickle.dump(data, f)
        return True
    except Exception as e:
        print(f"Error saving {filename}: {e}")
        return False


def load_pickle(filename: str) -> Optional[Any]:
    """Load data from pickle file"""
    ensure_directories()
    try:
        filepath = DATA_DIR / f"{filename}.pkl"
        if filepath.exists():
            with open(filepath, 'rb') as f:
                return pickle.load(f)
        return None
    except Exception as e:
        print(f"Error loading {filename}: {e}")
        return None


def save_json(data: dict, filename: str) -> bool:
    """Save data to JSON file (for human-readable data)"""
    ensure_directories()
    try:
        filepath = DATA_DIR / f"{filename}.json"
        with open(filepath, 'w') as f:
            json.dump(data, f, indent=2, default=str)
        return True
    except Exception as e:
        print(f"Error saving {filename}: {e}")
        return False


def load_json(filename: str) -> Optional[dict]:
    """Load data from JSON file"""
    ensure_directories()
    try:
        filepath = DATA_DIR / f"{filename}.json"
        if filepath.exists():
            with open(filepath, 'r') as f:
                return json.load(f)
        return None
    except Exception as e:
        print(f"Error loading {filename}: {e}")
        return None


def create_backup(filename: str) -> bool:
    """Create timestamped backup of data file"""
    ensure_directories()
    try:
        source = DATA_DIR / f"{filename}.pkl"
        if source.exists():
            timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
            backup_path = BACKUP_DIR / f"{filename}_{timestamp}.pkl"
            with open(source, 'rb') as src:
                with open(backup_path, 'wb') as dst:
                    dst.write(src.read())
            return True
        return False
    except Exception as e:
        print(f"Error creating backup for {filename}: {e}")
        return False


def list_backups(filename: str) -> list:
    """List all backups for a given filename"""
    ensure_directories()
    pattern = f"{filename}_*.pkl"
    return sorted(BACKUP_DIR.glob(pattern), reverse=True)


def restore_backup(backup_path: Path, filename: str) -> bool:
    """Restore data from a backup file"""
    try:
        if backup_path.exists():
            dest = DATA_DIR / f"{filename}.pkl"
            with open(backup_path, 'rb') as src:
                with open(dest, 'wb') as dst:
                    dst.write(src.read())
            return True
        return False
    except Exception as e:
        print(f"Error restoring backup: {e}")
        return False


# Specific save/load functions for IntruWatch data

def save_checkins(checkin_list) -> bool:
    """Save check-in linked list"""
    return save_pickle(checkin_list, "checkins")


def load_checkins():
    """Load check-in linked list"""
    return load_pickle("checkins")


def save_logins(login_list) -> bool:
    """Save login linked list"""
    return save_pickle(login_list, "logins")


def load_logins():
    """Load login linked list"""
    return load_pickle("logins")


def save_guards(guard_tree) -> bool:
    """Save guard BST"""
    return save_pickle(guard_tree, "guards")


def load_guards():
    """Load guard BST"""
    return load_pickle("guards")


def save_alerts(alert_system) -> bool:
    """Save alert system"""
    return save_pickle(alert_system, "alerts")


def load_alerts():
    """Load alert system"""
    return load_pickle("alerts")


def save_events(event_list) -> bool:
    """Save event log"""
    return save_pickle(event_list, "events")


def load_events():
    """Load event log"""
    return load_pickle("events")
