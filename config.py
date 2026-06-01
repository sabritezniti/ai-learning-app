"""
Configuration and constants for the AI Learning Application.
"""

# Activation Key
ACTIVATION_KEY = "22459129071981"

# Supported Languages
LANGUAGES = {
    "fr": "Français",
    "en": "English",
    "ar": "العربية"
}

# Default Language
DEFAULT_LANGUAGE = "fr"

# Ollama Configuration
OLLAMA_MODEL = "llama3.2"  # Change to your preferred local model
OLLAMA_BASE_URL = "http://localhost:11434"

# App Configuration
APP_TITLE = "AI Learning Hub"
APP_ICON = "🎓"

# Course Data
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

# Translations
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
        "footer": "© 2026 AI Learning Hub - Propulsé par Streamlit",
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
        "footer": "© 2026 AI Learning Hub - Powered by Streamlit",
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
        "footer": "© 2026 مركز تعلم الذكاء الاصطناعي - مدعوم بواسطة Streamlit",
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
    }
}
