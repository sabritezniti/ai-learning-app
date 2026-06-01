"""
AI Learning Hub v3.0 - Cours complets + Audio + Mentor IA
"""

import streamlit as st
import requests
import json
import base64
import io
import re

ACTIVATION_KEY = "22459129071981"
OLLAMA_MODEL = "llama3.2"
OLLAMA_BASE_URL = "http://localhost:11434"
DEFAULT_LANGUAGE = "ar"

LANGUAGES = {
    "fr": "Français",
    "en": "English",
    "ar": "العربية"
}


COURSES = {
    "fr": [
        {
            "id": "intro_ml",
            "title": "Introduction au Machine Learning",
            "description": "Apprenez les bases du Machine Learning.",
            "level": "Débutant",
            "duration": "8 heures",
            "icon": "🤖",
            "color": "#4CAF50",
            "modules": [
                {
                    "title": "Qu'est-ce que le Machine Learning ?",
                    "content": "Le Machine Learning est une branche de l'IA qui permet aux ordinateurs d'apprendre automatiquement a partir de donnees. Les 3 types principaux sont : apprentissage supervise, non supervise et par renforcement. Applications : reconnaissance faciale, recommandations Netflix, detection de fraudes, voitures autonomes.",
                    "duration": "45 min"
                },
                {
                    "title": "Types d'apprentissage",
                    "content": "Supervise : donnees etiquetees pour la prediction. Non supervise : decouverte de structures cachees. Renforcement : apprentissage par recompenses et penalites. Algorithmes : Regression lineaire, KNN, K-Means, Q-Learning.",
                    "duration": "50 min"
                },
                {
                    "title": "Regression lineaire",
                    "content": "Algorithme fondamental modelisant la relation lineaire y = mx + b. Methode des moindres carres pour minimiser l'erreur. Metriques : R2, MAE, RMSE. Applications : prix immobiliers, previsions de ventes.",
                    "duration": "55 min"
                },
                {
                    "title": "Classification avec KNN",
                    "content": "K-Nearest Neighbors classe un point selon ses K voisins les plus proches. Distance euclidienne. Choix de K par validation croisee. Avantages : simple, intuitif. Limites : lent, sensible a l'echelle.",
                    "duration": "50 min"
                },
                {
                    "title": "Clustering avec K-Means",
                    "content": "Partitionnement en K clusters homogenes. Algorithme iteratif : initialisation, attribution, mise a jour. Methode du coude pour choisir K. Applications : segmentation marketing, compression d'images.",
                    "duration": "55 min"
                },
                {
                    "title": "Evaluation des modeles",
                    "content": "Separation train/validation/test. Metriques classification : Accuracy, Precision, Recall, F1-Score, ROC-AUC. Overfitting vs Underfitting. Validation croisee K-fold. Biais-Variance tradeoff.",
                    "duration": "60 min"
                }
            ]
        },
        {
            "id": "deep_learning",
            "title": "Deep Learning Fondamental",
            "description": "Reseaux de neurones, CNN, RNN et Transformers.",
            "level": "Intermediaire",
            "duration": "12 heures",
            "icon": "🧠",
            "color": "#2196F3",
            "modules": [
                {
                    "title": "Perceptron et reseaux de neurones",
                    "content": "Le perceptron est le bloc fondamental. Formule : sortie = f(w1*x1 + w2*x2 + ... + wn*xn + b). Reseaux multicouches MLP empilent plusieurs couches. Forward propagation. Theoreme d'approximation universelle.",
                    "duration": "60 min"
                },
                {
                    "title": "Fonction d'activation et backpropagation",
                    "content": "ReLU : max(0,x) - la plus populaire. Sigmoid : 1/(1+e^-x). Tanh : centree sur zero. Backpropagation ajuste les poids via la descente de gradient. Optimiseurs : SGD, Momentum, Adam.",
                    "duration": "65 min"
                },
                {
                    "title": "Reseaux convolutifs CNN",
                    "content": "3 operations : Convolution (filtres glissants), Pooling (sous-echantillonnage), Activation ReLU. Architecture typique : Conv2D -> MaxPool -> Conv2D -> MaxPool -> Flatten -> Dense -> Softmax. Architectures : LeNet, AlexNet, VGG, ResNet, EfficientNet.",
                    "duration": "70 min"
                },
                {
                    "title": "Reseaux recurrents RNN/LSTM",
                    "content": "RNN maintiennent un etat cache pour traiter les sequences. Formule : h_t = tanh(W_hh*h_{t-1} + W_xh*x_t + b). LSTM resout le vanishing gradient avec 3 portes : oubli, entree, sortie. GRU : version simplifiee. Applications : traduction, generation de texte, series temporelles.",
                    "duration": "65 min"
                },
                {
                    "title": "Introduction aux Transformers",
                    "content": "Mecanisme d'attention : Self-Attention calcule l'importance relative de chaque mot. Multi-Head Attention : plusieurs attentions en parallele. Architecture : Encodeur + Decodeur. Modeles : BERT (comprehension), GPT (generation), T5 (traduction). Avantages : parallelisation, dependances lointaines.",
                    "duration": "70 min"
                },
                {
                    "title": "Fine-tuning et transfer learning",
                    "content": "Reutiliser des modeles pre-entraines. Approches : Feature Extraction (geler les couches) ou Fine-tuning complet. Modeles : ResNet, BERT, GPT, T5. Techniques avancees : LoRA, Prompt Engineering, In-Context Learning.",
                    "duration": "60 min"
                }
            ]
        },
        {
            "id": "nlp",
            "title": "Traitement du Langage Naturel NLP",
            "description": "Tokenization, embeddings, modeles de langage.",
            "level": "Avance",
            "duration": "10 heures",
            "icon": "💬",
            "color": "#9C27B0",
            "modules": [
                {
                    "title": "Pretraitement du texte",
                    "content": "Pipeline : Tokenization (mots/sous-mots), Normalisation (lowercase, accents), Suppression stop words, Lemmatization. Types de tokenization : Word-level, Character-level, Subword (BPE, WordPiece).",
                    "duration": "45 min"
                },
                {
                    "title": "Word Embeddings Word2Vec GloVe",
                    "content": "Representations vectorielles denses capturant le sens semantique. Word2Vec : CBOW (predict from context) et Skip-gram (predict context from word). GloVe : matrice de co-occurrence. FastText : sous-mots de caracteres. Analogies : roi - homme + femme = reine.",
                    "duration": "55 min"
                },
                {
                    "title": "Modeles de sequence Seq2Seq",
                    "content": "Architecture encodeur-decodeur pour traduction et resume. Encodeur : resume la sequence en vecteur de contexte. Decodeur : genere mot par mot. Attention : permet de se concentrer sur les parties pertinentes. Teacher Forcing et Beam Search.",
                    "duration": "60 min"
                },
                {
                    "title": "BERT et modeles pre-entraines",
                    "content": "BERT : apprentissage bidirectionnel avec MLM (Masked Language Model) et NSP (Next Sentence Prediction). BERT-Base : 12 couches, 110M parametres. BERT-Large : 24 couches, 340M parametres. Variantes : RoBERTa, ALBERT, DistilBERT, CamemBERT.",
                    "duration": "65 min"
                },
                {
                    "title": "Fine-tuning pour la classification",
                    "content": "Adapter BERT avec un learning rate tres faible (2e-5 a 5e-5). Utiliser le token [CLS] pour la classification. Strategies : Gradual Unfreezing, Discriminative Fine-tuning. Evaluation : Accuracy, F1-Score, Matrice de confusion.",
                    "duration": "55 min"
                },
                {
                    "title": "Generation de texte avec GPT",
                    "content": "GPT : modele autoregressif predictant le mot suivant. GPT-1 : 117M params. GPT-2 : 1.5B params. GPT-3 : 175B params. GPT-4 : multimodal. Strategies : Greedy Decoding, Beam Search, Top-k Sampling, Nucleus Sampling, Temperature. Prompt Engineering : Zero-shot, Few-shot, Chain-of-Thought.",
                    "duration": "60 min"
                }
            ]
        },
        {
            "id": "computer_vision",
            "title": "Vision par Ordinateur",
            "description": "OpenCV, detection d'objets, segmentation.",
            "level": "Intermediaire",
            "duration": "10 heures",
            "icon": "👁️",
            "color": "#FF9800",
            "modules": [
                {
                    "title": "Traitement d'image avec OpenCV",
                    "content": "OpenCV : 2500+ fonctions. Operations : lecture, redimensionnement, rotation, recadrage, conversion couleurs. Filtres : GaussianBlur, medianBlur, bilateralFilter. Morphologie : erosion, dilatation, ouverture, fermeture. Histogrammes et egalisation.",
                    "duration": "50 min"
                },
                {
                    "title": "Detection de contours et features",
                    "content": "Sobel : gradient horizontal et vertical. Canny : reduction bruit, gradient, suppression non-maxima, seuillage hysteresis. Harris : detection de coins. SIFT et ORB : points d'interet invariants. findContours : extraction de formes.",
                    "duration": "55 min"
                },
                {
                    "title": "Classification d'images avec CNN",
                    "content": "Utiliser des CNN pour classifier des images. Transfer learning avec ResNet, VGG, EfficientNet pre-entraines sur ImageNet. Fine-tuning des dernieres couches. Data augmentation : rotation, flip, zoom, shift.",
                    "duration": "65 min"
                },
                {
                    "title": "Detection d'objets YOLO SSD",
                    "content": "YOLO : You Only Look Once - detection en une seule passe. SSD : Single Shot MultiBox Detector avec anchor boxes. Metrique mAP (mean Average Precision). YOLOv8 : derniere version avec meilleures performances.",
                    "duration": "70 min"
                },
                {
                    "title": "Segmentation semantique",
                    "content": "Classifier chaque pixel de l'image. U-Net : architecture en U pour segmentation medicale. Mask R-CNN : instance segmentation (chaque objet a son masque). Applications : conduite autonome, imagerie medicale.",
                    "duration": "60 min"
                },
                {
                    "title": "Generation d'images GANs",
                    "content": "GANs : Generateur et Discriminateur en competition. DCGAN : GAN convolutif. StyleGAN : controle du style. CycleGAN : transfert non supervise entre domaines. Applications : generation de visages, transfert de style, super-resolution.",
                    "duration": "65 min"
                }
            ]
        },
        {
            "id": "reinforcement",
            "title": "Apprentissage par Renforcement",
            "description": "Agents IA, Q-Learning, DQN, PPO.",
            "level": "Avance",
            "duration": "14 heures",
            "icon": "🎮",
            "color": "#E91E63",
            "modules": [
                {
                    "title": "Concepts fondamentaux MDP",
                    "content": "Processus de Decision Markovien : etats S, actions A, recompenses R, politique pi. Fonction valeur V(s) et fonction action-valeur Q(s,a). Equation de Bellman. L'agent maximise la recompense cumulative actualisee.",
                    "duration": "55 min"
                },
                {
                    "title": "Q-Learning et SARSA",
                    "content": "Q-Learning : off-policy, met a jour Q(s,a) avec max(Q(s',a')). SARSA : on-policy, utilise l'action reelle prise. Exploration vs Exploitation : epsilon-greedy. Table Q pour les petits espaces d'etats.",
                    "duration": "60 min"
                },
                {
                    "title": "Deep Q-Networks DQN",
                    "content": "DQN utilise un reseau de neurones pour approximer Q(s,a). Techniques cles : Experience Replay (stocker et reechantillonner les transitions), Target Network (reseau cible stable), Double DQN (reduire le sur-estimation).",
                    "duration": "65 min"
                },
                {
                    "title": "Policy Gradient Methods",
                    "content": "Apprendre directement la politique pi(a|s) au lieu de la fonction valeur. REINFORCE : algorithme de base utilisant le gradient de la politique. Baseline pour reduire la variance.",
                    "duration": "60 min"
                },
                {
                    "title": "Actor-Critic A2C PPO",
                    "content": "Actor-Critic combine policy gradient (Actor) et valeur (Critic). A2C : Advantage Actor-Critic utilisant A(s,a) = Q(s,a) - V(s). PPO : Proximal Policy Optimization avec clipping pour plus de stabilite. TRPO : Trust Region Policy Optimization.",
                    "duration": "70 min"
                },
                {
                    "title": "Applications reelles",
                    "content": "Robotique : apprentissage de la marche, manipulation d'objets. Jeux : AlphaGo, Dota 2, StarCraft II. Trading algorithmique. Conduite autonome. Sim-to-Real : transfert simulation vers realite. Defis : sample efficiency, safety, generalisation.",
                    "duration": "55 min"
                }
            ]
        },
        {
            "id": "mlops",
            "title": "MLOps et Deploiement",
            "description": "CI/CD, monitoring, Docker, FastAPI.",
            "level": "Intermediaire",
            "duration": "8 heures",
            "icon": "🚀",
            "color": "#00BCD4",
            "modules": [
                {
                    "title": "Pipeline ML avec scikit-learn",
                    "content": "Creer des pipelines reproductibles avec Pipeline et make_pipeline. Enchainement : preprocessing, feature selection, model, evaluation. GridSearchCV et RandomizedSearchCV pour l'optimisation d'hyperparametres.",
                    "duration": "45 min"
                },
                {
                    "title": "Versioning des modeles MLflow",
                    "content": "MLflow Tracking : suivre les experiences, parametres, metriques. MLflow Models : packaging standardise. MLflow Registry : gestion du cycle de vie des modeles. Comparaison et selection des meilleurs modeles.",
                    "duration": "50 min"
                },
                {
                    "title": "Conteneurisation avec Docker",
                    "content": "Dockeriser les modeles ML pour un deploiement reproductible. Dockerfile : FROM, COPY, RUN, CMD. Docker Compose pour les services multiples. Images legeres avec multi-stage builds.",
                    "duration": "55 min"
                },
                {
                    "title": "Deploiement avec FastAPI",
                    "content": "Creer des APIs REST avec FastAPI. Pydantic pour la validation des donnees. Documentation automatique Swagger UI. Async/await pour les performances. Deploiement avec Uvicorn et Gunicorn.",
                    "duration": "60 min"
                },
                {
                    "title": "Monitoring et drift detection",
                    "content": "Surveiller les performances en production. Data drift : changement dans la distribution des entrees. Concept drift : changement dans la relation entree-sortie. Outils : Evidently, WhyLabs, Arize. Alertes et reentrainement automatique.",
                    "duration": "55 min"
                },
                {
                    "title": "CI/CD pour le ML",
                    "content": "Integration et deploiement continus pour le ML. Tests : unites, integration, modele. GitHub Actions, Jenkins, GitLab CI. MLOps platforms : Kubeflow, SageMaker, Azure ML. Maturite MLOps : niveaux 0 a 5.",
                    "duration": "50 min"
                }
            ]
        }
    ],
    "en": [],
    "ar": []
}

TRANSLATIONS = {
    "fr": {
        "app_title": "🎓 AI Learning Hub",
        "welcome": "Bienvenue sur AI Learning Hub",
        "subtitle": "Votre plateforme d'apprentissage de l'Intelligence Artificielle",
        "activation": "Activation",
        "enter_key": "Entrez votre cle d'activation",
        "activate": "Activer",
        "invalid_key": "Cle invalide. Veuillez reessayer.",
        "access_granted": "Acces autorise ! Bienvenue.",
        "home": "🏠 Accueil",
        "courses": "📚 Cours",
        "mentor": "🤖 Mentor IA",
        "profile": "👤 Profil",
        "catalogue": "Catalogue de Cours",
        "my_progress": "Ma Progression",
        "total_courses": "Cours totaux",
        "completed": "Completes",
        "in_progress": "En cours",
        "hours": "heures",
        "level": "Niveau",
        "duration": "Duree",
        "modules": "Modules",
        "start_course": "Commencer le cours",
        "continue": "Continuer",
        "completed_btn": "Termine",
        "mentor_title": "Votre Mentor IA",
        "mentor_desc": "Posez vos questions sur le cours selectionne. Le mentor connait le contenu de chaque lecon.",
        "ask_question": "Posez votre question...",
        "send": "Envoyer",
        "thinking": "Le mentor reflechit...",
        "no_ollama": "Ollama n'est pas disponible. Verifiez que le service est lance.",
        "profile_title": "Mon Profil",
        "profile_desc": "Gerez vos preferences et suivez vos progres.",
        "language": "Langue",
        "change_language": "Changer la langue",
        "progress_overview": "Vue d'ensemble de la progression",
        "overall_progress": "Progression globale",
        "recent_activity": "Activite recente",
        "no_activity": "Aucune activite recente",
        "logout": "Deconnexion",
        "footer": "2026 AI Learning Hub",
        "beginner": "Debutant",
        "intermediate": "Intermediaire",
        "advanced": "Avance",
        "select_course_chat": "Cours actuel",
        "no_course": "Discussion generale",
        "chat_placeholder": "Comment fonctionne un reseau de neurones ?",
        "welcome_home": "Bienvenue sur votre plateforme d'apprentissage !",
        "home_desc": "Explorez nos cours interactifs sur l'IA, ecoutez les lecons en audio, posez vos questions au Mentor IA, et suivez votre progression.",
        "feature_courses": "Cours Complets",
        "feature_courses_desc": "6 modules couvrant ML, Deep Learning, NLP, Vision, RL et MLOps",
        "feature_mentor": "Mentor IA par Cours",
        "feature_mentor_desc": "Assistant intelligent specialise dans le contenu de chaque lecon",
        "feature_progress": "Suivi de Progression",
        "feature_progress_desc": "Barres de progression et statistiques detaillees",
        "feature_audio": "Audio TTS",
        "feature_audio_desc": "Ecoutez chaque lecon en audio avec synthese vocale",
        "get_started": "Commencer l'apprentissage",
        "stats_courses": "Cours disponibles",
        "stats_hours": "Heures de contenu",
        "stats_modules": "Modules a explorer",
        "stats_level": "Niveaux de difficulte",
        "clear_chat": "Effacer la conversation",
        "offline_response": "Le service Ollama n'est pas disponible. Pour utiliser le Mentor IA, veuillez installer et lancer Ollama localement.",
        "listen_lesson": "🔊 Ecouter la lecon",
        "lesson_content": "Contenu de la lecon",
        "lesson_duration": "Duree",
        "mark_complete": "Marquer comme termine",
        "lesson_completed": "Lecon terminee !",
        "ask_about_lesson": "Poser une question sur cette lecon",
        "course_context": "Contexte du cours",
        "back_to_course": "Retour au cours",
        "next_lesson": "Lecon suivante",
        "prev_lesson": "Lecon precedente",
        "course_overview": "Vue d'ensemble du cours",
        "lessons_list": "Liste des lecons",
        "start_learning": "Commencer a apprendre",
    },
    "en": {
        "app_title": "🎓 AI Learning Hub",
        "welcome": "Welcome to AI Learning Hub",
        "subtitle": "Your Artificial Intelligence Learning Platform",
        "activation": "Activation",
        "enter_key": "Enter your activation key",
        "activate": "Activate",
        "invalid_key": "Invalid key. Please try again.",
        "access_granted": "Access granted! Welcome.",
        "home": "🏠 Home",
        "courses": "📚 Courses",
        "mentor": "🤖 AI Mentor",
        "profile": "👤 Profile",
        "catalogue": "Course Catalog",
        "my_progress": "My Progress",
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
        "mentor_title": "Your AI Mentor",
        "mentor_desc": "Ask questions about the selected course. The mentor knows each lesson content.",
        "ask_question": "Ask your question...",
        "send": "Send",
        "thinking": "The mentor is thinking...",
        "no_ollama": "Ollama is not available. Please check that the service is running.",
        "profile_title": "My Profile",
        "profile_desc": "Manage your preferences and track your progress.",
        "language": "Language",
        "change_language": "Change language",
        "progress_overview": "Progress overview",
        "overall_progress": "Overall progress",
        "recent_activity": "Recent activity",
        "no_activity": "No recent activity",
        "logout": "Logout",
        "footer": "2026 AI Learning Hub",
        "beginner": "Beginner",
        "intermediate": "Intermediate",
        "advanced": "Advanced",
        "select_course_chat": "Current course",
        "no_course": "General discussion",
        "chat_placeholder": "How does a neural network work?",
        "welcome_home": "Welcome to your learning platform!",
        "home_desc": "Explore our interactive AI courses, listen to lessons in audio, ask questions to the AI Mentor, and track your progress.",
        "feature_courses": "Complete Courses",
        "feature_courses_desc": "6 modules covering ML, Deep Learning, NLP, Vision, RL and MLOps",
        "feature_mentor": "Course-Specific AI Mentor",
        "feature_mentor_desc": "Intelligent assistant specialized in each lesson content",
        "feature_progress": "Progress Tracking",
        "feature_progress_desc": "Progress bars and detailed statistics",
        "feature_audio": "Audio TTS",
        "feature_audio_desc": "Listen to each lesson with text-to-speech synthesis",
        "get_started": "Start learning",
        "stats_courses": "Available courses",
        "stats_hours": "Hours of content",
        "stats_modules": "Modules to explore",
        "stats_level": "Difficulty levels",
        "clear_chat": "Clear conversation",
        "offline_response": "The Ollama service is unavailable. To use the AI Mentor, please install and run Ollama locally.",
        "listen_lesson": "🔊 Listen to lesson",
        "lesson_content": "Lesson content",
        "lesson_duration": "Duration",
        "mark_complete": "Mark as completed",
        "lesson_completed": "Lesson completed!",
        "ask_about_lesson": "Ask a question about this lesson",
        "course_context": "Course context",
        "back_to_course": "Back to course",
        "next_lesson": "Next lesson",
        "prev_lesson": "Previous lesson",
        "course_overview": "Course overview",
        "lessons_list": "Lessons list",
        "start_learning": "Start learning",
    },
    "ar": {
        "app_title": "🎓 مركز تعلم الذكاء الاصطناعي",
        "welcome": "مرحباً بك في مركز تعلم الذكاء الاصطناعي",
        "subtitle": "منصتك لتعلم الذكاء الاصطناعي",
        "activation": "التفعيل",
        "enter_key": "أدخل مفتاح التفعيل",
        "activate": "تفعيل",
        "invalid_key": "مفتاح غير صالح. يرجى المحاولة مرة أخرى.",
        "access_granted": "تم منح الوصول! أهلاً بك.",
        "home": "🏠 الرئيسية",
        "courses": "📚 الدورات",
        "mentor": "🤖 المرشد الذكي",
        "profile": "👤 الملف الشخصي",
        "catalogue": "دليل الدورات",
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
        "mentor_desc": "اطرح أسئلتك حول الدورة المحددة. يعرف المرشد محتوى كل درس.",
        "ask_question": "اطرح سؤالك...",
        "send": "إرسال",
        "thinking": "🤔 المرشد يفكر...",
        "no_ollama": "⚠️ Ollama غير متوفر. يرجى التحقق من تشغيل الخدمة محلياً.",
        "profile_title": "👤 ملفي الشخصي",
        "profile_desc": "إدارة تفضيلاتك ومتابعة تقدمك.",
        "language": "اللغة",
        "change_language": "تغيير اللغة",
        "progress_overview": "نظرة عامة على التقدم",
        "overall_progress": "التقدم العام",
        "recent_activity": "النشاط الأخير",
        "no_activity": "لا يوجد نشاط حديث",
        "logout": "تسجيل الخروج",
        "footer": "© 2026 مركز تعلم الذكاء الاصطناعي",
        "beginner": "مبتدئ",
        "intermediate": "متوسط",
        "advanced": "متقدم",
        "select_course_chat": "الدورة الحالية",
        "no_course": "مناقشة عامة",
        "chat_placeholder": "كيف يعمل الشبكة العصبية؟",
        "welcome_home": "مرحباً بك في منصتك التعليمية!",
        "home_desc": "استكشف دورات الذكاء الاصطناعي التفاعلية، استمع إلى الدروس صوتياً، اطرح أسئلتك على المرشد الذكي، وتابع تقدمك.",
        "feature_courses": "📚 دورات كاملة",
        "feature_courses_desc": "6 وحدات تغطي ML، التعلم العميق، NLP، الرؤية، RL و MLOps",
        "feature_mentor": "🤖 مرشد ذكي متخصص",
        "feature_mentor_desc": "مساعد ذكي متخصص في محتوى كل درس",
        "feature_progress": "📊 تتبع التقدم",
        "feature_progress_desc": "أشرطة التقدم وإحصائيات مفصلة",
        "feature_audio": "🔊 صوت TTS",
        "feature_audio_desc": "استمع إلى كل درس بصوت مُنشئ نصوص",
        "get_started": "ابدأ التعلم",
        "stats_courses": "الدورات المتاحة",
        "stats_hours": "ساعات المحتوى",
        "stats_modules": "وحدات للاستكشاف",
        "stats_level": "مستويات الصعوبة",
        "clear_chat": "مسح المحادثة",
        "offline_response": "🤖 **المرشد الذكي** (وضع عدم الاتصال)\n\nعذراً، خدمة Ollama غير متوفرة حالياً. لاستخدام المرشد الذكي، يرجى تثبيت Ollama وتشغيلها محلياً.",
        "listen_lesson": "🔊 استمع للدرس",
        "lesson_content": "محتوى الدرس",
        "lesson_duration": "المدة",
        "mark_complete": "وضع علامة مكتمل",
        "lesson_completed": "تم إكمال الدرس!",
        "ask_about_lesson": "اسأل سؤالاً عن هذا الدرس",
        "course_context": "سياق الدورة",
        "back_to_course": "العودة للدورة",
        "next_lesson": "الدرس التالي",
        "prev_lesson": "الدرس السابق",
        "course_overview": "نظرة عامة على الدورة",
        "lessons_list": "قائمة الدروس",
        "start_learning": "ابدأ التعلم",
    }
}

CUSTOM_CSS = """
<style>
@import url('https://fonts.googleapis.com/css2?family=Inter:wght@300;400;500;600;700&display=swap');

.stApp { font-family: 'Inter', sans-serif; }

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

.activation-container {
    max-width: 500px; margin: 80px auto; padding: 48px;
    background: linear-gradient(145deg, #ffffff 0%, #f8f9fa 100%);
    border-radius: 24px; box-shadow: 0 20px 60px rgba(0,0,0,0.1);
    text-align: center;
}

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

.stProgress > div > div {
    background: linear-gradient(90deg, #667eea 0%, #764ba2 100%);
    border-radius: 10px;
}

.main-header {
    background: linear-gradient(135deg, #1a1a2e 0%, #16213e 100%);
    color: white; padding: 40px; border-radius: 20px;
    margin-bottom: 32px; text-align: center;
    position: relative; overflow: hidden;
}
.main-header h1 { font-size: 36px; font-weight: 700; margin-bottom: 8px; }
.main-header p { font-size: 16px; opacity: 0.8; }

.feature-card {
    background: white; border-radius: 16px; padding: 28px;
    text-align: center; box-shadow: 0 4px 20px rgba(0,0,0,0.06);
    border: 1px solid rgba(0,0,0,0.05); transition: all 0.3s ease; height: 100%;
}
.feature-card:hover { transform: translateY(-6px); box-shadow: 0 12px 40px rgba(0,0,0,0.12); }
.feature-icon { font-size: 40px; margin-bottom: 16px; }
.feature-title { font-size: 18px; font-weight: 600; color: #1a1a2e; margin-bottom: 8px; }
.feature-desc { font-size: 14px; color: #666; line-height: 1.5; }

.rtl { direction: rtl; text-align: right; }
.rtl .course-meta { flex-direction: row-reverse; }
.rtl .chat-user { margin-left: 0; margin-right: auto; border-radius: 16px 16px 4px 16px; }
.rtl .chat-assistant { margin-right: 0; margin-left: auto; border-radius: 16px 16px 16px 4px; }

.lesson-card {
    background: white; border-radius: 16px; padding: 32px;
    box-shadow: 0 4px 20px rgba(0,0,0,0.06); border: 1px solid rgba(0,0,0,0.05);
    margin-bottom: 24px;
}
.lesson-title { font-size: 24px; font-weight: 700; color: #1a1a2e; margin-bottom: 16px; }
.lesson-content { font-size: 15px; line-height: 1.8; color: #444; }
.lesson-content h3 { color: #667eea; margin-top: 20px; }
.lesson-content ul { margin-left: 20px; }
.lesson-content code { background: #f4f4f4; padding: 2px 6px; border-radius: 4px; font-size: 13px; }
.lesson-content pre { background: #f4f4f4; padding: 16px; border-radius: 8px; overflow-x: auto; }

.audio-player {
    background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
    border-radius: 12px; padding: 16px; margin: 16px 0;
    color: white;
}

::-webkit-scrollbar { width: 8px; }
::-webkit-scrollbar-track { background: #f1f1f1; border-radius: 4px; }
::-webkit-scrollbar-thumb { background: linear-gradient(180deg, #667eea 0%, #764ba2 100%); border-radius: 4px; }

.stTextInput > div > div > input {
    border-radius: 12px; border: 2px solid #e0e0e0;
    padding: 12px 16px; font-size: 14px;
}
.stTextInput > div > div > input:focus {
    border-color: #667eea; box-shadow: 0 0 0 3px rgba(102,126,234,0.1);
}

.stSuccess { border-radius: 12px; background: linear-gradient(135deg, #d4edda 0%, #c3e6cb 100%); border: none; padding: 16px; }
.stError { border-radius: 12px; background: linear-gradient(135deg, #f8d7da 0%, #f5c6cb 100%); border: none; padding: 16px; }

hr { border: none; height: 1px; background: linear-gradient(90deg, transparent 0%, #ddd 50%, transparent 100%); margin: 32px 0; }
</style>
"""

# ═══════════════════════════════════════════════════════════════════════════════
# CLIENT OLLAMA + FONCTIONS AUDIO
# ═══════════════════════════════════════════════════════════════════════════════

class OllamaClient:
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


def get_system_prompt(lang="fr", course_title="", lesson_title="", lesson_content=""):
    base_prompts = {
        "fr": f"""Tu es un mentor IA expert en intelligence artificielle. Tu aides les etudiants a comprendre le cours suivant :

COURS : {course_title}
LECON : {lesson_title}
CONTENU DE LA LECON :
{lesson_content}

REGLES :
1. Reponds UNIQUEMENT en te basant sur le contenu de la lecon ci-dessus
2. Si la question ne concerne pas cette lecon, oriente l'etudiant vers le bon sujet
3. Sois pedagogique, clair et encourageant
4. Utilise des exemples concrets quand c'est utile
5. Reponds en francais""",
        "en": f"""You are an expert AI tutor. You help students understand the following course:

COURSE: {course_title}
LESSON: {lesson_title}
LESSON CONTENT:
{lesson_content}

RULES:
1. Answer ONLY based on the lesson content above
2. If the question is not about this lesson, guide the student to the right topic
3. Be pedagogical, clear and encouraging
4. Use concrete examples when useful
5. Answer in English""",
        "ar": f"""أنت مرشد ذكي متخصص في الذكاء الاصطناعي. تساعد الطلاب في فهم الدورة التالية:

الدورة: {course_title}
الدرس: {lesson_title}
محتوى الدرس:
{lesson_content}

القواعد:
1. أجب بناءً فقط على محتوى الدرس أعلاه
2. إذا كان السؤال لا يتعلق بهذا الدرس، وجه الطالب إلى الموضوع الصحيح
3. كن تعليمياً وواضحاً ومشجعاً
4. استخدم أمثلة ملموسة عندما يكون ذلك مفيداً
5. أجب باللغة العربية"""
    }
    return base_prompts.get(lang, base_prompts["en"])


def text_to_speech(text, lang="fr"):
    try:
        from gtts import gTTS
        # Configuration langue avec accent
        lang_config = {
            "fr": {"lang": "fr", "tld": "fr"},
            "en": {"lang": "en", "tld": "us"},
            "ar": {"lang": "ar", "tld": "com"}
        }
        config = lang_config.get(lang, {"lang": "fr", "tld": "fr"})
        # Nettoyer le texte pour TTS
        clean_text = re.sub(r'[#*`|]', '', text)
        clean_text = re.sub(r'\\n+', ' ', clean_text)
        clean_text = clean_text[:4000]
        tts = gTTS(text=clean_text, lang=config["lang"], tld=config["tld"], slow=False)
        fp = io.BytesIO()
        tts.write_to_fp(fp)
        fp.seek(0)
        audio_bytes = fp.read()
        return audio_bytes
    except Exception as e:
        st.error(f"Erreur TTS: {e}")
        return None



def autoplay_audio(audio_bytes, key=None):
    """Play audio automatically using base64 HTML audio tag (fallback)"""
    if audio_bytes:
        b64 = base64.b64encode(audio_bytes).decode()
        md = f'<audio controls autoplay="true"><source src="data:audio/mp3;base64,{b64}" type="audio/mp3"></audio>'
        st.markdown(md, unsafe_allow_html=True)


# ═══════════════════════════════════════════════════════════════════════════════
# FONCTIONS UI - PAGES
# ═══════════════════════════════════════════════════════════════════════════════

def render_activation_page(lang="fr"):
    t = TRANSLATIONS[lang]
    st.markdown(f"""
    <div class="activation-container">
        <div style="font-size: 64px; margin-bottom: 24px;">🔐</div>
        <div style="font-size: 28px; font-weight: 700; color: #1a1a2e; margin-bottom: 12px;">{t['activation']}</div>
        <div style="font-size: 16px; color: #666; margin-bottom: 32px;">{t['enter_key']}</div>
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
    st.markdown(f"""
    <div class="main-header">
        <h1>{t['welcome']}</h1>
        <p>{t['subtitle']}</p>
    </div>
    """, unsafe_allow_html=True)


def render_course_card(course, t, lang="fr"):
    progress = st.session_state.get(f"progress_{course['id']}", 0)
    total_lessons = len(course['modules'])
    completed_lessons = sum(1 for i in range(total_lessons) 
                           if st.session_state.get(f"lesson_done_{course['id']}_{i}", False))
    lesson_progress = int((completed_lessons / total_lessons) * 100) if total_lessons > 0 else 0

    if lesson_progress == 0:
        btn_text, btn_emoji = t['start_course'], "🚀"
    elif lesson_progress < 100:
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
            <div class="course-meta-item"><span>📋</span> {total_lessons} {t['modules']}</div>
        </div>
        <div style="font-size: 12px; color: #888; margin-bottom: 4px; display: flex; justify-content: space-between;">
            <span>{t['overall_progress']}</span><span>{lesson_progress}%</span>
        </div>
    </div>
    """, unsafe_allow_html=True)

    st.progress(lesson_progress / 100)

    col1, col2 = st.columns([3, 1])
    with col2:
        if st.button(f"{btn_emoji} {btn_text}", key=f"btn_{course['id']}_{lang}", use_container_width=True):
            st.session_state.current_course = course['id']
            st.session_state.current_lesson = 0
            st.session_state.current_page = "lesson"
            st.rerun()

    with st.expander(f"📋 {t['modules']}"):
        for i, module in enumerate(course['modules']):
            done = st.session_state.get(f"lesson_done_{course['id']}_{i}", False)
            icon = "✅" if done else "⭕"
            st.markdown(f"{icon} {module['title']} ({module['duration']})")


def render_stats_section(t, lang="fr"):
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
    features = [
        (t['feature_courses'], t['feature_courses_desc'], "📚"),
        (t['feature_mentor'], t['feature_mentor_desc'], "🤖"),
        (t['feature_progress'], t['feature_progress_desc'], "📊"),
        (t['feature_audio'], t['feature_audio_desc'], "🔊")
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
    st.markdown(f"""
    <div style="text-align: center; margin-bottom: 32px;">
        <h1 style="font-size: 32px; color: #1a1a2e;">{t['catalogue']}</h1>
        <p style="color: #666;">{t['subtitle']}</p>
    </div>
    """, unsafe_allow_html=True)

    courses = COURSES[lang]
    total_lessons_all = sum(len(c['modules']) for c in courses)
    completed_lessons_all = sum(
        sum(1 for i in range(len(c['modules'])) 
            if st.session_state.get(f"lesson_done_{c['id']}_{i}", False))
        for c in courses
    )
    avg_progress = int((completed_lessons_all / total_lessons_all) * 100) if total_lessons_all > 0 else 0

    col1, col2, col3 = st.columns(3)
    with col1: st.metric(t['total_courses'], len(courses))
    with col2: st.metric(t['completed'], sum(1 for c in courses if all(
        st.session_state.get(f"lesson_done_{c['id']}_{i}", False) 
        for i in range(len(c['modules'])))))
    with col3: st.metric(t['overall_progress'], f"{avg_progress}%")
    st.progress(avg_progress / 100)
    st.markdown("<hr>", unsafe_allow_html=True)

    cols = st.columns(2)
    for i, course in enumerate(courses):
        with cols[i % 2]:
            render_course_card(course, t, lang)
            st.markdown("<br>", unsafe_allow_html=True)


def render_lesson_page(t, lang="fr"):
    """Page de lecture d'une lecon specifique avec audio et mentor"""
    course_id = st.session_state.get("current_course", "intro_ml")
    lesson_idx = st.session_state.get("current_lesson", 0)

    courses = COURSES[lang]
    course = None
    for c in courses:
        if c['id'] == course_id:
            course = c
            break

    if not course:
        st.error("Cours non trouve")
        return

    if lesson_idx >= len(course['modules']):
        st.success("Felicitations ! Vous avez termine ce cours.")
        if st.button(t['back_to_course']):
            st.session_state.current_page = "courses"
            st.rerun()
        return

    lesson = course['modules'][lesson_idx]

    # Header avec navigation
    col1, col2, col3 = st.columns([1, 3, 1])
    with col1:
        if st.button("⬅️ " + t['back_to_course']):
            st.session_state.current_page = "courses"
            st.rerun()
    with col2:
        st.markdown(f"""
        <div style="text-align: center;">
            <div style="font-size: 14px; color: #888;">{course['title']}</div>
            <div style="font-size: 18px; font-weight: 600; color: #1a1a2e;">
                Lecon {lesson_idx + 1} / {len(course['modules'])}
            </div>
        </div>
        """, unsafe_allow_html=True)
    with col3:
        if lesson_idx < len(course['modules']) - 1:
            if st.button(t['next_lesson'] + " ➡️"):
                st.session_state.current_lesson = lesson_idx + 1
                st.rerun()

    st.markdown("<hr>", unsafe_allow_html=True)

    # Titre de la lecon
    st.markdown(f"""
    <div class="lesson-card">
        <div class="lesson-title">{lesson['title']}</div>
        <div style="color: #888; font-size: 13px; margin-bottom: 16px;">
            ⏱️ {t['lesson_duration']} : {lesson['duration']}
        </div>
    </div>
    """, unsafe_allow_html=True)

    # Section Audio
    audio_key = f"audio_{course_id}_{lesson_idx}"
    col_audio1, col_audio2 = st.columns([1, 3])
    with col_audio1:
        if st.button("🔊 " + t['listen_lesson'], type="secondary", use_container_width=True):
            with st.spinner("Generation audio en cours..."):
                audio_bytes = text_to_speech(lesson['content'], lang)
                if audio_bytes:
                    st.session_state[audio_key] = audio_bytes
                    st.success("Audio genere !")
                    st.rerun()

    # Afficher le lecteur audio avec autoplay via HTML base64
    if audio_key in st.session_state:
        st.audio(st.session_state[audio_key], format="audio/mp3")
        # Autoplay via HTML pour lecture automatique
        b64 = base64.b64encode(st.session_state[audio_key]).decode()
        autoplay_html = f'<audio autoplay controls><source src="data:audio/mp3;base64,{b64}" type="audio/mp3"></audio>'
        st.markdown(autoplay_html, unsafe_allow_html=True)

    st.markdown("<hr>", unsafe_allow_html=True)

    # Contenu de la lecon
    st.subheader("📖 " + t['lesson_content'])
    st.markdown(f'<div class="lesson-content">{lesson["content"].replace(chr(10), "<br>")}</div>', unsafe_allow_html=True)

    st.markdown("<hr>", unsafe_allow_html=True)

    # Bouton marquer comme termine
    lesson_done_key = f"lesson_done_{course_id}_{lesson_idx}"
    is_done = st.session_state.get(lesson_done_key, False)

    col_done1, col_done2 = st.columns([1, 2])
    with col_done1:
        if not is_done:
            if st.button("✅ " + t['mark_complete'], type="primary", use_container_width=True):
                st.session_state[lesson_done_key] = True
                st.success(t['lesson_completed'])
                st.rerun()
        else:
            st.success("✅ " + t['lesson_completed'])

    with col_done2:
        if lesson_idx < len(course['modules']) - 1 and is_done:
            if st.button(t['next_lesson'] + " →", type="primary", use_container_width=True):
                st.session_state.current_lesson = lesson_idx + 1
                st.rerun()

    st.markdown("<hr>", unsafe_allow_html=True)

    # Section Mentor IA specifique a cette lecon
    st.subheader("🤖 " + t['ask_about_lesson'])

    if "lesson_chat" not in st.session_state:
        st.session_state.lesson_chat = []

    # Afficher l'historique du chat
    for msg in st.session_state.lesson_chat:
        role_class = "chat-user" if msg["role"] == "user" else "chat-assistant"
        avatar = "👤" if msg["role"] == "user" else "🤖"
        st.markdown(f"""
        <div style="display: flex; align-items: flex-start; margin: 8px 0;">
            <div style="width: 36px; height: 36px; border-radius: 50%; display: flex; align-items: center; justify-content: center; font-size: 18px; margin-right: 8px; background: {'linear-gradient(135deg, #667eea 0%, #764ba2 100%)' if msg['role'] == 'user' else '#f0f0f0'};">{avatar}</div>
            <div class="chat-message {role_class}">{msg['content']}</div>
        </div>
        """, unsafe_allow_html=True)

    # Input pour question
    col_chat1, col_chat2 = st.columns([5, 1])
    with col_chat1:
        user_question = st.text_input("", placeholder=t['chat_placeholder'], label_visibility="collapsed", key="lesson_chat_input")
    with col_chat2:
        send_clicked = st.button(t['send'], type="primary", use_container_width=True)

    if send_clicked and user_question.strip():
        st.session_state.lesson_chat.append({"role": "user", "content": user_question})

        with st.spinner(t['thinking']):
            mentor = OllamaClient()
            if mentor.is_available:
                system_prompt = get_system_prompt(
                    lang=lang,
                    course_title=course['title'],
                    lesson_title=lesson['title'],
                    lesson_content=lesson['content']
                )
                messages = [{"role": "system", "content": system_prompt}]
                for msg in st.session_state.lesson_chat[-10:]:
                    messages.append({"role": msg["role"], "content": msg["content"]})

                response = mentor.chat(messages)
                if response:
                    st.session_state.lesson_chat.append({"role": "assistant", "content": response})
                else:
                    st.session_state.lesson_chat.append({"role": "assistant", "content": "Desole, je n'ai pas pu generer de reponse."})
            else:
                st.session_state.lesson_chat.append({"role": "assistant", "content": t['offline_response']})
        st.rerun()

    if st.session_state.lesson_chat:
        if st.button("🗑️ " + t['clear_chat'], key="clear_lesson_chat"):
            st.session_state.lesson_chat = []
            st.rerun()


def render_mentor_page(t, lang="fr"):
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
        st.markdown(f"""
        <div style="display: flex; align-items: flex-start; margin: 8px 0;">
            <div style="width: 36px; height: 36px; border-radius: 50%; display: flex; align-items: center; justify-content: center; font-size: 18px; margin-right: 8px; background: {'linear-gradient(135deg, #667eea 0%, #764ba2 100%)' if msg['role'] == 'user' else '#f0f0f0'};">{avatar}</div>
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
            context = f"Cours: {selected_course['title']}\nDescription: {selected_course['description']}\nModules: {', '.join([m['title'] for m in selected_course['modules']])}"

        with st.spinner(t['thinking']):
            mentor = OllamaClient()
            if mentor.is_available:
                system = f"Tu es un mentor IA expert en intelligence artificielle. Tu aides les etudiants a apprendre. Sois pedagogique et clair.\n\nContexte du cours: {context}"
                messages = [{"role": "system", "content": system}]
                for msg in st.session_state.chat_history[-10:]:
                    messages.append({"role": msg["role"], "content": msg["content"]})

                response = mentor.chat(messages)
                if response:
                    st.session_state.chat_history.append({"role": "assistant", "content": response})
                else:
                    st.session_state.chat_history.append({"role": "assistant", "content": "Desole, je n'ai pas pu generer de reponse."})
            else:
                st.session_state.chat_history.append({"role": "assistant", "content": t['offline_response']})
        st.rerun()

    if st.session_state.chat_history:
        if st.button("🗑️ " + t['clear_chat'], key="clear_chat"):
            st.session_state.chat_history = []
            st.rerun()


def render_profile_page(t, lang="fr"):
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
        total_lessons = sum(len(c['modules']) for c in courses)
        completed_lessons = sum(
            sum(1 for i in range(len(c['modules'])) 
                if st.session_state.get(f"lesson_done_{c['id']}_{i}", False))
            for c in courses
        )
        in_progress = sum(
            any(st.session_state.get(f"lesson_done_{c['id']}_{i}", False) 
                for i in range(len(c['modules']))) 
            and not all(st.session_state.get(f"lesson_done_{c['id']}_{i}", False) 
                       for i in range(len(c['modules'])))
            for c in courses
        )
        avg = int((completed_lessons / total_lessons) * 100) if total_lessons > 0 else 0

        col_a, col_b, col_c = st.columns(3)
        with col_a: st.metric(t['total_courses'], len(courses))
        with col_b: st.metric(t['completed'], sum(1 for c in courses if all(
            st.session_state.get(f"lesson_done_{c['id']}_{i}", False) 
            for i in range(len(c['modules'])))))
        with col_c: st.metric(t['in_progress'], in_progress)
        st.progress(avg / 100)
        st.caption(f"{t['overall_progress']}: {avg:.1f}%")

    st.markdown("<hr>", unsafe_allow_html=True)
    st.subheader(t['my_progress'])

    for course in courses:
        total = len(course['modules'])
        done = sum(1 for i in range(total) if st.session_state.get(f"lesson_done_{course['id']}_{i}", False))
        prog = int((done / total) * 100) if total > 0 else 0
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
    has_activity = any(st.session_state.get(f"lesson_done_{c['id']}_{i}", False) 
                      for c in courses for i in range(len(c['modules'])))
    if not has_activity:
        st.info(t['no_activity'])
    else:
        for course in courses:
            for i, module in enumerate(course['modules']):
                if st.session_state.get(f"lesson_done_{course['id']}_{i}", False):
                    st.markdown(f"✅ **{course['title']}** - {module['title']}")

# ═══════════════════════════════════════════════════════════════════════════════
# INITIALISATION & POINT D'ENTREE
# ═══════════════════════════════════════════════════════════════════════════════

def initialize_session_state():
    defaults = {
        "activated": False,
        "access_granted": False,
        "current_page": "home",
        "language": DEFAULT_LANGUAGE,
        "chat_history": [],
        "lesson_chat": [],
        "current_course": "intro_ml",
        "current_lesson": 0,
    }
    for key, value in defaults.items():
        if key not in st.session_state:
            st.session_state[key] = value

    # Progression des lecons
    for lang in COURSES:
        for course in COURSES[lang]:
            for i in range(len(course['modules'])):
                key = f"lesson_done_{course['id']}_{i}"
                if key not in st.session_state:
                    st.session_state[key] = False


def main():
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
        elif current_page == "lesson":
            render_lesson_page(t, lang)
        elif current_page == "mentor":
            render_mentor_page(t, lang)
        elif current_page == "profile":
            render_profile_page(t, lang)

    if lang == "ar":
        st.markdown('</div>', unsafe_allow_html=True)


if __name__ == "__main__":
    main()
