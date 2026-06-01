# 🎓 AI Learning Hub

Plateforme d'apprentissage interactive de l'Intelligence Artificielle propulsée par Streamlit.

## ✨ Fonctionnalités

- **🔐 Système d'Activation** : Clé sécurisée pour l'accès au contenu
- **📚 Catalogue de Cours** : 6 modules complets couvrant ML, Deep Learning, NLP, Vision, RL et MLOps
- **🤖 Mentor IA Local** : Intégration Ollama/LangChain avec LLM local
- **📊 Suivi de Progression** : Barres de progression et statistiques détaillées
- **🌍 Multilingue** : Interface en Français, Anglais et Arabe (avec support RTL)
- **📱 Design Responsive** : Interface moderne inspirée des LMS professionnels

## 🚀 Installation

### 1. Cloner le projet
```bash
git clone <repository-url>
cd ai_learning_app
```

### 2. Créer un environnement virtuel
```bash
python -m venv venv

# Windows
venv\Scripts\activate

# Linux/Mac
source venv/bin/activate
```

### 3. Installer les dépendances
```bash
pip install -r requirements.txt
```

### 4. (Optionnel) Configurer Ollama pour le Mentor IA
```bash
# Installer Ollama
curl -fsSL https://ollama.com/install.sh | sh

# Télécharger un modèle (ex: llama3.2)
ollama pull llama3.2

# Démarrer le serveur
ollama serve
```

## 🎮 Lancement

```bash
streamlit run app.py
```

L'application sera accessible à l'adresse : `http://localhost:8501`

## 🔑 Clé d'Activation

La clé d'activation par défaut est : **`22459129071981`**

## 📁 Structure du Projet

```
ai_learning_app/
├── app.py                 # Point d'entrée principal
├── config.py              # Configuration et données
├── requirements.txt       # Dépendances
├── README.md             # Documentation
└── utils/
    ├── __init__.py
    ├── styles.py          # CSS personnalisé
    ├── components.py      # Composants UI réutilisables
    └── ollama_client.py   # Client Ollama/LangChain
```

## 🌐 Langues Supportées

| Langue | Code | Direction |
|--------|------|-----------|
| Français | `fr` | LTR |
| English | `en` | LTR |
| العربية | `ar` | RTL |

## 📚 Modules de Cours

1. **Introduction au Machine Learning** (Débutant - 8h)
2. **Deep Learning Fondamental** (Intermédiaire - 12h)
3. **Traitement du Langage Naturel (NLP)** (Avancé - 10h)
4. **Vision par Ordinateur** (Intermédiaire - 10h)
5. **Apprentissage par Renforcement** (Avancé - 14h)
6. **MLOps et Déploiement** (Intermédiaire - 8h)

## 🛠️ Technologies

- **Streamlit** : Framework web interactif
- **Ollama** : LLM local (llama3.2)
- **Python** : Langage principal
- **CSS3** : Styles personnalisés

## 📝 Licence

MIT License - 2026 AI Learning Hub
