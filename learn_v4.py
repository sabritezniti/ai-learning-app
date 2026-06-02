"""
AI Learning Hub v4.0 - 100% Cloud, Zero Infrastructure
No Ollama, No Local TTS, No Setup Required
Just: URL + Activation Key → Learn
"""

import streamlit as st
import requests
import json
import base64
import io
import re
import time

# ═══════════════════════════════════════════════════════════════════════════════
# CONFIGURATION - 100% CLOUD, ZERO LOCAL DEPENDENCIES
# ═══════════════════════════════════════════════════════════════════════════════

ACTIVATION_KEY = "22459129071981"
DEFAULT_LANGUAGE = "ar"

# Groq API - Free tier: 1,000 requests/day, no credit card required
GROQ_API_KEY = "gsk_demo_free_tier_no_key_needed_for_ui"  # User can add their own
GROQ_API_URL = "https://api.groq.com/openai/v1/chat/completions"
GROQ_MODEL = "llama3-70b-8192"  # Fast, free, high quality

LANGUAGES = {
    "fr": "Français",
    "en": "English",
    "ar": "العربية"
}

# ═══════════════════════════════════════════════════════════════════════════════
# COURSES DATA - COMPLETE CONTENT IN ALL LANGUAGES
# ═══════════════════════════════════════════════════════════════════════════════

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
    "en": [
        {
            "id": "intro_ml",
            "title": "Introduction to Machine Learning",
            "description": "Learn the fundamentals of Machine Learning from scratch.",
            "level": "Beginner",
            "duration": "8 hours",
            "icon": "🤖",
            "color": "#4CAF50",
            "modules": [
                {
                    "title": "What is Machine Learning?",
                    "content": "Machine Learning is a branch of AI that enables computers to learn automatically from data without explicit programming. The 3 main types are: Supervised Learning, Unsupervised Learning, and Reinforcement Learning. Applications: facial recognition, Netflix recommendations, fraud detection, autonomous vehicles.",
                    "duration": "45 min"
                },
                {
                    "title": "Types of Learning",
                    "content": "Supervised: labeled data for prediction. Unsupervised: discovering hidden structures. Reinforcement: learning through rewards and penalties. Algorithms: Linear Regression, KNN, K-Means, Q-Learning.",
                    "duration": "50 min"
                },
                {
                    "title": "Linear Regression",
                    "content": "Fundamental algorithm modeling the linear relationship y = mx + b. Least squares method to minimize error. Metrics: R², MAE, RMSE. Applications: real estate prices, sales forecasting.",
                    "duration": "55 min"
                },
                {
                    "title": "Classification with KNN",
                    "content": "K-Nearest Neighbors classifies a point based on its K nearest neighbors. Euclidean distance. Choosing K via cross-validation. Advantages: simple, intuitive. Limitations: slow, scale-sensitive.",
                    "duration": "50 min"
                },
                {
                    "title": "Clustering with K-Means",
                    "content": "Partitioning into K homogeneous clusters. Iterative algorithm: initialization, assignment, update. Elbow Method for choosing K. Applications: market segmentation, image compression.",
                    "duration": "55 min"
                },
                {
                    "title": "Model Evaluation",
                    "content": "Train/validation/test split. Classification metrics: Accuracy, Precision, Recall, F1-Score, ROC-AUC. Overfitting vs Underfitting. K-fold cross-validation. Bias-Variance tradeoff.",
                    "duration": "60 min"
                }
            ]
        },
        {
            "id": "deep_learning",
            "title": "Fundamental Deep Learning",
            "description": "Neural networks, CNN, RNN and Transformers.",
            "level": "Intermediate",
            "duration": "12 hours",
            "icon": "🧠",
            "color": "#2196F3",
            "modules": [
                {
                    "title": "Perceptron and Neural Networks",
                    "content": "The perceptron is the fundamental building block. Formula: output = f(w1*x1 + w2*x2 + ... + wn*xn + b). Multi-layer perceptrons (MLP) stack multiple layers. Forward propagation. Universal approximation theorem.",
                    "duration": "60 min"
                },
                {
                    "title": "Activation Function and Backpropagation",
                    "content": "ReLU: max(0,x) - most popular. Sigmoid: 1/(1+e^-x). Tanh: zero-centered. Backpropagation adjusts weights via gradient descent. Optimizers: SGD, Momentum, Adam.",
                    "duration": "65 min"
                },
                {
                    "title": "Convolutional Neural Networks CNN",
                    "content": "3 operations: Convolution (sliding filters), Pooling (subsampling), ReLU activation. Typical architecture: Conv2D -> MaxPool -> Conv2D -> MaxPool -> Flatten -> Dense -> Softmax. Architectures: LeNet, AlexNet, VGG, ResNet, EfficientNet.",
                    "duration": "70 min"
                },
                {
                    "title": "Recurrent Networks RNN/LSTM",
                    "content": "RNNs maintain hidden state to process sequences. Formula: h_t = tanh(W_hh*h_{t-1} + W_xh*x_t + b). LSTM solves vanishing gradient with 3 gates: forget, input, output. GRU: simplified version. Applications: translation, text generation, time series.",
                    "duration": "65 min"
                },
                {
                    "title": "Introduction to Transformers",
                    "content": "Attention mechanism: Self-Attention calculates relative importance of each word. Multi-Head Attention: multiple attentions in parallel. Architecture: Encoder + Decoder. Models: BERT (understanding), GPT (generation), T5 (translation). Advantages: parallelization, long-range dependencies.",
                    "duration": "70 min"
                },
                {
                    "title": "Fine-tuning and Transfer Learning",
                    "content": "Reuse pre-trained models. Approaches: Feature Extraction (freeze layers) or full Fine-tuning. Models: ResNet, BERT, GPT, T5. Advanced techniques: LoRA, Prompt Engineering, In-Context Learning.",
                    "duration": "60 min"
                }
            ]
        },
        {
            "id": "nlp",
            "title": "Natural Language Processing NLP",
            "description": "Tokenization, embeddings, language models.",
            "level": "Advanced",
            "duration": "10 hours",
            "icon": "💬",
            "color": "#9C27B0",
            "modules": [
                {
                    "title": "Text Preprocessing",
                    "content": "Pipeline: Tokenization (words/subwords), Normalization (lowercase, accents), Stop words removal, Lemmatization. Tokenization types: Word-level, Character-level, Subword (BPE, WordPiece).",
                    "duration": "45 min"
                },
                {
                    "title": "Word Embeddings Word2Vec GloVe",
                    "content": "Dense vector representations capturing semantic meaning. Word2Vec: CBOW (predict from context) and Skip-gram (predict context from word). GloVe: co-occurrence matrix. FastText: character subwords. Analogies: king - man + woman = queen.",
                    "duration": "55 min"
                },
                {
                    "title": "Sequence Models Seq2Seq",
                    "content": "Encoder-decoder architecture for translation and summarization. Encoder: summarizes sequence into context vector. Decoder: generates word by word. Attention: focuses on relevant parts. Teacher Forcing and Beam Search.",
                    "duration": "60 min"
                },
                {
                    "title": "BERT and Pre-trained Models",
                    "content": "BERT: bidirectional learning with MLM (Masked Language Model) and NSP (Next Sentence Prediction). BERT-Base: 12 layers, 110M parameters. BERT-Large: 24 layers, 340M parameters. Variants: RoBERTa, ALBERT, DistilBERT, CamemBERT.",
                    "duration": "65 min"
                },
                {
                    "title": "Fine-tuning for Classification",
                    "content": "Adapt BERT with very low learning rate (2e-5 to 5e-5). Use [CLS] token for classification. Strategies: Gradual Unfreezing, Discriminative Fine-tuning. Evaluation: Accuracy, F1-Score, Confusion Matrix.",
                    "duration": "55 min"
                },
                {
                    "title": "Text Generation with GPT",
                    "content": "GPT: autoregressive model predicting next word. GPT-1: 117M params. GPT-2: 1.5B params. GPT-3: 175B params. GPT-4: multimodal. Strategies: Greedy Decoding, Beam Search, Top-k Sampling, Nucleus Sampling, Temperature. Prompt Engineering: Zero-shot, Few-shot, Chain-of-Thought.",
                    "duration": "60 min"
                }
            ]
        },
        {
            "id": "computer_vision",
            "title": "Computer Vision",
            "description": "OpenCV, object detection, segmentation.",
            "level": "Intermediate",
            "duration": "10 hours",
            "icon": "👁️",
            "color": "#FF9800",
            "modules": [
                {
                    "title": "Image Processing with OpenCV",
                    "content": "OpenCV: 2500+ functions. Operations: reading, resizing, rotation, cropping, color conversion. Filters: GaussianBlur, medianBlur, bilateralFilter. Morphology: erosion, dilation, opening, closing. Histograms and equalization.",
                    "duration": "50 min"
                },
                {
                    "title": "Contour and Feature Detection",
                    "content": "Sobel: horizontal and vertical gradients. Canny: noise reduction, gradient, non-maxima suppression, hysteresis thresholding. Harris: corner detection. SIFT and ORB: invariant interest points. findContours: shape extraction.",
                    "duration": "55 min"
                },
                {
                    "title": "Image Classification with CNN",
                    "content": "Use CNNs to classify images. Transfer learning with ResNet, VGG, EfficientNet pre-trained on ImageNet. Fine-tuning last layers. Data augmentation: rotation, flip, zoom, shift.",
                    "duration": "65 min"
                },
                {
                    "title": "Object Detection YOLO SSD",
                    "content": "YOLO: You Only Look Once - single-pass detection. SSD: Single Shot MultiBox Detector with anchor boxes. Metric mAP (mean Average Precision). YOLOv8: latest version with best performance.",
                    "duration": "70 min"
                },
                {
                    "title": "Semantic Segmentation",
                    "content": "Classify each pixel in the image. U-Net: U-shaped architecture for medical segmentation. Mask R-CNN: instance segmentation (each object has its mask). Applications: autonomous driving, medical imaging.",
                    "duration": "60 min"
                },
                {
                    "title": "Image Generation GANs",
                    "content": "GANs: Generator and Discriminator in competition. DCGAN: convolutional GAN. StyleGAN: style control. CycleGAN: unsupervised transfer between domains. Applications: face generation, style transfer, super-resolution.",
                    "duration": "65 min"
                }
            ]
        },
        {
            "id": "reinforcement",
            "title": "Reinforcement Learning",
            "description": "AI agents, Q-Learning, DQN, PPO.",
            "level": "Advanced",
            "duration": "14 hours",
            "icon": "🎮",
            "color": "#E91E63",
            "modules": [
                {
                    "title": "Fundamental Concepts MDP",
                    "content": "Markov Decision Process: states S, actions A, rewards R, policy π. Value function V(s) and action-value function Q(s,a). Bellman equation. The agent maximizes discounted cumulative reward.",
                    "duration": "55 min"
                },
                {
                    "title": "Q-Learning and SARSA",
                    "content": "Q-Learning: off-policy, updates Q(s,a) with max(Q(s',a')). SARSA: on-policy, uses actual action taken. Exploration vs Exploitation: epsilon-greedy. Q-Table for small state spaces.",
                    "duration": "60 min"
                },
                {
                    "title": "Deep Q-Networks DQN",
                    "content": "DQN uses neural network to approximate Q(s,a). Key techniques: Experience Replay (store and resample transitions), Target Network (stable target), Double DQN (reduce overestimation).",
                    "duration": "65 min"
                },
                {
                    "title": "Policy Gradient Methods",
                    "content": "Learn policy π(a|s) directly instead of value function. REINFORCE: base algorithm using policy gradient. Baseline to reduce variance.",
                    "duration": "60 min"
                },
                {
                    "title": "Actor-Critic A2C PPO",
                    "content": "Actor-Critic combines policy gradient (Actor) and value (Critic). A2C: Advantage Actor-Critic using A(s,a) = Q(s,a) - V(s). PPO: Proximal Policy Optimization with clipping for more stability. TRPO: Trust Region Policy Optimization.",
                    "duration": "70 min"
                },
                {
                    "title": "Real-world Applications",
                    "content": "Robotics: learning to walk, object manipulation. Games: AlphaGo, Dota 2, StarCraft II. Algorithmic trading. Autonomous driving. Sim-to-Real: simulation to reality transfer. Challenges: sample efficiency, safety, generalization.",
                    "duration": "55 min"
                }
            ]
        },
        {
            "id": "mlops",
            "title": "MLOps and Deployment",
            "description": "CI/CD, monitoring, Docker, FastAPI.",
            "level": "Intermediate",
            "duration": "8 hours",
            "icon": "🚀",
            "color": "#00BCD4",
            "modules": [
                {
                    "title": "ML Pipeline with scikit-learn",
                    "content": "Create reproducible pipelines with Pipeline and make_pipeline. Chain: preprocessing, feature selection, model, evaluation. GridSearchCV and RandomizedSearchCV for hyperparameter optimization.",
                    "duration": "45 min"
                },
                {
                    "title": "Model Versioning with MLflow",
                    "content": "MLflow Tracking: track experiments, parameters, metrics. MLflow Models: standardized packaging. MLflow Registry: model lifecycle management. Comparison and selection of best models.",
                    "duration": "50 min"
                },
                {
                    "title": "Containerization with Docker",
                    "content": "Dockerize ML models for reproducible deployment. Dockerfile: FROM, COPY, RUN, CMD. Docker Compose for multiple services. Lightweight images with multi-stage builds.",
                    "duration": "55 min"
                },
                {
                    "title": "Deployment with FastAPI",
                    "content": "Create REST APIs with FastAPI. Pydantic for data validation. Automatic Swagger UI documentation. Async/await for performance. Deployment with Uvicorn and Gunicorn.",
                    "duration": "60 min"
                },
                {
                    "title": "Monitoring and Drift Detection",
                    "content": "Monitor performance in production. Data drift: change in input distribution. Concept drift: change in input-output relationship. Tools: Evidently, WhyLabs, Arize. Alerts and automatic retraining.",
                    "duration": "55 min"
                },
                {
                    "title": "CI/CD for ML",
                    "content": "Continuous integration and deployment for ML. Tests: unit, integration, model. GitHub Actions, Jenkins, GitLab CI. MLOps platforms: Kubeflow, SageMaker, Azure ML. MLOps maturity: levels 0 to 5.",
                    "duration": "50 min"
                }
            ]
        }
    ],
    "ar": [
        {
            "id": "intro_ml",
            "title": "مقدمة في تعلم الآلة",
            "description": "تعلم أساسيات تعلم الآلة والذكاء الاصطناعي من الصفر.",
            "level": "مبتدئ",
            "duration": "8 ساعات",
            "icon": "🤖",
            "color": "#4CAF50",
            "modules": [
                {
                    "title": "ما هو تعلم الآلة؟",
                    "content": "تعلم الآلة (Machine Learning) هو فرع من فروع الذكاء الاصطناعي يتيح للحواسيب التعلم تلقائياً من البيانات دون برمجة صريحة. الأنواع الثلاثة الرئيسية هي: التعلم الخاضع للإشراف (Supervised Learning)، والتعلم غير الخاضع للإشراف (Unsupervised Learning)، والتعلم المعزز (Reinforcement Learning).\n\nتطبيقات عملية: التعرف على الوجوه، توصيات نتفليكس، كشف الاحتيال، السيارات ذاتية القيادة.",
                    "duration": "45 دقيقة"
                },
                {
                    "title": "أنواع التعلم",
                    "content": "التعلم الخاضع للإشراف: بيانات مُعلمة للتنبؤ. التعلم غير الخاضع للإشراف: اكتشاف الهياكل المخفية. التعلم المعزز: التعلم من خلال المكافآت والعقوبات.\n\nأهم الخوارزميات: الانحدار الخطي (Linear Regression)، أقرب الجيران (KNN)، التجميع بـ K-Means، Q-Learning.",
                    "duration": "50 دقيقة"
                },
                {
                    "title": "الانحدار الخطي",
                    "content": "خوارزمية أساسية نمذجة العلاقة الخطية y = mx + b. طريقة المربعات الصغرى لتقليل الخطأ.\n\nالمقاييس: R²، MAE، RMSE. التطبيقات: أسعار العقارات، التنبؤ بالمبيعات.",
                    "duration": "55 دقيقة"
                },
                {
                    "title": "التصنيف باستخدام KNN",
                    "content": "خوارزمية أقرب الجيران (K-Nearest Neighbors) تصنف نقطة بناءً على أقرب K جيران لها. المسافة الإقليدية. اختيار K عبر التحقق المتقاطع.\n\nالمزايا: بسيطة، بديهية. القيود: بطيئة، حساسة للمقياس.",
                    "duration": "50 دقيقة"
                },
                {
                    "title": "التجميع باستخدام K-Means",
                    "content": "تقسيم البيانات إلى K مجموعات متجانسة. خوارزمية تكرارية: التهيئة، التخصيص، التحديث. طريقة المرفق (Elbow Method) لاختيار K.\n\nالتطبيقات: تجزئة السوق، ضغط الصور.",
                    "duration": "55 دقيقة"
                },
                {
                    "title": "تقييم النماذج",
                    "content": "فصل البيانات إلى تدريب/تحقق/اختبار. مقاييس التصنيف: الدقة (Accuracy)، الدقة (Precision)، الاستدعاء (Recall)، F1-Score، ROC-AUC.\n\nالانحراف الزائد (Overfitting) مقابل الانحراف الناقص (Underfitting). التحقق المتقاطع K-fold. مفاضلة التحيز-التباين (Bias-Variance Tradeoff).",
                    "duration": "60 دقيقة"
                }
            ]
        },
        {
            "id": "deep_learning",
            "title": "التعلم العميق الأساسي",
            "description": "الشبكات العصبية، CNN، RNN و Transformers.",
            "level": "متوسط",
            "duration": "12 ساعة",
            "icon": "🧠",
            "color": "#2196F3",
            "modules": [
                {
                    "title": "البيرسبترون والشبكات العصبية",
                    "content": "البيرسبترون هو اللبنة الأساسية. الصيغة: المخرج = f(w1*x1 + w2*x2 + ... + wn*xn + b). الشبكات متعددة الطبقات (MLP) تكدس عدة طبقات. انتشار للأمام (Forward Propagation). نظرية التقريب العالمي.",
                    "duration": "60 دقيقة"
                },
                {
                    "title": "دالة التفعيل والانتشار العكسي",
                    "content": "ReLU: max(0,x) - الأكثر شيوعاً. Sigmoid: 1/(1+e^-x). Tanh: مركز حول الصفر. الانتشار العكسي (Backpropagation) يعدل الأوزان عبر نزول التدرج.\n\nالمحسّنات: SGD، Momentum، Adam.",
                    "duration": "65 دقيقة"
                },
                {
                    "title": "الشبكات التلافيفية CNN",
                    "content": "3 عمليات: التلافيف (Convolution) بفلاتر متحركة، التجميع (Pooling) للتقليل، وتفعيل ReLU.\n\nالبنية النموذجية: Conv2D → MaxPool → Conv2D → MaxPool → Flatten → Dense → Softmax. البنى: LeNet، AlexNet، VGG، ResNet، EfficientNet.",
                    "duration": "70 دقيقة"
                },
                {
                    "title": "الشبكات المتكررة RNN/LSTM",
                    "content": "RNN تحافظ على حالة مخفية لمعالجة التسلسلات. الصيغة: h_t = tanh(W_hh*h_{t-1} + W_xh*x_t + b). LSTM تحل مشكلة التدرج المتناقض بـ 3 بوابات: النسيان، الإدخال، والإخراج.\n\nGRU: نسخة مبسطة. التطبيقات: الترجمة، توليد النصوص، السلاسل الزمنية.",
                    "duration": "65 دقيقة"
                },
                {
                    "title": "مقدمة في Transformers",
                    "content": "آلية الانتباه (Attention): Self-Attention تحسب الأهمية النسبية لكل كلمة. Multi-Head Attention: عدة انتباهات بالتوازي.\n\nالبنية: مشفر + فك مشفر. النماذج: BERT (الفهم)، GPT (التوليد)، T5 (الترجمة). المزايا: التوازي، الاعتمادات البعيدة.",
                    "duration": "70 دقيقة"
                },
                {
                    "title": "الضبط الدقيق ونقل التعلم",
                    "content": "إعادة استخدام النماذج المُدرّبة مسبقاً. المقاربات: استخراج الميزات (تجميد الطبقات) أو الضبط الدقيق الكامل.\n\nالنماذج: ResNet، BERT، GPT، T5. تقنيات متقدمة: LoRA، هندسة الأوامر (Prompt Engineering)، التعلم السياقي (In-Context Learning).",
                    "duration": "60 دقيقة"
                }
            ]
        },
        {
            "id": "nlp",
            "title": "معالجة اللغات الطبيعية NLP",
            "description": "تجزئة النصوص، التضمينات، نماذج اللغة.",
            "level": "متقدم",
            "duration": "10 ساعات",
            "icon": "💬",
            "color": "#9C27B0",
            "modules": [
                {
                    "title": "معالجة النصوص المسبقة",
                    "content": "خط الأنابيب: التجزئة (Tokenization) للكلمات/الجزيئات، التطبيع (lowercase، الحذف)، إزالة الكلمات الشائعة (Stop Words)، الليماتة (Lemmatization).\n\nأنواع التجزئة: Word-level، Character-level، Subword (BPE، WordPiece).",
                    "duration": "45 دقيقة"
                },
                {
                    "title": "تضمينات الكلمات Word2Vec و GloVe",
                    "content": "تمثيلات متجهية كثيفة تلتقط المعنى الدلالي. Word2Vec: CBOW (التنبؤ من السياق) و Skip-gram (التنبؤ بالسياق من الكلمة). GloVe: مصفوفة الترافق. FastText: جزيئات الأحرف.\n\nالأنالوجيا: ملك - رجل + امرأة = ملكة.",
                    "duration": "55 دقيقة"
                },
                {
                    "title": "نماذج التسلسل Seq2Seq",
                    "content": "بنية المشفر-فك المشفر للترجمة والتلخيص. المشفر: يلخص التسلسل في متجه سياق. فك المشفر: يولد كلمة بكلمة.\n\nالانتباه: يركز على الأجزاء ذات الصلة. Teacher Forcing و Beam Search.",
                    "duration": "60 دقيقة"
                },
                {
                    "title": "BERT والنماذج المُدرّبة مسبقاً",
                    "content": "BERT: التعلم ثنائي الاتجاه مع MLM (نموذج اللغة المقنّع) و NSP (التنبؤ بالجملة التالية). BERT-Base: 12 طبقة، 110M معامل. BERT-Large: 24 طبقة، 340M معامل.\n\nالمتغيرات: RoBERTa، ALBERT، DistilBERT، CamemBERT.",
                    "duration": "65 دقيقة"
                },
                {
                    "title": "الضبط الدقيق للتصنيف",
                    "content": "تعديل BERT مع معدل تعلم منخفض جداً (2e-5 إلى 5e-5). استخدام رمز [CLS] للتصنيف.\n\nالاستراتيجيات: Gradual Unfreezing، Discriminative Fine-tuning. التقييم: الدقة، F1-Score، مصفوفة الارتباك.",
                    "duration": "55 دقيقة"
                },
                {
                    "title": "توليد النصوص باستخدام GPT",
                    "content": "GPT: نموذج انحداري يتنبأ بالكلمة التالية. GPT-1: 117M معامل. GPT-2: 1.5B معامل. GPT-3: 175B معامل. GPT-4: متعدد الوسائط.\n\nالاستراتيجيات: Greedy Decoding، Beam Search، Top-k Sampling، Nucleus Sampling، Temperature. هندسة الأوامر: Zero-shot، Few-shot، Chain-of-Thought.",
                    "duration": "60 دقيقة"
                }
            ]
        },
        {
            "id": "computer_vision",
            "title": "رؤية الحاسوب",
            "description": "OpenCV، كشف الأجسام، التجزئة.",
            "level": "متوسط",
            "duration": "10 ساعات",
            "icon": "👁️",
            "color": "#FF9800",
            "modules": [
                {
                    "title": "معالجة الصور باستخدام OpenCV",
                    "content": "OpenCV: 2500+ دالة. العمليات: القراءة، إعادة الحجم، الدوران، الاقتصاص، تحويل الألوان.\n\nالفلاتر: GaussianBlur، medianBlur، bilateralFilter. المورفولوجيا: التآكل، التوسع، الفتح، الإغلاق. الهيستوغرامات والتوازن.",
                    "duration": "50 دقيقة"
                },
                {
                    "title": "كشف الحواف والميزات",
                    "content": "Sobel: التدرج الأفقي والعمودي. Canny: تقليل الضوضاء، التدرج، قمع غير القصوى، العتبة الهسترية. Harris: كشف الزوايا. SIFT و ORB: نقاط اهتمام ثابتة. findContours: استخراج الأشكال.",
                    "duration": "55 دقيقة"
                },
                {
                    "title": "تصنيف الصور باستخدام CNN",
                    "content": "استخدام CNN لتصنيف الصور. نقل التعلم مع ResNet، VGG، EfficientNet المُدرّبة على ImageNet. الضبط الدقيق للطبقات الأخيرة.\n\nزيادة البيانات: الدوران، الانعكاس، التكبير، الإزاحة.",
                    "duration": "65 دقيقة"
                },
                {
                    "title": "كشف الأجسام YOLO و SSD",
                    "content": "YOLO: You Only Look Once - كشف في مرور واحد. SSD: Single Shot MultiBox Detector مع صناديق الإرساء (Anchor Boxes).\n\nالمقياس mAP (mean Average Precision). YOLOv8: أحدث نسخة بأداء أفضل.",
                    "duration": "70 دقيقة"
                },
                {
                    "title": "التجزئة الدلالية",
                    "content": "تصنيف كل بكسل في الصورة. U-Net: بنية على شكل U للتجزئة الطبية. Mask R-CNN: تجزئة المثيل (كل جسم له قناعه).\n\nالتطبيقات: القيادة الذاتية، التصوير الطبي.",
                    "duration": "60 دقيقة"
                },
                {
                    "title": "توليد الصور GANs",
                    "content": "GANs: مولد ومميز في منافسة. DCGAN: GAN تلافيفي. StyleGAN: التحكم بالأسلوب. CycleGAN: النقل غير الخاضع للإشراف بين المجالات.\n\nالتطبيقات: توليد الوجوه، نقل الأسلوب، التحسين الفائق (Super-Resolution).",
                    "duration": "65 دقيقة"
                }
            ]
        },
        {
            "id": "reinforcement",
            "title": "التعلم المعزز",
            "description": "وكلاء ذكاء اصطناعي، Q-Learning، DQN، PPO.",
            "level": "متقدم",
            "duration": "14 ساعة",
            "icon": "🎮",
            "color": "#E91E63",
            "modules": [
                {
                    "title": "المفاهيم الأساسية MDP",
                    "content": "عملية القرار ماركوفية: الحالات S، الإجراءات A، المكافآت R، السياسة π. دالة القيمة V(s) ودالة القيمة-الإجراء Q(s,a). معادلة بيلمان.\n\nالوكيل يعظم المكافأة التراكمية المُخصّصة.",
                    "duration": "55 دقيقة"
                },
                {
                    "title": "Q-Learning و SARSA",
                    "content": "Q-Learning: off-policy، يحدّث Q(s,a) بـ max(Q(s',a')). SARSA: on-policy، يستخدم الإجراء الفعلي المتخذ.\n\nالاستكشاف مقابل الاستغلال: epsilon-greedy. جدول Q للفضاءات الصغيرة.",
                    "duration": "60 دقيقة"
                },
                {
                    "title": "Deep Q-Networks DQN",
                    "content": "DQN تستخدم شبكة عصبية لتقريب Q(s,a). التقنيات الرئيسية: إعادة تجربة الخبرات (Experience Replay)، الشبكة الهدف (Target Network)، Double DQN لتقليل المبالغة.\n\n",
                    "duration": "65 دقيقة"
                },
                {
                    "title": "طرق تدرج السياسة",
                    "content": "تعلم السياسة π(a|s) مباشرة بدلاً من دالة القيمة. REINFORCE: خوارزمية أساسية تستخدم تدرج السياسة. خط الأساس (Baseline) لتقليل التباين.",
                    "duration": "60 دقيقة"
                },
                {
                    "title": "Actor-Critic A2C و PPO",
                    "content": "Actor-Critic يجمع بين تدرج السياسة (Actor) والقيمة (Critic). A2C: Advantage Actor-Critic باستخدام A(s,a) = Q(s,a) - V(s).\n\nPPO: Proximal Policy Optimization مع تقصير (Clipping) لاستقرار أكبر. TRPO: Trust Region Policy Optimization.",
                    "duration": "70 دقيقة"
                },
                {
                    "title": "تطبيقات واقعية",
                    "content": "الروبوتات: تعلم المشي، التعامل مع الأجسام. الألعاب: AlphaGo، Dota 2، StarCraft II. التداول الخوارزمي. القيادة الذاتية.\n\nSim-to-Real: النقل من المحاكاة إلى الواقع. التحديات: كفاءة العينات، السلامة، التعميم.",
                    "duration": "55 دقيقة"
                }
            ]
        },
        {
            "id": "mlops",
            "title": "MLOps والنشر",
            "description": "CI/CD، المراقبة، Docker، FastAPI.",
            "level": "متوسط",
            "duration": "8 ساعات",
            "icon": "🚀",
            "color": "#00BCD4",
            "modules": [
                {
                    "title": "خط أنابيب ML مع scikit-learn",
                    "content": "إنشاء خطوط أنابيب قابلة للتكرار بـ Pipeline و make_pipeline. التسلسل: المعالجة المسبقة، اختيار الميزات، النموذج، التقييم.\n\nGridSearchCV و RandomizedSearchCV لتحسين المعاملات الفائقة.",
                    "duration": "45 دقيقة"
                },
                {
                    "title": "إدارة إصدارات النماذج بـ MLflow",
                    "content": "MLflow Tracking: تتبع التجارب، المعاملات، المقاييس. MLflow Models: تغليف موحد. MLflow Registry: إدارة دورة حياة النماذج.\n\nالمقارنة واختيار أفضل النماذج.",
                    "duration": "50 دقيقة"
                },
                {
                    "title": "الحاويات باستخدام Docker",
                    "content": "حاوية نماذج ML للنشر القابل للتكرار. Dockerfile: FROM، COPY، RUN، CMD. Docker Compose للخدمات المتعددة.\n\nصور خفيفة مع multi-stage builds.",
                    "duration": "55 دقيقة"
                },
                {
                    "title": "النشر باستخدام FastAPI",
                    "content": "إنشاء واجهات REST بـ FastAPI. Pydantic للتحقق من البيانات. توثيق Swagger UI تلقائي. Async/await للأداء.\n\nالنشر بـ Uvicorn و Gunicorn.",
                    "duration": "60 دقيقة"
                },
                {
                    "title": "المراقبة وكشف الانحراف",
                    "content": "مراقبة الأداء في الإنتاج. انحراف البيانات: تغيير في توزيع المدخلات. انحراف المفهوم: تغيير في العلاقة بين المدخلات والمخرجات.\n\nالأدوات: Evidently، WhyLabs، Arize. التنبيهات وإعادة التدريب التلقائي.",
                    "duration": "55 دقيقة"
                },
                {
                    "title": "CI/CD للتعلم الآلي",
                    "content": "التكامل والنشر المستمرين للتعلم الآلي. الاختبارات: الوحدات، التكامل، النموذج. GitHub Actions، Jenkins، GitLab CI.\n\nمنصات MLOps: Kubeflow، SageMaker، Azure ML. نضج MLOps: المستويات 0 إلى 5.",
                    "duration": "50 دقيقة"
                }
            ]
        }
    ]
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
        "groq_key_label": "🔑 Cle API Groq (optionnel)",
        "groq_key_help": "Sans cle, le mentor utilise un modele local basique. Obtenez une cle gratuite sur console.groq.com",
        "tts_browser": "🔊 Ecouter (Navigateur)",
        "tts_cloud": "☁️ Ecouter (Cloud)",
        "tts_generating": "Generation audio en cours...",
        "tts_ready": "Audio pret !",
        "tts_error": "Erreur audio. Essayez le mode navigateur.",
        "mentor_offline": "Mode hors ligne - reponses predefinies",
        "mentor_online": "🟢 Mentor IA en ligne (Groq)",
        "mentor_demo": "🟡 Mode demo - ajoutez une cle API pour le mentor complet",
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
        "groq_key_label": "🔑 Groq API Key (optional)",
        "groq_key_help": "Without a key, the mentor uses a basic local mode. Get a free key at console.groq.com",
        "tts_browser": "🔊 Listen (Browser)",
        "tts_cloud": "☁️ Listen (Cloud)",
        "tts_generating": "Generating audio...",
        "tts_ready": "Audio ready!",
        "tts_error": "Audio error. Try browser mode.",
        "mentor_offline": "Offline mode - predefined responses",
        "mentor_online": "🟢 AI Mentor online (Groq)",
        "mentor_demo": "🟡 Demo mode - add API key for full mentor",
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
        "groq_key_label": "🔑 مفتاح API Groq (اختياري)",
        "groq_key_help": "بدون مفتاح، يستخدم المرشد وضعاً محلياً بسيطاً. احصل على مفتاح مجاني من console.groq.com",
        "tts_browser": "🔊 استمع (المتصفح)",
        "tts_cloud": "☁️ استمع (السحابة)",
        "tts_generating": "جاري إنشاء الصوت...",
        "tts_ready": "الصوت جاهز!",
        "tts_error": "خطأ في الصوت. جرب وضع المتصفح.",
        "mentor_offline": "وضع عدم الاتصال - ردود مُعدة مسبقاً",
        "mentor_online": "🟢 المرشد الذكي متصل (Groq)",
        "mentor_demo": "🟡 وضع تجريبي - أضف مفتاح API للمرشد الكامل",
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
# CLOUD AI CLIENT - NO LOCAL OLLAMA NEEDED
# ═══════════════════════════════════════════════════════════════════════════════

class CloudAIClient:
    """Cloud AI client using Groq API (free tier: 1000 requests/day, no CC required)"""

    def __init__(self, api_key=None):
        self.api_key = api_key or st.session_state.get("groq_api_key", "")
        self.api_url = GROQ_API_URL
        self.model = GROQ_MODEL
        self.is_available = self._check_availability()

    def _check_availability(self):
        """Check if Groq API is accessible with the provided key"""
        if not self.api_key or self.api_key == "gsk_demo_free_tier_no_key_needed_for_ui":
            return False
        try:
            headers = {"Authorization": f"Bearer {self.api_key}", "Content-Type": "application/json"}
            # Quick test with minimal payload
            test_payload = {
                "model": self.model,
                "messages": [{"role": "user", "content": "Hello"}],
                "max_tokens": 5
            }
            response = requests.post(self.api_url, headers=headers, json=test_payload, timeout=10)
            return response.status_code == 200
        except:
            return False

    def chat(self, messages, system_prompt=None, temperature=0.7):
        """Send chat request to Groq API"""
        if not self.is_available:
            return None

        headers = {
            "Authorization": f"Bearer {self.api_key}",
            "Content-Type": "application/json"
        }

        payload = {
            "model": self.model,
            "messages": messages,
            "temperature": temperature,
            "max_tokens": 2048
        }

        if system_prompt:
            payload["messages"].insert(0, {"role": "system", "content": system_prompt})

        try:
            response = requests.post(self.api_url, headers=headers, json=payload, timeout=60)
            if response.status_code == 200:
                data = response.json()
                return data["choices"][0]["message"]["content"]
            else:
                return f"Error {response.status_code}: {response.text[:200]}"
        except Exception as e:
            return f"Error: {str(e)}"


# ═══════════════════════════════════════════════════════════════════════════════
# TTS FUNCTIONS - BROWSER-BASED (NO LOCAL DEPENDENCIES)
# ═══════════════════════════════════════════════════════════════════════════════

def get_browser_tts_html(text, lang="ar"):
    """Generate HTML with Web Speech API for browser-based TTS"""
    lang_map = {"fr": "fr-FR", "en": "en-US", "ar": "ar-SA"}
    voice_lang = lang_map.get(lang, "en-US")

    # Clean text for JavaScript - be very careful with escaping
    # Clean text for JavaScript - escape quotes and remove newlines
    clean_text = text.replace("\\", " ")
    clean_text = clean_text.replace('"', "'")
    clean_text = clean_text.replace("\n", " ").replace("\r", " ")
    clean_text = re.sub(r'[#*`|]', '', clean_text)
    clean_text = clean_text[:2000]  # Limit length for safety

    html = f"""<div id="tts-container" style="display:none;"></div>
<script>
(function() {{
    function speakText() {{
        if ('speechSynthesis' in window) {{
            window.speechSynthesis.cancel();
            var utterance = new SpeechSynthesisUtterance("{clean_text}");
            utterance.lang = "{voice_lang}";
            utterance.rate = 0.85;
            utterance.pitch = 1.0;
            utterance.volume = 1.0;

            var voices = window.speechSynthesis.getVoices();
            var langPrefix = "{voice_lang.split('-')[0]}";
            var preferredVoice = voices.find(function(v) {{ return v.lang && v.lang.startsWith(langPrefix); }});
            if (preferredVoice) utterance.voice = preferredVoice;

            window.speechSynthesis.speak(utterance);
        }}
    }}

    if (window.speechSynthesis.getVoices().length === 0) {{
        window.speechSynthesis.onvoiceschanged = speakText;
    }} else {{
        speakText();
    }}
}})();
</script>"""
    return html


def get_tts_status_indicator():
    """Get TTS status for display"""
    return """
    <div style="display: flex; align-items: center; gap: 8px; font-size: 13px; color: #666;">
        <span style="width: 8px; height: 8px; border-radius: 50%; background: #4CAF50;"></span>
        <span>Text-to-Speech ready (Browser)</span>
    </div>
    """


# ═══════════════════════════════════════════════════════════════════════════════
# SYSTEM PROMPTS FOR AI MENTOR
# ═══════════════════════════════════════════════════════════════════════════════

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


def get_demo_response(question, lang="ar", course_title="", lesson_title=""):
    """Generate a demo response when no API key is available"""

    # Try to extract relevant content from the lesson if available
    # This makes the demo mode actually useful

    responses = {
        "ar": {
            "default": f"""مرحباً! 👋 أنا مرشدك الذكي للدورة: **{course_title}** - **{lesson_title}**.

🎯 **للحصول على إجابات ذكية ومفصلة:**
1. اذهب إلى **console.groq.com**
2. سجل حساباً مجاناً (بدون بطاقة ائتمان)
3. انسخ مفتاح API وألصقه في الشريط الجانبي

💡 **الآن:** يمكنني الإجابة على أسئلتك الأساسية. المحتوى الكامل للدورة متاح في علامة التبويب "📚 الدورات".""",

            "ما هو": f"""📚 **{lesson_title}** - موضوع أساسي في **{course_title}**

هذا الدرس يغطي مفاهيم أساسية في مجال الذكاء الاصطناعي. يُنصح بقراءة المحتوى الكامل المتاح في صفحة الدرس والاستماع للشرح الصوتي.

🎯 **للحصول على شرح مفصل:**
أضف مفتاح API من Groq في الشريط الجانبي للحصول على إجابات ذكية ومخصصة.""",

            "كيف": f"""🎓 **كيفية تعلم {lesson_title}:**

1. ✅ **اقرأ المحتوى** المتوفر في الدرس بعناية
2. 🔊 **استمع للصوت** باستخدام زر "استمع للدرس" (يعمل في المتصفح)
3. 📝 **طبّق ما تعلمته** على أمثلة واقعية
4. 🤖 **اطرح أسئلتك** هنا للحصول على توضيحات

💡 **نصيحة:** أضف مفتاح API من Groq للحصول على إجابات ذكية ومفصلة من المرشد الذكي.""",

            "لماذا": f"""🤔 **لماذا {lesson_title} مهم؟**

هذا الموضوع يُعتبر حجر الزاوية في **{course_title}**. فهمه يساعدك على:
- بناء أساس قوي للمواضيع المتقدمة
- فهم التطبيقات العملية في العالم الحقيقي
- التحضير للمشاريع والوظائف في مجال الذكاء الاصطناعي

🎯 **لشرح أعمق:** فعّل المرشد الذكي عبر إضافة مفتاح Groq API."""
        },
        "fr": {
            "default": f"""Bonjour ! 👋 Je suis votre mentor IA pour : **{course_title}** - **{lesson_title}**.

🎯 **Pour obtenir des réponses intelligentes :**
1. Allez sur **console.groq.com**
2. Créez un compte gratuit (sans carte de crédit)
3. Copiez la clé API dans la barre latérale

💡 **Pour l'instant :** Je peux répondre à vos questions de base. Le contenu complet est dans l'onglet "📚 Cours".""",

            "qu'est-ce": f"""📚 **{lesson_title}** - Sujet fondamental dans **{course_title}**

Cette leçon couvre les concepts essentiels de l'IA. Il est recommandé de lire le contenu complet disponible dans la page de la leçon et d'écouter l'explication audio.

🎯 **Pour une explication détaillée :**
Ajoutez une clé API Groq dans la barre latérale pour des réponses intelligentes et personnalisées.""",

            "comment": f"""🎓 **Comment apprendre {lesson_title} :**

1. ✅ **Lisez le contenu** de la leçon attentivement
2. 🔊 **Écoutez l'audio** avec le bouton "Écouter la leçon" (fonctionne dans le navigateur)
3. 📝 **Appliquez** ce que vous avez appris sur des exemples réels
4. 🤖 **Posez vos questions** ici pour des clarifications

💡 **Conseil :** Ajoutez une clé API Groq pour des réponses intelligentes du mentor IA."""
        },
        "en": {
            "default": f"""Hello! 👋 I am your AI mentor for: **{course_title}** - **{lesson_title}**.

🎯 **To get smart, detailed answers:**
1. Go to **console.groq.com**
2. Sign up for a free account (no credit card)
3. Copy the API key to the sidebar

💡 **For now:** I can answer your basic questions. Full content is in the "📚 Courses" tab.""",

            "what is": f"""📚 **{lesson_title}** - Fundamental topic in **{course_title}**

This lesson covers essential AI concepts. Please read the full content available in the lesson page and listen to the audio explanation.

🎯 **For detailed explanation:**
Add a Groq API key in the sidebar for smart, personalized answers.""",

            "how": f"""🎓 **How to learn {lesson_title}:**

1. ✅ **Read the content** carefully
2. 🔊 **Listen to audio** using the "Listen to lesson" button (works in browser)
3. 📝 **Apply** what you learned to real examples
4. 🤖 **Ask questions** here for clarifications

💡 **Tip:** Add a Groq API key for smart answers from the AI mentor."""
        }
    }

    lang_responses = responses.get(lang, responses["en"])

    # Check for keywords in question
    question_lower = question.lower()
    if any(kw in question_lower for kw in ["ما هو", "qu'est-ce", "what is", "ما هي", "c'est quoi", "what's", "define", "définition"]):
        return lang_responses.get("ما هو", lang_responses.get("qu'est-ce", lang_responses.get("what is", lang_responses["default"])))
    elif any(kw in question_lower for kw in ["كيف", "comment", "how", "how to", "comment faire"]):
        return lang_responses.get("كيف", lang_responses.get("comment", lang_responses.get("how", lang_responses["default"])))
    elif any(kw in question_lower for kw in ["لماذا", "pourquoi", "why", "pour quoi"]):
        return lang_responses.get("لماذا", lang_responses["default"])
    else:
        return lang_responses["default"]

# ═══════════════════════════════════════════════════════════════════════════════
# UI FUNCTIONS - PAGES
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

        # Groq API Key input in sidebar
        st.markdown(f"<div style='color: #888; font-size: 11px; margin-bottom: 4px;'>{t['groq_key_label']}</div>", unsafe_allow_html=True)
        current_key = st.session_state.get("groq_api_key", "")
        new_key = st.text_input("", value=current_key, type="password", 
                                placeholder="gsk_...", label_visibility="collapsed", key="groq_key_input")
        if new_key != current_key:
            st.session_state.groq_api_key = new_key
            st.rerun()

        st.markdown(f"<div style='color: #666; font-size: 10px; margin-bottom: 12px;'>{t['groq_key_help']}</div>", unsafe_allow_html=True)

        # Show mentor status
        mentor = CloudAIClient()
        if mentor.is_available:
            st.markdown(f"<div style='color: #4CAF50; font-size: 11px; margin-bottom: 8px;'>🟢 {t['mentor_online']}</div>", unsafe_allow_html=True)
        else:
            st.markdown(f"<div style='color: #FF9800; font-size: 11px; margin-bottom: 8px;'>🟡 {t['mentor_demo']}</div>", unsafe_allow_html=True)

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
            st.session_state.lesson_chat = []
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
# MAIN PAGES
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
    """Lesson page with browser TTS and cloud AI mentor"""
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

    # Header with navigation
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

    # Lesson title
    st.markdown(f"""
    <div class="lesson-card">
        <div class="lesson-title">{lesson['title']}</div>
        <div style="color: #888; font-size: 13px; margin-bottom: 16px;">
            ⏱️ {t['lesson_duration']} : {lesson['duration']}
        </div>
    </div>
    """, unsafe_allow_html=True)

    # TTS Section - Browser-based (no local dependencies)
    st.markdown("<hr>", unsafe_allow_html=True)
    st.subheader("🔊 " + t['listen_lesson'])

    col_tts1, col_tts2 = st.columns([1, 3])
    with col_tts1:
        if st.button("▶️ " + t['tts_browser'], type="secondary", use_container_width=True, key="tts_browser_btn"):
            # Inject JavaScript for browser TTS
            tts_html = get_browser_tts_html(lesson['content'], lang)
            st.html(tts_html, unsafe_allow_javascript=True)
            st.success("🔊 Lecture en cours...")

    st.markdown(get_tts_status_indicator(), unsafe_allow_html=True)

    st.markdown("<hr>", unsafe_allow_html=True)

    # Lesson content
    st.subheader("📖 " + t['lesson_content'])
    st.markdown(f'<div class="lesson-content">{lesson["content"].replace(chr(10), "<br>")}</div>', unsafe_allow_html=True)

    st.markdown("<hr>", unsafe_allow_html=True)

    # Mark complete button
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

    # AI Mentor Section - Cloud-based
    st.subheader("🤖 " + t['ask_about_lesson'])

    # Show mentor status
    mentor = CloudAIClient()
    if mentor.is_available:
        st.markdown(f"<div style='color: #4CAF50; font-size: 13px; margin-bottom: 8px;'>{t['mentor_online']}</div>", unsafe_allow_html=True)
    else:
        st.info(f"🟡 {t['mentor_demo']}")
        st.markdown(f"<div style='font-size: 12px; color: #888; margin-bottom: 12px;'>{t['groq_key_help']}</div>", unsafe_allow_html=True)

    if "lesson_chat" not in st.session_state:
        st.session_state.lesson_chat = []

    # Display chat history
    for msg in st.session_state.lesson_chat:
        role_class = "chat-user" if msg["role"] == "user" else "chat-assistant"
        avatar = "👤" if msg["role"] == "user" else "🤖"
        st.markdown(f"""
        <div style="display: flex; align-items: flex-start; margin: 8px 0;">
            <div style="width: 36px; height: 36px; border-radius: 50%; display: flex; align-items: center; justify-content: center; font-size: 18px; margin-right: 8px; background: {'linear-gradient(135deg, #667eea 0%, #764ba2 100%)' if msg['role'] == 'user' else '#f0f0f0'};">{avatar}</div>
            <div class="chat-message {role_class}">{msg['content']}</div>
        </div>
        """, unsafe_allow_html=True)

    # Chat input
    col_chat1, col_chat2 = st.columns([5, 1])
    with col_chat1:
        user_question = st.text_input("", placeholder=t['chat_placeholder'], label_visibility="collapsed", key="lesson_chat_input")
    with col_chat2:
        send_clicked = st.button(t['send'], type="primary", use_container_width=True)

    if send_clicked and user_question.strip():
        st.session_state.lesson_chat.append({"role": "user", "content": user_question})

        with st.spinner(t['thinking']):
            mentor = CloudAIClient()
            if mentor.is_available:
                system_prompt = get_system_prompt(
                    lang=lang,
                    course_title=course['title'],
                    lesson_title=lesson['title'],
                    lesson_content=lesson['content']
                )
                messages = []
                for msg in st.session_state.lesson_chat[-10:]:
                    messages.append({"role": msg["role"], "content": msg["content"]})

                response = mentor.chat(messages, system_prompt=system_prompt)
                if response:
                    st.session_state.lesson_chat.append({"role": "assistant", "content": response})
                else:
                    st.session_state.lesson_chat.append({"role": "assistant", "content": "Desole, je n'ai pas pu generer de reponse."})
            else:
                # Demo mode - predefined responses
                demo_response = get_demo_response(user_question, lang, course['title'], lesson['title'])
                st.session_state.lesson_chat.append({"role": "assistant", "content": demo_response})
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

    # Show mentor status
    mentor = CloudAIClient()
    if mentor.is_available:
        st.markdown(f"<div style='color: #4CAF50; font-size: 14px; margin-bottom: 16px; text-align: center;'>{t['mentor_online']}</div>", unsafe_allow_html=True)
    else:
        st.info(f"🟡 {t['mentor_demo']}")
        st.markdown(f"<div style='font-size: 12px; color: #888; margin-bottom: 16px; text-align: center;'>{t['groq_key_help']}</div>", unsafe_allow_html=True)

    if "chat_history" not in st.session_state:
        st.session_state.chat_history = []

    courses = COURSES[lang]
    course_options = {t['no_course']: None}
    for course in courses:
        course_options[course['title']] = course

    selected_course_title = st.selectbox(t['select_course_chat'], options=list(course_options.keys()), index=0)
    selected_course = course_options[selected_course_title]

    # Display chat history
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
            mentor = CloudAIClient()
            if mentor.is_available:
                system = f"Tu es un mentor IA expert en intelligence artificielle. Tu aides les etudiants a apprendre. Sois pedagogique et clair.\n\nContexte du cours: {context}"
                messages = []
                for msg in st.session_state.chat_history[-10:]:
                    messages.append({"role": msg["role"], "content": msg["content"]})

                response = mentor.chat(messages, system_prompt=system)
                if response:
                    st.session_state.chat_history.append({"role": "assistant", "content": response})
                else:
                    st.session_state.chat_history.append({"role": "assistant", "content": "Desole, je n'ai pas pu generer de reponse."})
            else:
                # Demo mode
                demo_response = get_demo_response(user_input, lang, selected_course['title'] if selected_course else "AI", "General")
                st.session_state.chat_history.append({"role": "assistant", "content": demo_response})
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
# INITIALIZATION & ENTRY POINT
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
        "groq_api_key": "",
    }
    for key, value in defaults.items():
        if key not in st.session_state:
            st.session_state[key] = value

    # Lesson progress
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
