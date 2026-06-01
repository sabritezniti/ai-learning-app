"""
AI Learning Hub - Main Application
====================================
Interactive Streamlit application for learning Artificial Intelligence.
Features: Activation system, Course catalog, Local AI Mentor, Progress tracking.
Supports: French, English, Arabic

Author: AI Learning Hub
Version: 1.0.0
"""

import streamlit as st

# Must be the first Streamlit command
st.set_page_config(
    page_title="AI Learning Hub",
    page_icon="🎓",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Import configuration and utilities
from config import TRANSLATIONS, DEFAULT_LANGUAGE
from utils.styles import get_custom_css
from utils.components import (
    render_activation_page,
    render_sidebar,
    render_home_page,
    render_courses_page,
    render_mentor_page,
    render_profile_page
)


def initialize_session_state():
    """Initialize all session state variables."""
    if "activated" not in st.session_state:
        st.session_state.activated = False
    if "access_granted" not in st.session_state:
        st.session_state.access_granted = False
    if "current_page" not in st.session_state:
        st.session_state.current_page = "home"
    if "language" not in st.session_state:
        st.session_state.language = DEFAULT_LANGUAGE
    if "chat_history" not in st.session_state:
        st.session_state.chat_history = []

    # Initialize course progress
    from config import COURSES
    for lang in COURSES:
        for course in COURSES[lang]:
            key = f"progress_{course['id']}"
            if key not in st.session_state:
                st.session_state[key] = 0


def main():
    """Main application entry point."""
    # Initialize session state
    initialize_session_state()

    # Get current language
    lang = st.session_state.get("language", DEFAULT_LANGUAGE)
    t = TRANSLATIONS[lang]

    # Apply custom CSS
    st.markdown(get_custom_css(), unsafe_allow_html=True)

    # Apply RTL for Arabic
    if lang == "ar":
        st.markdown('<div class="rtl">', unsafe_allow_html=True)

    # Check activation
    if not st.session_state.activated:
        # Show activation page (no sidebar)
        render_activation_page(lang)
    else:
        # Show main application with sidebar
        render_sidebar(t, lang)

        # Render current page
        current_page = st.session_state.get("current_page", "home")

        if current_page == "home":
            render_home_page(t, lang)
        elif current_page == "courses":
            render_courses_page(t, lang)
        elif current_page == "mentor":
            render_mentor_page(t, lang)
        elif current_page == "profile":
            render_profile_page(t, lang)

    # Close RTL div for Arabic
    if lang == "ar":
        st.markdown('</div>', unsafe_allow_html=True)


if __name__ == "__main__":
    main()
