"""
Custom CSS styles for the AI Learning Application.
"""

def get_custom_css():
    """Returns the custom CSS styles for the application."""
    return """
    <style>
    /* ========== GLOBAL STYLES ========== */
    @import url('https://fonts.googleapis.com/css2?family=Inter:wght@300;400;500;600;700&display=swap');

    .stApp {
        font-family: 'Inter', sans-serif;
    }

    /* ========== SIDEBAR STYLES ========== */
    [data-testid="stSidebar"] {
        background: linear-gradient(180deg, #1a1a2e 0%, #16213e 100%);
        border-right: 1px solid rgba(255,255,255,0.1);
    }

    [data-testid="stSidebar"] .stButton > button {
        width: 100%;
        border-radius: 12px;
        border: none;
        padding: 12px 20px;
        margin: 4px 0;
        font-weight: 500;
        font-size: 14px;
        transition: all 0.3s ease;
        background: transparent;
        color: #b0b0b0;
        text-align: left;
    }

    [data-testid="stSidebar"] .stButton > button:hover {
        background: rgba(255,255,255,0.1);
        color: #ffffff;
        transform: translateX(5px);
    }

    [data-testid="stSidebar"] .stButton > button[kind="primary"] {
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        color: white;
        box-shadow: 0 4px 15px rgba(102, 126, 234, 0.4);
    }

    [data-testid="stSidebar"] .stButton > button[kind="primary"]:hover {
        background: linear-gradient(135deg, #764ba2 0%, #667eea 100%);
        transform: translateX(5px);
    }

    /* ========== CARD STYLES ========== */
    .course-card {
        background: linear-gradient(145deg, #ffffff 0%, #f8f9fa 100%);
        border-radius: 20px;
        padding: 24px;
        margin: 12px 0;
        box-shadow: 0 8px 32px rgba(0,0,0,0.08);
        border: 1px solid rgba(0,0,0,0.05);
        transition: all 0.4s cubic-bezier(0.175, 0.885, 0.32, 1.275);
        position: relative;
        overflow: hidden;
    }

    .course-card:hover {
        transform: translateY(-8px) scale(1.02);
        box-shadow: 0 20px 60px rgba(0,0,0,0.15);
    }

    .course-card::before {
        content: '';
        position: absolute;
        top: 0;
        left: 0;
        width: 100%;
        height: 4px;
        background: var(--card-color, #667eea);
    }

    .course-icon {
        font-size: 48px;
        margin-bottom: 12px;
        display: block;
    }

    .course-title {
        font-size: 20px;
        font-weight: 700;
        color: #1a1a2e;
        margin-bottom: 8px;
        line-height: 1.3;
    }

    .course-description {
        font-size: 14px;
        color: #666;
        line-height: 1.6;
        margin-bottom: 16px;
    }

    .course-meta {
        display: flex;
        gap: 16px;
        margin-bottom: 16px;
        flex-wrap: wrap;
    }

    .course-meta-item {
        display: flex;
        align-items: center;
        gap: 6px;
        font-size: 13px;
        color: #888;
        background: #f0f0f0;
        padding: 4px 12px;
        border-radius: 20px;
    }

    .course-progress {
        margin-top: 12px;
    }

    .progress-label {
        font-size: 12px;
        color: #888;
        margin-bottom: 4px;
        display: flex;
        justify-content: space-between;
    }

    /* ========== BUTTON STYLES ========== */
    .stButton > button {
        border-radius: 12px;
        font-weight: 600;
        padding: 10px 24px;
        transition: all 0.3s ease;
        border: none;
    }

    .stButton > button[kind="primary"] {
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        color: white;
        box-shadow: 0 4px 15px rgba(102, 126, 234, 0.4);
    }

    .stButton > button[kind="primary"]:hover {
        background: linear-gradient(135deg, #764ba2 0%, #667eea 100%);
        box-shadow: 0 6px 20px rgba(102, 126, 234, 0.6);
        transform: translateY(-2px);
    }

    .btn-start {
        background: linear-gradient(135deg, #11998e 0%, #38ef7d 100%) !important;
        color: white !important;
    }

    .btn-continue {
        background: linear-gradient(135deg, #f093fb 0%, #f5576c 100%) !important;
        color: white !important;
    }

    .btn-completed {
        background: linear-gradient(135deg, #4facfe 0%, #00f2fe 100%) !important;
        color: white !important;
    }

    /* ========== ACTIVATION PAGE ========== */
    .activation-container {
        max-width: 500px;
        margin: 80px auto;
        padding: 48px;
        background: linear-gradient(145deg, #ffffff 0%, #f8f9fa 100%);
        border-radius: 24px;
        box-shadow: 0 20px 60px rgba(0,0,0,0.1);
        text-align: center;
    }

    .activation-icon {
        font-size: 64px;
        margin-bottom: 24px;
    }

    .activation-title {
        font-size: 28px;
        font-weight: 700;
        color: #1a1a2e;
        margin-bottom: 12px;
    }

    .activation-subtitle {
        font-size: 16px;
        color: #666;
        margin-bottom: 32px;
    }

    /* ========== CHAT STYLES ========== */
    .chat-message {
        padding: 16px 20px;
        border-radius: 16px;
        margin: 8px 0;
        max-width: 85%;
        word-wrap: break-word;
        animation: fadeIn 0.3s ease;
    }

    @keyframes fadeIn {
        from { opacity: 0; transform: translateY(10px); }
        to { opacity: 1; transform: translateY(0); }
    }

    .chat-user {
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        color: white;
        margin-left: auto;
        border-bottom-right-radius: 4px;
    }

    .chat-assistant {
        background: #f0f0f0;
        color: #333;
        margin-right: auto;
        border-bottom-left-radius: 4px;
    }

    .chat-avatar {
        width: 36px;
        height: 36px;
        border-radius: 50%;
        display: flex;
        align-items: center;
        justify-content: center;
        font-size: 18px;
        margin-right: 8px;
    }

    /* ========== STATS CARDS ========== */
    .stat-card {
        background: linear-gradient(145deg, #ffffff 0%, #f8f9fa 100%);
        border-radius: 16px;
        padding: 24px;
        text-align: center;
        box-shadow: 0 4px 20px rgba(0,0,0,0.06);
        border: 1px solid rgba(0,0,0,0.05);
        transition: transform 0.3s ease;
    }

    .stat-card:hover {
        transform: translateY(-4px);
    }

    .stat-value {
        font-size: 36px;
        font-weight: 700;
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        background-clip: text;
    }

    .stat-label {
        font-size: 14px;
        color: #888;
        margin-top: 8px;
    }

    /* ========== PROGRESS BAR ========== */
    .stProgress > div > div {
        background: linear-gradient(90deg, #667eea 0%, #764ba2 100%);
        border-radius: 10px;
        transition: width 0.5s ease;
    }

    /* ========== HEADER ========== */
    .main-header {
        background: linear-gradient(135deg, #1a1a2e 0%, #16213e 100%);
        color: white;
        padding: 40px;
        border-radius: 20px;
        margin-bottom: 32px;
        text-align: center;
        position: relative;
        overflow: hidden;
    }

    .main-header::before {
        content: '';
        position: absolute;
        top: -50%;
        left: -50%;
        width: 200%;
        height: 200%;
        background: radial-gradient(circle, rgba(102,126,234,0.1) 0%, transparent 70%);
        animation: pulse 4s ease-in-out infinite;
    }

    @keyframes pulse {
        0%, 100% { transform: scale(1); opacity: 0.5; }
        50% { transform: scale(1.1); opacity: 0.8; }
    }

    .main-header h1 {
        font-size: 36px;
        font-weight: 700;
        margin-bottom: 8px;
        position: relative;
        z-index: 1;
    }

    .main-header p {
        font-size: 16px;
        opacity: 0.8;
        position: relative;
        z-index: 1;
    }

    /* ========== FEATURE CARDS ========== */
    .feature-card {
        background: white;
        border-radius: 16px;
        padding: 28px;
        text-align: center;
        box-shadow: 0 4px 20px rgba(0,0,0,0.06);
        border: 1px solid rgba(0,0,0,0.05);
        transition: all 0.3s ease;
        height: 100%;
    }

    .feature-card:hover {
        transform: translateY(-6px);
        box-shadow: 0 12px 40px rgba(0,0,0,0.12);
    }

    .feature-icon {
        font-size: 40px;
        margin-bottom: 16px;
    }

    .feature-title {
        font-size: 18px;
        font-weight: 600;
        color: #1a1a2e;
        margin-bottom: 8px;
    }

    .feature-desc {
        font-size: 14px;
        color: #666;
        line-height: 1.5;
    }

    /* ========== RTL SUPPORT ========== */
    .rtl {
        direction: rtl;
        text-align: right;
    }

    .rtl .course-meta {
        flex-direction: row-reverse;
    }

    .rtl .chat-user {
        margin-left: 0;
        margin-right: auto;
        border-bottom-right-radius: 16px;
        border-bottom-left-radius: 4px;
    }

    .rtl .chat-assistant {
        margin-right: 0;
        margin-left: auto;
        border-bottom-left-radius: 16px;
        border-bottom-right-radius: 4px;
    }

    /* ========== RESPONSIVE ========== */
    @media (max-width: 768px) {
        .activation-container {
            margin: 20px;
            padding: 24px;
        }

        .main-header h1 {
            font-size: 24px;
        }

        .course-card {
            padding: 16px;
        }
    }

    /* ========== SCROLLBAR ========== */
    ::-webkit-scrollbar {
        width: 8px;
    }

    ::-webkit-scrollbar-track {
        background: #f1f1f1;
        border-radius: 4px;
    }

    ::-webkit-scrollbar-thumb {
        background: linear-gradient(180deg, #667eea 0%, #764ba2 100%);
        border-radius: 4px;
    }

    /* ========== INPUT STYLES ========== */
    .stTextInput > div > div > input {
        border-radius: 12px;
        border: 2px solid #e0e0e0;
        padding: 12px 16px;
        font-size: 14px;
        transition: all 0.3s ease;
    }

    .stTextInput > div > div > input:focus {
        border-color: #667eea;
        box-shadow: 0 0 0 3px rgba(102, 126, 234, 0.1);
    }

    /* ========== SELECT BOX ========== */
    .stSelectbox > div > div {
        border-radius: 12px;
    }

    /* ========== EXPANDER ========== */
    .streamlit-expanderHeader {
        border-radius: 12px;
        background: #f8f9fa;
        font-weight: 600;
    }

    /* ========== SUCCESS/ERROR MESSAGES ========== */
    .stSuccess {
        border-radius: 12px;
        background: linear-gradient(135deg, #d4edda 0%, #c3e6cb 100%);
        border: none;
        padding: 16px;
    }

    .stError {
        border-radius: 12px;
        background: linear-gradient(135deg, #f8d7da 0%, #f5c6cb 100%);
        border: none;
        padding: 16px;
    }

    /* ========== DIVIDER ========== */
    hr {
        border: none;
        height: 1px;
        background: linear-gradient(90deg, transparent 0%, #ddd 50%, transparent 100%);
        margin: 32px 0;
    }
    </style>
    """

def get_level_badge(level_key, lang="fr"):
    """Returns HTML for a level badge."""
    colors = {
        "beginner": "#4CAF50",
        "intermediate": "#FF9800",
        "advanced": "#F44336",
        "مبتدئ": "#4CAF50",
        "متوسط": "#FF9800",
        "متقدم": "#F44336"
    }
    color = colors.get(level_key.lower(), "#667eea")
    return f'<span style="background: {color}20; color: {color}; padding: 4px 12px; border-radius: 20px; font-size: 12px; font-weight: 600;">{level_key}</span>'
