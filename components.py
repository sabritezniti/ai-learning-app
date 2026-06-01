"""
Reusable UI components for the AI Learning Application.
"""

import streamlit as st
from config import COURSES, TRANSLATIONS
from utils.styles import get_level_badge


def render_activation_page(lang="fr"):
    """Render the activation page with key input."""
    t = TRANSLATIONS[lang]

    st.markdown(f"""
    <div class="activation-container">
        <div class="activation-icon">🔐</div>
        <div class="activation-title">{t['activation']}</div>
        <div class="activation-subtitle">{t['enter_key']}</div>
    </div>
    """, unsafe_allow_html=True)

    col1, col2, col3 = st.columns([1, 2, 1])
    with col2:
        key_input = st.text_input(
            "",
            type="password",
            placeholder="••••••••••••••",
            label_visibility="collapsed"
        )

        if st.button(t['activate'], type="primary", use_container_width=True):
            from config import ACTIVATION_KEY
            if key_input == ACTIVATION_KEY:
                st.session_state.activated = True
                st.session_state.access_granted = True
                st.success(t['access_granted'])
                st.rerun()
            else:
                st.error(t['invalid_key'])


def render_sidebar(t, lang="fr"):
    """Render the sidebar navigation."""
    with st.sidebar:
        st.markdown(f"""
        <div style="text-align: center; padding: 20px 0;">
            <div style="font-size: 48px; margin-bottom: 8px;">🎓</div>
            <div style="font-size: 20px; font-weight: 700; color: white;">AI Learning Hub</div>
            <div style="font-size: 12px; color: #888; margin-top: 4px;">{t['subtitle']}</div>
        </div>
        <hr style="border-color: rgba(255,255,255,0.1); margin: 16px 0;">
        """, unsafe_allow_html=True)

        # Navigation buttons
        pages = [
            ("home", t['home']),
            ("courses", t['courses']),
            ("mentor", t['mentor']),
            ("profile", t['profile'])
        ]

        current_page = st.session_state.get("current_page", "home")

        for page_key, page_label in pages:
            btn_type = "primary" if current_page == page_key else "secondary"
            if st.button(page_label, key=f"nav_{page_key}", type=btn_type, use_container_width=True):
                st.session_state.current_page = page_key
                st.rerun()

        st.markdown("<hr style='border-color: rgba(255,255,255,0.1); margin: 16px 0;'>", unsafe_allow_html=True)

        # Language selector
        st.markdown(f"<div style='color: #888; font-size: 12px; margin-bottom: 8px;'>{t['language']}</div>", unsafe_allow_html=True)

        lang_options = {"fr": "🇫🇷 Français", "en": "🇬🇧 English", "ar": "🇸🇦 العربية"}
        current_lang = st.session_state.get("language", lang)
        selected_lang = st.selectbox(
            "",
            options=list(lang_options.keys()),
            format_func=lambda x: lang_options[x],
            index=list(lang_options.keys()).index(current_lang),
            label_visibility="collapsed"
        )

        if selected_lang != current_lang:
            st.session_state.language = selected_lang
            st.rerun()

        # Logout button
        st.markdown("<div style='margin-top: auto; padding-top: 20px;'>", unsafe_allow_html=True)
        if st.button(t['logout'], key="logout_btn", use_container_width=True):
            st.session_state.activated = False
            st.session_state.access_granted = False
            st.session_state.current_page = "home"
            st.rerun()

        st.markdown(f"""
        <div style="text-align: center; padding: 16px 0; color: #666; font-size: 11px;">
            {t['footer']}
        </div>
        """, unsafe_allow_html=True)


def render_header(t, lang="fr"):
    """Render the main header."""
    st.markdown(f"""
    <div class="main-header">
        <h1>{t['welcome']}</h1>
        <p>{t['subtitle']}</p>
    </div>
    """, unsafe_allow_html=True)


def render_course_card(course, t, lang="fr"):
    """Render a single course card."""
    progress = st.session_state.get(f"progress_{course['id']}", 0)

    # Determine button state
    if progress == 0:
        btn_text = t['start_course']
        btn_class = "btn-start"
    elif progress < 100:
        btn_text = t['continue']
        btn_class = "btn-continue"
    else:
        btn_text = t['completed_btn']
        btn_class = "btn-completed"

    st.markdown(f"""
    <div class="course-card" style="--card-color: {course['color']};">
        <span class="course-icon">{course['icon']}</span>
        <div class="course-title">{course['title']}</div>
        <div class="course-description">{course['description']}</div>
        <div class="course-meta">
            <div class="course-meta-item">
                <span>📊</span> {course['level']}
            </div>
            <div class="course-meta-item">
                <span>⏱️</span> {course['duration']}
            </div>
            <div class="course-meta-item">
                <span>📋</span> {len(course['modules'])} {t['modules']}
            </div>
        </div>
        <div class="course-progress">
            <div class="progress-label">
                <span>{t['overall_progress']}</span>
                <span>{progress}%</span>
            </div>
        </div>
    </div>
    """, unsafe_allow_html=True)

    # Progress bar
    st.progress(progress / 100)

    # Action button
    col1, col2 = st.columns([3, 1])
    with col2:
        if st.button(btn_text, key=f"btn_{course['id']}", use_container_width=True):
            if progress < 100:
                new_progress = min(progress + 20, 100)
                st.session_state[f"progress_{course['id']}"] = new_progress
                st.rerun()

    # Modules expander
    with st.expander(f"📋 {t['modules']}"):
        for i, module in enumerate(course['modules']):
            module_completed = progress >= ((i + 1) / len(course['modules'])) * 100
            icon = "✅" if module_completed else "⭕"
            st.markdown(f"{icon} {module}")


def render_stats_section(t, lang="fr"):
    """Render statistics cards."""
    courses = COURSES[lang]
    total_hours = sum(int(c['duration'].split()[0]) for c in courses)
    total_modules = sum(len(c['modules']) for c in courses)

    cols = st.columns(4)
    stats = [
        (len(courses), t['stats_courses']),
        (total_hours, t['stats_hours']),
        (total_modules, t['stats_modules']),
        (3, t['stats_level'])
    ]

    for col, (value, label) in zip(cols, stats):
        with col:
            st.markdown(f"""
            <div class="stat-card">
                <div class="stat-value">{value}</div>
                <div class="stat-label">{label}</div>
            </div>
            """, unsafe_allow_html=True)


def render_feature_cards(t, lang="fr"):
    """Render feature highlight cards."""
    features = [
        (t['feature_courses'], t['feature_courses_desc'], "📚"),
        (t['feature_mentor'], t['feature_mentor_desc'], "🤖"),
        (t['feature_progress'], t['feature_progress_desc'], "📊"),
        (t['feature_multilingual'], t['feature_multilingual_desc'], "🌍")
    ]

    cols = st.columns(4)
    for col, (title, desc, icon) in zip(cols, features):
        with col:
            st.markdown(f"""
            <div class="feature-card">
                <div class="feature-icon">{icon}</div>
                <div class="feature-title">{title}</div>
                <div class="feature-desc">{desc}</div>
            </div>
            """, unsafe_allow_html=True)


def render_home_page(t, lang="fr"):
    """Render the home page."""
    render_header(t, lang)

    # Stats
    render_stats_section(t, lang)

    st.markdown("<br>", unsafe_allow_html=True)

    # Features
    st.subheader(t['welcome_home'])
    st.write(t['home_desc'])

    render_feature_cards(t, lang)

    st.markdown("<br>", unsafe_allow_html=True)

    # CTA
    col1, col2, col3 = st.columns([1, 2, 1])
    with col2:
        if st.button(t['get_started'], type="primary", use_container_width=True):
            st.session_state.current_page = "courses"
            st.rerun()


def render_courses_page(t, lang="fr"):
    """Render the courses catalog page."""
    st.markdown(f"""
    <div style="text-align: center; margin-bottom: 32px;">
        <h1 style="font-size: 32px; color: #1a1a2e;">{t['catalogue']}</h1>
        <p style="color: #666;">{t['subtitle']}</p>
    </div>
    """, unsafe_allow_html=True)

    courses = COURSES[lang]

    # Progress overview
    total_progress = 0
    completed_courses = 0
    for course in courses:
        prog = st.session_state.get(f"progress_{course['id']}", 0)
        total_progress += prog
        if prog == 100:
            completed_courses += 1

    avg_progress = total_progress / len(courses) if courses else 0

    col1, col2, col3 = st.columns(3)
    with col1:
        st.metric(t['total_courses'], len(courses))
    with col2:
        st.metric(t['completed'], completed_courses)
    with col3:
        st.metric(t['overall_progress'], f"{avg_progress:.0f}%")

    st.progress(avg_progress / 100)

    st.markdown("<hr>", unsafe_allow_html=True)

    # Course cards grid
    cols = st.columns(2)
    for i, course in enumerate(courses):
        with cols[i % 2]:
            render_course_card(course, t, lang)
            st.markdown("<br>", unsafe_allow_html=True)


def render_mentor_page(t, lang="fr"):
    """Render the AI Mentor chat page."""
    st.markdown(f"""
    <div style="text-align: center; margin-bottom: 24px;">
        <h1 style="font-size: 32px; color: #1a1a2e;">{t['mentor_title']}</h1>
        <p style="color: #666;">{t['mentor_desc']}</p>
    </div>
    """, unsafe_allow_html=True)

    # Initialize chat history
    if "chat_history" not in st.session_state:
        st.session_state.chat_history = []

    # Course context selector
    courses = COURSES[lang]
    course_options = {t['no_course']: None}
    for course in courses:
        course_options[course['title']] = course

    selected_course_title = st.selectbox(
        t['select_course_chat'],
        options=list(course_options.keys()),
        index=0
    )
    selected_course = course_options[selected_course_title]

    # Chat container
    chat_container = st.container()

    with chat_container:
        # Display chat history
        for msg in st.session_state.chat_history:
            role_class = "chat-user" if msg["role"] == "user" else "chat-assistant"
            avatar = "👤" if msg["role"] == "user" else "🤖"

            st.markdown(f"""
            <div style="display: flex; align-items: flex-start; margin: 8px 0; {'flex-direction: row-reverse;' if msg['role'] == 'user' and lang == 'ar' else ''}">
                <div class="chat-avatar" style="background: {'linear-gradient(135deg, #667eea 0%, #764ba2 100%)' if msg['role'] == 'user' else '#f0f0f0'};">
                    {avatar}
                </div>
                <div class="chat-message {role_class}">
                    {msg['content']}
                </div>
            </div>
            """, unsafe_allow_html=True)

    # Input area
    st.markdown("<hr>", unsafe_allow_html=True)

    col1, col2 = st.columns([5, 1])
    with col1:
        user_input = st.text_input(
            "",
            placeholder=t['chat_placeholder'],
            label_visibility="collapsed",
            key="chat_input"
        )
    with col2:
        send_clicked = st.button(t['send'], type="primary", use_container_width=True)

    if send_clicked and user_input.strip():
        # Add user message
        st.session_state.chat_history.append({"role": "user", "content": user_input})

        # Get context
        context = ""
        if selected_course:
            context = f"Course: {selected_course['title']}\nDescription: {selected_course['description']}\nModules: {', '.join(selected_course['modules'])}"

        # Get AI response
        from utils.ollama_client import initialize_mentor, get_system_prompt

        mentor = initialize_mentor()

        with st.spinner(t['thinking']):
            if mentor.is_available:
                # Build messages from history
                messages = []
                system_prompt = get_system_prompt(lang)

                # Add recent history (last 10 messages)
                for msg in st.session_state.chat_history[-10:]:
                    messages.append({"role": msg["role"], "content": msg["content"]})

                response = mentor.generate(user_input, system_prompt=system_prompt, context=context)

                if response:
                    st.session_state.chat_history.append({"role": "assistant", "content": response})
                else:
                    st.session_state.chat_history.append({
                        "role": "assistant", 
                        "content": "Désolé, je n'ai pas pu générer de réponse. Veuillez réessayer." if lang == "fr" else 
                                   "Sorry, I couldn't generate a response. Please try again." if lang == "en" else
                                   "عذراً، لم أتمكن من توليد رد. يرجى المحاولة مرة أخرى."
                    })
            else:
                # Fallback response when Ollama is not available
                fallback_responses = {
                    "fr": f"🤖 **Mentor IA** (Mode hors-ligne)\n\nJe suis désolé, mais le service Ollama n'est pas disponible actuellement. Pour utiliser le Mentor IA, veuillez :\n\n1. Installer Ollama : `curl -fsSL https://ollama.com/install.sh | sh`\n2. Télécharger un modèle : `ollama pull llama3.2`\n3. Démarrer le service : `ollama serve`\n\n**Votre question** : {user_input}\n\n**Contexte** : {selected_course['title'] if selected_course else 'Discussion générale'}",
                    "en": f"🤖 **AI Mentor** (Offline Mode)\n\nI'm sorry, but the Ollama service is currently unavailable. To use the AI Mentor, please:\n\n1. Install Ollama: `curl -fsSL https://ollama.com/install.sh | sh`\n2. Download a model: `ollama pull llama3.2`\n3. Start the service: `ollama serve`\n\n**Your question**: {user_input}\n\n**Context**: {selected_course['title'] if selected_course else 'General discussion'}",
                    "ar": f"🤖 **المرشد الذكي** (وضع عدم الاتصال)\n\nعذراً، خدمة Ollama غير متوفرة حالياً. لاستخدام المرشد الذكي، يرجى:\n\n1. تثبيت Ollama: `curl -fsSL https://ollama.com/install.sh | sh`\n2. تحميل نموذج: `ollama pull llama3.2`\n3. تشغيل الخدمة: `ollama serve`\n\n**سؤالك**: {user_input}\n\n**السياق**: {selected_course['title'] if selected_course else 'مناقشة عامة'}"
                }
                st.session_state.chat_history.append({
                    "role": "assistant", 
                    "content": fallback_responses.get(lang, fallback_responses["en"])
                })

        st.rerun()

    # Clear chat button
    if st.session_state.chat_history:
        if st.button("🗑️ " + ("Effacer" if lang == "fr" else "Clear" if lang == "en" else "مسح"), key="clear_chat"):
            st.session_state.chat_history = []
            st.rerun()


def render_profile_page(t, lang="fr"):
    """Render the user profile page."""
    st.markdown(f"""
    <div style="text-align: center; margin-bottom: 24px;">
        <h1 style="font-size: 32px; color: #1a1a2e;">{t['profile_title']}</h1>
        <p style="color: #666;">{t['profile_desc']}</p>
    </div>
    """, unsafe_allow_html=True)

    courses = COURSES[lang]

    # User info card
    col1, col2 = st.columns([1, 2])
    with col1:
        st.markdown("""
        <div style="text-align: center; padding: 24px;">
            <div style="font-size: 80px;">👤</div>
            <div style="font-size: 20px; font-weight: 600; margin-top: 8px;">Apprenant AI</div>
            <div style="font-size: 14px; color: #888;">apprenant@ai-learning.com</div>
        </div>
        """, unsafe_allow_html=True)

    with col2:
        # Progress overview
        st.subheader(t['progress_overview'])

        total_progress = 0
        completed_courses = 0
        in_progress_courses = 0

        for course in courses:
            prog = st.session_state.get(f"progress_{course['id']}", 0)
            total_progress += prog
            if prog == 100:
                completed_courses += 1
            elif prog > 0:
                in_progress_courses += 1

        avg_progress = total_progress / len(courses) if courses else 0

        col_a, col_b, col_c = st.columns(3)
        with col_a:
            st.metric(t['total_courses'], len(courses))
        with col_b:
            st.metric(t['completed'], completed_courses)
        with col_c:
            st.metric(t['in_progress'], in_progress_courses)

        st.progress(avg_progress / 100)
        st.caption(f"{t['overall_progress']}: {avg_progress:.1f}%")

    st.markdown("<hr>", unsafe_allow_html=True)

    # Course progress details
    st.subheader(t['my_progress'])

    for course in courses:
        prog = st.session_state.get(f"progress_{course['id']}", 0)

        col1, col2, col3 = st.columns([3, 1, 1])
        with col1:
            st.write(f"{course['icon']} **{course['title']}**")
        with col2:
            st.progress(prog / 100)
        with col3:
            st.caption(f"{prog}%")

    st.markdown("<hr>", unsafe_allow_html=True)

    # Settings
    st.subheader("⚙️ " + t['language'])

    lang_options = {"fr": "🇫🇷 Français", "en": "🇬🇧 English", "ar": "🇸🇦 العربية"}
    current_lang = st.session_state.get("language", lang)
    selected_lang = st.selectbox(
        t['change_language'],
        options=list(lang_options.keys()),
        format_func=lambda x: lang_options[x],
        index=list(lang_options.keys()).index(current_lang)
    )

    if selected_lang != current_lang:
        st.session_state.language = selected_lang
        st.rerun()

    # Recent activity
    st.markdown("<hr>", unsafe_allow_html=True)
    st.subheader("📝 " + t['recent_activity'])

    has_activity = any(st.session_state.get(f"progress_{c['id']}", 0) > 0 for c in courses)

    if not has_activity:
        st.info(t['no_activity'])
    else:
        for course in courses:
            prog = st.session_state.get(f"progress_{course['id']}", 0)
            if prog > 0:
                status = t['completed'] if prog == 100 else t['in_progress']
                st.markdown(f"✅ **{course['title']}** - {status} ({prog}%)")
