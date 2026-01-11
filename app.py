

import os
import numpy as np
import pandas as pd
import streamlit as st
import matplotlib.pyplot as plt
from datetime import datetime
from pathlib import Path

# Get the directory of this script for proper imports
import sys
SCRIPT_DIR = Path(__file__).resolve().parent
if str(SCRIPT_DIR) not in sys.path:
    sys.path.insert(0, str(SCRIPT_DIR))

# Import custom data structures
from data_structures import (
    LoginLinkedList, CheckInLinkedList, EventLinkedList,
    GuardNode, flatten_bst_bfs, assign_guards_to_locations,
    AlertSystem, CampusGraph, create_giki_campus_graph
)

# Import utilities
from utils import (
    hash_password, verify_password, is_valid_giki_email,
    validate_registration_number, validate_employee_id,
    validate_password_strength, sanitize_input,
    save_checkins, load_checkins, save_logins, load_logins,
    save_guards, load_guards, save_alerts, load_alerts,
    detect_faces, save_face_image, train_face_recognizer,
    load_face_recognizer, recognize_face, get_registered_users,
    sort_reg_numbers, binary_search
)

# ============================================================================
# PAGE CONFIGURATION (Must be first Streamlit command)
# ============================================================================
st.set_page_config(
    page_title="IntruWatch - GIKI Security",
    page_icon="🔒",
    layout="wide",
    initial_sidebar_state="expanded"
)

# ============================================================================
# CUSTOM CYBER SECURITY STYLING
# ============================================================================
st.markdown("""
<style>
    @import url('https://fonts.googleapis.com/css2?family=Orbitron:wght@400;500;600;700;800;900&family=Rajdhani:wght@300;400;500;600;700&family=Share+Tech+Mono&display=swap');
    
    /* Main App Background */
    .stApp {
        background: linear-gradient(135deg, #0a0f1a 0%, #0d1520 25%, #0a1628 50%, #081018 100%);
        font-family: 'Rajdhani', sans-serif;
    }
    
    /* Sidebar Styling */
    section[data-testid="stSidebar"] {
        background: linear-gradient(180deg, #0a0f1a 0%, #0d1825 50%, #0a1220 100%);
        border-right: 1px solid rgba(0, 255, 136, 0.3);
    }
    
    section[data-testid="stSidebar"] .stRadio label {
        font-family: 'Rajdhani', sans-serif;
        font-weight: 500;
        letter-spacing: 0.5px;
    }
    
    section[data-testid="stSidebar"] .stRadio label:hover {
        color: #00ff88 !important;
        text-shadow: 0 0 10px rgba(0, 255, 136, 0.5);
    }
    
    /* Headers */
    h1, h2, h3 {
        font-family: 'Orbitron', monospace !important;
        color: #00ff88 !important;
        text-shadow: 0 0 20px rgba(0, 255, 136, 0.4);
        letter-spacing: 2px;
    }
    
    h1 { font-size: 2.5rem !important; }
    h2 { font-size: 1.8rem !important; color: #00c8ff !important; }
    h3 { font-size: 1.4rem !important; color: #00e5ff !important; }
    
    /* Subheaders */
    .stSubheader {
        font-family: 'Orbitron', monospace !important;
        color: #00c8ff !important;
    }
    
    /* Text and Labels */
    p, span, label, .stMarkdown {
        font-family: 'Rajdhani', sans-serif !important;
        color: #c0d0e0 !important;
    }
    
    /* Metrics */
    [data-testid="stMetricValue"] {
        font-family: 'Orbitron', monospace !important;
        color: #00ff88 !important;
        text-shadow: 0 0 15px rgba(0, 255, 136, 0.5);
    }
    
    [data-testid="stMetricLabel"] {
        font-family: 'Rajdhani', sans-serif !important;
        color: #8892a0 !important;
        text-transform: uppercase;
        letter-spacing: 1px;
    }
    
    /* Buttons */
    .stButton > button {
        font-family: 'Orbitron', monospace !important;
        background: linear-gradient(135deg, rgba(0, 255, 136, 0.1) 0%, rgba(0, 200, 255, 0.1) 100%);
        border: 2px solid #00ff88;
        color: #00ff88 !important;
        font-weight: 600;
        letter-spacing: 1px;
        text-transform: uppercase;
        transition: all 0.3s ease;
        border-radius: 8px;
        padding: 0.5rem 1.5rem;
    }
    
    .stButton > button:hover {
        background: linear-gradient(135deg, rgba(0, 255, 136, 0.3) 0%, rgba(0, 200, 255, 0.2) 100%);
        box-shadow: 0 0 20px rgba(0, 255, 136, 0.4), inset 0 0 20px rgba(0, 255, 136, 0.1);
        transform: translateY(-2px);
    }
    
    /* Input Fields */
    .stTextInput > div > div > input,
    .stSelectbox > div > div,
    .stNumberInput > div > div > input {
        font-family: 'Rajdhani', sans-serif !important;
        background: rgba(10, 15, 26, 0.8) !important;
        border: 1px solid rgba(0, 255, 136, 0.3) !important;
        color: #00c8ff !important;
        border-radius: 6px;
    }
    
    .stTextInput > div > div > input:focus,
    .stSelectbox > div > div:focus {
        border-color: #00ff88 !important;
        box-shadow: 0 0 10px rgba(0, 255, 136, 0.3) !important;
    }
    
    /* Radio Buttons */
    .stRadio > label {
        font-family: 'Rajdhani', sans-serif !important;
        color: #c0d0e0 !important;
    }
    
    /* DataFrames */
    .stDataFrame {
        border: 1px solid rgba(0, 255, 136, 0.3);
        border-radius: 8px;
        overflow: hidden;
    }
    
    [data-testid="stDataFrame"] {
        background: rgba(10, 15, 26, 0.9);
    }
    
    /* Success/Error/Warning/Info Messages */
    .stSuccess {
        background: linear-gradient(90deg, rgba(0, 255, 136, 0.15) 0%, rgba(0, 255, 136, 0.05) 100%);
        border-left: 4px solid #00ff88;
        font-family: 'Rajdhani', sans-serif;
    }
    
    .stError {
        background: linear-gradient(90deg, rgba(255, 68, 68, 0.15) 0%, rgba(255, 68, 68, 0.05) 100%);
        border-left: 4px solid #ff4444;
    }
    
    .stWarning {
        background: linear-gradient(90deg, rgba(255, 170, 0, 0.15) 0%, rgba(255, 170, 0, 0.05) 100%);
        border-left: 4px solid #ffaa00;
    }
    
    .stInfo {
        background: linear-gradient(90deg, rgba(0, 200, 255, 0.15) 0%, rgba(0, 200, 255, 0.05) 100%);
        border-left: 4px solid #00c8ff;
    }
    
    /* Cards and Containers */
    .cyber-card {
        background: linear-gradient(135deg, rgba(13, 21, 32, 0.95) 0%, rgba(10, 22, 40, 0.9) 100%);
        border: 1px solid rgba(0, 255, 136, 0.2);
        border-radius: 12px;
        padding: 20px;
        margin: 10px 0;
        box-shadow: 0 4px 20px rgba(0, 0, 0, 0.3), inset 0 1px 0 rgba(0, 255, 136, 0.1);
    }
    
    .cyber-card:hover {
        border-color: rgba(0, 255, 136, 0.4);
        box-shadow: 0 4px 30px rgba(0, 255, 136, 0.1), inset 0 1px 0 rgba(0, 255, 136, 0.2);
    }
    
    /* Scan Line Animation */
    .scan-effect {
        position: relative;
        overflow: hidden;
    }
    
    .scan-effect::after {
        content: '';
        position: absolute;
        top: 0;
        left: 0;
        right: 0;
        height: 2px;
        background: linear-gradient(90deg, transparent, #00ff88, transparent);
        animation: scan 3s linear infinite;
    }
    
    @keyframes scan {
        0% { top: 0; }
        100% { top: 100%; }
    }
    
    /* Glow Effects */
    .glow-text {
        text-shadow: 0 0 10px currentColor, 0 0 20px currentColor, 0 0 30px currentColor;
    }
    
    /* Shimmer Animation */
    @keyframes shimmer {
        0% { background-position: -200% 0; }
        100% { background-position: 200% 0; }
    }
    
    .shimmer {
        background: linear-gradient(90deg, transparent, rgba(0, 255, 136, 0.1), transparent);
        background-size: 200% 100%;
        animation: shimmer 2s infinite;
    }
    
    /* Corner Decorations */
    .corner-frame {
        position: relative;
    }
    
    .corner-frame::before,
    .corner-frame::after {
        content: '';
        position: absolute;
        width: 20px;
        height: 20px;
        border: 2px solid #00ff88;
    }
    
    .corner-frame::before {
        top: 0;
        left: 0;
        border-right: none;
        border-bottom: none;
    }
    
    .corner-frame::after {
        bottom: 0;
        right: 0;
        border-left: none;
        border-top: none;
    }
    
    /* Alert Severity */
    .alert-critical {
        background: linear-gradient(90deg, rgba(255, 68, 68, 0.2) 0%, rgba(255, 68, 68, 0.1) 100%);
        border: 1px solid #ff4444;
        border-radius: 8px;
        padding: 15px;
        animation: pulse-red 2s infinite;
    }
    
    .alert-warning {
        background: linear-gradient(90deg, rgba(255, 170, 0, 0.2) 0%, rgba(255, 170, 0, 0.1) 100%);
        border: 1px solid #ffaa00;
        border-radius: 8px;
        padding: 15px;
    }
    
    .alert-info {
        background: linear-gradient(90deg, rgba(0, 255, 136, 0.2) 0%, rgba(0, 255, 136, 0.1) 100%);
        border: 1px solid #00ff88;
        border-radius: 8px;
        padding: 15px;
    }
    
    @keyframes pulse-red {
        0%, 100% { box-shadow: 0 0 5px rgba(255, 68, 68, 0.5); }
        50% { box-shadow: 0 0 20px rgba(255, 68, 68, 0.8); }
    }
    
    /* Status Indicators */
    .status-online { color: #00ff88; }
    .status-warning { color: #ffaa00; }
    .status-offline { color: #ff4444; }
    
    /* Table Styling */
    .dataframe {
        font-family: 'Rajdhani', sans-serif !important;
    }
    
    /* Expanders */
    .streamlit-expanderHeader {
        font-family: 'Orbitron', monospace !important;
        background: rgba(0, 255, 136, 0.05);
        border: 1px solid rgba(0, 255, 136, 0.2);
        border-radius: 8px;
    }
    
    /* Tabs */
    .stTabs [data-baseweb="tab-list"] {
        gap: 8px;
    }
    
    .stTabs [data-baseweb="tab"] {
        font-family: 'Orbitron', monospace;
        background: rgba(0, 255, 136, 0.05);
        border: 1px solid rgba(0, 255, 136, 0.2);
        border-radius: 8px 8px 0 0;
    }
    
    .stTabs [aria-selected="true"] {
        background: rgba(0, 255, 136, 0.15);
        border-color: #00ff88;
    }
    
    /* Dividers */
    hr {
        border: none;
        height: 1px;
        background: linear-gradient(90deg, transparent, rgba(0, 255, 136, 0.5), transparent);
        margin: 20px 0;
    }
    
    /* Form Styling */
    [data-testid="stForm"] {
        background: rgba(10, 15, 26, 0.5);
        border: 1px solid rgba(0, 255, 136, 0.2);
        border-radius: 12px;
        padding: 20px;
    }
    
    /* Progress Bar */
    .stProgress > div > div {
        background: linear-gradient(90deg, #00ff88, #00c8ff);
    }
    
    /* Selectbox */
    [data-baseweb="select"] {
        font-family: 'Rajdhani', sans-serif !important;
    }
    
    /* Camera Input */
    [data-testid="stCameraInput"] {
        border: 2px solid rgba(0, 255, 136, 0.3);
        border-radius: 12px;
        overflow: hidden;
    }
    
    /* Hide Streamlit Branding */
    #MainMenu {visibility: hidden;}
    footer {visibility: hidden;}
    
    /* Scrollbar */
    ::-webkit-scrollbar {
        width: 8px;
        height: 8px;
    }
    
    ::-webkit-scrollbar-track {
        background: #0a0f1a;
    }
    
    ::-webkit-scrollbar-thumb {
        background: linear-gradient(180deg, #00ff88, #00c8ff);
        border-radius: 4px;
    }
    
    ::-webkit-scrollbar-thumb:hover {
        background: #00ff88;
    }
</style>
""", unsafe_allow_html=True)

# ============================================================================
# SESSION STATE INITIALIZATION
# ============================================================================
def init_session_state():
    """Initialize all session state variables"""
    defaults = {
        "logged_in": False,
        "current_user": None,
        "started": False,
        "login_list": LoginLinkedList(),
        "checkin_list": CheckInLinkedList(),
        "event_log": EventLinkedList(max_size=20),
        "alert_system": AlertSystem(),
        "guard_tree": GuardNode(),
        "campus_graph": create_giki_campus_graph(),
        "face_recognizer": None,
        "face_labels": {},
        "face_capture_count": {}
    }
    
    for key, value in defaults.items():
        if key not in st.session_state:
            st.session_state[key] = value
    
    # Load persisted data
    loaded_logins = load_logins()
    if loaded_logins:
        st.session_state.login_list = loaded_logins
    
    loaded_checkins = load_checkins()
    if loaded_checkins:
        st.session_state.checkin_list = loaded_checkins
    
    # Create default admin if no admins exist
    if not st.session_state.login_list.head:
        st.session_state.login_list.insert("admin", hash_password("admin123"), "admin@giki.edu.pk", "admin")
        save_logins(st.session_state.login_list)
    
    # Initialize guards with sample data
    if st.session_state.guard_tree.guard_id is None:
        sample_guards = [
            ("John", 101, "Main Gate"),
            ("Alice", 102, "Library"),
            ("Bob", 103, "FCSE"),
            ("Eve", 104, "TUC"),
            ("Charlie", 105, "H1-H4"),
            ("Diana", 106, "H5-H7"),
            ("Frank", 107, "GH/NGH"),
            ("Grace", 108, "Faculty Residence"),
        ]
        for name, gid, duty in sample_guards:
            st.session_state.guard_tree.insert(name, gid, duty)

init_session_state()

# ============================================================================
# AUTHENTICATION FUNCTIONS
# ============================================================================
def login_page():
    """Admin authentication portal"""
    st.markdown("""
    <div style="text-align: center; margin-bottom: 30px;">
        <h1 style="font-family: 'Orbitron', monospace; color: #00ff88; text-shadow: 0 0 30px rgba(0, 255, 136, 0.5);">
            SECURITY AUTHENTICATION
        </h1>
        <p style="font-family: 'Rajdhani', sans-serif; color: #8892a0; font-size: 1.1rem;">
            Authorized Personnel Access Portal
        </p>
    </div>
    """, unsafe_allow_html=True)
    
    col1, col2 = st.columns(2)
    
    with col1:
        st.markdown("""
        <div class="cyber-card">
            <h3 style="color: #00c8ff; font-family: 'Orbitron', monospace; margin-bottom: 15px;">
                OPERATOR LOGIN
            </h3>
        </div>
        """, unsafe_allow_html=True)
        
        username = st.text_input("Operator ID", key="login_username", placeholder="Enter your operator ID")
        password = st.text_input("Access Code", type="password", key="login_password", placeholder="Enter access code")
        
        if st.button("AUTHENTICATE", key="login_btn", use_container_width=True):
            username = sanitize_input(username)
            if username and password:
                password_hash = hash_password(password)
                success, user = st.session_state.login_list.authenticate(username, password_hash)
                if success:
                    # Verify email is valid GIKI format
                    if user.email and is_valid_giki_email(user.email):
                        st.session_state.logged_in = True
                        st.session_state.current_user = username
                        st.session_state.event_log.add_event(f"Operator {username} authenticated")
                        st.success(f"ACCESS GRANTED - Welcome, {username}")
                        st.rerun()
                    else:
                        st.error("AUTHENTICATION BLOCKED - Account email is not verified GIKI format")
                else:
                    st.error("AUTHENTICATION FAILED - Invalid credentials")
            else:
                st.warning("All fields required for authentication")
    
    with col2:
        st.markdown("""
        <div class="cyber-card">
            <h3 style="color: #00c8ff; font-family: 'Orbitron', monospace; margin-bottom: 15px;">
                NEW OPERATOR REGISTRATION
            </h3>
        </div>
        """, unsafe_allow_html=True)
        
        new_username = st.text_input("Operator ID", key="signup_username", placeholder="Choose operator ID")
        new_email = st.text_input("Institutional Email", key="signup_email", placeholder="your.email@giki.edu.pk")
        
        # Real-time email validation feedback
        if new_email and not is_valid_giki_email(new_email):
            st.error("⚠️ Invalid email format - Must be @giki.edu.pk")
        
        new_password = st.text_input("Access Code", type="password", key="signup_password", placeholder="Create access code")
        confirm_password = st.text_input("Confirm Access Code", type="password", key="signup_confirm", placeholder="Re-enter access code")
        
        if st.button("REGISTER OPERATOR", key="signup_btn", use_container_width=True):
            new_username = sanitize_input(new_username)
            new_email = sanitize_input(new_email).lower().strip()
            
            if not new_username or not new_email or not new_password:
                st.error("All fields required for registration")
            elif not is_valid_giki_email(new_email):
                st.error("REGISTRATION BLOCKED - Only institutional emails (@giki.edu.pk) are permitted. Example: yourname@giki.edu.pk")
            elif new_password != confirm_password:
                st.error("Access codes do not match")
            elif st.session_state.login_list.username_exists(new_username):
                st.error("Operator ID already registered")
            else:
                valid, msg = validate_password_strength(new_password)
                if not valid:
                    st.error(msg)
                else:
                    password_hash = hash_password(new_password)
                    st.session_state.login_list.insert(new_username, password_hash, new_email)
                    save_logins(st.session_state.login_list)
                    st.success(f"OPERATOR REGISTERED - {new_username} access granted")

# ============================================================================
# CHECK-IN / CHECK-OUT PAGES
# ============================================================================
def checkin_page():
    """Resident access entry with form or biometric verification"""
    st.markdown("""
    <h1 style="font-family: 'Orbitron', monospace; color: #00ff88; text-shadow: 0 0 20px rgba(0, 255, 136, 0.4);">
        ACCESS ENTRY PORTAL
    </h1>
    <p style="font-family: 'Rajdhani', sans-serif; color: #8892a0;">
        Register identity for campus access authorization
    </p>
    """, unsafe_allow_html=True)
    
    # Check-in method selection
    checkin_method = st.radio(
        "Select Verification Method",
        ["Profile Registration", "Biometric Verification"],
        horizontal=True
    )
    
    st.markdown("---")
    
    if checkin_method == "Profile Registration":
        # Traditional form-based check-in
        st.markdown("""
        <h3 style="font-family: 'Orbitron', monospace; color: #00c8ff;">
            IDENTITY PROFILE CREATION
        </h3>
        """, unsafe_allow_html=True)
        
        designation = st.selectbox("Designation", ["Student", "Faculty", "Other"])
        username = st.text_input("Full Name")
        
        reg_no = None
        employee_no = None
        room_no = None
        
        if designation == "Student":
            reg_no = st.text_input("Registration Number (e.g., 2024113)")
            room_no = st.selectbox("Hostel", ["H1", "H2", "H3", "H4", "H5", "H6", "H7", "GH", "NGH"])
            
            if reg_no:
                valid, msg = validate_registration_number(reg_no)
                if not valid:
                    st.warning(msg)
        
        elif designation == "Faculty":
            employee_no = st.text_input("Employee ID (e.g., EMP456)")
            room_no = st.selectbox("Residence Type", ["D", "E", "F"])
            reg_no = employee_no
            
            if employee_no:
                valid, msg = validate_employee_id(employee_no)
                if not valid:
                    st.warning(msg)
        else:
            reg_no = st.text_input("ID Number")
        
        gender = st.selectbox("Gender", ["Male", "Female"])
        gender_code = "M" if gender == "Male" else "F"
        
        if st.button("Complete Check-In"):
            username = sanitize_input(username)
            if not username or not reg_no:
                st.error("Please fill all required fields")
            else:
                # Strict validation based on designation
                validation_passed = True
                
                if designation == "Student":
                    valid, msg = validate_registration_number(reg_no)
                    if not valid:
                        st.error(f"INVALID REGISTRATION: {msg}")
                        validation_passed = False
                elif designation == "Faculty":
                    valid, msg = validate_employee_id(reg_no)
                    if not valid:
                        st.error(f"INVALID EMPLOYEE ID: {msg}")
                        validation_passed = False
                
                if validation_passed:
                    st.session_state.checkin_list.insert(
                        username, reg_no, designation, gender_code, room_no, employee_no
                    )
                    save_checkins(st.session_state.checkin_list)
                    st.session_state.event_log.add_event(f"{designation} {username} checked in via profile")
                    st.success(f"{designation} {username} successfully checked in!")
                    st.balloons()
    
    else:
        # Face recognition check-in
        st.markdown("""
        <h3 style="font-family: 'Orbitron', monospace; color: #00c8ff;">
            BIOMETRIC FACE SCAN
        </h3>
        """, unsafe_allow_html=True)
        
        st.markdown("""
        <div style="background: rgba(0, 200, 255, 0.1); border: 1px solid rgba(0, 200, 255, 0.3); border-radius: 8px; padding: 15px; margin-bottom: 20px;">
            <p style="font-family: 'Rajdhani', sans-serif; color: #00c8ff; margin: 0;">
                <strong>PROTOCOL:</strong><br>
                1. New subjects: Capture 3 biometric samples for enrollment<br>
                2. Registered subjects: Verify identity for access authorization
            </p>
        </div>
        """, unsafe_allow_html=True)
        
        person_name = st.text_input("Enter Your Name", placeholder="e.g., Ahmed Khan")
        
        if not person_name:
            st.warning("Please enter your name to proceed")
            return
        
        person_name = sanitize_input(person_name)
        
        # Additional info for new registrations
        col1, col2 = st.columns(2)
        with col1:
            designation = st.selectbox("Designation", ["Student", "Faculty", "Other"], key="face_designation")
        with col2:
            if designation == "Student":
                reg_no = st.text_input("Registration Number (YYYYNNN)", key="face_reg", placeholder="e.g., 2024113")
                room_no = st.selectbox("Hostel", ["H1", "H2", "H3", "H4", "H5", "H6", "H7", "GH", "NGH"], key="face_hostel")
                if reg_no:
                    valid, msg = validate_registration_number(reg_no)
                    if not valid:
                        st.error(f"INVALID: {msg}")
            elif designation == "Faculty":
                reg_no = st.text_input("Employee ID (EMP###)", key="face_emp", placeholder="e.g., EMP456")
                room_no = st.selectbox("Residence", ["D", "E", "F"], key="face_res")
                if reg_no:
                    valid, msg = validate_employee_id(reg_no)
                    if not valid:
                        st.error(f"INVALID: {msg}")
            else:
                reg_no = st.text_input("ID Number", key="face_id")
                room_no = "N/A"
        
        gender = st.selectbox("Gender", ["Male", "Female"], key="face_gender")
        gender_code = "M" if gender == "Male" else "F"
        
        if person_name not in st.session_state.face_capture_count:
            st.session_state.face_capture_count[person_name] = 0
        
        current_count = st.session_state.face_capture_count[person_name]
        
        st.markdown("---")
        
        if current_count < 3:
            st.info(f"Registration Mode: Capture photo {current_count + 1}/3 for {person_name}")
        else:
            st.success(f"Recognition Mode: {person_name} is registered - Verify to check in")
        
        img_file = st.camera_input("Capture Face")
        
        if img_file is not None:
            import cv2
            file_bytes = np.asarray(bytearray(img_file.getvalue()), dtype=np.uint8)
            img_bgr = cv2.imdecode(file_bytes, cv2.IMREAD_COLOR)
            
            if current_count < 3:
                success, message = save_face_image(person_name, img_bgr, current_count + 1)
                if success:
                    st.session_state.face_capture_count[person_name] = current_count + 1
                    st.success(message)
                    
                    if st.session_state.face_capture_count[person_name] == 3:
                        st.balloons()
                        st.success(f"{person_name} face registered successfully!")
                        trained, train_msg = train_face_recognizer()
                        if trained:
                            st.info(train_msg)
                else:
                    st.error(message)
            else:
                # Load recognizer if needed
                if st.session_state.face_recognizer is None:
                    recognizer, labels, msg = load_face_recognizer()
                    st.session_state.face_recognizer = recognizer
                    st.session_state.face_labels = labels
                
                recognized_name, message, confidence = recognize_face(
                    img_bgr,
                    st.session_state.face_recognizer,
                    st.session_state.face_labels
                )
                
                if recognized_name and recognized_name == person_name:
                    # Validate ID before allowing check-in
                    id_valid = True
                    if designation == "Student":
                        valid, msg = validate_registration_number(reg_no)
                        if not valid:
                            st.error(f"INVALID REGISTRATION: {msg}")
                            id_valid = False
                    elif designation == "Faculty":
                        valid, msg = validate_employee_id(reg_no)
                        if not valid:
                            st.error(f"INVALID EMPLOYEE ID: {msg}")
                            id_valid = False
                    
                    if id_valid:
                        st.success("IDENTITY VERIFIED - Entry Authorized")
                        st.balloons()
                        # Auto check-in on successful verification
                        st.session_state.checkin_list.insert(
                            person_name, reg_no, designation, gender_code, room_no, None
                        )
                        save_checkins(st.session_state.checkin_list)
                        st.session_state.event_log.add_event(f"{designation} {person_name} checked in via face recognition")
                elif recognized_name:
                    st.warning(f"Face recognized as {recognized_name}, not {person_name}")
                    st.session_state.alert_system.add_alert(2, f"Identity mismatch: {person_name}", "Main Gate")
                else:
                    st.error("INTRUSION ALERT - Unknown Person Detected")
                    st.session_state.alert_system.add_alert(1, f"Unknown person: {person_name}", "Main Gate")
                    st.session_state.event_log.add_event(f"Intrusion detected: Unknown person")

def checkout_page():
    """Resident access exit portal"""
    st.markdown("""
    <h1 style="font-family: 'Orbitron', monospace; color: #00ff88; text-shadow: 0 0 20px rgba(0, 255, 136, 0.4);">
        ACCESS EXIT PORTAL
    </h1>
    <p style="font-family: 'Rajdhani', sans-serif; color: #8892a0;">
        Deregister campus access authorization
    </p>
    """, unsafe_allow_html=True)
    
    st.markdown("---")
    
    designation = st.selectbox("Personnel Classification", ["Student", "Faculty", "Other"])
    username = st.text_input("Full Name")
    identifier = st.text_input("Registration Number / Employee ID")
    location = st.text_input("Assigned Location")
    
    if st.button("PROCESS EXIT", use_container_width=True):
        username = sanitize_input(username)
        if st.session_state.checkin_list.remove(username, identifier, designation, location):
            save_checkins(st.session_state.checkin_list)
            st.session_state.event_log.add_event(f"{designation} {username} access revoked")
            st.success(f"ACCESS REVOKED - {designation} {username} exit processed")
        else:
            st.error("NO MATCH FOUND - Verify credentials")

# ============================================================================
# DASHBOARD
# ============================================================================
def dashboard_page():
    """Command center dashboard with metrics and surveillance map"""
    st.markdown("""
    <h1 style="font-family: 'Orbitron', monospace; color: #00ff88; text-shadow: 0 0 20px rgba(0, 255, 136, 0.4);">
        COMMAND CENTER
    </h1>
    """, unsafe_allow_html=True)
    
    # Get counts from linked list
    students, faculty, others = st.session_state.checkin_list.get_counts()
    total_guards = st.session_state.guard_tree.count_nodes()
    active_alerts = st.session_state.alert_system.count_alerts()
    
    # Metrics row with cyber styling
    cols = st.columns(6)
    metrics = [
        ("STUDENTS", students),
        ("FACULTY", faculty),
        ("SECURITY", total_guards),
        ("ALERTS", active_alerts),
        ("CAMERAS", 37),
        ("ZONES", 9)
    ]
    
    for col, (label, value) in zip(cols, metrics):
        with col:
            st.metric(label, value)
    
    st.markdown("---")
    
    # Camera Surveillance Grid
    col1, col2 = st.columns([2, 1])
    
    with col1:
        st.subheader("Camera Surveillance Grid")
        
        # Camera data with location zones
        cameras = [
            {"id": "CAM-001", "name": "Main Gate", "zone": "Entry", "status": "online", "type": "ANPR"},
            {"id": "CAM-002", "name": "FCSE Building", "zone": "Academic", "status": "online", "type": "PTZ"},
            {"id": "CAM-003", "name": "Library", "zone": "Academic", "status": "online", "type": "Dome"},
            {"id": "CAM-004", "name": "TUC", "zone": "Common", "status": "warning", "type": "Fixed"},
            {"id": "CAM-005", "name": "H1-H4 Hostels", "zone": "Residential", "status": "online", "type": "PTZ"},
            {"id": "CAM-006", "name": "H5-H7 Hostels", "zone": "Residential", "status": "online", "type": "PTZ"},
            {"id": "CAM-007", "name": "Admin Block", "zone": "Admin", "status": "online", "type": "Dome"},
            {"id": "CAM-008", "name": "Sports Complex", "zone": "Recreation", "status": "offline", "type": "Fixed"},
            {"id": "CAM-009", "name": "Parking Area", "zone": "Entry", "status": "online", "type": "ANPR"},
            {"id": "CAM-010", "name": "Faculty Residence", "zone": "Residential", "status": "online", "type": "Fixed"},
            {"id": "CAM-011", "name": "FME Building", "zone": "Academic", "status": "online", "type": "PTZ"},
            {"id": "CAM-012", "name": "Cafeteria", "zone": "Common", "status": "online", "type": "Dome"},
        ]
        
        # Count by status
        online_count = len([c for c in cameras if c["status"] == "online"])
        warning_count = len([c for c in cameras if c["status"] == "warning"])
        offline_count = len([c for c in cameras if c["status"] == "offline"])
        
        # Build camera grid HTML
        camera_cards_html = ""
        for cam in cameras:
            status_color = "#00ff88" if cam["status"] == "online" else "#ffaa00" if cam["status"] == "warning" else "#ff4444"
            status_glow = f"0 0 10px {status_color}"
            pulse_animation = "animation: pulse 2s infinite;" if cam["status"] == "online" else ""
            
            camera_cards_html += f'''
            <div class="camera-card">
                <div class="camera-status" style="background: {status_color}; box-shadow: {status_glow}; {pulse_animation}"></div>
                <div class="camera-info">
                    <div class="camera-id">{cam["id"]}</div>
                    <div class="camera-name">{cam["name"]}</div>
                    <div class="camera-meta">
                        <span class="camera-zone">{cam["zone"]}</span>
                        <span class="camera-type">{cam["type"]}</span>
                    </div>
                </div>
            </div>
            '''
        
        surveillance_html = f'''
        <style>
            @import url('https://fonts.googleapis.com/css2?family=Orbitron:wght@400;700&family=Rajdhani:wght@400;500;600&family=Share+Tech+Mono&display=swap');
            
            @keyframes pulse {{
                0%, 100% {{ opacity: 1; transform: scale(1); }}
                50% {{ opacity: 0.7; transform: scale(1.1); }}
            }}
            
            @keyframes scan {{
                0% {{ left: -100%; }}
                100% {{ left: 100%; }}
            }}
            
            .surveillance-container {{
                background: linear-gradient(135deg, #0a0f1a 0%, #0d1520 50%, #0a1628 100%);
                border: 2px solid #00ff88;
                border-radius: 12px;
                overflow: hidden;
                box-shadow: 0 0 30px rgba(0, 255, 136, 0.2), inset 0 0 60px rgba(0, 255, 136, 0.03);
            }}
            
            .surveillance-header {{
                background: linear-gradient(90deg, rgba(0, 255, 136, 0.15) 0%, rgba(0, 200, 255, 0.1) 50%, rgba(0, 255, 136, 0.15) 100%);
                padding: 15px 20px;
                border-bottom: 1px solid rgba(0, 255, 136, 0.3);
                display: flex;
                justify-content: space-between;
                align-items: center;
                position: relative;
                overflow: hidden;
            }}
            
            .surveillance-header::after {{
                content: '';
                position: absolute;
                top: 0;
                left: -100%;
                width: 100%;
                height: 100%;
                background: linear-gradient(90deg, transparent, rgba(0, 255, 136, 0.1), transparent);
                animation: scan 3s linear infinite;
            }}
            
            .header-title {{
                font-family: 'Orbitron', monospace;
                color: #00ff88;
                font-size: 16px;
                font-weight: 700;
                letter-spacing: 2px;
                text-shadow: 0 0 10px rgba(0, 255, 136, 0.5);
            }}
            
            .header-stats {{
                display: flex;
                gap: 20px;
                font-family: 'Share Tech Mono', monospace;
                font-size: 12px;
            }}
            
            .stat-item {{
                display: flex;
                align-items: center;
                gap: 6px;
            }}
            
            .stat-dot {{
                width: 8px;
                height: 8px;
                border-radius: 50%;
            }}
            
            .stat-dot.online {{ background: #00ff88; box-shadow: 0 0 8px #00ff88; }}
            .stat-dot.warning {{ background: #ffaa00; box-shadow: 0 0 8px #ffaa00; }}
            .stat-dot.offline {{ background: #ff4444; box-shadow: 0 0 8px #ff4444; }}
            
            .stat-label {{ color: #8892a0; }}
            .stat-value {{ color: #00c8ff; font-weight: 600; }}
            
            .camera-grid {{
                display: grid;
                grid-template-columns: repeat(auto-fill, minmax(200px, 1fr));
                gap: 12px;
                padding: 20px;
            }}
            
            .camera-card {{
                background: rgba(0, 255, 136, 0.03);
                border: 1px solid rgba(0, 255, 136, 0.2);
                border-radius: 8px;
                padding: 12px;
                display: flex;
                align-items: center;
                gap: 12px;
                transition: all 0.3s ease;
            }}
            
            .camera-card:hover {{
                background: rgba(0, 255, 136, 0.08);
                border-color: rgba(0, 255, 136, 0.4);
                transform: translateY(-2px);
                box-shadow: 0 4px 15px rgba(0, 255, 136, 0.15);
            }}
            
            .camera-status {{
                width: 12px;
                height: 12px;
                border-radius: 50%;
                flex-shrink: 0;
            }}
            
            .camera-info {{
                flex: 1;
                min-width: 0;
            }}
            
            .camera-id {{
                font-family: 'Share Tech Mono', monospace;
                color: #00c8ff;
                font-size: 11px;
                letter-spacing: 1px;
            }}
            
            .camera-name {{
                font-family: 'Rajdhani', sans-serif;
                color: #e0e8f0;
                font-size: 14px;
                font-weight: 600;
                white-space: nowrap;
                overflow: hidden;
                text-overflow: ellipsis;
            }}
            
            .camera-meta {{
                display: flex;
                gap: 8px;
                margin-top: 4px;
            }}
            
            .camera-zone, .camera-type {{
                font-family: 'Rajdhani', sans-serif;
                font-size: 10px;
                padding: 2px 6px;
                border-radius: 3px;
                text-transform: uppercase;
                letter-spacing: 0.5px;
            }}
            
            .camera-zone {{
                background: rgba(0, 200, 255, 0.15);
                color: #00c8ff;
                border: 1px solid rgba(0, 200, 255, 0.3);
            }}
            
            .camera-type {{
                background: rgba(0, 255, 136, 0.1);
                color: #00ff88;
                border: 1px solid rgba(0, 255, 136, 0.2);
            }}
            
            .surveillance-footer {{
                background: rgba(0, 0, 0, 0.3);
                padding: 10px 20px;
                border-top: 1px solid rgba(0, 255, 136, 0.2);
                display: flex;
                justify-content: space-between;
                align-items: center;
            }}
            
            .footer-info {{
                font-family: 'Rajdhani', sans-serif;
                color: #8892a0;
                font-size: 12px;
            }}
            
            .footer-time {{
                font-family: 'Share Tech Mono', monospace;
                color: #00ff88;
                font-size: 12px;
            }}
        </style>
        
        <div class="surveillance-container">
            <div class="surveillance-header">
                <div class="header-title">GIKI CAMPUS SURVEILLANCE</div>
                <div class="header-stats">
                    <div class="stat-item">
                        <div class="stat-dot online"></div>
                        <span class="stat-label">Online:</span>
                        <span class="stat-value">{online_count}</span>
                    </div>
                    <div class="stat-item">
                        <div class="stat-dot warning"></div>
                        <span class="stat-label">Warning:</span>
                        <span class="stat-value">{warning_count}</span>
                    </div>
                    <div class="stat-item">
                        <div class="stat-dot offline"></div>
                        <span class="stat-label">Offline:</span>
                        <span class="stat-value">{offline_count}</span>
                    </div>
                </div>
            </div>
            
            <div class="camera-grid">
                {camera_cards_html}
            </div>
            
            <div class="surveillance-footer">
                <div class="footer-info">Total Cameras: {len(cameras)} | Active Zones: 6</div>
                <div class="footer-time" id="liveTime"></div>
            </div>
        </div>
        
        <script>
            function updateLiveTime() {{
                const now = new Date();
                document.getElementById('liveTime').textContent = now.toLocaleTimeString() + ' | LIVE';
            }}
            updateLiveTime();
            setInterval(updateLiveTime, 1000);
        </script>
        '''
        
        st.components.v1.html(surveillance_html, height=450)
    
    with col2:
        st.markdown("""
        <h3 style="font-family: 'Orbitron', monospace; color: #00c8ff; font-size: 1rem;">
            SYSTEM ACTIVITY LOG
        </h3>
        """, unsafe_allow_html=True)
        events = st.session_state.event_log.get_all_events()
        if events:
            for event in events[:5]:
                st.info(event)
        else:
            st.info("No recent system activity")
    
    st.markdown("---")
    
    # Registered residents table
    st.markdown("""
    <h3 style="font-family: 'Orbitron', monospace; color: #00c8ff;">
        ACTIVE PERSONNEL REGISTRY
    </h3>
    """, unsafe_allow_html=True)
    data = st.session_state.checkin_list.to_list()
    if data:
        df = pd.DataFrame(data)
        st.dataframe(df, use_container_width=True)
    else:
        st.info("No personnel currently registered in system")


# ============================================================================
# ALERTS PAGE (Priority Queue - Threat Monitor)
# ============================================================================
def alerts_page():
    """Security threat monitoring with priority queue"""
    st.markdown("""
    <h1 style="font-family: 'Orbitron', monospace; color: #00ff88; text-shadow: 0 0 20px rgba(0, 255, 136, 0.4);">
        THREAT MONITOR
    </h1>
    <p style="font-family: 'Rajdhani', sans-serif; color: #8892a0;">
        Priority-based security alert management system
    </p>
    """, unsafe_allow_html=True)
    
    # Add alert form
    st.markdown("""
    <h3 style="font-family: 'Orbitron', monospace; color: #00c8ff;">
        REPORT NEW THREAT
    </h3>
    """, unsafe_allow_html=True)
    
    with st.form("alert_form"):
        message = st.text_input("Threat Description")
        priority = st.selectbox("Severity Level", [1, 2, 3], format_func=lambda x: f"LEVEL {x} - {'CRITICAL' if x==1 else 'WARNING' if x==2 else 'NOTICE'}")
        location = st.selectbox("Affected Zone", st.session_state.campus_graph.get_all_locations())
        
        if st.form_submit_button("SUBMIT ALERT"):
            if message:
                st.session_state.alert_system.add_alert(priority, sanitize_input(message), location)
                save_alerts(st.session_state.alert_system)
                st.success("ALERT REGISTERED - Dispatching to security personnel")
    
    st.markdown("---")
    
    # Display alerts
    st.markdown("""
    <h3 style="font-family: 'Orbitron', monospace; color: #00c8ff;">
        ACTIVE THREATS
    </h3>
    """, unsafe_allow_html=True)
    
    alerts_data = st.session_state.alert_system.to_dataframe_format()
    if alerts_data:
        df = pd.DataFrame(alerts_data)
        st.dataframe(df, use_container_width=True)
        
        # Priority distribution
        counts = st.session_state.alert_system.count_by_priority()
        st.markdown("**Threat Level Distribution**")
        st.bar_chart({"Critical": counts[1], "Warning": counts[2], "Notice": counts[3]})
    else:
        st.info("NO ACTIVE THREATS - System secure")

# ============================================================================
# GUARDS MANAGER (BST - Personnel Manager)
# ============================================================================
def guards_page():
    """Security personnel management using BST"""
    st.markdown("""
    <h1 style="font-family: 'Orbitron', monospace; color: #00ff88; text-shadow: 0 0 20px rgba(0, 255, 136, 0.4);">
        PERSONNEL MANAGER
    </h1>
    <p style="font-family: 'Rajdhani', sans-serif; color: #8892a0;">
        Security staff registry and deployment management
    </p>
    """, unsafe_allow_html=True)
    
    col1, col2 = st.columns(2)
    
    with col1:
        st.markdown("""
        <h3 style="font-family: 'Orbitron', monospace; color: #00c8ff;">
            REGISTER PERSONNEL
        </h3>
        """, unsafe_allow_html=True)
        name = st.text_input("Personnel Name")
        guard_id = st.number_input("Badge ID", min_value=1, step=1)
        duty = st.text_input("Assigned Zone")
        
        if st.button("REGISTER", use_container_width=True):
            if name and duty:
                st.session_state.guard_tree.insert(sanitize_input(name), int(guard_id), sanitize_input(duty))
                save_guards(st.session_state.guard_tree)
                st.success(f"REGISTERED - {name} added to system")
    
    with col2:
        st.markdown("""
        <h3 style="font-family: 'Orbitron', monospace; color: #00c8ff;">
            PERSONNEL LOOKUP
        </h3>
        """, unsafe_allow_html=True)
        search_id = st.number_input("Search by Badge ID", min_value=1, step=1, key="search_id")
        if st.button("SEARCH", use_container_width=True):
            result = st.session_state.guard_tree.find(int(search_id))
            if result:
                st.success(f"FOUND: {result.name} - Zone: {result.duty}")
            else:
                st.error("NO MATCH - Personnel not found")
    
    st.markdown("---")
    
    # Display all guards (inorder traversal)
    st.markdown("""
    <h3 style="font-family: 'Orbitron', monospace; color: #00c8ff;">
        ACTIVE ROSTER (Sorted by ID)
    </h3>
    """, unsafe_allow_html=True)
    guards = st.session_state.guard_tree.inorder()
    if guards:
        df = pd.DataFrame(guards, columns=["Name", "Badge ID", "Zone"])
        st.dataframe(df, use_container_width=True)
    
    # Location assignments
    st.markdown("""
    <h3 style="font-family: 'Orbitron', monospace; color: #00c8ff;">
        ZONE DEPLOYMENT
    </h3>
    """, unsafe_allow_html=True)
    locations = {
        "FCSE": 1, "FME": 1, "FBS": 1, "Library": 1,
        "TUC": 2, "Main Gate": 1, "Residential": 3
    }
    assignments = assign_guards_to_locations(st.session_state.guard_tree, locations)
    
    for loc, guards_list in assignments.items():
        st.markdown(f"**{loc}**: {', '.join(guards_list) if guards_list else 'Unassigned'}")

# ============================================================================
# ANALYTICS PAGE (Admin - Comprehensive Analytics)
# ============================================================================
def analytics_page():
    """Comprehensive security analytics dashboard"""
    st.markdown("""
    <h1 style="font-family: 'Orbitron', monospace; color: #00ff88; text-shadow: 0 0 20px rgba(0, 255, 136, 0.4);">
        ANALYTICS CENTER
    </h1>
    <p style="font-family: 'Rajdhani', sans-serif; color: #8892a0;">
        Real-time security metrics and population analysis
    </p>
    """, unsafe_allow_html=True)
    
    # Get data and filter for valid entries only
    raw_data = st.session_state.checkin_list.to_list()
    
    # Filter out invalid entries - only show verified personnel in analytics
    valid_data = []
    for entry in raw_data:
        designation = entry.get("Designation", "")
        reg_no = entry.get("Reg No", "")
        
        if designation == "Student":
            valid, _ = validate_registration_number(reg_no)
            if valid:
                valid_data.append(entry)
        elif designation == "Faculty":
            valid, _ = validate_employee_id(reg_no)
            if valid:
                valid_data.append(entry)
        else:
            # Other designations pass through
            valid_data.append(entry)
    
    # Count only valid entries
    valid_students = sum(1 for e in valid_data if e.get("Designation") == "Student")
    valid_faculty = sum(1 for e in valid_data if e.get("Designation") == "Faculty")
    valid_others = sum(1 for e in valid_data if e.get("Designation") == "Other")
    total_checked_in = valid_students + valid_faculty + valid_others
    active_alerts = st.session_state.alert_system.count_alerts()
    total_guards = st.session_state.guard_tree.count_nodes()
    
    # Top metrics row
    st.markdown("""
    <h3 style="font-family: 'Orbitron', monospace; color: #00c8ff;">
        SYSTEM STATUS
    </h3>
    """, unsafe_allow_html=True)
    cols = st.columns(5)
    with cols[0]:
        st.metric("TOTAL ACTIVE", total_checked_in)
    with cols[1]:
        st.metric("STUDENTS", valid_students)
    with cols[2]:
        st.metric("FACULTY", valid_faculty)
    with cols[3]:
        st.metric("VISITORS", valid_others)
    with cols[4]:
        st.metric("THREATS", active_alerts)
    
    st.markdown("---")
    
    if not valid_data:
        st.info("No verified personnel data available for analytics")
        return
    
    df = pd.DataFrame(valid_data)
    
    # Row 1: Distribution Charts
    st.subheader("Population Distribution Analysis")
    col1, col2, col3 = st.columns(3)
    
    with col1:
        st.markdown("**By Designation**")
        designation_counts = df["Designation"].value_counts()
        fig1, ax1 = plt.subplots(figsize=(6, 6))
        colors_designation = ['#00ff88', '#00c8ff', '#ffaa00']
        ax1.pie(designation_counts.values, labels=designation_counts.index, autopct='%1.1f%%',
                colors=colors_designation[:len(designation_counts)], startangle=90)
        ax1.set_facecolor('#0a0f1a')
        fig1.patch.set_facecolor('#0a0f1a')
        for text in ax1.texts:
            text.set_color('white')
        st.pyplot(fig1)
    
    with col2:
        st.markdown("**By Gender**")
        gender_counts = df["Gender"].value_counts()
        fig2, ax2 = plt.subplots(figsize=(6, 6))
        colors_gender = ['#00c8ff', '#ff6b9d']
        ax2.pie(gender_counts.values, labels=gender_counts.index, autopct='%1.1f%%',
                colors=colors_gender[:len(gender_counts)], startangle=90)
        ax2.set_facecolor('#0a0f1a')
        fig2.patch.set_facecolor('#0a0f1a')
        for text in ax2.texts:
            text.set_color('white')
        st.pyplot(fig2)
    
    with col3:
        st.markdown("**By Location**")
        if "Hostel No" in df.columns:
            hostel_counts = df["Hostel No"].value_counts()
            fig3, ax3 = plt.subplots(figsize=(6, 6))
            ax3.barh(hostel_counts.index, hostel_counts.values, color='#00ff88')
            ax3.set_facecolor('#0a0f1a')
            ax3.tick_params(colors='white')
            ax3.spines['bottom'].set_color('white')
            ax3.spines['left'].set_color('white')
            ax3.spines['top'].set_visible(False)
            ax3.spines['right'].set_visible(False)
            fig3.patch.set_facecolor('#0a0f1a')
            st.pyplot(fig3)
    
    st.markdown("---")
    
    # Row 2: Detailed Charts
    st.subheader("Detailed Analytics")
    col4, col5 = st.columns(2)
    
    with col4:
        st.markdown("**Check-in by Hostel/Residence**")
        if "Hostel No" in df.columns:
            hostel_data = df["Hostel No"].value_counts()
            fig4, ax4 = plt.subplots(figsize=(10, 5))
            bars = ax4.bar(hostel_data.index, hostel_data.values, color='#00c8ff', edgecolor='#00ff88', linewidth=2)
            ax4.set_xlabel('Location', color='white')
            ax4.set_ylabel('Count', color='white')
            ax4.set_facecolor('#0a0f1a')
            ax4.tick_params(colors='white')
            ax4.spines['bottom'].set_color('#00ff88')
            ax4.spines['left'].set_color('#00ff88')
            ax4.spines['top'].set_visible(False)
            ax4.spines['right'].set_visible(False)
            fig4.patch.set_facecolor('#0a0f1a')
            # Add value labels on bars
            for bar, val in zip(bars, hostel_data.values):
                ax4.text(bar.get_x() + bar.get_width()/2, bar.get_height() + 0.1, 
                        str(val), ha='center', va='bottom', color='white', fontweight='bold')
            st.pyplot(fig4)
    
    with col5:
        st.markdown("**Gender by Designation**")
        gender_designation = df.groupby(['Designation', 'Gender']).size().unstack(fill_value=0)
        fig5, ax5 = plt.subplots(figsize=(10, 5))
        x = range(len(gender_designation.index))
        width = 0.35
        colors = {'M': '#00c8ff', 'F': '#ff6b9d'}
        for i, gender in enumerate(gender_designation.columns):
            offset = width * (i - 0.5)
            ax5.bar([xi + offset for xi in x], gender_designation[gender], width, 
                   label=f'{"Male" if gender == "M" else "Female"}', color=colors.get(gender, '#ffffff'))
        ax5.set_xticks(x)
        ax5.set_xticklabels(gender_designation.index)
        ax5.legend()
        ax5.set_facecolor('#0a0f1a')
        ax5.tick_params(colors='white')
        ax5.spines['bottom'].set_color('#00ff88')
        ax5.spines['left'].set_color('#00ff88')
        ax5.spines['top'].set_visible(False)
        ax5.spines['right'].set_visible(False)
        ax5.legend(facecolor='#1a1f2e', edgecolor='#00ff88', labelcolor='white')
        fig5.patch.set_facecolor('#0a0f1a')
        st.pyplot(fig5)
    
    st.markdown("---")
    
    # Row 3: Security Overview
    st.subheader("Security Status")
    col6, col7 = st.columns(2)
    
    with col6:
        st.markdown("**Alert Priority Distribution**")
        alert_counts = st.session_state.alert_system.count_by_priority()
        fig6, ax6 = plt.subplots(figsize=(8, 5))
        priorities = ['High', 'Medium', 'Low']
        values = [alert_counts.get(1, 0), alert_counts.get(2, 0), alert_counts.get(3, 0)]
        colors_alert = ['#ff4444', '#ffaa00', '#00ff88']
        bars = ax6.bar(priorities, values, color=colors_alert, edgecolor='white', linewidth=1)
        ax6.set_ylabel('Count', color='white')
        ax6.set_facecolor('#0a0f1a')
        ax6.tick_params(colors='white')
        ax6.spines['bottom'].set_color('#00ff88')
        ax6.spines['left'].set_color('#00ff88')
        ax6.spines['top'].set_visible(False)
        ax6.spines['right'].set_visible(False)
        fig6.patch.set_facecolor('#0a0f1a')
        for bar, val in zip(bars, values):
            ax6.text(bar.get_x() + bar.get_width()/2, bar.get_height() + 0.1, 
                    str(val), ha='center', va='bottom', color='white', fontweight='bold')
        st.pyplot(fig6)
    
    with col7:
        st.markdown("**Guard Deployment**")
        guards = st.session_state.guard_tree.inorder()
        if guards:
            guard_locations = {}
            for name, gid, duty in guards:
                guard_locations[duty] = guard_locations.get(duty, 0) + 1
            
            fig7, ax7 = plt.subplots(figsize=(8, 5))
            ax7.barh(list(guard_locations.keys()), list(guard_locations.values()), color='#00ff88')
            ax7.set_xlabel('Guards Assigned', color='white')
            ax7.set_facecolor('#0a0f1a')
            ax7.tick_params(colors='white')
            ax7.spines['bottom'].set_color('#00ff88')
            ax7.spines['left'].set_color('#00ff88')
            ax7.spines['top'].set_visible(False)
            ax7.spines['right'].set_visible(False)
            fig7.patch.set_facecolor('#0a0f1a')
            st.pyplot(fig7)
        else:
            st.info("No guards assigned yet")
    
    st.markdown("---")
    
    # Data Table
    st.subheader("Current Check-in Records")
    st.dataframe(df, use_container_width=True)

# ============================================================================
# CAMPUS GRAPH PAGE (Navigation Grid)
# ============================================================================
def graph_page():
    """Campus navigation with shortest path"""
    st.markdown("""
    <h1 style="font-family: 'Orbitron', monospace; color: #00ff88; text-shadow: 0 0 20px rgba(0, 255, 136, 0.4);">
        NAVIGATION GRID
    </h1>
    <p style="font-family: 'Rajdhani', sans-serif; color: #8892a0;">
        Campus pathfinding and route optimization
    </p>
    """, unsafe_allow_html=True)
    st.markdown("### Campus Navigation Map")
    
    graph = st.session_state.campus_graph
    
    col1, col2 = st.columns(2)
    
    with col1:
        st.subheader("Find Shortest Path")
        locations = graph.get_all_locations()
        start = st.selectbox("From", locations, key="start_loc")
        end = st.selectbox("To", locations, key="end_loc")
        
        if st.button("Find Path"):
            distance, path = graph.dijkstra(start, end)
            if distance != float('inf'):
                st.success(f"Distance: {distance}m")
                st.info(f"Path: {' → '.join(path)}")
            else:
                st.error("No path found")
    
    with col2:
        st.subheader("Graph Traversals")
        if st.button("BFS from Main Gate"):
            bfs_result = graph.bfs_traversal("Main Gate")
            st.write(bfs_result)
        
        if st.button("DFS from Main Gate"):
            dfs_result = graph.dfs_traversal("Main Gate")
            st.write(dfs_result)

# ============================================================================
# ABOUT PAGE
# ============================================================================
def about_page():
    """About page"""
    st.markdown("""
    <h1 style="font-family: 'Orbitron', monospace; color: #00ff88; text-shadow: 0 0 20px rgba(0, 255, 136, 0.4);">
        SYSTEM INFO
    </h1>
    """, unsafe_allow_html=True)
    
    st.markdown("""
    <div class="cyber-card">
        <h3 style="color: #00c8ff; font-family: 'Orbitron', monospace;">OUR MISSION</h3>
        <p style="color: #c0d0e0; font-family: 'Rajdhani', sans-serif; font-size: 1.1rem;">
            Making GIKI safer for all its inhabitants through intelligent security monitoring.
        </p>
    </div>
    """, unsafe_allow_html=True)
    
    st.markdown("""
    <div class="cyber-card">
        <h3 style="color: #00c8ff; font-family: 'Orbitron', monospace;">KEY FEATURES</h3>
        <ul style="color: #c0d0e0; font-family: 'Rajdhani', sans-serif; font-size: 1rem;">
            <li>Real-time surveillance with 37 camera network</li>
            <li>Biometric face recognition for access control</li>
            <li>Priority-based threat detection and response</li>
            <li>Campus-wide navigation and pathfinding</li>
            <li>Personnel management and tracking</li>
        </ul>
    </div>
    """, unsafe_allow_html=True)
    
    st.markdown("""
    <div class="cyber-card">
        <h3 style="color: #00c8ff; font-family: 'Orbitron', monospace;">DEVELOPMENT TEAM</h3>
        <div style="display: flex; flex-direction: column; gap: 10px; margin-top: 15px;">
            <div style="background: rgba(0, 255, 136, 0.05); padding: 10px 15px; border-radius: 6px; border-left: 3px solid #00ff88;">
                <span style="color: #00ff88; font-family: 'Orbitron', monospace;">Areej Arif</span>
                <span style="color: #8892a0; font-family: 'Rajdhani', sans-serif;"> - 2024127</span>
            </div>
            <div style="background: rgba(0, 255, 136, 0.05); padding: 10px 15px; border-radius: 6px; border-left: 3px solid #00c8ff;">
                <span style="color: #00c8ff; font-family: 'Orbitron', monospace;">Ayesha Khalid</span>
                <span style="color: #8892a0; font-family: 'Rajdhani', sans-serif;"> - 2024127</span>
            </div>
            <div style="background: rgba(0, 255, 136, 0.05); padding: 10px 15px; border-radius: 6px; border-left: 3px solid #00ff88;">
                <span style="color: #00ff88; font-family: 'Orbitron', monospace;">Nabiha Nasir</span>
                <span style="color: #8892a0; font-family: 'Rajdhani', sans-serif;"> - 2024514</span>
            </div>
        </div>
    </div>
    """, unsafe_allow_html=True)
    
    st.markdown("""
    <div class="cyber-card" style="text-align: center;">
        <h3 style="color: #00c8ff; font-family: 'Orbitron', monospace;">CONTACT</h3>
        <p style="color: #00ff88; font-family: 'Share Tech Mono', monospace; font-size: 1.1rem;">
            IntruWatch@gmail.com
        </p>
    </div>
    """, unsafe_allow_html=True)

# ============================================================================
# MAIN APPLICATION
# ============================================================================
def main():
    # Cyber-themed Landing page
    if not st.session_state.started:
        st.markdown("""
        <style>
            @keyframes glitch {
                0%, 100% { text-shadow: 0 0 20px #00ff88, 0 0 40px #00ff88, 0 0 60px #00ff88; }
                25% { text-shadow: -2px 0 #ff0040, 2px 0 #00c8ff; }
                50% { text-shadow: 2px 0 #ff0040, -2px 0 #00c8ff; }
                75% { text-shadow: 0 0 30px #00ff88, 0 0 50px #00c8ff; }
            }
            
            @keyframes scanline {
                0% { transform: translateY(-100%); }
                100% { transform: translateY(100vh); }
            }
            
            @keyframes pulse-glow {
                0%, 100% { box-shadow: 0 0 20px rgba(0, 255, 136, 0.4), 0 0 40px rgba(0, 255, 136, 0.2); }
                50% { box-shadow: 0 0 40px rgba(0, 255, 136, 0.6), 0 0 80px rgba(0, 255, 136, 0.4); }
            }
            
            .landing-container {
                text-align: center;
                padding: 60px 20px;
                position: relative;
                overflow: hidden;
            }
            
            .landing-container::before {
                content: '';
                position: absolute;
                top: 0;
                left: 0;
                right: 0;
                height: 2px;
                background: linear-gradient(90deg, transparent, #00ff88, transparent);
                animation: scanline 4s linear infinite;
            }
            
            .cyber-title {
                font-family: 'Orbitron', monospace;
                font-size: 4.5rem;
                font-weight: 900;
                color: #00ff88;
                text-transform: uppercase;
                letter-spacing: 8px;
                margin-bottom: 10px;
                animation: glitch 3s infinite;
            }
            
            .cyber-subtitle {
                font-family: 'Rajdhani', sans-serif;
                font-size: 1.5rem;
                color: #00c8ff;
                letter-spacing: 4px;
                text-transform: uppercase;
                margin-bottom: 20px;
            }
            
            .cyber-description {
                font-family: 'Rajdhani', sans-serif;
                font-size: 1.1rem;
                color: #8892a0;
                max-width: 600px;
                margin: 0 auto 40px;
                line-height: 1.6;
            }
            
        </style>
        
        <div class="landing-container">
            <div class="cyber-title">INTRUWATCH</div>
            <div class="cyber-subtitle">Campus Security Command Center</div>
            <div class="cyber-description">
                Advanced Intrusion Detection & Access Control System<br>
                Real-time surveillance, biometric verification, and threat monitoring for GIKI Campus
            </div>
        </div>
        """, unsafe_allow_html=True)
        
        # Feature cards using Streamlit columns
        col1, col2, col3 = st.columns(3)
        
        with col1:
            st.markdown("""
            <div style="background: rgba(0, 255, 136, 0.05); border: 1px solid rgba(0, 255, 136, 0.2); border-radius: 12px; padding: 20px; text-align: center;">
                <h4 style="font-family: 'Orbitron', monospace; color: #00ff88; font-size: 0.9rem; margin-bottom: 8px;">BIOMETRIC ACCESS</h4>
                <p style="font-family: 'Rajdhani', sans-serif; color: #8892a0; font-size: 0.85rem;">Face recognition entry verification</p>
            </div>
            """, unsafe_allow_html=True)
        
        with col2:
            st.markdown("""
            <div style="background: rgba(0, 255, 136, 0.05); border: 1px solid rgba(0, 255, 136, 0.2); border-radius: 12px; padding: 20px; text-align: center;">
                <h4 style="font-family: 'Orbitron', monospace; color: #00ff88; font-size: 0.9rem; margin-bottom: 8px;">THREAT DETECTION</h4>
                <p style="font-family: 'Rajdhani', sans-serif; color: #8892a0; font-size: 0.85rem;">Priority-based alert system</p>
            </div>
            """, unsafe_allow_html=True)
        
        with col3:
            st.markdown("""
            <div style="background: rgba(0, 255, 136, 0.05); border: 1px solid rgba(0, 255, 136, 0.2); border-radius: 12px; padding: 20px; text-align: center;">
                <h4 style="font-family: 'Orbitron', monospace; color: #00ff88; font-size: 0.9rem; margin-bottom: 8px;">SURVEILLANCE GRID</h4>
                <p style="font-family: 'Rajdhani', sans-serif; color: #8892a0; font-size: 0.85rem;">37 camera network monitoring</p>
            </div>
            """, unsafe_allow_html=True)
        
        # Status bar
        st.markdown("""
        <div style="display: flex; justify-content: center; gap: 30px; margin-top: 40px; font-family: 'Share Tech Mono', monospace; font-size: 0.85rem; color: #00c8ff;">
            <div style="display: flex; align-items: center; gap: 8px;">
                <div style="width: 8px; height: 8px; border-radius: 50%; background: #00ff88; box-shadow: 0 0 10px #00ff88;"></div> SYSTEM ONLINE
            </div>
            <div style="display: flex; align-items: center; gap: 8px;">
                <div style="width: 8px; height: 8px; border-radius: 50%; background: #00ff88; box-shadow: 0 0 10px #00ff88;"></div> CAMERAS ACTIVE
            </div>
            <div style="display: flex; align-items: center; gap: 8px;">
                <div style="width: 8px; height: 8px; border-radius: 50%; background: #00ff88; box-shadow: 0 0 10px #00ff88;"></div> SECURE CONNECTION
            </div>
        </div>
        </div>
        """, unsafe_allow_html=True)
        
        col1, col2, col3 = st.columns([1, 1, 1])
        with col2:
            if st.button("INITIALIZE SYSTEM", use_container_width=True):
                st.session_state.started = True
                st.rerun()
        return
    
    # Post-login navigation (Operator Mode)
    if st.session_state.logged_in:
        st.sidebar.markdown(f"""
        <div style="text-align: center; padding: 15px; background: rgba(0, 255, 136, 0.05); border-radius: 8px; border: 1px solid rgba(0, 255, 136, 0.2); margin-bottom: 20px;">
            <p style="font-family: 'Rajdhani', sans-serif; color: #8892a0; font-size: 0.9rem; margin: 0;">OPERATOR</p>
            <p style="font-family: 'Orbitron', monospace; color: #00ff88; font-size: 1.1rem; margin: 5px 0;">{st.session_state.current_user.upper()}</p>
            <p style="font-family: 'Share Tech Mono', monospace; color: #00c8ff; font-size: 0.75rem; margin: 0;">SESSION ACTIVE</p>
        </div>
        """, unsafe_allow_html=True)
        
        if st.sidebar.button("TERMINATE SESSION", use_container_width=True):
            st.session_state.event_log.add_event(f"Operator {st.session_state.current_user} session terminated")
            st.session_state.logged_in = False
            st.session_state.current_user = None
            st.rerun()
        
        st.sidebar.markdown("---")
        st.sidebar.markdown("""
        <p style="font-family: 'Orbitron', monospace; color: #00c8ff; font-size: 0.8rem; letter-spacing: 2px; margin-bottom: 10px;">COMMAND CENTER</p>
        """, unsafe_allow_html=True)
        
        menu = ["Control Panel", "Analytics Center", "Threat Monitor", "Personnel Manager", 
                "Navigation Grid", "System Logs"]
        choice = st.sidebar.radio("", menu, label_visibility="collapsed")
        
        if choice == "Control Panel":
            dashboard_page()
        elif choice == "Analytics Center":
            analytics_page()
        elif choice == "Threat Monitor":
            alerts_page()
        elif choice == "Personnel Manager":
            guards_page()
        elif choice == "Navigation Grid":
            graph_page()
        elif choice == "System Logs":
            st.markdown("""
            <h1 style="font-family: 'Orbitron', monospace; color: #00ff88;">SYSTEM EVENT LOGS</h1>
            """, unsafe_allow_html=True)
            events = st.session_state.event_log.get_all_events()
            if events:
                df = pd.DataFrame({"Event": events})
                st.dataframe(df, use_container_width=True)
            else:
                st.info("No events recorded in system logs")
    
    # Pre-login navigation (Public Mode)
    else:
        st.sidebar.markdown("""
        <div style="text-align: center; padding: 15px; margin-bottom: 20px;">
            <p style="font-family: 'Orbitron', monospace; color: #00ff88; font-size: 1.2rem; letter-spacing: 2px;">INTRUWATCH</p>
            <p style="font-family: 'Rajdhani', sans-serif; color: #8892a0; font-size: 0.85rem;">Access Control Terminal</p>
        </div>
        """, unsafe_allow_html=True)
        
        st.sidebar.markdown("---")
        st.sidebar.markdown("""
        <p style="font-family: 'Orbitron', monospace; color: #00c8ff; font-size: 0.8rem; letter-spacing: 2px; margin-bottom: 10px;">NAVIGATION</p>
        """, unsafe_allow_html=True)
        
        menu = ["Operator Login", "Access Entry", "Access Exit", "System Info"]
        choice = st.sidebar.radio("", menu, label_visibility="collapsed")
        
        if choice == "Operator Login":
            login_page()
        elif choice == "Access Entry":
            checkin_page()
        elif choice == "Access Exit":
            checkout_page()
        elif choice == "System Info":
            about_page()


if __name__ == "__main__":
    main()
