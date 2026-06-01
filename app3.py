"""
╔══════════════════════════════════════════════════════════════════════════════╗
║                    🎓 AI LEARNING HUB - Application Complète                  ║
║         Plateforme d'apprentissage de l'IA - Multilingue (FR/EN/AR)          ║
╚══════════════════════════════════════════════════════════════════════════════╝

Architecture: Monofichier Streamlit (compatible Streamlit Cloud)
Auteur: AI Learning Hub
Version: 2.0.0
"""

import streamlit as st
import requests
import json

# ═══════════════════════════════════════════════════════════════════════════════
# CONFIGURATION
# ═══════════════════════════════════════════════════════════════════════════════

ACTIVATION_KEY = "22459129071981"
OLLAMA_MODEL = "llama3.2"
OLLAMA_BASE_URL = "http://localhost:114114"
DEFAULT_LANGUAGE = "fr"

LANGUAGES = {
    "fr": "Français",
    "en": "English",
    "ar": "العربية"
}

# ═══════════════════════════════════════════════════════════════════════════════
# DONNÉES DES COURS (3 langues)
# ═══════════════════════════════════════════════════════════════════════════════

COURSES = {
    "fr": [
        {
            "id": "intro_ml",
            "title": "Introduction au Machine Learning",
            "description": "Apprenez les bases du Machine Learning : algorithmes supervisés et non supervisés, régression, classification et clustering.",
            "level": "Débutant",
            "duration": "8 heures",
            "progress": 0,
            "icon": "🤖",
            "color": "#4CAF50",
            "modules": [
                "Qu'est-ce que le Machine Learning ?",
                "Types d'apprentissage",
                "Régression linéaire",
                "Classification avec KNN",
                "Clustering avec K-Means",
                "Évaluation des modèles"
            ]
        },
        {
            "id": "deep_learning",
            "title": "Deep Learning Fondamental",
            "description": "Plongez dans les réseaux de neurones artificiels, les CNN, les RNN et les architectures modernes comme les Transformers.",
            "level": "Intermédiaire",
            "duration": "12 heures",
            "progress": 0,
            "icon": "🧠",
            "color": "#2196F3",
            "modules": [
                "Perceptron et réseaux de neurones",
                "Fonction d'activation et backpropagation",
                "Réseaux convolutifs (CNN)",
                "Réseaux récurrents (RNN/LSTM)",
                "Introduction aux Transformers",
                "Fine-tuning et transfer learning"
            ]
        },
        {
            "id": "nlp",
            "title": "Traitement du Langage Naturel (NLP)",
            "description": "Maîtrisez les techniques NLP modernes : tokenization, embeddings, modèles de langage et génération de texte.",
            "level": "Avancé",
            "duration": "10 heures",
            "progress": 0,
            "icon": "💬",
            "color": "#9C27B0",
            "modules": [
                "Prétraitement du texte",
                "Word Embeddings (Word2Vec, GloVe)",
                "Modèles de séquence (Seq2Seq)",
                "BERT et modèles pré-entraînés",
                "Fine-tuning pour la classification",
                "Génération de texte avec GPT"
            ]
        },
        {
            "id": "computer_vision",
            "title": "Vision par Ordinateur",
            "description": "Apprenez à traiter et analyser des images avec l'IA : détection d'objets, segmentation et génération d'images.",
            "level": "Intermédiaire",
            "duration": "10 heures",
            "progress": 0,
            "icon": "👁️",
            "color": "#FF9800",
            "modules": [
                "Traitement d'image avec OpenCV",
                "Détection de contours et features",
                "Classification d'images avec CNN",
                "Détection d'objets (YOLO, SSD)",
                "Segmentation sémantique",
                "Génération d'images (GANs)"
            ]
        },
        {
            "id": "reinforcement",
            "title": "Apprentissage par Renforcement",
            "description": "Découvrez comment les agents IA apprennent à prendre des décisions optimales dans des environnements complexes.",
            "level": "Avancé",
            "duration": "14 heures",
            "progress": 0,
            "icon": "🎮",
            "color": "#E91E63",
            "modules": [
                "Concepts fondamentaux (MDP)",
                "Q-Learning et SARSA",
                "Deep Q-Networks (DQN)",
                "Policy Gradient Methods",
                "Actor-Critic (A2C, PPO)",
                "Applications réelles (robotique, jeux)"
            ]
        },
        {
            "id": "mlops",
            "title": "MLOps et Déploiement",
            "description": "Apprenez à industrialiser vos modèles ML : CI/CD, monitoring, conteneurisation et mise en production.",
            "level": "Intermédiaire",
            "duration": "8 heures",
            "progress": 0,
            "icon": "🚀",
            "color": "#00BCD4",
            "modules": [
                "Pipeline ML avec scikit-learn",
                "Versioning des modèles (MLflow)",
                "Conteneurisation avec Docker",
                "Déploiement avec FastAPI",
                "Monitoring et drift detection",
                "CI/CD pour le ML"
            ]
        }
    ],
    "en": [
        {
            "id": "intro_ml",
            "title": "Introduction to Machine Learning",
            "description": "Learn the basics of Machine Learning: supervised and unsupervised algorithms, regression, classification, and clustering.",
            "level": "Beginner",
            "duration": "8 hours",
            "progress": 0,
            "icon": "🤖",
            "color": "#4CAF50",
            "modules": [
                "What is Machine Learning?",
                "Types of learning",
                "Linear regression",
                "Classification with KNN",
                "Clustering with K-Means",
                "Model evaluation"
            ]
        },
        {
            "id": "deep_learning",
            "title": "Fundamental Deep Learning",
            "description": "Dive into artificial neural networks, CNNs, RNNs, and modern architectures like Transformers.",
            "level": "Intermediate",
            "duration": "12 hours",
            "progress": 0,
            "icon": "🧠",
            "color": "#2196F3",
            "modules": [
                "Perceptron and neural networks",
                "Activation function and backpropagation",
                "Convolutional networks (CNN)",
                "Recurrent networks (RNN/LSTM)",
                "Introduction to Transformers",
                "Fine-tuning and transfer learning"
            ]
        },
        {
            "id": "nlp",
            "title": "Natural Language Processing (NLP)",
            "description": "Master modern NLP techniques: tokenization, embeddings, language models, and text generation.",
            "level": "Advanced",
            "duration": "10 hours",
            "progress": 0,
            "icon": "💬",
            "color": "#9C27B0",
            "modules": [
                "Text preprocessing",
                "Word Embeddings (Word2Vec, GloVe)",
                "Sequence models (Seq2Seq)",
                "BERT and pre-trained models",
                "Fine-tuning for classification",
                "Text generation with GPT"
            ]
        },
        {
            "id": "computer_vision",
            "title": "Computer Vision",
            "description": "Learn to process and analyze images with AI: object detection, segmentation, and image generation.",
            "level": "Intermediate",
            "duration": "10 hours",
            "progress": 0,
            "icon": "👁️",
            "color": "#FF9800",
            "modules": [
                "Image processing with OpenCV",
                "Edge detection and features",
                "Image classification with CNN",
                "Object detection (YOLO, SSD)",
                "Semantic segmentation",
                "Image generation (GANs)"
            ]
        },
        {
            "id": "reinforcement",
            "title": "Reinforcement Learning",
            "description": "Discover how AI agents learn to make optimal decisions in complex environments.",
            "level": "Advanced",
            "duration": "14 hours",
            "progress": 0,
            "icon": "🎮",
            "color": "#E91E63",
            "modules": [
                "Fundamental concepts (MDP)",
                "Q-Learning and SARSA",
                "Deep Q-Networks (DQN)",
                "Policy Gradient Methods",
                "Actor-Critic (A2C, PPO)",
                "Real-world applications (robotics, games)"
            ]
        },
        {
            "id": "mlops",
            "title": "MLOps and Deployment",
            "description": "Learn to industrialize your ML models: CI/CD, monitoring, containerization, and production deployment.",
            "level": "Intermediate",
            "duration": "8 hours",
            "progress": 0,
            "icon": "🚀",
            "color": "#00BCD4",
            "modules": [
                "ML pipeline with scikit-learn",
                "Model versioning (MLflow)",
                "Containerization with Docker",
                "Deployment with FastAPI",
                "Monitoring and drift detection",
                "CI/CD for ML"
            ]
        }
    ],
    "ar": [
        {
            "id": "intro_ml",
            "title": "مقدمة في التعلم الآلي",
            "description": "تعلم أساسيات التعلم الآلي: الخوارزميات الخاضعة للإشراف وغير الخاضعة للإشراف، الانحدار، التصنيف، والتجميع.",
            "level": "مبتدئ",
            "duration": "8 ساعات",
            "progress": 0,
            "icon": "🤖",
            "color": "#4CAF50",
            "modules": [
                "ما هو التعلم الآلي؟",
                "أنواع التعلم",
                "الانحدار الخطي",
                "التصنيف باستخدام KNN",
                "التجميع باستخدام K-Means",
                "تقييم النماذج"
            ]
        },
        {
            "id": "deep_learning",
            "title": "التعلم العميق الأساسي",
            "description": "تعمق في الشبكات العصبية الاصطناعية، CNN، RNN، والهياكل الحديثة مثل Transformers.",
            "level": "متوسط",
            "duration": "12 ساعة",
            "progress": 0,
            "icon": "🧠",
            "color": "#2196F3",
            "modules": [
                "الشبكات العصبية والبيرسبترون",
                "دالة التنشيط والانتشار العكسي",
                "الشبكات التلافيفية (CNN)",
                "الشبكات المتكررة (RNN/LSTM)",
                "مقدمة في Transformers",
                "الضبط الدقيق ونقل التعلم"
            ]
        },
        {
            "id": "nlp",
            "title": "معالجة اللغات الطبيعية (NLP)",
            "description": "أتقن تقنيات NLP الحديثة: الترميز، التضمينات، نماذج اللغة، وتوليد النصوص.",
            "level": "متقدم",
            "duration": "10 ساعات",
            "progress": 0,
            "icon": "💬",
            "color": "#9C27B0",
            "modules": [
                "معالجة النصوص المسبقة",
                "تضمينات الكلمات (Word2Vec, GloVe)",
                "نماذج التسلسل (Seq2Seq)",
                "BERT والنماذج المدربة مسبقاً",
                "الضبط الدقيق للتصنيف",
                "توليد النصوص باستخدام GPT"
            ]
        },
        {
            "id": "computer_vision",
            "title": "رؤية الحاسوب",
            "description": "تعلم معالجة وتحليل الصور بالذكاء الاصطناعي: كشف الأجسام، التجزئة، وتوليد الصور.",
            "level": "متوسط",
            "duration": "10 ساعات",
            "progress": 0,
            "icon": "👁️",
            "color": "#FF9800",
            "modules": [
                "معالجة الصور باستخدام OpenCV",
                "كشف الحواف والميزات",
                "تصنيف الصور باستخدام CNN",
                "كشف الأجسام (YOLO, SSD)",
                "التجزئة الدلالية",
                "توليد الصور (GANs)"
            ]
        },
        {
            "id": "reinforcement",
            "title": "التعلم المعزز",
            "description": "اكتشف كيف تتعلم وكلاء الذكاء الاصطناعي لاتخاذ قرارات مثلى في بيئات معقدة.",
            "level": "متقدم",
            "duration": "14 ساعة",
            "progress": 0,
            "icon": "🎮",
            "color": "#E91E63",
            "modules": [
                "المفاهيم الأساسية (MDP)",
                "Q-Learning و SARSA",
                "شبكات Q العميقة (DQN)",
                "طرق Policy Gradient",
                "Actor-Critic (A2C, PPO)",
                "تطبيقات واقعية (الروبوتات، الألعاب)"
            ]
        },
        {
            "id": "mlops",
            "title": "MLOps والنشر",
            "description": "تعلم صناعية نماذج ML: CI/CD، المراقبة، الحاويات، والنشر في الإنتاج.",
            "level": "متوسط",
            "duration": "8 ساعات",
            "progress": 0,
            "icon": "🚀",
            "color": "#00BCD4",
            "modules": [
                "خط أنابيب ML مع scikit-learn",
                "إصدار النماذج (MLflow)",
                "الحاويات مع Docker",
                "النشر مع FastAPI",
                "المراقبة وكشف الانحراف",
                "CI/CD للتعلم الآلي"
            ]
        }
    ]
}

# ═══════════════════════════════════════════════════════════════════════════════
# TRADUCTIONS
# ═══════════════════════════════════════════════════════════════════════════════

TRANSLATIONS = {
    "fr": {
        "app_title": "🎓 AI Learning Hub",
        "welcome": "Bienvenue sur AI Learning Hub",
        "subtitle": "Votre plateforme d'apprentissage de l'Intelligence Artificielle",
        "activation": "Activation",
        "enter_key": "Entrez votre clé d'activation",
        "activate": "Activer",
        "invalid_key": "❌ Clé invalide. Veuillez réessayer.",
        "access_granted": "✅ Accès autorisé ! Bienvenue.",
        "home": "🏠 Accueil",
        "courses": "📚 Cours",
        "mentor": "🤖 Mentor IA",
        "profile": "👤 Profil",
        "catalogue": "📖 Catalogue de Cours",
        "my_progress": "📊 Ma Progression",
        "total_courses": "Cours totaux",
        "completed": "Complétés",
        "in_progress": "En cours",
        "hours": "heures",
        "level": "Niveau",
        "duration": "Durée",
        "modules": "Modules",
        "start_course": "Commencer le cours",
        "continue": "Continuer",
        "completed_btn": "Terminé",
        "mentor_title": "🤖 Votre Mentor IA",
        "mentor_desc": "Posez vos questions sur l'IA, les cours, ou tout sujet technique. Le mentor conserve le contexte de votre conversation.",
        "ask_question": "Posez votre question...",
        "send": "Envoyer",
        "thinking": "🤔 Le mentor réfléchit...",
        "no_ollama": "⚠️ Ollama n'est pas disponible. Vérifiez que le service est lancé localement.",
        "profile_title": "👤 Mon Profil",
        "profile_desc": "Gérez vos préférences et suivez vos progrès.",
        "language": "Langue",
        "change_language": "Changer la langue",
        "dark_mode": "Mode sombre",
        "light_mode": "Mode clair",
        "progress_overview": "Vue d'ensemble de la progression",
        "overall_progress": "Progression globale",
        "recent_activity": "Activité récente",
        "no_activity": "Aucune activité récente",
        "logout": "Déconnexion",
        "footer": "© 2026 AI Learning Hub",
        "beginner": "Débutant",
        "intermediate": "Intermédiaire",
        "advanced": "Avancé",
        "select_course_chat": "Sélectionnez un cours pour le contexte de la discussion",
        "no_course": "Discussion générale",
        "chat_placeholder": "Comment fonctionne un réseau de neurones ?",
        "welcome_home": "Bienvenue sur votre plateforme d'apprentissage !",
        "home_desc": "Explorez nos cours interactifs sur l'Intelligence Artificielle, posez vos questions à notre Mentor IA, et suivez votre progression en temps réel.",
        "feature_courses": "📚 Cours Complets",
        "feature_courses_desc": "6 modules couvrant ML, Deep Learning, NLP, Vision, RL et MLOps",
        "feature_mentor": "🤖 Mentor IA Local",
        "feature_mentor_desc": "Assistant intelligent propulsé par un LLM local via Ollama",
        "feature_progress": "📊 Suivi de Progression",
        "feature_progress_desc": "Barres de progression et statistiques détaillées",
        "feature_multilingual": "🌍 Multilingue",
        "feature_multilingual_desc": "Interface disponible en Français, Anglais et Arabe",
        "get_started": "Commencer l'apprentissage",
        "stats_courses": "Cours disponibles",
        "stats_hours": "Heures de contenu",
        "stats_modules": "Modules à explorer",
        "stats_level": "Niveaux de difficulté",
        "clear_chat": "Effacer la conversation",
        "offline_response": "🤖 **Mentor IA** (Mode hors-ligne)\n\nJe suis désolé, mais le service Ollama n'est pas disponible actuellement. Pour utiliser le Mentor IA, veuillez :\n\n1. Installer Ollama : `curl -fsSL https://ollama.com/install.sh | sh`\n2. Télécharger un modèle : `ollama pull llama3.2`\n3. Démarrer le service : `ollama serve`",
    },
    "en": {
        "app_title": "🎓 AI Learning Hub",
        "welcome": "Welcome to AI Learning Hub",
        "subtitle": "Your Artificial Intelligence Learning Platform",
        "activation": "Activation",
        "enter_key": "Enter your activation key",
        "activate": "Activate",
        "invalid_key": "❌ Invalid key. Please try again.",
        "access_granted": "✅ Access granted! Welcome.",
        "home": "🏠 Home",
        "courses": "📚 Courses",
        "mentor": "🤖 AI Mentor",
        "profile": "👤 Profile",
        "catalogue": "📖 Course Catalog",
        "my_progress": "📊 My Progress",
        "total_courses": "Total courses",
        "completed": "Completed",
        "in_progress": "In progress",
        "hours": "hours",
        "level": "Level",
        "duration": "Duration",
        "modules": "Modules",
        "start_course": "Start course",
        "continue": "Continue",
        "completed_btn": "Completed",
        "mentor_title": "🤖 Your AI Mentor",
        "mentor_desc": "Ask your questions about AI, courses, or any technical topic. The mentor keeps the context of your conversation.",
        "ask_question": "Ask your question...",
        "send": "Send",
        "thinking": "🤔 The mentor is thinking...",
        "no_ollama": "⚠️ Ollama is not available. Please check that the service is running locally.",
        "profile_title": "👤 My Profile",
        "profile_desc": "Manage your preferences and track your progress.",
        "language": "Language",
        "change_language": "Change language",
        "dark_mode": "Dark mode",
        "light_mode": "Light mode",
        "progress_overview": "Progress overview",
        "overall_progress": "Overall progress",
        "recent_activity": "Recent activity",
        "no_activity": "No recent activity",
        "logout": "Logout",
        "footer": "© 2026 AI Learning Hub",
        "beginner": "Beginner",
        "intermediate": "Intermediate",
        "advanced": "Advanced",
        "select_course_chat": "Select a course for discussion context",
        "no_course": "General discussion",
        "chat_placeholder": "How does a neural network work?",
        "welcome_home": "Welcome to your learning platform!",
        "home_desc": "Explore our interactive AI courses, ask questions to our AI Mentor, and track your progress in real-time.",
        "feature_courses": "📚 Complete Courses",
        "feature_courses_desc": "6 modules covering ML, Deep Learning, NLP, Vision, RL and MLOps",
        "feature_mentor": "🤖 Local AI Mentor",
        "feature_mentor_desc": "Intelligent assistant powered by a local LLM via Ollama",
        "feature_progress": "📊 Progress Tracking",
        "feature_progress_desc": "Progress bars and detailed statistics",
        "feature_multilingual": "🌍 Multilingual",
        "feature_multilingual_desc": "Interface available in French, English and Arabic",
        "get_started": "Start learning",
        "stats_courses": "Available courses",
        "stats_hours": "Hours of content",
        "stats_modules": "Modules to explore",
        "stats_level": "Difficulty levels",
        "clear_chat": "Clear conversation",
        "offline_response": "🤖 **AI Mentor** (Offline Mode)\n\nI'm sorry, but the Ollama service is currently unavailable. To use the AI Mentor, please:\n\n1. Install Ollama: `curl -fsSL https://ollama.com/install.sh | sh`\n2. Download a model: `ollama pull llama3.2`\n3. Start the service: `ollama serve`",
    },
    "ar": {
        "app_title": "🎓 مركز تعلم الذكاء الاصطناعي",
        "welcome": "مرحباً بك في مركز تعلم الذكاء الاصطناعي",
        "subtitle": "منصتك لتعلم الذكاء الاصطناعي",
        "activation": "التفعيل",
        "enter_key": "أدخل مفتاح التفعيل",
        "activate": "تفعيل",
        "invalid_key": "❌ مفتاح غير صالح. يرجى المحاولة مرة أخرى.",
        "access_granted": "✅ تم منح الوصول! أهلاً بك.",
        "home": "🏠 الرئيسية",
        "courses": "📚 الدورات",
        "mentor": "🤖 المرشد الذكي",
        "profile": "👤 الملف الشخصي",
        "catalogue": "📖 دليل الدورات",
        "my_progress": "📊 تقدمي",
        "total_courses": "إجمالي الدورات",
        "completed": "مكتمل",
        "in_progress": "قيد التقدم",
        "hours": "ساعات",
        "level": "المستوى",
        "duration": "المدة",
        "modules": "الوحدات",
        "start_course": "ابدأ الدورة",
        "continue": "استمر",
        "completed_btn": "مكتمل",
        "mentor_title": "🤖 مرشدك الذكي",
        "mentor_desc": "اطرح أسئلتك حول الذكاء الاصطناعي، الدورات، أو أي موضوع تقني. يحتفظ المرشد بسياق محادثتك.",
        "ask_question": "اطرح سؤالك...",
        "send": "إرسال",
        "thinking": "🤔 المرشد يفكر...",
        "no_ollama": "⚠️ Ollama غير متوفر. يرجى التحقق من تشغيل الخدمة محلياً.",
        "profile_title": "👤 ملفي الشخصي",
        "profile_desc": "إدارة تفضيلاتك ومتابعة تقدمك.",
        "language": "اللغة",
        "change_language": "تغيير اللغة",
        "dark_mode": "الوضع الداكن",
        "light_mode": "الوضع الفاتح",
        "progress_overview": "نظرة عامة على التقدم",
        "overall_progress": "التقدم العام",
        "recent_activity": "النشاط الأخير",
        "no_activity": "لا يوجد نشاط حديث",
        "logout": "تسجيل الخروج",
        "footer": "© 2026 مركز تعلم الذكاء الاصطناعي",
        "beginner": "مبتدئ",
        "intermediate": "متوسط",
        "advanced": "متقدم",
        "select_course_chat": "اختر دورة لسياق المناقشة",
        "no_course": "مناقشة عامة",
        "chat_placeholder": "كيف يعمل الشبكة العصبية؟",
        "welcome_home": "مرحباً بك في منصتك التعليمية!",
        "home_desc": "استكشف دورات الذكاء الاصطناعي التفاعلية، اطرح أسئلتك على المرشد الذكي، وتابع تقدمك في الوقت الفعلي.",
        "feature_courses": "📚 دورات كاملة",
        "feature_courses_desc": "6 وحدات تغطي ML، التعلم العميق، NLP، الرؤية، RL و MLOps",
        "feature_mentor": "🤖 مرشد ذكي محلي",
        "feature_mentor_desc": "مساعد ذكي مدعوم بنموذج لغوي محلي عبر Ollama",
        "feature_progress": "📊 تتبع التقدم",
        "feature_progress_desc": "أشرطة التقدم وإحصائيات مفصلة",
        "feature_multilingual": "🌍 متعدد اللغات",
        "feature_multilingual_desc": "واجهة متاحة بالفرنسية والإنجليزية والعربية",
        "get_started": "ابدأ التعلم",
        "stats_courses": "الدورات المتاحة",
        "stats_hours": "ساعات المحتوى",
        "stats_modules": "وحدات للاستكشاف",
        "stats_level": "مستويات الصعوبة",
        "clear_chat": "مسح المحادثة",
        "offline_response": "🤖 **المرشد الذكي** (وضع عدم الاتصال)\n\nعذراً، خدمة Ollama غير متوفرة حالياً. لاستخدام المرشد الذكي، يرجى:\n\n1. تثبيت Ollama: `curl -fsSL https://ollama.com/install.sh | sh`\n2. تحميل نموذج: `ollama pull llama3.2`\n3. تشغيل الخدمة: `ollama serve`",
    }
}

# ═══════════════════════════════════════════════════════════════════════════════
# CSS PERSONNALISÉ
# ═══════════════════════════════════════════════════════════════════════════════

CUSTOM_CSS = """
<style>
@import url('https://fonts.googleapis.com/css2?family=Inter:wght@300;400;500;600;700&display=swap');

.stApp { font-family: 'Inter', sans-serif; }

/* ===== SIDEBAR ===== */
[data-testid="stSidebar"] {
    background: linear-gradient(180deg, #1a1a2e 0%, #16213e 100%);
    border-right: 1px solid rgba(255,255,255,0.1);
}
[data-testid="stSidebar"] .stButton > button {
    width: 100%; border-radius: 12px; border: none;
    padding: 12px 20px; margin: 4px 0; font-weight: 500;
    font-size: 14px; transition: all 0.3s ease;
    background: transparent; color: #b0b0b0; text-align: left;
}
[data-testid="stSidebar"] .stButton > button:hover {
    background: rgba(255,255,255,0.1); color: #fff; transform: translateX(5px);
}
[data-testid="stSidebar"] .stButton > button[kind="primary"] {
    background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
    color: white; box-shadow: 0 4px 15px rgba(102,126,234,0.4);
}

/* ===== COURSE CARDS ===== */
.course-card {
    background: linear-gradient(145deg, #ffffff 0%, #f8f9fa 100%);
    border-radius: 20px; padding: 24px; margin: 12px 0;
    box-shadow: 0 8px 32px rgba(0,0,0,0.08);
    border: 1px solid rgba(0,0,0,0.05);
    transition: all 0.4s cubic-bezier(0.175, 0.885, 0.32, 1.275);
    position: relative; overflow: hidden;
}
.course-card:hover {
    transform: translateY(-8px) scale(1.02);
    box-shadow: 0 20px 60px rgba(0,0,0,0.15);
}
.course-card::before {
    content: ''; position: absolute; top: 0; left: 0;
    width: 100%; height: 4px;
    background: var(--card-color, #667eea);
}
.course-icon { font-size: 48px; margin-bottom: 12px; display: block; }
.course-title { font-size: 20px; font-weight: 700; color: #1a1a2e; margin-bottom: 8px; }
.course-description { font-size: 14px; color: #666; line-height: 1.6; margin-bottom: 16px; }
.course-meta { display: flex; gap: 16px; margin-bottom: 16px; flex-wrap: wrap; }
.course-meta-item {
    display: flex; align-items: center; gap: 6px; font-size: 13px;
    color: #888; background: #f0f0f0; padding: 4px 12px; border-radius: 20px;
}

/* ===== BUTTONS ===== */
.stButton > button {
    border-radius: 12px; font-weight: 600; padding: 10px 24px;
    transition: all 0.3s ease; border: none;
}
.stButton > button[kind="primary"] {
    background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
    color: white; box-shadow: 0 4px 15px rgba(102,126,234,0.4);
}
.stButton > button[kind="primary"]:hover {
    background: linear-gradient(135deg, #764ba2 0%, #667eea 100%);
    box-shadow: 0 6px 20px rgba(102,126,234,0.6);
    transform: translateY(-2px);
}

/* ===== ACTIVATION ===== */
.activation-container {
    max-width: 500px; margin: 80px auto; padding: 48px;
    background: linear-gradient(145deg, #ffffff 0%, #f8f9fa 100%);
    border-radius: 24px; box-shadow: 0 20px 60px rgba(0,0,0,0.1);
    text-align: center;
}
.activation-icon { font-size: 64px; margin-bottom: 24px; }
.activation-title { font-size: 28px; font-weight: 700; color: #1a1a2e; margin-bottom: 12px; }
.activation-subtitle { font-size: 16px; color: #666; margin-bottom: 32px; }

/* ===== CHAT ===== */
.chat-message {
    padding: 16px 20px; border-radius: 16px; margin: 8px 0;
    max-width: 85%; word-wrap: break-word;
    animation: fadeIn 0.3s ease;
}
@keyframes fadeIn {
    from { opacity: 0; transform: translateY(10px); }
    to { opacity: 1; transform: translateY(0); }
}
.chat-user {
    background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
    color: white; margin-left: auto; border-bottom-right-radius: 4px;
}
.chat-assistant {
    background: #f0f0f0; color: #333; margin-right: auto;
    border-bottom-left-radius: 4px;
}
.chat-avatar {
    width: 36px; height: 36px; border-radius: 50%;
    display: flex; align-items: center; justify-content: center;
    font-size: 18px; margin-right: 8px;
}

/* ===== STATS ===== */
.stat-card {
    background: linear-gradient(145deg, #ffffff 0%, #f8f9fa 100%);
    border-radius: 16px; padding: 24px; text-align: center;
    box-shadow: 0 4px 20px rgba(0,0,0,0.06);
    border: 1px solid rgba(0,0,0,0.05);
    transition: transform 0.3s ease;
}
.stat-card:hover { transform: translateY(-4px); }
.stat-value {
    font-size: 36px; font-weight: 700;
    background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
    -webkit-background-clip: text; -webkit-text-fill-color: transparent;
}
.stat-label { font-size: 14px; color: #888; margin-top: 8px; }

/* ===== PROGRESS ===== */
.stProgress > div > div {
    background: linear-gradient(90deg, #667eea 0%, #764ba2 100%);
    border-radius: 10px;
}

/* ===== HEADER ===== */
.main-header {
    background: linear-gradient(135deg, #1a1a2e 0%, #16213e 100%);
    color: white; padding: 40px; border-radius: 20px;
    margin-bottom: 32px; text-align: center;
    position: relative; overflow: hidden;
}
.main-header h1 { font-size: 36px; font-weight: 700; margin-bottom: 8px; position: relative; z-index: 1; }
.main-header p { font-size: 16px; opacity: 0.8; position: relative; z-index: 1; }

/* ===== FEATURES ===== */
.feature-card {
    background: white; border-radius: 16px; padding: 28px;
    text-align: center; box-shadow: 0 4px 20px rgba(0,0,0,0.06);
    border: 1px solid rgba(0,0,0,0.05); transition: all 0.3s ease; height: 100%;
}
.feature-card:hover { transform: translateY(-6px); box-shadow: 0 12px 40px rgba(0,0,0,0.12); }
.feature-icon { font-size: 40px; margin-bottom: 16px; }
.feature-title { font-size: 18px; font-weight: 600; color: #1a1a2e; margin-bottom: 8px; }
.feature-desc { font-size: 14px; color: #666; line-height: 1.5; }

/* ===== RTL ===== */
.rtl { direction: rtl; text-align: right; }
.rtl .course-meta { flex-direction: row-reverse; }
.rtl .chat-user { margin-left: 0; margin-right: auto; border-radius: 16px 16px 4px 16px; }
.rtl .chat-assistant { margin-right: 0; margin-left: auto; border-radius: 16px 16px 16px 4px; }

/* ===== RESPONSIVE ===== */
@media (max-width: 768px) {
    .activation-container { margin: 20px; padding: 24px; }
    .main-header h1 { font-size: 24px; }
    .course-card { padding: 16px; }
}

/* ===== SCROLLBAR ===== */
::-webkit-scrollbar { width: 8px; }
::-webkit-scrollbar-track { background: #f1f1f1; border-radius: 4px; }
::-webkit-scrollbar-thumb { background: linear-gradient(180deg, #667eea 0%, #764ba2 100%); border-radius: 4px; }

/* ===== INPUTS ===== */
.stTextInput > div > div > input {
    border-radius: 12px; border: 2px solid #e0e0e0;
    padding: 12px 16px; font-size: 14px; transition: all 0.3s ease;
}
.stTextInput > div > div > input:focus {
    border-color: #667eea; box-shadow: 0 0 0 3px rgba(102,126,234,0.1);
}

/* ===== MESSAGES ===== */
.stSuccess { border-radius: 12px; background: linear-gradient(135deg, #d4edda 0%, #c3e6cb 100%); border: none; padding: 16px; }
.stError { border-radius: 12px; background: linear-gradient(135deg, #f8d7da 0%, #f5c6cb 100%); border: none; padding: 16px; }

/* ===== DIVIDER ===== */
hr { border: none; height: 1px; background: linear-gradient(90deg, transparent 0%, #ddd 50%, transparent 100%); margin: 32px 0; }
</style>
"""

# ═══════════════════════════════════════════════════════════════════════════════
# CLIENT OLLAMA
# ═══════════════════════════════════════════════════════════════════════════════

class OllamaClient:
    """Client pour interagir avec Ollama LLM local."""

    def __init__(self, model=None, base_url=None):
        self.model = model or OLLAMA_MODEL
        self.base_url = base_url or OLLAMA_BASE_URL
        self.is_available = self._check_availability()

    def _check_availability(self):
        try:
            response = requests.get(f"{self.base_url}/api/tags", timeout=3)
            return response.status_code == 200
        except:
            return False

    def chat(self, messages, system_prompt=None, temperature=0.7, stream=False):
        if not self.is_available:
            return None
        payload = {
            "model": self.model,
            "messages": messages,
            "options": {"temperature": temperature},
            "stream": stream
        }
        if system_prompt:
            payload["system"] = system_prompt
        try:
            response = requests.post(
                f"{self.base_url}/api/chat",
                json=payload, timeout=120
            )
            return response.json().get("message", {}).get("content", "")
        except Exception as e:
            return f"Error: {str(e)}"


def get_system_prompt(lang="fr"):
    prompts = {
        "fr": """Tu es un mentor IA expert en intelligence artificielle. Tu aides les étudiants à apprendre le Machine Learning, le Deep Learning, le NLP, la vision par ordinateur et l'apprentissage par renforcement. Sois pédagogique, encourageant et clair. Utilise des exemples concrets quand c'est utile. Réponds toujours en français.""",
        "en": """You are an expert AI tutor specializing in Artificial Intelligence. You help students learn Machine Learning, Deep Learning, NLP, Computer Vision, and Reinforcement Learning. Be pedagogical, encouraging, and clear. Always respond in English.""",
        "ar": """أنت مرشد ذكي متخصص في الذكاء الاصطناعي. تساعد الطلاب في تعلم التعلم الآلي، التعلم العميق، معالجة اللغات الطبيعية، رؤية الحاسوب، والتعلم المعزز. كن تعليمياً، مشجعاً، وواضحاً. رد دائماً باللغة العربية."""
    }
    return prompts.get(lang, prompts["en"])


# ═══════════════════════════════════════════════════════════════════════════════
# FONCTIONS UI - PAGES
# ═══════════════════════════════════════════════════════════════════════════════

def render_activation_page(lang="fr"):
    """Page d'activation avec clé sécurisée."""
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
        key_input = st.text_input("", type="password", placeholder="••••••••••••••", label_visibility="collapsed")
        if st.button(t['activate'], type="primary", use_container_width=True):
            if key_input == ACTIVATION_KEY:
                st.session_state.activated = True
                st.session_state.access_granted = True
                st.success(t['access_granted'])
                st.rerun()
            else:
                st.error(t['invalid_key'])


def render_sidebar(t, lang="fr"):
    """Barre latérale de navigation."""
    with st.sidebar:
        st.markdown(f"""
        <div style="text-align: center; padding: 20px 0;">
            <div style="font-size: 48px; margin-bottom: 8px;">🎓</div>
            <div style="font-size: 20px; font-weight: 700; color: white;">AI Learning Hub</div>
            <div style="font-size: 12px; color: #888; margin-top: 4px;">{t['subtitle']}</div>
        </div>
        <hr style="border-color: rgba(255,255,255,0.1); margin: 16px 0;">
        """, unsafe_allow_html=True)

        pages = [("home", t['home']), ("courses", t['courses']), ("mentor", t['mentor']), ("profile", t['profile'])]
        current_page = st.session_state.get("current_page", "home")

        for page_key, page_label in pages:
            btn_type = "primary" if current_page == page_key else "secondary"
            if st.button(page_label, key=f"nav_{page_key}", type=btn_type, use_container_width=True):
                st.session_state.current_page = page_key
                st.rerun()

        st.markdown("<hr style='border-color: rgba(255,255,255,0.1); margin: 16px 0;'>", unsafe_allow_html=True)

        st.markdown(f"<div style='color: #888; font-size: 12px; margin-bottom: 8px;'>{t['language']}</div>", unsafe_allow_html=True)
        lang_options = {"fr": "🇫🇷 Français", "en": "🇬🇧 English", "ar": "🇸🇦 العربية"}
        current_lang = st.session_state.get("language", lang)
        selected_lang = st.selectbox("", options=list(lang_options.keys()),
                                     format_func=lambda x: lang_options[x],
                                     index=list(lang_options.keys()).index(current_lang),
                                     label_visibility="collapsed")
        if selected_lang != current_lang:
            st.session_state.language = selected_lang
            st.rerun()

        st.markdown("<div style='margin-top: auto; padding-top: 20px;'>", unsafe_allow_html=True)
        if st.button(t['logout'], key="logout_btn", use_container_width=True):
            st.session_state.activated = False
            st.session_state.access_granted = False
            st.session_state.current_page = "home"
            st.session_state.chat_history = []
            st.rerun()

        st.markdown(f"""
        <div style="text-align: center; padding: 16px 0; color: #666; font-size: 11px;">
            {t['footer']}
        </div>
        """, unsafe_allow_html=True)


def render_header(t, lang="fr"):
    """En-tête principal."""
    st.markdown(f"""
    <div class="main-header">
        <h1>{t['welcome']}</h1>
        <p>{t['subtitle']}</p>
    </div>
    """, unsafe_allow_html=True)


def render_course_card(course, t, lang="fr"):
    """Carte de cours individuelle."""
    progress = st.session_state.get(f"progress_{course['id']}", 0)

    if progress == 0:
        btn_text, btn_emoji = t['start_course'], "🚀"
    elif progress < 100:
        btn_text, btn_emoji = t['continue'], "▶️"
    else:
        btn_text, btn_emoji = t['completed_btn'], "✅"

    st.markdown(f"""
    <div class="course-card" style="--card-color: {course['color']};">
        <span class="course-icon">{course['icon']}</span>
        <div class="course-title">{course['title']}</div>
        <div class="course-description">{course['description']}</div>
        <div class="course-meta">
            <div class="course-meta-item"><span>📊</span> {course['level']}</div>
            <div class="course-meta-item"><span>⏱️</span> {course['duration']}</div>
            <div class="course-meta-item"><span>📋</span> {len(course['modules'])} {t['modules']}</div>
        </div>
        <div style="font-size: 12px; color: #888; margin-bottom: 4px; display: flex; justify-content: space-between;">
            <span>{t['overall_progress']}</span><span>{progress}%</span>
        </div>
    </div>
    """, unsafe_allow_html=True)

    st.progress(progress / 100)

    col1, col2 = st.columns([3, 1])
    with col2:
        if st.button(f"{btn_emoji} {btn_text}", key=f"btn_{course['id']}_{lang}", use_container_width=True):
            if progress < 100:
                st.session_state[f"progress_{course['id']}"] = min(progress + 20, 100)
                st.rerun()

    with st.expander(f"📋 {t['modules']}"):
        for i, module in enumerate(course['modules']):
            module_completed = progress >= ((i + 1) / len(course['modules'])) * 100
            icon = "✅" if module_completed else "⭕"
            st.markdown(f"{icon} {module}")


def render_stats_section(t, lang="fr"):
    """Cartes de statistiques."""
    courses = COURSES[lang]
    total_hours = sum(int(c['duration'].split()[0]) for c in courses)
    total_modules = sum(len(c['modules']) for c in courses)

    cols = st.columns(4)
    stats = [(len(courses), t['stats_courses']), (total_hours, t['stats_hours']),
             (total_modules, t['stats_modules']), (3, t['stats_level'])]

    for col, (value, label) in zip(cols, stats):
        with col:
            st.markdown(f"""
            <div class="stat-card">
                <div class="stat-value">{value}</div>
                <div class="stat-label">{label}</div>
            </div>
            """, unsafe_allow_html=True)


def render_feature_cards(t, lang="fr"):
    """Cartes de fonctionnalités."""
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


# ═══════════════════════════════════════════════════════════════════════════════
# PAGES PRINCIPALES
# ═══════════════════════════════════════════════════════════════════════════════

def render_home_page(t, lang="fr"):
    """Page d'accueil."""
    render_header(t, lang)
    render_stats_section(t, lang)
    st.markdown("<br>", unsafe_allow_html=True)

    st.subheader(t['welcome_home'])
    st.write(t['home_desc'])
    render_feature_cards(t, lang)
    st.markdown("<br>", unsafe_allow_html=True)

    col1, col2, col3 = st.columns([1, 2, 1])
    with col2:
        if st.button(t['get_started'], type="primary", use_container_width=True):
            st.session_state.current_page = "courses"
            st.rerun()


def render_courses_page(t, lang="fr"):
    """Page du catalogue de cours."""
    st.markdown(f"""
    <div style="text-align: center; margin-bottom: 32px;">
        <h1 style="font-size: 32px; color: #1a1a2e;">{t['catalogue']}</h1>
        <p style="color: #666;">{t['subtitle']}</p>
    </div>
    """, unsafe_allow_html=True)

    courses = COURSES[lang]
    total_progress = sum(st.session_state.get(f"progress_{c['id']}", 0) for c in courses)
    completed_courses = sum(1 for c in courses if st.session_state.get(f"progress_{c['id']}", 0) == 100)
    avg_progress = total_progress / len(courses) if courses else 0

    col1, col2, col3 = st.columns(3)
    with col1: st.metric(t['total_courses'], len(courses))
    with col2: st.metric(t['completed'], completed_courses)
    with col3: st.metric(t['overall_progress'], f"{avg_progress:.0f}%")
    st.progress(avg_progress / 100)
    st.markdown("<hr>", unsafe_allow_html=True)

    cols = st.columns(2)
    for i, course in enumerate(courses):
        with cols[i % 2]:
            render_course_card(course, t, lang)
            st.markdown("<br>", unsafe_allow_html=True)


def render_mentor_page(t, lang="fr"):
    """Page du Mentor IA."""
    st.markdown(f"""
    <div style="text-align: center; margin-bottom: 24px;">
        <h1 style="font-size: 32px; color: #1a1a2e;">{t['mentor_title']}</h1>
        <p style="color: #666;">{t['mentor_desc']}</p>
    </div>
    """, unsafe_allow_html=True)

    if "chat_history" not in st.session_state:
        st.session_state.chat_history = []

    courses = COURSES[lang]
    course_options = {t['no_course']: None}
    for course in courses:
        course_options[course['title']] = course

    selected_course_title = st.selectbox(t['select_course_chat'], options=list(course_options.keys()), index=0)
    selected_course = course_options[selected_course_title]

    # Affichage de l'historique
    for msg in st.session_state.chat_history:
        role_class = "chat-user" if msg["role"] == "user" else "chat-assistant"
        avatar = "👤" if msg["role"] == "user" else "🤖"
        align = "flex-direction: row-reverse;" if msg["role"] == "user" and lang == "ar" else ""
        st.markdown(f"""
        <div style="display: flex; align-items: flex-start; margin: 8px 0; {align}">
            <div class="chat-avatar" style="background: {'linear-gradient(135deg, #667eea 0%, #764ba2 100%)' if msg['role'] == 'user' else '#f0f0f0'};">{avatar}</div>
            <div class="chat-message {role_class}">{msg['content']}</div>
        </div>
        """, unsafe_allow_html=True)

    st.markdown("<hr>", unsafe_allow_html=True)

    col1, col2 = st.columns([5, 1])
    with col1:
        user_input = st.text_input("", placeholder=t['chat_placeholder'], label_visibility="collapsed", key="chat_input")
    with col2:
        send_clicked = st.button(t['send'], type="primary", use_container_width=True)

    if send_clicked and user_input.strip():
        st.session_state.chat_history.append({"role": "user", "content": user_input})

        context = ""
        if selected_course:
            context = f"Course: {selected_course['title']}\nDescription: {selected_course['description']}\nModules: {', '.join(selected_course['modules'])}"

        with st.spinner(t['thinking']):
            mentor = OllamaClient()
            if mentor.is_available:
                messages = [{"role": "system", "content": get_system_prompt(lang)}]
                for msg in st.session_state.chat_history[-10:]:
                    messages.append({"role": msg["role"], "content": msg["content"]})

                response = mentor.chat(messages)
                if response:
                    st.session_state.chat_history.append({"role": "assistant", "content": response})
                else:
                    st.session_state.chat_history.append({
                        "role": "assistant",
                        "content": "Désolé, je n'ai pas pu générer de réponse." if lang == "fr" else
                                   "Sorry, I couldn't generate a response." if lang == "en" else
                                   "عذراً، لم أتمكن من توليد رد."
                    })
            else:
                st.session_state.chat_history.append({
                    "role": "assistant",
                    "content": t['offline_response']
                })
        st.rerun()

    if st.session_state.chat_history:
        if st.button("🗑️ " + t['clear_chat'], key="clear_chat"):
            st.session_state.chat_history = []
            st.rerun()


def render_profile_page(t, lang="fr"):
    """Page de profil utilisateur."""
    st.markdown(f"""
    <div style="text-align: center; margin-bottom: 24px;">
        <h1 style="font-size: 32px; color: #1a1a2e;">{t['profile_title']}</h1>
        <p style="color: #666;">{t['profile_desc']}</p>
    </div>
    """, unsafe_allow_html=True)

    courses = COURSES[lang]

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
        st.subheader(t['progress_overview'])
        total_progress = 0
        completed = 0
        in_progress = 0
        for course in courses:
            prog = st.session_state.get(f"progress_{course['id']}", 0)
            total_progress += prog
            if prog == 100: completed += 1
            elif prog > 0: in_progress += 1
        avg = total_progress / len(courses) if courses else 0

        col_a, col_b, col_c = st.columns(3)
        with col_a: st.metric(t['total_courses'], len(courses))
        with col_b: st.metric(t['completed'], completed)
        with col_c: st.metric(t['in_progress'], in_progress)
        st.progress(avg / 100)
        st.caption(f"{t['overall_progress']}: {avg:.1f}%")

    st.markdown("<hr>", unsafe_allow_html=True)
    st.subheader(t['my_progress'])

    for course in courses:
        prog = st.session_state.get(f"progress_{course['id']}", 0)
        c1, c2, c3 = st.columns([3, 1, 1])
        with c1: st.write(f"{course['icon']} **{course['title']}**")
        with c2: st.progress(prog / 100)
        with c3: st.caption(f"{prog}%")

    st.markdown("<hr>", unsafe_allow_html=True)
    st.subheader("⚙️ " + t['language'])

    lang_options = {"fr": "🇫🇷 Français", "en": "🇬🇧 English", "ar": "🇸🇦 العربية"}
    current_lang = st.session_state.get("language", lang)
    selected_lang = st.selectbox(t['change_language'], options=list(lang_options.keys()),
                                 format_func=lambda x: lang_options[x],
                                 index=list(lang_options.keys()).index(current_lang))
    if selected_lang != current_lang:
        st.session_state.language = selected_lang
        st.rerun()

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


# ═══════════════════════════════════════════════════════════════════════════════
# INITIALISATION & POINT D'ENTRÉE
# ═══════════════════════════════════════════════════════════════════════════════

def initialize_session_state():
    """Initialise toutes les variables de session."""
    defaults = {
        "activated": False,
        "access_granted": False,
        "current_page": "home",
        "language": DEFAULT_LANGUAGE,
        "chat_history": []
    }
    for key, value in defaults.items():
        if key not in st.session_state:
            st.session_state[key] = value

    # Progression des cours
    for lang in COURSES:
        for course in COURSES[lang]:
            key = f"progress_{course['id']}"
            if key not in st.session_state:
                st.session_state[key] = 0


def main():
    """Point d'entrée principal de l'application."""
    st.set_page_config(page_title="AI Learning Hub", page_icon="🎓", layout="wide", initial_sidebar_state="expanded")

    initialize_session_state()
    lang = st.session_state.get("language", DEFAULT_LANGUAGE)
    t = TRANSLATIONS[lang]

    st.markdown(CUSTOM_CSS, unsafe_allow_html=True)

    if lang == "ar":
        st.markdown('<div class="rtl">', unsafe_allow_html=True)

    if not st.session_state.activated:
        render_activation_page(lang)
    else:
        render_sidebar(t, lang)
        current_page = st.session_state.get("current_page", "home")

        if current_page == "home":
            render_home_page(t, lang)
        elif current_page == "courses":
            render_courses_page(t, lang)
        elif current_page == "mentor":
            render_mentor_page(t, lang)
        elif current_page == "profile":
            render_profile_page(t, lang)

    if lang == "ar":
        st.markdown('</div>', unsafe_allow_html=True)


if __name__ == "__main__":
    main()
