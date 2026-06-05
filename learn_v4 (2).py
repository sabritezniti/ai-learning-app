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
                    "content": """Le Machine Learning (ML) est une branche de l'Intelligence Artificielle qui permet aux ordinateurs d'apprendre automatiquement a partir de donnees, sans etre explicitement programmes pour chaque tache.

🔑 DEFINITION CLEE :
Traditionnellement, un programmeur ecrit des regles explicites (SI temperature > 30 ALORS afficher 'chaud'). Avec le ML, on montre des milliers d'exemples au modele, et il DECOUVRE lui-meme les regles.

📊 LES 3 TYPES FONDAMENTAUX :

1. APPRENTISSAGE SUPERVISE
   - On fournit des donnees ETIQUETEES (entree + bonne reponse)
   - Exemple : 10 000 photos de chats et chiens, chacune avec son etiquette
   - Le modele apprend la correspondance entree → sortie
   - Usages : classification d'emails (spam/normal), prediction de prix

2. APPRENTISSAGE NON SUPERVISE
   - Donnees SANS etiquettes : le modele trouve des structures cachees seul
   - Exemple : grouper des clients par comportement d'achat sans les avoir definis
   - Usages : segmentation, detection d'anomalies, compression de donnees

3. APPRENTISSAGE PAR RENFORCEMENT
   - Un AGENT apprend par essais-erreurs dans un environnement
   - Il recoit des RECOMPENSES (+) ou PENALITES (-) selon ses actions
   - Exemple : AlphaGo apprend a jouer aux echecs en jouant des milliers de parties
   - Usages : robotique, jeux video, trading algorithmique

🌍 APPLICATIONS REELLES :
• Reconnaissance faciale (Face ID sur iPhone)
• Recommandations Netflix / Spotify / YouTube
• Detection de fraudes bancaires en temps reel
• Voitures autonomes (Tesla Autopilot)
• Traduction automatique (Google Translate)
• Assistants vocaux (Siri, Alexa, Google Assistant)
• Diagnostic medical (detection de cancers sur IRM)

💡 ANALOGIE PEDAGOGIQUE :
Le ML c'est comme apprendre a reconnaitre un chien. Un enfant voit des centaines de chiens (donnees), apprend progressivement leurs caracteristiques (pattes, museau, fourrure), et finit par reconnaitre un chien qu'il n'a jamais vu. C'est exactement ce que fait un modele ML.""",
                    "duration": "45 min"
                },
                {
                    "title": "Types d'apprentissage",
                    "content": """Dans cette lecon, nous approfondissons chaque type d'apprentissage avec des exemples concrets et les algorithmes associes.

🟢 APPRENTISSAGE SUPERVISE — "Apprendre avec un professeur"

Comment ca marche :
  Donnees d'entree (X) + Etiquettes correctes (Y) → Le modele apprend f(X) = Y

Deux grandes categories :
  a) CLASSIFICATION : predire une CATEGORIE discrete
     - Exemple : email → [spam, normal]
     - Exemple : photo → [chat, chien, oiseau]
     - Algorithmes : KNN, SVM, Arbre de decision, Random Forest, Reseau de neurones

  b) REGRESSION : predire une VALEUR continue
     - Exemple : surface + quartier → prix du logement en euros
     - Exemple : temperature d'hier → temperature de demain
     - Algorithmes : Regression lineaire, Ridge, Lasso, Gradient Boosting

🟡 APPRENTISSAGE NON SUPERVISE — "Apprendre sans professeur"

Pas d'etiquettes ! Le modele decouvre des structures cachees dans les donnees.

  a) CLUSTERING (Regroupement) :
     - K-Means : divise les donnees en K groupes compacts
     - DBSCAN : trouve des groupes de forme arbitraire
     - Hierarchical : construit un arbre de similarite

  b) REDUCTION DE DIMENSIONNALITE :
     - PCA : compresse les donnees en gardant l'essentiel
     - t-SNE : visualise des donnees complexes en 2D/3D
     - Autoencoders : compression neuronale non lineaire

  c) REGLES D'ASSOCIATION :
     - Trouver des correlations : "Les gens qui achetent X achetent aussi Y"
     - Algorithme Apriori pour les paniers d'achat

🔴 APPRENTISSAGE PAR RENFORCEMENT — "Apprendre par experience"

Composants cles :
  • Agent : le modele qui prend des decisions
  • Environnement : le monde dans lequel l'agent agit
  • Etat (s) : description de la situation actuelle
  • Action (a) : ce que l'agent peut faire
  • Recompense (r) : signal de feedback (+/-) apres chaque action
  • Politique (π) : strategie que l'agent suit

Boucle d'apprentissage :
  Agent observe l'etat → choisit une action → recoit une recompense → met a jour sa strategie

Algorithmes : Q-Learning, DQN (Deep Q-Network), PPO, A3C

📋 TABLEAU COMPARATIF :
Type              | Donnees      | Objectif               | Exemple
Supervise         | Etiquetees   | Predire la sortie      | Spam ou pas ?
Non supervise     | Non etiquetees | Trouver des patterns | Segmenter clients
Renforcement      | Interactions | Maximiser recompense   | Jouer aux echecs""",
                    "duration": "50 min"
                },
                {
                    "title": "Regression lineaire",
                    "content": """La regression lineaire est l'un des algorithmes les plus fondamentaux du ML. Elle modélise la relation entre une variable de sortie (Y) et une ou plusieurs variables d'entree (X).

📐 LA FORMULE MATHEMATIQUE :

Regression lineaire SIMPLE (1 variable) :
   y = mx + b
   • y = valeur predite (ex: prix d'une maison)
   • x = variable d'entree (ex: surface en m²)
   • m = pente (coefficient) : combien y augmente quand x augmente de 1
   • b = ordonnee a l'origine (biais) : valeur de y quand x = 0

Regression lineaire MULTIPLE (plusieurs variables) :
   y = w₁x₁ + w₂x₂ + ... + wₙxₙ + b
   Ex: prix = 2500 × surface + 15000 × nb_chambres - 5000 × anciennete + 50000

🎯 COMMENT LE MODELE APPREND — La Methode des Moindres Carres :

Objectif : trouver la droite qui passe AU PLUS PRES de tous les points.

   Erreur = Σ (valeur_reelle - valeur_predite)²
   
On minimise cette somme des erreurs au carre (MSE) pour trouver les meilleurs m et b.

Pourquoi au CARRE ? Pour :
  1. Rendre toutes les erreurs positives
  2. Penaliser davantage les grandes erreurs

📏 METRIQUES D'EVALUATION :

• R² (coefficient de determination) : entre 0 et 1
  - R² = 1 → modele parfait, explique 100% de la variance
  - R² = 0.85 → le modele explique 85% de la variation des donnees
  - R² < 0 → le modele est pire que la moyenne !

• MAE (Mean Absolute Error) : erreur moyenne en valeur absolue
  - Facile a interpreter : "en moyenne, je me trompe de X euros"

• RMSE (Root Mean Square Error) : penalise plus les grandes erreurs
  - Meme unite que y, mais plus sensible aux outliers

💡 EXEMPLE CONCRET — Prediction du prix d'une maison :
   Donnees : 1000 maisons avec surface, nb_chambres, quartier, prix

   Apres entrainement, le modele trouve :
   prix = 2800 × surface + 12000 × nb_chambres + 30000 × (quartier_premium) + 40000

   Pour une maison de 80m², 3 chambres, quartier normal :
   prix = 2800×80 + 12000×3 + 0 + 40000 = 224000 + 36000 + 40000 = 300 000 €

⚠️ HYPOTHESES ET LIMITES :
   • Suppose une relation LINEAIRE (si la vraie relation est courbe → probleme)
   • Sensible aux OUTLIERS (valeurs extremes)
   • Ne capture pas les interactions complexes entre variables
   • Pour les relations non-lineaires : utiliser Polynomial Regression, Random Forest, etc.

🐍 CODE PYTHON (scikit-learn) :
   from sklearn.linear_model import LinearRegression
   from sklearn.metrics import r2_score, mean_absolute_error

   model = LinearRegression()
   model.fit(X_train, y_train)        # Entrainement
   y_pred = model.predict(X_test)     # Prediction
   print(f"R² = {r2_score(y_test, y_pred):.3f}")""",
                    "duration": "55 min"
                },
                {
                    "title": "Classification avec KNN",
                    "content": """K-Nearest Neighbors (KNN) est un algorithme intuitif qui classe un nouvel element en regardant les K elements les plus proches dans les donnees d'entrainement.

🧠 L'INTUITION :
"Dis-moi qui sont tes voisins, je te dirai qui tu es"
→ Un point est classifie par VOTE MAJORITAIRE parmi ses K plus proches voisins.

📍 COMMENT CA MARCHE (etape par etape) :

1. Pour un nouveau point a classifier :
2. Calculer la DISTANCE avec tous les points d'entrainement
3. Selectionner les K points les plus proches (voisins)
4. Faire un VOTE : la classe majoritaire parmi les K voisins est la prediction
5. (Pour la regression : faire la MOYENNE des valeurs des K voisins)

📏 LES DISTANCES — Comment mesurer la "proximite" ?

• Distance EUCLIDIENNE (la plus courante) :
  d = √[(x₁-x₂)² + (y₁-y₂)²]
  → La distance "a vol d'oiseau" en geometrie classique

• Distance de MANHATTAN :
  d = |x₁-x₂| + |y₁-y₂|
  → Comme se deplacer dans un quadrillage de rues

• Distance de MINKOWSKI : generalisation des deux precedentes

🔢 CHOISIR K — L'hyperparametres le plus important :

• K PETIT (ex: K=1) :
  → Modele tres complexe, s'adapte trop aux donnees d'entrainement
  → Risque d'OVERFITTING (surajustement) : mauvaise generalisation
  → Frontiere de decision tres irreguliere

• K GRAND (ex: K=100) :
  → Modele trop simple, ignore les details importants
  → Risque d'UNDERFITTING (sous-ajustement)
  → Frontiere de decision trop lisse

• K OPTIMAL : trouver par VALIDATION CROISEE (Cross-Validation)
  → Tester K = 1, 3, 5, 7, 11, ... et garder le meilleur

💡 REGLE PRATIQUE : K impair pour eviter les ex aequo en classification binaire.

✅ AVANTAGES :
• Tres simple a comprendre et implementer
• Aucun entrainement ! (algorithme "lazy")
• Naturellement adapte aux problemes multi-classes
• Peut apprendre des frontieres de decision complexes

❌ LIMITES :
• LENT a la prediction : calcule toutes les distances a chaque fois (O(n×d))
• Sensible a l'ECHELLE : normaliser les donnees est OBLIGATOIRE
• Sensible aux dimensions irrelevantes (fledu de la dimensionalite)
• Necessite de stocker TOUT le dataset en memoire

🔄 PREPROCESSING OBLIGATOIRE — Normalisation :
  Sans normalisation : si surface = 80 et prix = 200000, la distance est dominee par le prix !
  Avec StandardScaler : toutes les features ont meme importance.

  from sklearn.preprocessing import StandardScaler
  scaler = StandardScaler()
  X_train_scaled = scaler.fit_transform(X_train)
  X_test_scaled = scaler.transform(X_test)

🐍 CODE PYTHON :
  from sklearn.neighbors import KNeighborsClassifier
  model = KNeighborsClassifier(n_neighbors=5, metric='euclidean')
  model.fit(X_train_scaled, y_train)
  y_pred = model.predict(X_test_scaled)""",
                    "duration": "50 min"
                },
                {
                    "title": "Clustering avec K-Means",
                    "content": """K-Means est l'algorithme de clustering (regroupement) le plus populaire. Il divise les donnees en K groupes (clusters) de maniere a ce que les points d'un meme groupe soient aussi similaires que possible.

🎯 OBJECTIF :
Minimiser la somme des distances des points a leur centre de cluster (centroid).
  Minimiser : Σ Σ ||x - μₖ||²

💡 ANALOGIE :
Imaginez 1000 eleves qu'on veut repartir en K classes. K-Means trouve automatiquement les regroupements les plus homogenes basés sur leurs profils academiques.

🔄 ALGORITHME ITERATIF (4 etapes) :

ETAPE 1 — INITIALISATION :
   Choisir aleatoirement K points comme centres initiaux (centroids)
   (Methode avancee : K-Means++ qui choisit des centres bien espaces)

ETAPE 2 — ATTRIBUTION :
   Assigner chaque point au cluster dont le centroid est le plus proche
   Pour chaque point x : cluster = argmin_k ||x - μₖ||²

ETAPE 3 — MISE A JOUR :
   Recalculer les centroids comme la MOYENNE de tous les points du cluster
   μₖ = (1/|Cₖ|) × Σ x  pour x dans Cₖ

ETAPE 4 — CONVERGENCE :
   Repeter les etapes 2 et 3 jusqu'a ce que les clusters ne changent plus
   (ou apres un nombre max d'iterations)

🔢 CHOISIR K — La Methode du COUDE (Elbow Method) :

On calcule l'inertie (somme des distances² internes) pour K = 1, 2, 3, ..., 10.
On trace une courbe et on cherche le "coude" = point ou l'amelioration ralentit.

Exemple :
   K=1 : inertie = 1000
   K=2 : inertie = 500  (gain de 500)
   K=3 : inertie = 280  (gain de 220)
   K=4 : inertie = 200  (gain de 80)  ← COUDE ici, K=3 ou 4 optimal
   K=5 : inertie = 180  (gain de 20)

✅ AVANTAGES :
• Simple et rapide (O(n×K×i×d))
• Fonctionne bien avec des clusters spheriques et bien separes
• Scalable pour de grandes donnees

❌ LIMITES :
• Doit specifier K a l'avance
• Sensible a l'initialisation aleatoire → utiliser K-Means++
• Ne gere pas les clusters de formes non-spheriques
• Sensible aux outliers (les valeurs extremes deplacent les centroids)
• Ne fonctionne pas bien si les clusters ont des tailles tres differentes

🌍 APPLICATIONS REELLES :

1. SEGMENTATION MARKETING :
   Regrouper les clients par comportement (frequence d'achat, panier moyen, etc.)
   → Adapter les campagnes publicitaires a chaque segment

2. COMPRESSION D'IMAGES :
   Remplacer chaque couleur par la couleur du centroid le plus proche
   → Reduire de 16M couleurs a seulement K couleurs

3. DETECTION D'ANOMALIES :
   Les points tres eloignes de tout centroid sont suspects

4. PREPARATION DE DONNEES :
   Utiliser les assignations de cluster comme nouvelles features

🐍 CODE PYTHON :
  from sklearn.cluster import KMeans
  import matplotlib.pyplot as plt

  # Trouver le K optimal
  inerties = []
  for k in range(1, 11):
      kmeans = KMeans(n_clusters=k, init='k-means++', n_init=10)
      kmeans.fit(X)
      inerties.append(kmeans.inertia_)

  # Modele final
  kmeans = KMeans(n_clusters=4, init='k-means++', n_init=10, random_state=42)
  labels = kmeans.fit_predict(X)
  centres = kmeans.cluster_centers_""",
                    "duration": "55 min"
                },
                {
                    "title": "Evaluation des modeles",
                    "content": """L'evaluation des modeles est une etape cruciale pour s'assurer que notre modele generalisera bien sur de nouvelles donnees, et pas seulement sur celles qu'il a vues.

📂 SEPARATION DES DONNEES — La Regle d'Or :

On divise TOUJOURS le dataset en 3 parties :
• TRAIN (70%) : apprendre les parametres du modele
• VALIDATION (15%) : choisir les hyperparametres et comparer les modeles
• TEST (15%) : evaluation finale (toucher UNE SEULE FOIS a la fin !)

⚠️ ERREUR CLASSIQUE : utiliser les donnees de test pour optimiser → les resultats seront trop optimistes !

📊 METRIQUES DE CLASSIFICATION :

Exemple : detection de cancer (Positif = malade, Negatif = sain)

La Matrice de Confusion (pour 100 patients) :
                  | Predit Positif | Predit Negatif |
  Reel Positif   |   TP = 40     |   FN = 10     |
  Reel Negatif   |   FP = 5      |   TN = 45     |

• ACCURACY (Precision globale) = (TP+TN) / Total = 85/100 = 85%
  ⚠️ Probleme : si 95% des emails sont normaux, un modele qui predit "normal" a chaque fois a 95% d'accuracy !

• PRECISION = TP / (TP + FP) = 40/45 = 88.9%
  "Parmi ceux que j'ai identifies comme malades, combien l'etaient vraiment ?"

• RECALL (Sensibilite) = TP / (TP + FN) = 40/50 = 80%
  "Parmi tous les vrais malades, combien ai-je detectes ?"
  → Critique en medical : rater un malade est tres grave (FN dangereux)

• F1-SCORE = 2 × (Precision × Recall) / (Precision + Recall)
  → Equilibre entre Precision et Recall, utile quand les classes sont desequilibrees

• ROC-AUC : aire sous la courbe ROC (taux vrais positifs vs faux positifs)
  → AUC = 1.0 : modele parfait | AUC = 0.5 : modele aleatoire

🎭 OVERFITTING vs UNDERFITTING — Les 2 ennemis :

UNDERFITTING (Sous-ajustement) :
  → Le modele est TROP SIMPLE pour capturer la complexite des donnees
  → Mauvais sur train ET sur test
  → Solutions : modele plus complexe, plus de features, moins de regularisation

OVERFITTING (Surajustement) :
  → Le modele a MEMORISE les donnees d'entrainement (bruit inclus)
  → Excellent sur train, mauvais sur test
  → Solutions : plus de donnees, regularisation (L1/L2), Dropout, validation croisee

🔄 VALIDATION CROISEE K-FOLD :

Au lieu d'une seule separation train/test, on fait K rotations :
  Fold 1 : [TEST] [TRAIN] [TRAIN] [TRAIN] [TRAIN]
  Fold 2 : [TRAIN] [TEST] [TRAIN] [TRAIN] [TRAIN]
  ...
  Score final = MOYENNE des K scores → estimation plus fiable !

⚖️ BIAIS-VARIANCE TRADEOFF :

• BIAIS : erreur systematique (modele trop simple)
• VARIANCE : sensibilite aux fluctuations des donnees (modele trop complexe)
• On cherche le JUSTE MILIEU ou les deux sont faibles

🐍 CODE PYTHON :
  from sklearn.model_selection import cross_val_score, train_test_split
  from sklearn.metrics import classification_report, confusion_matrix

  X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

  # Validation croisee
  scores = cross_val_score(model, X_train, y_train, cv=5, scoring='f1')
  print(f"F1 moyen : {scores.mean():.3f} ± {scores.std():.3f}")

  # Rapport complet
  y_pred = model.predict(X_test)
  print(classification_report(y_test, y_pred))""",
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
                    "content": """Le perceptron est la brique elementaire de tous les reseaux de neurones. Comprendre son fonctionnement est essentiel pour maitriser le deep learning.

🧠 INSPIRATION BIOLOGIQUE :
Un neurone biologique recoit des signaux de ses dendrites, les cumule, et si le seuil est depasse, envoie un signal par son axone. Le perceptron artificiel s'inspire de ce mecanisme.

📐 LE PERCEPTRON — FORMULE COMPLETE :

  sortie = f( w₁×x₁ + w₂×x₂ + ... + wₙ×xₙ + b )

Decryptage :
• x₁, x₂, ..., xₙ = entrees (features du probleme)
• w₁, w₂, ..., wₙ = poids (importance de chaque entree)
• b = biais (permet de decaler la frontiere de decision)
• f = fonction d'activation (introduit la non-linearite)
• La somme w×x + b = COMBINAISON LINEAIRE (produit scalaire)

💡 EXEMPLE CONCRET :
  Detection de spam (2 features) :
  - x₁ = nombre de mots-cles suspects (ex: "argent", "gratuit")
  - x₂ = taille de l'email en mots

  Apres entrainement : w₁ = 0.8, w₂ = -0.3, b = -1.5
  Pour un email (x₁=3, x₂=50) :
  z = 0.8×3 + (-0.3)×50 + (-1.5) = 2.4 - 15 - 1.5 = -14.1
  sortie = sigmoid(-14.1) ≈ 0 → PAS SPAM

🏗️ RESEAUX MULTICOUCHES (MLP - Multi-Layer Perceptron) :

Un seul perceptron ne peut resoudre que des problemes lineairement separables.
La solution : empiler plusieurs perceptrons en COUCHES :

  Couche d'ENTREE → Couches CACHEES → Couche de SORTIE

Architecture typique pour classification d'images :
  784 entrees (28×28 pixels) → [256] → [128] → [64] → 10 sorties (chiffres 0-9)

FORWARD PROPAGATION (propagation avant) :
  A chaque couche : z = W × a + b, puis a = f(z)
  Les activations se propagent couche par couche jusqu'a la sortie.

🌐 THEOREME D'APPROXIMATION UNIVERSELLE :
Un MLP avec UNE SEULE couche cachee suffisamment grande peut approximer TOUTE fonction continue.
→ Theoriquement, un reseau de neurones peut apprendre n'importe quoi !
→ En pratique : les reseaux PROFONDS (plusieurs couches) apprennent mieux avec moins de neurones.

📊 REPRESENTATION VECTORIELLE :
Avec des matrices, le calcul de toute une couche est :
   A[l] = f( W[l] × A[l-1] + b[l] )
→ Tres efficace avec GPU et bibliotheques comme NumPy/TensorFlow/PyTorch

🐍 CODE PYTHON (PyTorch) :
  import torch
  import torch.nn as nn

  class MLP(nn.Module):
      def __init__(self):
          super().__init__()
          self.couches = nn.Sequential(
              nn.Linear(784, 256),
              nn.ReLU(),
              nn.Linear(256, 128),
              nn.ReLU(),
              nn.Linear(128, 10),
              nn.Softmax(dim=1)
          )

      def forward(self, x):
          return self.couches(x)""",
                    "duration": "60 min"
                },
                {
                    "title": "Fonction d'activation et backpropagation",
                    "content": """Les fonctions d'activation et la backpropagation sont les deux mecanismes qui permettent aux reseaux de neurones d'apprendre des representations complexes.

⚡ FONCTIONS D'ACTIVATION — Pourquoi sont-elles necessaires ?

Sans fonction d'activation, empiler des couches lineaires donnera TOUJOURS un resultat lineaire (Ax + b). La non-linearite permet de modeliser des frontieres de decision complexes.

Les principales fonctions :

1. ReLU (Rectified Linear Unit) — La plus populaire aujourd'hui :
   f(x) = max(0, x)
   • Derivee : 1 si x > 0, 0 sinon
   ✅ Rapide a calculer, evite le vanishing gradient pour x > 0
   ❌ "Neurones morts" : si un neurone a toujours une entree negative, son gradient = 0

2. Sigmoid :
   f(x) = 1 / (1 + e^{-x}) → sortie entre 0 et 1
   ✅ Ideal pour la sortie en classification binaire (probabilite)
   ❌ Vanishing gradient pour des valeurs extremes (|x| >> 0, derivee ≈ 0)

3. Tanh (Tangente Hyperbolique) :
   f(x) = (e^x - e^{-x}) / (e^x + e^{-x}) → sortie entre -1 et 1
   ✅ Centree sur zero (meilleure convergence que sigmoid)
   ❌ Meme probleme de vanishing gradient

4. Variantes modernes :
   • Leaky ReLU : f(x) = max(0.01x, x) → resout les neurones morts
   • GELU : utilisee dans BERT, GPT → plus douce que ReLU
   • Swish : f(x) = x × sigmoid(x) → souvent mieux que ReLU en pratique

🔄 BACKPROPAGATION — Comment le reseau apprend :

La backpropagation est l'algorithme qui calcule comment modifier chaque poids pour reduire l'erreur. Elle utilise la REGLE DE CHAINE du calcul differentiel.

ETAPES :

1. FORWARD PASS : calculer la prediction y_pred
2. CALCULER LA PERTE (Loss) :
   - Classification : Cross-Entropy Loss = -Σ y × log(y_pred)
   - Regression : MSE = (1/n) × Σ (y - y_pred)²
3. BACKWARD PASS : calculer ∂Loss/∂w pour chaque poids w
4. MISE A JOUR des poids :
   w = w - α × ∂Loss/∂w
   (α = learning rate, taux d'apprentissage)

📉 DESCENTE DE GRADIENT :
Imaginez une sphere sur une montagne brumeuse cherchant la vallee (minimum de perte) :
• Gradient = direction de la pente la plus raide (vers le haut)
• On va dans la direction OPPOSEE au gradient (vers le bas)
• Learning rate α = taille du pas

VARIANTES de l'optimiseur :
• SGD (Stochastic Gradient Descent) : 1 exemple a la fois
• Mini-batch SGD : par lots de 32/64/128 exemples (le standard)
• Momentum : accumule les gradients passes pour accelerer
• Adam (Adaptive Moment Estimation) : combine Momentum + taux adaptatif par poids
  → Adam est le plus utilise en pratique !

🐍 CODE PYTORCH :
  criterion = nn.CrossEntropyLoss()
  optimizer = torch.optim.Adam(model.parameters(), lr=0.001)

  for epoch in range(100):
      optimizer.zero_grad()         # Reinitialiser les gradients
      y_pred = model(X_batch)       # Forward pass
      loss = criterion(y_pred, y)   # Calculer la perte
      loss.backward()               # Backpropagation
      optimizer.step()              # Mise a jour des poids""",
                    "duration": "65 min"
                },
                {
                    "title": "Reseaux convolutifs CNN",
                    "content": """Les reseaux de neurones convolutifs (CNN) ont revolutionne la vision par ordinateur. Ils exploitent la structure spatiale des images pour apprendre des representations hierachiques.

🖼️ POURQUOI LES CNN POUR LES IMAGES ?

Un MLP classique pour une image 224×224×3 pixels = 150 528 entrees !
→ Problemes : trop de parametres, ignore la structure spatiale, pas invariant aux translations.

Les CNN resolvent tout ca avec 3 idees cles : localite, poids partages, hierarchie.

🔩 LES 3 OPERATIONS FONDAMENTALES :

1. CONVOLUTION (Couche Conv2D) :
   Un FILTRE (kernel) glisse sur l'image et calcule des produits scalaires.
   • Filtre 3×3 = 9 poids (partages sur toute l'image !)
   • Le meme filtre detecte le meme motif partout dans l'image
   • 32 filtres → 32 "cartes de features" (feature maps)
   
   Ce que les filtres detectent :
   • Couches basses : bords, coins, couleurs
   • Couches moyennes : textures, formes simples
   • Couches hautes : visages, roues, yeux...

2. POOLING (Max Pooling) :
   Reduit la taille spatiale en gardant l'information la plus importante.
   • MaxPool 2×2 : prend le MAXIMUM dans chaque region 2×2
   • Divise la taille par 2 → moins de calculs, plus robuste aux petites translations

3. ACTIVATION ReLU :
   Apres chaque convolution : f(x) = max(0, x)
   → Introduit la non-linearite

📐 ARCHITECTURE COMPLETE TYPE :

  Image (224×224×3)
  → Conv2D(32 filtres, 3×3) + ReLU → (222×222×32)
  → MaxPool(2×2)              → (111×111×32)
  → Conv2D(64 filtres, 3×3) + ReLU → (109×109×64)
  → MaxPool(2×2)              → (54×54×64)
  → Flatten                   → (186624,)
  → Dense(256) + ReLU         → (256,)
  → Dense(10) + Softmax       → (10,) [10 classes]

🏗️ ARCHITECTURES CELEBRES :

• LeNet (1998) : premier CNN, MNIST (chiffres manuscrits)
• AlexNet (2012) : revolution ! ImageNet, 5 couches conv, Dropout
• VGG (2014) : tres profond, filtres 3×3 seulement, 138M parametres
• ResNet (2015) : connexions residuelles → entrainer des reseaux de 152 couches !
  Innovation : skip connections y = F(x) + x → evite le vanishing gradient
• EfficientNet (2019) : scaling optimal largeur/profondeur/resolution

💡 PARAMETRES D'UNE COUCHE CONV :
   Conv2D(64, (3,3)) sur une image en entree de 32 canaux :
   Nb parametres = 64 × (3×3×32 + 1) = 64 × 289 = 18 496
   (tres peu compare a un layer Dense !)

🐍 CODE KERAS/TENSORFLOW :
  from tensorflow.keras import layers, models

  model = models.Sequential([
      layers.Conv2D(32, (3,3), activation='relu', input_shape=(224,224,3)),
      layers.MaxPooling2D(2,2),
      layers.Conv2D(64, (3,3), activation='relu'),
      layers.MaxPooling2D(2,2),
      layers.Conv2D(128, (3,3), activation='relu'),
      layers.Flatten(),
      layers.Dense(512, activation='relu'),
      layers.Dropout(0.5),
      layers.Dense(10, activation='softmax')
  ])""",
                    "duration": "70 min"
                },
                {
                    "title": "Reseaux recurrents RNN/LSTM",
                    "content": """Les reseaux recurrents (RNN) et LSTM sont concus pour traiter des SEQUENCES : texte, audio, series temporelles, ADN...

🔄 POURQUOI LES RNN ?

Un MLP ou CNN traite chaque entree INDEPENDAMMENT.
Mais pour comprendre "Le chat mange la souris qu'il a chassee", le mot "il" depend du mot "chat" bien avant dans la phrase.
→ Les RNN ont une MEMOIRE : ils maintiennent un etat cache h_t qui encode l'historique.

📐 FORMULE DU RNN :

A chaque pas de temps t :
   h_t = tanh( W_hh × h_{t-1} + W_xh × x_t + b )
   y_t = W_hy × h_t + b_y

• h_t = etat cache actuel (la "memoire" du reseau)
• h_{t-1} = etat cache precedent
• x_t = entree au temps t (ex: embedding du mot actuel)
• W_hh = matrice de recurrence (comment le passe influence le present)
• W_xh = matrice d'entree (comment l'entree influence l'etat)

💡 ANALOGIE :
Un lecteur qui lit mot par mot. A chaque mot, il met a jour sa comprehension (h_t) en combinant ce qu'il vient de lire (x_t) et ce qu'il a compris jusque-la (h_{t-1}).

⚠️ PROBLEME DU VANISHING GRADIENT :

Lors de la backpropagation a travers le temps (BPTT), les gradients sont multiplies par W_hh a chaque etape.
• Si |W_hh| < 1 : les gradients DISPARAISSENT → le reseau oublie les dependances lointaines
• Si |W_hh| > 1 : les gradients EXPLOSENT → entrainement instable

🔮 LSTM — Long Short-Term Memory (solution au vanishing gradient) :

Le LSTM ajoute une CELLULE MEMOIRE c_t et 3 PORTES (gates) :

1. PORTE D'OUBLI (Forget Gate) f_t :
   f_t = σ(W_f × [h_{t-1}, x_t] + b_f)
   → Decide quoi OUBLIER de la memoire precedente
   → 0 = tout oublier, 1 = tout garder

2. PORTE D'ENTREE (Input Gate) i_t :
   i_t = σ(W_i × [h_{t-1}, x_t] + b_i)
   c̃_t = tanh(W_c × [h_{t-1}, x_t] + b_c)
   → Decide quoi AJOUTER a la memoire

3. MISE A JOUR DE LA CELLULE :
   c_t = f_t ⊙ c_{t-1} + i_t ⊙ c̃_t
   (⊙ = multiplication element par element)

4. PORTE DE SORTIE (Output Gate) o_t :
   o_t = σ(W_o × [h_{t-1}, x_t] + b_o)
   h_t = o_t ⊙ tanh(c_t)

🔵 GRU (Gated Recurrent Unit) :
Version simplifiee du LSTM avec seulement 2 portes (reset et update).
→ Moins de parametres, souvent aussi performant, plus rapide a entrainer.

📊 COMPARAISON :
   RNN    : simple, rapide, oubli rapide des longues dependances
   LSTM   : puissant, memoire longue, beaucoup de parametres
   GRU    : bon compromis vitesse/performance

🌍 APPLICATIONS :
• Traduction automatique (seq2seq avec attention)
• Generation de texte (GPT-2 utilisait des Transformers, mais les LSTM ont precede)
• Reconnaissance vocale
• Prediction de series temporelles (bourse, meteo)
• Analyse de sentiment

🐍 CODE PYTORCH :
  import torch.nn as nn

  class LSTMModel(nn.Module):
      def __init__(self, vocab_size, embed_dim, hidden_dim, n_layers):
          super().__init__()
          self.embedding = nn.Embedding(vocab_size, embed_dim)
          self.lstm = nn.LSTM(embed_dim, hidden_dim, n_layers, batch_first=True)
          self.fc = nn.Linear(hidden_dim, vocab_size)

      def forward(self, x, hidden):
          x = self.embedding(x)
          out, hidden = self.lstm(x, hidden)
          return self.fc(out), hidden""",
                    "duration": "65 min"
                },
                {
                    "title": "Introduction aux Transformers",
                    "content": """Les Transformers ont revolutionne le NLP en 2017 (article "Attention Is All You Need") et dominent maintenant tout le deep learning, y compris la vision.

🎯 LE PROBLEME QUE LES TRANSFORMERS RESOLVENT :

Les RNN/LSTM traitent les sequences MOT PAR MOT → lent, difficile a paralleliser.
Les Transformers traitent toute la sequence EN PARALLELE → beaucoup plus rapide !

⚡ LE MECANISME D'ATTENTION (Self-Attention) :

L'idee centrale : chaque mot peut "regarder" tous les autres mots de la phrase pour comprendre son contexte.

Pour chaque mot, on cree 3 vecteurs :
• Q (Query) : "Qu'est-ce que je cherche ?"
• K (Key) : "Qu'est-ce que j'offre ?"
• V (Value) : "Quelle information je transporte ?"

Calcul de l'attention :
   Attention(Q, K, V) = softmax( Q × Kᵀ / √d_k ) × V

• Q × Kᵀ = score de compatibilite entre chaque paire de mots
• / √d_k = normalisation pour eviter les gradients trop petits
• softmax = convertit les scores en probabilites (somme = 1)
• × V = ponderation des valeurs par l'attention

💡 EXEMPLE :
Phrase : "La banque a refuse mon pret car elle n'avait plus d'argent"
Pour "elle" → l'attention sera FORTE vers "banque" (pas "pret") → desambiguation !

🎭 MULTI-HEAD ATTENTION :

Au lieu d'une seule attention, on en fait H en PARALLELE (ex: H=8 ou H=16).
Chaque "tete" apprend a s'interesser a des relations differentes :
• Tete 1 : relations syntaxiques (sujet-verbe)
• Tete 2 : relations semantiques (synonymes)
• Tete 3 : relations de co-reference ("il" → "le president")
...

Resultat : concatenation de toutes les tetes → projection lineaire finale.

🏗️ ARCHITECTURE COMPLETE DU TRANSFORMER :

ENCODEUR (comprendre) :
  Pour chaque couche (×N) :
  → Multi-Head Self-Attention
  → Add & Norm (connexion residuelle + normalisation)
  → Feed-Forward Network (2 couches denses)
  → Add & Norm

DECODEUR (generer) :
  Pour chaque couche :
  → Masked Multi-Head Self-Attention (ne peut voir que le passe)
  → Cross-Attention (attention sur l'encodeur)
  → Feed-Forward Network

POSITIONAL ENCODING :
  Contrairement aux RNN, les Transformers n'ont pas d'ordre naturel.
  → On AJOUTE un encodage positionnel aux embeddings pour injecter l'information de position.

🌟 LES GRANDS MODELES :

• BERT (2018, Google) : encodeur seulement, bidirectionnel
  → Pre-entraine sur MLM (mots masques) et NSP
  → Excelle en comprehension, classification, QA

• GPT (OpenAI) : decodeur seulement, unidirectionnel
  → Pre-entraine pour predire le mot suivant
  → GPT-2 (1.5B), GPT-3 (175B), GPT-4 (multimodal)
  → Excelle en generation de texte

• T5 (Google) : encodeur + decodeur, tout en "text-to-text"
  → Traduction, resume, questions-reponses

• Vision Transformer (ViT) : applique les Transformers aux images !
  → Decoupe l'image en patches de 16×16 pixels traites comme des mots

✅ AVANTAGES :
• Parallelisation complete → GPU tres efficace
• Capture des dependances tres lointaines
• Transfert de connaissances via pre-entrainement

❌ LIMITES :
• Memoire : O(n²) pour l'attention → limite pour de tres longues sequences
• Necessite enormement de donnees et de calcul pour le pre-entrainement""",
                    "duration": "70 min"
                },
                {
                    "title": "Fine-tuning et transfer learning",
                    "content": """Le transfer learning est l'une des techniques les plus puissantes du deep learning moderne : reutiliser la connaissance acquise sur une tache pour accelerer l'apprentissage sur une autre.

🧠 POURQUOI LE TRANSFER LEARNING ?

Probleme : entrainer ResNet-50 sur ImageNet depuis zero prend des semaines sur 8 GPU.
Solution : telecharger les poids pre-entraines et les adapter a notre tache specifique.

Intuition : un expert en photographie (pre-entraine sur millions d'images) apprend plus vite a distinguer des maladies sur des radiographies qu'un debutant.

🔑 CE QUE LE MODELE A DEJA APPRIS :

Pour un CNN comme ResNet pre-entraine sur ImageNet :
• Couches basses : detecteurs de bords, coins, couleurs (universels)
• Couches moyennes : textures, motifs (semi-universels)
• Couches hautes : parties d'objets specifiques a ImageNet (moins universels)

→ Les couches basses et moyennes sont REUTILISABLES pour presque toutes les taches de vision !

📋 DEUX APPROCHES PRINCIPALES :

1. FEATURE EXTRACTION (Extraction de features) :
   → Geler TOUS les poids du modele pre-entraine
   → Ajouter uniquement de nouvelles couches de classification a la fin
   → N'entrainer que ces nouvelles couches
   
   Quand l'utiliser : dataset tres petit (<1000 images), tache similaire a la source

2. FINE-TUNING COMPLET :
   → Charger les poids pre-entraines
   → "Degeler" tout ou partie du modele
   → Entrainer avec un learning rate TRES petit (ex: 1e-5 vs 1e-3 normal)
   → Gradient tres faible pour ne pas "oublier" la connaissance acquise
   
   Quand l'utiliser : dataset moyen a grand, tache differente de la source

🔧 FINE-TUNING PROGRESSIF (Gradual Unfreezing) :
   Etape 1 : entrainer seulement la tete de classification
   Etape 2 : degeler les dernieres couches + entrainer
   Etape 3 : degeler tout le modele + entrainer avec lr tres faible

📊 TECHNIQUES AVANCEES :

• LoRA (Low-Rank Adaptation) :
  Au lieu de modifier tous les poids, on ajoute de petites matrices de rang faible.
  → Reduit les parametres entrainables de 99% !
  → Tres populaire pour les LLMs (GPT, LLaMA)

• Prompt Engineering :
  Guider le modele par des instructions dans le prompt, sans modifier les poids.
  → Zero-shot : "Traduis ce texte en espagnol : ..."
  → Few-shot : donner 3-5 exemples dans le prompt

• In-Context Learning :
  Les grands modeles (GPT-4, Claude) apprennent a partir des exemples dans le contexte.
  → Pas de gradient, pas de mise a jour des poids !

• RLHF (Reinforcement Learning from Human Feedback) :
  Technique utilisee pour aligner ChatGPT, Claude, Gemini...
  → Des evaluateurs humains notent les reponses
  → Un modele de recompense est entraine
  → Le LLM est ensuite optimise via PPO

🐍 CODE KERAS (Feature Extraction) :
  from tensorflow.keras.applications import ResNet50
  from tensorflow.keras import layers, models

  # Charger ResNet50 sans la tete de classification
  base_model = ResNet50(weights='imagenet', include_top=False, input_shape=(224,224,3))
  base_model.trainable = False  # GELER

  # Ajouter notre tete personnalisee
  model = models.Sequential([
      base_model,
      layers.GlobalAveragePooling2D(),
      layers.Dense(256, activation='relu'),
      layers.Dropout(0.5),
      layers.Dense(num_classes, activation='softmax')
  ])

  model.compile(optimizer='adam', loss='categorical_crossentropy', metrics=['accuracy'])""",
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
                    "content": """Avant d'alimenter un modele NLP, le texte brut doit etre transforme en une representation numerique. Cette etape de preprocessing est cruciale et impacte directement la qualite du modele.

📝 PIPELINE COMPLET DE PREPROCESSING :

Texte brut → Nettoyage → Tokenisation → Normalisation → Suppression stop words → Lemmatisation → Vecteurs numeriques

1️⃣ NETTOYAGE DU TEXTE :
• Supprimer les balises HTML : <p>Bonjour</p> → "Bonjour"
• Supprimer les URLs : "visitez https://exemple.com" → "visitez"
• Supprimer les caracteres speciaux : "C'est super!!!" → "C est super"
• Gerer les emojis : les conserver (sentiment), supprimer, ou convertir en texte

2️⃣ TOKENISATION — Diviser le texte en unites :

a) WORD-LEVEL (mots) :
   "Le chat mange" → ["Le", "chat", "mange"]
   ✅ Intuitif | ❌ Vocabulaire enorme, mots rares inconnus (OOV)

b) CHARACTER-LEVEL (caracteres) :
   "chat" → ["c", "h", "a", "t"]
   ✅ Pas de mots inconnus | ❌ Sequences tres longues, moins de sens

c) SUBWORD (sous-mots) — LE STANDARD MODERNE :
   BPE (Byte Pair Encoding) : "mangeons" → ["mange", "ons"]
   → Commence avec des caracteres et fusionne les paires les plus frequentes
   → Utilise par GPT-2, RoBERTa

   WordPiece : "jouons" → ["jou", "##ons"]
   → Similaire a BPE, utilise par BERT
   → ## = continuation de mot

   SentencePiece : tokenisation multilangue, gere les espaces differemment
   → Utilise par T5, mBART, LLaMA

3️⃣ NORMALISATION :
• Lowercasing : "Bonjour" → "bonjour"
  ⚠️ Attention : "Apple" (entreprise) vs "apple" (fruit) → perte d'information !
• Suppression accents : "été" → "ete" (parfois utile)
• Expansion des contractions : "don't" → "do not"

4️⃣ SUPPRESSION DES STOP WORDS :
Mots tres frequents qui n'apportent pas de sens : "le", "la", "est", "de", "un"...
✅ Reduit le bruit pour les taches de recherche d'information
❌ Peut hurt les taches ou la syntaxe compte (analyse de sentiment, traduction)

5️⃣ STEMMING vs LEMMATISATION :

STEMMING (rapide, approximatif) :
   "mangeons", "mange", "mangeait" → "mang" (coupe brutalement)
   Porter Stemmer, Snowball Stemmer

LEMMATISATION (plus lent, precis) :
   "mangeons", "mange", "mangeait" → "manger" (forme de base du dictionnaire)
   Necessite une analyse morphologique et grammaticale
   Utilise SpaCy, NLTK avec des dictionnaires

6️⃣ ENCODAGE NUMERIQUE :
• One-Hot Encoding : vecteur binaire de taille |vocabulaire|
  "chat" → [0,0,1,0,0,...] (tres creux, pas de sens semantique)
• TF-IDF : frequence du terme × log(N/df)
  → Donne plus de poids aux mots rares et pertinents
• Word Embeddings : vecteurs denses de 50-300 dimensions (Word2Vec, GloVe)

🐍 CODE PYTHON (SpaCy) :
  import spacy
  nlp = spacy.load("fr_core_news_sm")

  texte = "Les chats mangent des souris depuis des siecles."
  doc = nlp(texte)

  tokens = [token.lemma_.lower() for token in doc
            if not token.is_stop and not token.is_punct]
  print(tokens)  # ['chat', 'manger', 'souris', 'siecle']""",
                    "duration": "45 min"
                },
                {
                    "title": "Word Embeddings Word2Vec GloVe",
                    "content": """Les word embeddings transforment les mots en vecteurs numeriques denses qui capturent le sens semantique. C'est l'une des avancees les plus importantes du NLP moderne.

🧩 POURQUOI LES EMBEDDINGS ?

One-Hot Encoding : "chat" = [1,0,0,...], "chien" = [0,1,0,...], "roi" = [0,0,1,...]
Probleme : les vecteurs sont orthogonaux → le modele ne sait pas que "chat" et "chien" sont similaires !

Word Embeddings : mots similaires ont des vecteurs proches dans l'espace !
   "chat"  → [0.2, -0.4, 0.7, ...]  (300 dimensions)
   "chien" → [0.3, -0.3, 0.8, ...]  (proche de "chat" !)
   "roi"   → [0.9,  0.1, 0.2, ...]  (loin)

📐 WORD2VEC — L'architecture originale (2013, Google) :

Hypothese distributionnelle : "un mot est defini par ses voisins"
→ "chat" et "chien" apparaissent dans des contextes similaires → ils auront des vecteurs similaires.

DEUX ARCHITECTURES :

1. CBOW (Continuous Bag of Words) :
   ENTREE : contexte (mots voisins) → SORTIE : mot central
   "Le ___ mange une souris" → predire "chat"
   ✅ Plus rapide, meilleur pour mots frequents

2. SKIP-GRAM :
   ENTREE : mot central → SORTIE : mots du contexte
   "chat" → predire ["Le", "mange", "une", "souris"]
   ✅ Meilleur pour mots rares, plus precisement semantique
   ✅ Standard en pratique

L'ASTUCE DU NEGATIVE SAMPLING :
Au lieu de calculer la probabilite sur tout le vocabulaire (tres couteux), on:
• Genere des exemples NEGATIFS (mots aleatoires non voisins)
• Entraine un classificateur binaire (vrai voisin vs aleatoire)
→ Reduit enormement le cout de calcul !

🌐 GLOVE — Global Vectors (2014, Stanford) :

Contrairement a Word2Vec qui utilise des fenetres locales, GloVe exploite la MATRICE DE CO-OCCURRENCE GLOBALE.

Pour chaque paire (i, j) de mots :
   X_ij = nombre de fois que j apparait dans le contexte de i

Objectif : Embeddings tels que wᵢ · w̃ⱼ + bᵢ + b̃ⱼ ≈ log(X_ij)

✅ Capture les statistiques globales du corpus
✅ Performant pour les analogies

⚡ FASTTEXT (2016, Facebook) :

Innovation : decompose les mots en N-GRAMMES DE CARACTERES
   "chat" → ["<ch", "cha", "hat", "at>", "<chat>"]

✅ Gere les MOTS HORS-VOCABULAIRE (OOV) : "chattons" inconnu → compose depuis les n-grammes
✅ Meilleur pour les langues morphologiquement riches (arabe, turc, francais...)
✅ Peut representer les fautes d'orthographe !

🔮 PROPRIETES FASCINANTES DES EMBEDDINGS :

Arithmetique vectorielle (analogies) :
   roi - homme + femme ≈ reine  ✨
   Paris - France + Allemagne ≈ Berlin  ✨
   grand - petit + lent ≈ rapide  ✨

Ces proprietes emergent NATURELLEMENT de l'entrainement !

Clustering semantique :
   Les villes sont groupees ensemble, les animaux ensemble, etc.

📊 COMPARAISON :
   Methode    | Taille vocab | OOV | Contexte   | Points forts
   Word2Vec   | Fixe         | Non | Local      | Rapide, embeddings de qualite
   GloVe      | Fixe         | Non | Global     | Analogies, stats globales
   FastText   | Infini       | Oui | Local+char | Morphologie, langues complexes
   BERT       | Fixe         | Non | Contextuel | Un mot = vecteur different selon le contexte !

🐍 CODE PYTHON :
  from gensim.models import Word2Vec

  # Entrainement
  phrases = [["le", "chat", "mange"], ["le", "chien", "court"], ...]
  model = Word2Vec(phrases, vector_size=100, window=5, min_count=1, workers=4)

  # Utilisation
  print(model.wv.similarity("chat", "chien"))  # 0.82
  print(model.wv.most_similar("roi"))           # [("reine", 0.91), ...]
  print(model.wv["chat"])                        # vecteur de 100 dimensions""",
                    "duration": "55 min"
                },
                {
                    "title": "Modeles de sequence Seq2Seq",
                    "content": """L'architecture Seq2Seq (sequence-to-sequence) permet de transformer une sequence en une autre sequence de longueur differente. C'est la base de la traduction automatique, du resume de texte, et des chatbots.

🔄 LE PROBLEME A RESOUDRE :

Entree : sequence de longueur variable (phrase en francais)
Sortie : sequence de longueur variable (traduction en anglais)
→ Les longueurs sont differentes, les mots ne correspondent pas 1:1 !

🏗️ ARCHITECTURE ENCODEUR-DECODEUR :

ENCODEUR :
• Lit la sequence d'entree MOT PAR MOT (avec un LSTM/GRU)
• Construit progressivement une comprehension du sens
• Produit un VECTEUR DE CONTEXTE (context vector) = h_T final
→ Ce vecteur est une representation comprimee de toute la phrase source

DECODEUR :
• Prend le vecteur de contexte comme etat initial
• Genere la sequence de sortie MOT PAR MOT
• A chaque etape, predit le prochain mot et utilise cette prediction comme entree suivante

Schema :
  [Le] → [chat] → [mange] → EOS
   ↓       ↓       ↓        ↓
  LSTM → LSTM → LSTM → [Contexte]
                              ↓
                       LSTM → "The"
                       LSTM → "cat"
                       LSTM → "eats"
                       LSTM → EOS

⚠️ PROBLEME DU GOULOT D'ETRANGLEMENT :
Tout le sens de la phrase doit tenir dans UN SEUL vecteur (ex: 256 dimensions).
Pour les longues phrases → perte d'information !

✨ MECANISME D'ATTENTION — La Solution :

Au lieu d'utiliser uniquement h_T, le decodeur peut "regarder" TOUS les etats de l'encodeur.

A chaque etape de decodage t :
1. Calculer un score entre l'etat du decodeur s_t et chaque etat de l'encodeur h_i :
   e_ti = score(s_t, h_i)  (ex: produit scalaire, MLP)

2. Appliquer softmax pour obtenir les poids d'attention :
   α_ti = softmax(e_ti)  → somme = 1, poids entre 0 et 1

3. Calculer le vecteur de contexte dynamique :
   c_t = Σ α_ti × h_i  (somme ponderee des etats de l'encodeur)

4. Utiliser c_t + s_t pour predire le prochain mot

💡 INTUITION :
Pour generer "chat" en anglais, le decodeur va fortement attendre le mot source "chat" en francais (alpha eleve), en ignorant les autres mots.

📊 TEACHER FORCING :
Pendant l'entrainement, on fournit le MOT REEL (et non la prediction) comme entree du decodeur a chaque etape.
✅ Converge plus vite
❌ Discordance train/inference (exposure bias) → solutions : scheduled sampling

🔍 BEAM SEARCH (decodage) :
Au lieu de toujours prendre le mot le plus probable (greedy), on maintient les K meilleures sequences partielles.
K=5 (beam width) → 5 sequences candidates en parallele → choisir la meilleure a la fin.
✅ Meilleur que greedy | ❌ Plus lent

🌍 APPLICATIONS :
• Traduction : FR → EN, AR → FR
• Resume automatique : article long → resume court
• Chatbots : question → reponse
• Code : description en langage naturel → code Python
• Correction grammaticale : texte errone → texte corrige""",
                    "duration": "60 min"
                },
                {
                    "title": "BERT et modeles pre-entraines",
                    "content": """BERT (Bidirectional Encoder Representations from Transformers) a redefinit les standards du NLP en 2018. Il utilise l'encodeur Transformer pour creer des representations contextuelles bidirectionnelles.

🎯 L'INNOVATION CLE : BIDIRECTIONNALITE

GPT (avant BERT) : lit le texte de GAUCHE A DROITE uniquement
   "La banque a refuse le ___" → predict le mot suivant

BERT : considere le contexte a GAUCHE ET A DROITE simultanement !
   "La ___ a refuse le pret" → "banque" (grace au contexte complet)

→ Un meme mot aura des representations DIFFERENTES selon son contexte :
   "banque" dans "compte en banque" ≠ "banque" dans "banque de donnees"
   (Embeddings CONTEXTUELS vs Word2Vec statique)

📚 PRE-ENTRAINEMENT — 2 TACHES :

1. MLM (Masked Language Model) :
   • Masquer aleatoirement 15% des tokens avec [MASK]
   • "Le chat [MASK] une souris" → predire "mange"
   • Force le modele a comprendre le contexte complet
   
   Les 15% masques sont traites ainsi :
   • 80% : remplace par [MASK]
   • 10% : remplace par un mot aleatoire
   • 10% : garde le mot original (apprentissage robuste)

2. NSP (Next Sentence Prediction) :
   • Predire si la phrase B suit NATURELLEMENT la phrase A
   • Phrase A : "Le chien aboie fort."
   • Phrase B (positive, 50%) : "Son maitre lui dit de se taire."
   • Phrase B (negative, 50%) : "Les etoiles brillent la nuit."
   → Force BERT a comprendre les relations entre phrases

📐 ARCHITECTURE BERT :

BERT utilise UNIQUEMENT l'encodeur du Transformer.

Tokens speciaux :
• [CLS] : debut de chaque sequence (sa representation finale = caracteristique de toute la phrase)
• [SEP] : separateur entre deux phrases
• [PAD] : remplissage pour uniformiser la longueur

BERT-Base : 12 couches, 12 heads d'attention, hidden=768, 110M parametres
BERT-Large : 24 couches, 16 heads, hidden=1024, 340M parametres

BERT traite jusqu'a 512 tokens en entree.

🌍 VARIANTES IMPORTANTES :

• RoBERTa (Facebook, 2019) :
  - BERT entraine plus longtemps, sur plus de donnees
  - Supprime NSP (tache jugee peu utile)
  - Batch size plus grand
  → Surpasse BERT sur la plupart des benchmarks

• ALBERT (Google, 2019) :
  - Partage les poids entre les couches → beaucoup moins de parametres
  - ALBERT-Base : 12M params seulement (vs 110M pour BERT-Base)
  → Meme performance, 10× moins de memoire

• DistilBERT (HuggingFace, 2019) :
  - "Distillation" de BERT : modele eleve entraine a imiter BERT
  - 40% moins de parametres, 60% plus rapide
  - Garde 97% des performances
  → Ideal pour le deploiement en production ou sur mobile

• CamemBERT / RoBERTa French (INRIA) :
  - BERT pre-entraine sur du texte FRANCAIS
  - Indispensable pour le NLP en francais

• AraBERT :
  - BERT pre-entraine sur du texte ARABE
  - Gere l'arabe dialectal et classique

🐍 CODE HUGGINGFACE :
  from transformers import BertTokenizer, BertModel
  import torch

  tokenizer = BertTokenizer.from_pretrained('bert-base-uncased')
  model = BertModel.from_pretrained('bert-base-uncased')

  texte = "Le chat mange une souris"
  inputs = tokenizer(texte, return_tensors='pt', padding=True)

  with torch.no_grad():
      outputs = model(**inputs)

  # Representation contextuelle de chaque token
  hidden_states = outputs.last_hidden_state  # (batch, seq_len, 768)
  # Representation de la phrase entiere ([CLS] token)
  sentence_embedding = hidden_states[:, 0, :]  # (batch, 768)""",
                    "duration": "65 min"
                },
                {
                    "title": "Fine-tuning pour la classification",
                    "content": """Le fine-tuning de BERT consiste a adapter le modele pre-entraine a une tache specifique avec un dataset relativement petit (des milliers, pas des millions d'exemples).

🎯 POURQUOI LE FINE-TUNING FONCTIONNE SI BIEN ?

BERT a deja appris :
• La grammaire et la syntaxe des langues
• Les relations semantiques entre mots
• Le sens contextuel des phrases
• Des connaissances factuelles du monde

Il suffit d'apprendre la TACHE SPECIFIQUE par-dessus cette base solide !

🏗️ ARCHITECTURE POUR LA CLASSIFICATION DE TEXTE :

  Texte → Tokenisation → [CLS] token1 token2 ... [SEP]
            ↓
       BERT (12 couches)
            ↓
  Representation [CLS] (768 dimensions)
            ↓
       Couche Dense(num_classes)
            ↓
       Softmax → Probabilites par classe

Pourquoi le token [CLS] ?
→ Il est concu pour agreger l'information de toute la sequence (grace a l'attention bidirectionnelle)

⚙️ HYPERPARAMETRES CRITIQUES :

• LEARNING RATE : extremement important !
  - Trop grand : ecrase les poids pre-entraines ("catastrophic forgetting")
  - Optimal : 2e-5 a 5e-5 (bien plus petit que 1e-3 standard)
  - Scheduler recommande : warmup lineaire + decay cosinus

• BATCH SIZE : 16 ou 32 (limite par la VRAM GPU)

• EPOCHS : 2 a 4 (au-dela → overfitting car BERT est deja tres bon)

• MAX_LENGTH : jusqu'a 512 tokens, mais 128 ou 256 souvent suffisent

🔧 STRATEGIES AVANCEES :

1. GRADUAL UNFREEZING :
   Epoch 1 : entrainer seulement la tete de classification
   Epoch 2 : degeler les 2 dernieres couches BERT + tete
   Epoch 3 : degeler tout BERT + tete
   → Evite de bruler les representations basses apprises

2. DISCRIMINATIVE LEARNING RATES :
   Couche de sortie : lr = 5e-5
   Couches intermediaires : lr = 3e-5
   Couches basses : lr = 1e-5
   → Les couches basses (universelles) changent moins vite

3. DATA AUGMENTATION NLP :
   • Paraphrase : generer des variantes de chaque phrase
   • Back-translation : FR → EN → FR
   • Random deletion / insertion / swap de mots
   → Ameliore la generalisation quand peu de donnees

📊 EVALUATION COMPLETE :

  Matrice de confusion (5 classes de sentiment) :
  → Identifier quelles classes sont confondues

  Rapport de classification :
                Precision  Recall  F1-Score  Support
  Tres negatif    0.91      0.88    0.89       200
  Negatif         0.84      0.86    0.85       180
  Neutre          0.78      0.80    0.79       150
  Positif         0.87      0.85    0.86       190
  Tres positif    0.92      0.91    0.91       180
  Macro avg       0.86      0.86    0.86       900

🐍 CODE COMPLET HUGGINGFACE :
  from transformers import BertForSequenceClassification, BertTokenizer
  from transformers import TrainingArguments, Trainer

  model = BertForSequenceClassification.from_pretrained(
      'bert-base-uncased', num_labels=5
  )

  training_args = TrainingArguments(
      output_dir='./results',
      num_train_epochs=3,
      per_device_train_batch_size=16,
      learning_rate=2e-5,
      warmup_steps=500,
      weight_decay=0.01,
      evaluation_strategy="epoch",
  )

  trainer = Trainer(
      model=model, args=training_args,
      train_dataset=train_dataset, eval_dataset=val_dataset
  )
  trainer.train()""",
                    "duration": "55 min"
                },
                {
                    "title": "Generation de texte avec GPT",
                    "content": """GPT (Generative Pre-trained Transformer) est une famille de modeles de generation de texte developpee par OpenAI. Contrairement a BERT, GPT est un modele AUTOREGRESSIF unidirectionnel.

🤖 ARCHITECTURE GPT — LE DECODEUR TRANSFORMER :

GPT utilise UNIQUEMENT les couches DECODEUR du Transformer.
A chaque position, le modele ne peut voir que les tokens PRECEDENTS (attention causale).

Entrainement pre-supervisé : predire le token suivant !
   "Le chat man___" → predire "ge"
   P(token_t | token_1, token_2, ..., token_{t-1})

📈 EVOLUTION DE LA FAMILLE GPT :

• GPT-1 (2018) : 117M parametres, 12 couches
  Premier modele a montrer la puissance du pre-entrainement + fine-tuning

• GPT-2 (2019) : 1.5B parametres, 48 couches
  "Trop dangereux pour etre publie" (OpenAI l'a retenu initialement)
  Premiere emergence des capacites zero-shot

• GPT-3 (2020) : 175B parametres (175 milliards !)
  Capacites Few-shot remarquables
  Base de ChatGPT (avec RLHF par-dessus)

• GPT-4 (2023) : architecture inconnue, multimodal (texte + images)
  Performances humaines sur de nombreux benchmarks

🎲 STRATEGIES DE DECODAGE — Comment generer du texte :

1. GREEDY DECODING :
   A chaque etape, choisir le token avec la PLUS HAUTE probabilite.
   ❌ Souvent repetitif et previsible : "The cat sat on the mat. The cat sat on the mat..."

2. BEAM SEARCH (k=5) :
   Maintenir les k meilleures sequences en parallele.
   ✅ Mieux que greedy | ❌ Tendance aux phrases courtes et generiques

3. TOP-K SAMPLING :
   Echantillonner parmi les K tokens les plus probables.
   K=50 : "Le chat ___ " → parmi {mange, dort, joue, court, ...}
   ✅ Plus de variete | ❌ K fixe peut inclure tokens improbables

4. NUCLEUS SAMPLING (Top-p) :
   Echantillonner dans le plus petit ensemble couvrant probabilite >= p.
   p=0.9 : prendre les tokens qui representent 90% de la probabilite totale
   ✅ Adaptatif selon la distribution | ✅ Le standard en production

5. TEMPERATURE :
   Controle la "creativite" du modele.
   • T < 1 : plus deterministe, plus concentre (texte factuel)
   • T = 1 : distribution originale
   • T > 1 : plus aleatoire, plus creatif (texte poetique, storytelling)
   
   logits_modifies = logits / temperature
   → T=0.7 pour les assistants, T=1.2 pour la creation

🎨 PROMPT ENGINEERING — Guider GPT sans modifier les poids :

ZERO-SHOT :
  "Traduis cette phrase en espagnol : Le chat est sur le tapis."
  → GPT traduit sans avoir ete entraine sur cette tache specifique !

FEW-SHOT (In-Context Learning) :
  "FR: Le chat mange. EN: The cat eats.
   FR: Le chien court. EN: The dog runs.
   FR: L'oiseau chante. EN:"
  → GPT comprend la tache par les exemples et complete !

CHAIN-OF-THOUGHT (Raisonnement etape par etape) :
  "Resous ce probleme en montrant chaque etape de raisonnement :
   Si Jean a 3 pommes et Marie lui en donne 5, combien en a-t-il ?
   Etape 1 : Jean commence avec 3 pommes.
   Etape 2 : Marie donne 5 pommes supplementaires.
   Etape 3 : Total = 3 + 5 = 8 pommes."
  ✅ Ameliore significativement les raisonnements complexes

🐍 CODE HUGGINGFACE :
  from transformers import GPT2LMHeadModel, GPT2Tokenizer

  tokenizer = GPT2Tokenizer.from_pretrained('gpt2')
  model = GPT2LMHeadModel.from_pretrained('gpt2')

  prompt = "The future of AI is"
  inputs = tokenizer.encode(prompt, return_tensors='pt')

  outputs = model.generate(
      inputs,
      max_length=100,
      do_sample=True,
      temperature=0.8,
      top_p=0.9,
      num_return_sequences=3
  )

  for i, output in enumerate(outputs):
      print(f"--- Generation {i+1} ---")
      print(tokenizer.decode(output, skip_special_tokens=True))""",
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
                    "content": """OpenCV est la bibliotheque de vision par ordinateur la plus utilisee au monde (2500+ fonctions).

Operations de base sur les images :
• Lecture / ecriture : cv2.imread(), cv2.imwrite(), cv2.VideoCapture()
• Redimensionnement : cv2.resize(img, (largeur, hauteur))
• Rotation : cv2.rotate() ou matrice de rotation cv2.getRotationMatrix2D()
• Recadrage : img[y1:y2, x1:x2]  (slicing NumPy)
• Conversion couleurs : cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
  (⚠️ OpenCV lit en BGR, pas RGB !)

Filtres de lissage :
• GaussianBlur : lissage doux, reduit le bruit gaussien
  cv2.GaussianBlur(img, (5,5), 0)
• medianBlur : excellent contre le bruit sel et poivre
  cv2.medianBlur(img, 5)
• bilateralFilter : lisse mais preserve les bords
  cv2.bilateralFilter(img, 9, 75, 75)

Operations morphologiques :
Utilisent un element structurant (kernel) qui glisse sur l image.
• Erosion : shrink les regions blanches, supprime le bruit
• Dilatation : expand les regions blanches, remplit les trous
• Ouverture = Erosion puis Dilatation : supprime le bruit
• Fermeture = Dilatation puis Erosion : comble les trous

Histogrammes :
• Represente la distribution des intensites de pixels
• Egalisation : rend la distribution uniforme → meilleur contraste
  cv2.equalizeHist(img_gris)
• CLAHE : egalisation adaptative par blocs (meilleur pour images medicales)

Code exemple :
  import cv2
  img = cv2.imread('photo.jpg')
  img_rgb = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
  img_blur = cv2.GaussianBlur(img, (5,5), 0)
  img_edges = cv2.Canny(img_blur, 100, 200)
  cv2.imshow('Contours', img_edges)
  cv2.waitKey(0)""",
                    "duration": "50 min"
                },
                {
                    "title": "Detection de contours et features",
                    "content": """La detection de contours et de caracteristiques est fondamentale pour la vision par ordinateur classique.

Detection de contours :

1. Sobel (gradient du premier ordre) :
   Calcule la derivee partielle dans chaque direction.
   Gx = [[-1,0,1],[-2,0,2],[-1,0,1]]  (horizontal)
   Gy = [[1,2,1],[0,0,0],[-1,-2,-1]]  (vertical)
   Magnitude = sqrt(Gx² + Gy²)
   → Detecte les bords mais sensible au bruit.

2. Canny (standard industriel) :
   Algorithme en 4 etapes :
   a) Lissage GaussianBlur pour reduire le bruit
   b) Calcul du gradient (Sobel)
   c) Suppression non-maxima : ne garder que les maxima locaux
   d) Seuillage par hysteresis : 2 seuils (bas/haut)
      - Pixel > seuil haut → bord sur
      - Pixel < seuil bas → elimine
      - Entre les deux → bord si connecte a un bord sur
   cv2.Canny(img, seuil_bas=100, seuil_haut=200)

Detection de coins :
3. Harris Corner Detector :
   Detecte les regions ou le gradient change dans toutes les directions.
   Matrice de structure M = Σ [Ix², IxIy; IxIy, Iy²]
   Score R = det(M) - k × trace(M)²
   R >> 0 → coin | R << 0 → bord | |R| ≈ 0 → plat

Points d'interet invariants :
4. SIFT (Scale-Invariant Feature Transform) :
   Detecte des points d'interet INVARIANTS aux changements :
   → Echelle (zoom), rotation, illumination, point de vue (partiel)
   Descripteur : histogramme de gradients locaux (128 dimensions)
   ✅ Tres robuste | ❌ Lent, brevet (maintenant libre)

5. ORB (Oriented FAST and Rotated BRIEF) :
   Alternative rapide et libre a SIFT.
   → Detecteur FAST + descripteur BRIEF oriente
   ✅ Temps reel | ✅ Gratuit

Extraction de formes :
6. findContours :
   Trouve les contours de regions connectees.
   contours, _ = cv2.findContours(mask, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
   Puis : cv2.boundingRect(contour), cv2.contourArea(c), cv2.arcLength(c, True)""",
                    "duration": "55 min"
                },
                {
                    "title": "Classification d'images avec CNN",
                    "content": """La classification d'images est la tache fondamentale de la vision par ordinateur : assigner une categorie a une image.

Approche avec CNN pre-entraine (Transfer Learning) :

1. CHOISIR LE MODELE DE BASE :
   Architecture  | Parametres | Top-5 Acc | Vitesse
   MobileNetV2   | 3.4M       | 91%       | Tres rapide (mobile)
   ResNet50      | 25.6M      | 93%       | Rapide
   EfficientNetB4| 19M        | 98%       | Moyen
   ViT-B/16      | 86M        | 99%       | Lent mais SOTA

2. DATA AUGMENTATION — indispensable pour eviter l'overfitting :
   Transformations qui preservent le label :
   • Rotation aleatoire : [-15°, +15°]
   • Flip horizontal (selon le contexte !)
   • Zoom aleatoire : [0.8, 1.2]
   • Decalage (shift) horizontal/vertical
   • Changement de luminosite / contraste
   • CutMix / MixUp : techniques modernes tres efficaces

   Keras code :
   from tensorflow.keras.preprocessing.image import ImageDataGenerator
   datagen = ImageDataGenerator(
       rotation_range=15, horizontal_flip=True,
       zoom_range=0.2, width_shift_range=0.1)

3. FINE-TUNING PROGRESSIF :
   Phase 1 : geler tout ResNet50, entrainer uniquement la tete
   Phase 2 : degeler les 50 dernieres couches, lr=1e-5
   Phase 3 : degeler tout, lr=1e-6

4. EVALUATION :
   → Matrice de confusion (quelles classes sont confondues ?)
   → Grad-CAM : visualiser les regions qui ont influence la decision !
      Permet d'interpreter les predictions du CNN.

5. DEPLOIEMENT :
   TensorFlow Lite pour mobile, ONNX pour cross-framework,
   TensorRT pour GPU NVIDIA en production.""",
                    "duration": "65 min"
                },
                {
                    "title": "Detection d'objets YOLO SSD",
                    "content": """La detection d'objets localise ET classe plusieurs objets dans une image simultanement.

DEUX ETAPES vs UNE ETAPE :

Approches a 2 etapes (plus precises, plus lentes) :
• R-CNN (2014) : regions candidates → CNN → classification
• Fast R-CNN : CNN partage pour toutes les regions
• Faster R-CNN : Region Proposal Network (RPN) integre
  → Excellent pour la precision | ❌ ~5-15 FPS

Approches a 1 etape (temps reel) :

1. YOLO (You Only Look Once) :
   L'image est divisee en grille S×S.
   Chaque cellule predit B boites + probabilites de classe.
   Prediction en UNE SEULE PASSE du reseau → tres rapide !
   YOLOv1 (2016) → v5 → v8 (2023) : ameliorations constantes
   YOLOv8 : ~80 FPS sur GPU, 53% mAP sur COCO

2. SSD (Single Shot MultiBox Detector) :
   Utilise des feature maps de plusieurs echelles
   Anchor boxes de tailles differentes pour chaque cellule
   → Detecte les petits et grands objets mieux que YOLOv1

📊 METRIQUES DE DETECTION :

IoU (Intersection over Union) :
   IoU = Aire(Intersection) / Aire(Union)
   → Mesure le chevauchement entre la boite predite et la vraie
   IoU > 0.5 → detection correcte (convention PASCAL VOC)

Precision-Recall :
   Pour chaque classe, calculer la courbe Precision vs Recall
   AP (Average Precision) = aire sous la courbe PR

mAP (mean Average Precision) :
   mAP = moyenne des AP sur toutes les classes
   mAP@0.5 : IoU threshold = 0.5
   mAP@0.5:0.95 : moyenne sur IoU de 0.5 a 0.95 (standard COCO)

NMS (Non-Maximum Suppression) :
   Supprime les boites redondantes qui se chevauchent.
   → Garde seulement la boite avec le score le plus eleve par objet.

Code YOLOv8 :
  from ultralytics import YOLO
  model = YOLO('yolov8n.pt')  # nano model
  results = model('image.jpg')
  results[0].show()""",
                    "duration": "70 min"
                },
                {
                    "title": "Segmentation semantique",
                    "content": """La segmentation d'images assigne une classe a CHAQUE PIXEL de l'image.

TROIS TYPES DE SEGMENTATION :

1. SEGMENTATION SEMANTIQUE :
   → Chaque pixel recoit une classe (chat, voiture, route...)
   → Tous les pixels du meme type = meme couleur
   → Probleme : ne distingue pas 2 voitures separees !

2. SEGMENTATION D'INSTANCES :
   → Detecte ET segmente chaque objet individuellement
   → Voiture n°1 ≠ Voiture n°2 (couleurs differentes)
   → Plus difficile, mais plus utile

3. SEGMENTATION PANOPTIQUE :
   → Combine les deux : semantique pour le fond, instances pour les objets
   → Standard moderne dans la conduite autonome

ARCHITECTURES CLES :

FCN (Fully Convolutional Network, 2015) :
   Remplace les couches denses par des convolutions
   → Sortie de meme taille que l'entree

U-Net (2015, segmentation medicale) :
   Architecture en forme de U avec skip connections :
   → Bras gauche (encodeur) : downsampling, capturer le contexte
   → Bras droit (decodeur) : upsampling, localisation precise
   → Skip connections : relie encodeur et decodeur pour les details fins
   ✅ Excellent avec PEU de donnees (medical : quelques centaines d'images)
   ✅ Preserver les details anatomiques fins

Mask R-CNN (2017) :
   Faster R-CNN + branche de masque en parallele
   → Pour chaque objet detecte : predit un masque binaire pixel par pixel
   ✅ Segmentation d'instances de haute qualite
   ❌ Lent (~5 FPS)

DeepLab v3+ (Google) :
   Atrous (dilated) convolution pour capturer le contexte multi-echelle
   ASPP (Atrous Spatial Pyramid Pooling)
   ✅ SOTA pour la segmentation semantique

Code U-Net (Keras) :
  def unet(input_shape=(256,256,1)):
      inputs = layers.Input(input_shape)
      # Encodeur
      c1 = layers.Conv2D(64, 3, activation='relu', padding='same')(inputs)
      p1 = layers.MaxPool2D()(c1)
      c2 = layers.Conv2D(128, 3, activation='relu', padding='same')(p1)
      p2 = layers.MaxPool2D()(c2)
      # Pont
      bridge = layers.Conv2D(256, 3, activation='relu', padding='same')(p2)
      # Decodeur
      u1 = layers.UpSampling2D()(bridge)
      u1 = layers.Concatenate()([u1, c2])  # skip connection
      u2 = layers.UpSampling2D()(u1)
      u2 = layers.Concatenate()([u2, c1])  # skip connection
      outputs = layers.Conv2D(1, 1, activation='sigmoid')(u2)
      return models.Model(inputs, outputs)""",
                    "duration": "60 min"
                },
                {
                    "title": "Generation d'images GANs",
                    "content": """Les GANs (Generative Adversarial Networks) sont des modeles generatifs qui apprennent a creer de nouvelles donnees realistes.

LE JEU ADVERSARIAL (Goodfellow, 2014) :

DEUX RESEAUX en competition :
• GENERATEUR G : prend un vecteur de bruit z aleatoire et genere une fausse image
• DISCRIMINATEUR D : doit distinguer les vraies images des fausses

Objectifs :
  G veut TROMPER D (maximiser la probabilite que D classe ses fausses images comme vraies)
  D veut DETECTER les fausses (minimiser sa propre erreur de classification)

Fonction de perte min-max :
  min_G max_D E[log D(x)] + E[log(1 - D(G(z)))]

Entrainement :
  → Alterner : entrainer D sur vraies+fausses, puis entrainer G
  → Equilibre de Nash : G genere des images parfaites, D predit 0.5 partout

ARCHITECTURES IMPORTANTES :

DCGAN (Deep Convolutional GAN, 2015) :
  → Utilise des convolutions transposees dans le generateur
  → Batch Normalization pour stabiliser l'entrainement
  ✅ Images de qualite acceptable pour l'epoque

StyleGAN (NVIDIA, 2019) :
  → Genere des visages humains photorea listes (thispersondoesnotexist.com)
  → Controle du style : coiffure, age, expression a differentes echelles
  → Architecture mapping + synthesis networks
  ✅ Qualite photographique, controle granulaire du style

CycleGAN (2017) :
  → Transfert de style non supervise entre domaines
  → Pas de paires d'images necessaires !
  → Cheval ↔ Zebre, Ete ↔ Hiver, Photo ↔ Tableau
  → 2 GANs + 2 losses de cycle-consistance

Conditional GAN (cGAN) :
  → Conditionner sur une entree : texte → image (DALL-E precurseur)
  → pix2pix : image → image (esquisse → photo realiste)

DEFIS DES GANs :
• Mode collapse : G genere toujours la meme image
• Instabilite : les deux reseaux doivent etre equilibres
• Evaluation difficile : comment mesurer la qualite ?
  → FID (Frechet Inception Distance) : standard moderne

APPLICATIONS :
• Generation de visages synthetiques (deepfakes, avatars)
• Augmentation de donnees medicales (peu de donnees reelles)
• Super-resolution : image basse qualite → haute qualite
• Retouche photo : inpainting, colorisation d'images NB
• Art et design generatif""",
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
                    "content": """Le Processus de Decision Markovien (MDP) est le cadre mathematique formel pour modeliser les problemes de Reinforcement Learning.

LES 5 COMPOSANTES D'UN MDP :
• S : espace des etats (tout ce que l'agent peut observer)
• A : espace des actions (ce que l'agent peut faire)
• P(s'|s,a) : probabilite de transition (dynamique de l'environnement)
• R(s,a,s') : fonction de recompense (signal de feedback)
• γ (gamma) : facteur d'actualisation [0,1] (importance du futur)

PROPRIETE DE MARKOV :
Le futur ne depend que de l'etat PRESENT, pas de l'historique complet.
  P(s_{t+1} | s_t, a_t) = P(s_{t+1} | s_0, a_0, ..., s_t, a_t)

L'OBJECTIF DE L'AGENT :
Maximiser la recompense cumulee ACTUALISEE :
  G_t = R_t + γ×R_{t+1} + γ²×R_{t+2} + ...
  = Σ γ^k × R_{t+k}
→ γ proche de 0 : agent myope (recompenses immediates)
→ γ proche de 1 : agent prevoyant (recompenses futures)

FONCTIONS DE VALEUR :

V^π(s) = valeur d'etat sous la politique π :
  V^π(s) = E[G_t | S_t = s, politique π]
  → Recompense cumulee attendue en partant de l'etat s

Q^π(s,a) = valeur action-etat (Q-function) :
  Q^π(s,a) = E[G_t | S_t = s, A_t = a, politique π]
  → Recompense cumulee attendue en prenant l'action a dans l'etat s

L'EQUATION DE BELLMAN (fondement theorique) :
Decompose la valeur de maniere recursive :
  V^π(s) = Σ_a π(a|s) × Σ_{s'} P(s'|s,a) × [R(s,a,s') + γ × V^π(s')]
  → La valeur maintenant = recompense immediate + valeur future actualisee

VALEUR OPTIMALE :
  V*(s) = max_a Q*(s,a)
  Q*(s,a) = R(s,a) + γ × Σ_{s'} P(s'|s,a) × V*(s')

LA POLITIQUE OPTIMALE :
  π*(s) = argmax_a Q*(s,a)
  → Si on connait Q*, on connait la politique optimale !""",
                    "duration": "55 min"
                },
                {
                    "title": "Q-Learning et SARSA",
                    "content": """Q-Learning et SARSA sont les deux algorithmes de base du RL tabular (avec une table Q explicite).

Q-LEARNING (Watkins, 1989) :

Mise a jour de la table Q :
  Q(s,a) ← Q(s,a) + α × [R + γ × max_{a'} Q(s',a') - Q(s,a)]

  • α = taux d'apprentissage (learning rate)
  • R = recompense recue
  • γ × max Q(s',a') = estimation de la valeur future optimale
  • [Crochet] = erreur TD (Temporal Difference)

OFF-POLICY : utilise toujours max Q pour la mise a jour,
quelle que soit l'action reellement prise.
→ Apprend la politique OPTIMALE meme en explorant !

SARSA (State-Action-Reward-State-Action) :

Mise a jour :
  Q(s,a) ← Q(s,a) + α × [R + γ × Q(s',a') - Q(s,a)]
  (a' est l'action REELLEMENT prise dans s')

ON-POLICY : la valeur future utilisee correspond a la politique ACTUELLE
(pas necessairement optimale).
→ Plus conservateur, suit exactement la politique d'exploration.

EXPLORATION vs EXPLOITATION :

Dilemme fondamental :
→ EXPLOITATION : choisir l'action connue comme la meilleure → aucun apprentissage
→ EXPLORATION : essayer des actions inconnues → risque mais potentiellement mieux

Strategies :
• Epsilon-greedy : avec probabilite ε, choisir aleatoire ; sinon, max Q
  ε decroissant avec le temps (plus d'exploration au debut)
• UCB (Upper Confidence Bound) : choisir l'action avec la meilleure borne superieure
• Thompson Sampling : echantillonnage bayesien

COMPARAISON Q-Learning vs SARSA :
  Critere        | Q-Learning       | SARSA
  Type           | Off-policy       | On-policy
  Mise a jour    | max Q(s',a')     | Q(s',a') actuel
  Comportement   | Plus agressif    | Plus conservateur
  Utilisation    | Environnements   | Environnements
                 | deterministes    | avec risques

LIMITES DU RL TABULAIRE :
→ Fonctionne UNIQUEMENT si l'espace d'etats est PETIT et DISCRET
→ Echecs en grille 4x4 → table de 16 entrees ✅
→ Jeux video avec pixels → table de 10^100 entrees ✗ → besoin de DQN !""",
                    "duration": "60 min"
                },
                {
                    "title": "Deep Q-Networks DQN",
                    "content": """DQN (Deep Q-Network) combine Q-Learning avec des reseaux de neurones profonds pour resoudre des problemes a grands espaces d'etats.

LE PROBLEME DU RL TABULAIRE :
Pour Atari (images 84×84, 4 canaux) : 4^(84×84) = 10^21000 etats !
→ Impossible de maintenir une table Q.

SOLUTION DQN (DeepMind, 2013/2015) :
Approximer Q(s,a) avec un RESEAU DE NEURONES :
  Q(s, a; θ) ≈ Q*(s, a)
  → Input : etat s (ex: image 84×84)
  → Output : valeur Q pour chaque action possible

TECHNIQUES CLES DE DQN :

1. EXPERIENCE REPLAY :
   Probleme : les transitions consecutives sont tres correlees → instabilite.
   Solution : stocker les transitions (s, a, r, s') dans un buffer de memoire.
   → Echantillonner des MINI-BATCHS aleatoires pour l'entrainement
   → Brise les correlations temporelles
   → Permet de reutiliser les experiences plusieurs fois

2. TARGET NETWORK (Reseau cible) :
   Probleme : la cible Q* change a chaque etape → boucle instable.
   Solution : utiliser un RESEAU CIBLE separe θ⁻ pour calculer la cible.
   → Copier les poids vers θ⁻ toutes les N iterations (ex: N=1000)
   → La cible est stable pendant N iterations

3. DOUBLE DQN (2016) :
   Probleme : DQN sur-estime systematiquement les Q-values (biais d'optimisme).
   Solution : utiliser le RESEAU PRINCIPAL pour choisir l'action,
   et le RESEAU CIBLE pour evaluer cette action :
     y = R + γ × Q(s', argmax_{a'} Q(s',a'; θ); θ⁻)

4. DUELING DQN (2016) :
   Decomposer Q(s,a) en deux composantes :
   Q(s,a) = V(s) + A(s,a)
   → V(s) : valeur de l'etat (independante de l'action)
   → A(s,a) : avantage de l'action (relative aux autres actions)
   → Apprend plus efficacement : V(s) est plus facile a apprendre que Q(s,a)

RESULTATS HISTORIQUES :
→ DQN a atteint le NIVEAU HUMAIN sur 49 jeux Atari (2015)
→ En apprenant seulement depuis les pixels bruts !

Code PyTorch simplifie :
  class DQN(nn.Module):
      def __init__(self, n_states, n_actions):
          super().__init__()
          self.net = nn.Sequential(
              nn.Linear(n_states, 128), nn.ReLU(),
              nn.Linear(128, 128), nn.ReLU(),
              nn.Linear(128, n_actions)
          )
      def forward(self, x):
          return self.net(x)""",
                    "duration": "65 min"
                },
                {
                    "title": "Policy Gradient Methods",
                    "content": """Les methodes de gradient de politique (Policy Gradient) apprennent DIRECTEMENT la politique π(a|s;θ) sans passer par une fonction valeur.

POURQUOI POLICY GRADIENT ?
Q-Learning/DQN → apprend Q(s,a), derive π* en prenant max.
Limites :
→ Requiert un espace d'actions DISCRET (comment faire max sur actions continues ?)
→ Difficile pour les politiques stochastiques (utiles dans les jeux a info incomplete)
→ Ne peut pas apprendre directement les policies parametrees

Policy Gradient : apprend θ tel que π(a|s;θ) maximise G.
✅ Fonctionne avec les espaces continus (robotique !)
✅ Converge vers un optimum local (garanties theoriques)
✅ Peut apprendre des politiques stochastiques

THEOREME DU GRADIENT DE POLITIQUE :
  ∇_θ J(θ) = E[∇_θ log π(a|s;θ) × Q^π(s,a)]

  → ∇_θ log π : comment changer θ pour rendre a plus/moins probable depuis s
  → Q^π(s,a) : a quel point cette action etait-elle bonne ?
  → Augmenter la probabilite des actions qui ont donne de bonnes recompenses !

ALGORITHME REINFORCE :
  1. Jouer un episode complet avec politique π_θ
  2. Calculer les retours G_t pour chaque etape
  3. Mise a jour : θ ← θ + α × Σ_t [G_t × ∇_θ log π(a_t|s_t;θ)]

PROBLEME : HAUTE VARIANCE
→ G_t peut varier enormement entre les episodes
→ Entraine une instabilite et une convergence lente

SOLUTION : BASELINE
Soustraire une baseline b(s) pour reduire la variance SANS biais :
  ∇_θ J(θ) = E[∇_θ log π(a|s;θ) × (Q^π(s,a) - b(s))]

Baselines courantes :
→ Valeur moyenne des retours
→ Fonction de valeur V(s) : donne l'algorithme ACTOR-CRITIC !

Avantage A(s,a) = Q(s,a) - V(s) :
→ > 0 : l'action etait MEILLEURE que la moyenne
→ < 0 : l'action etait PIRE que la moyenne
→ ≈ 0 : l'action etait typique""",
                    "duration": "60 min"
                },
                {
                    "title": "Actor-Critic A2C PPO",
                    "content": """Les methodes Actor-Critic et PPO representent l'etat de l'art du RL moderne, utilise dans les robots et les LLMs.

ACTOR-CRITIC :

DEUX RESEAUX :
→ ACTOR π(a|s;θ) : la politique (decide quoi faire)
→ CRITIC V(s;φ) : la fonction de valeur (evalue la situation)

Mise a jour :
  Avantage : A(s,a) = R + γ×V(s') - V(s)  [erreur TD]
  Actor  : θ ← θ + α × A(s,a) × ∇_θ log π(a|s;θ)
  Critic : φ ← φ - α × [R + γ×V(s') - V(s)]² × ∇_φ

A2C (Advantage Actor-Critic) :
→ Version synchrone d'A3C (Asynchronous A3C)
→ Plusieurs environnements en parallele pour des gradients moins correles
→ Plus stable que REINFORCE grace a la baseline (Critic)

TRPO (Trust Region Policy Optimization, 2015) :
→ Probleme cle : de trop grandes mises a jour de politique → catastrophique
→ Contrainte : la divergence KL entre l'ancienne et la nouvelle politique
   ne doit pas depasser un seuil δ
→ Garantit une amelioration monotone (en theorie)
→ Difficile a implementer (optimisation avec contraintes)

PPO (Proximal Policy Optimization, OpenAI 2017) :
Solution plus simple a TRPO → devient le standard !

Idee : clipper le ratio de probabilite pour limiter les grandes mises a jour :
  r(θ) = π(a|s;θ) / π(a|s;θ_old)
  L_CLIP(θ) = E[min(r×A, clip(r, 1-ε, 1+ε)×A)]
  (ε typiquement 0.1 ou 0.2)

→ Si l'action s'est bien passee (A > 0) : augmenter sa probabilite
   mais PAS trop (plafond a 1+ε)
→ Si mauvaise (A < 0) : diminuer mais PAS trop (plancher a 1-ε)

Utilisations de PPO :
✅ OpenAI Five (Dota 2), AlphaGo
✅ Robotique (locomotion)
✅ RLHF pour aligner les LLMs (ChatGPT, Claude !)

SAC (Soft Actor-Critic, 2018) :
→ Maximise la recompense + l'ENTROPIE de la politique
→ Encourage l'exploration tout en apprenant
→ Standard pour la robotique continue""",
                    "duration": "70 min"
                },
                {
                    "title": "Applications reelles",
                    "content": """Le RL est passe de la theorie aux applications reelles avec des succes spectaculaires ces dernieres annees.

APPLICATIONS MARQUANTES :

1. JEUX ET SIMULATIONS :
• AlphaGo (DeepMind, 2016) :
  Vaincu le champion mondial de Go Lee Sedol (4-1)
  → MCTS (Monte Carlo Tree Search) + CNN pour evaluer les positions
  → Self-play : joue contre lui-meme des millions de fois

• AlphaStar (StarCraft II, 2019) :
  Niveau Grand Master sans restrictions d'acces a l'information
  → Gestion du brouillard de guerre, micromanagement, strategie long terme

• OpenAI Five (Dota 2, 2019) :
  Vaincu l'equipe mondiale championne OG
  → 5 agents coordonnes entraines pendant 10 mois

2. ROBOTIQUE :
• Boston Dynamics / OpenAI : marche, course, sauts de robots
  → Necessitent SAC ou PPO avec des milliers d'heures de simulation
• Manipulation : saisir des objets inconnus
  → Enjeu : generalisation aux objets jamais vus

3. SIM-TO-REAL (Simulation vers Realite) :
Probleme : entrainer en simulation (gratuit, parallelisable) mais deployer en realite.
Defi : le gap de domaine (simulation ≠ realite exactement)
Solutions :
→ Domain randomization : varier les parametres physiques en simulation
→ Domain adaptation : adapter le modele a la realite

4. TRADING ALGORITHMIQUE :
→ Agent qui apprend a acheter/vendre en maximisant le profit
→ Defi : non-stationnarite des marches, transaction costs

5. GESTION DE L'ENERGIE :
→ AlphaGo applique aux datacenters Google : -40% de consommation cooling !

DEFIS MAJEURS DU RL :
• Sample efficiency : RL necessite ENORMEMENT d'interactions
  (DQN Atari : ~200M frames = 38 jours de jeu humain)
• Safety : eviter les comportements dangereux pendant l'exploration
• Generalisation : performance sur les scenarios non vus
• Credit assignment : associer les recompenses aux bonnes actions
• Reward shaping : concevoir la bonne fonction de recompense

FUTUR :
→ RL + LLMs : modeles de fondation pour la decision
→ World models : apprendre un modele du monde pour planifier""",
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
                    "content": """Les pipelines scikit-learn permettent d'enchaîner proprement toutes les etapes du ML et d'eviter les fuites de donnees.

POURQUOI LES PIPELINES ?

Probleme sans pipeline :
  scaler.fit(X_train)  # OK
  X_test_scaled = scaler.transform(X_test)  # Fuite potentielle !
  → Si on fit le scaler sur tout le dataset → data leakage

Avec pipeline : le fit() du scaler se fait UNIQUEMENT sur les donnees d'entrainement.

CREATION D'UN PIPELINE :
  from sklearn.pipeline import Pipeline
  from sklearn.preprocessing import StandardScaler
  from sklearn.svm import SVC

  pipe = Pipeline([
      ('scaler', StandardScaler()),
      ('feature_selection', SelectKBest(k=20)),
      ('classifier', SVC(kernel='rbf'))
  ])

  pipe.fit(X_train, y_train)   # fit de toutes les etapes
  y_pred = pipe.predict(X_test)

OPTIMISATION DES HYPERPARAMETRES :

1. GRID SEARCH (exhaustif) :
   Teste TOUTES les combinaisons → garantit le meilleur resultat
   Mais tres lent si beaucoup de parametres.

   param_grid = {
       'classifier__C': [0.1, 1, 10, 100],
       'classifier__gamma': ['scale', 'auto', 0.1, 0.01]
   }  # 4×4 = 16 combinaisons × 5 folds = 80 fits !

   from sklearn.model_selection import GridSearchCV
   search = GridSearchCV(pipe, param_grid, cv=5, scoring='f1', n_jobs=-1)
   search.fit(X_train, y_train)
   print(search.best_params_, search.best_score_)

2. RANDOM SEARCH (rapide) :
   Tire N combinaisons aleatoires → souvent trouve 90% de la performance
   avec 10% du temps de Grid Search.

   from sklearn.model_selection import RandomizedSearchCV
   search = RandomizedSearchCV(pipe, param_grid, n_iter=20, cv=5)

3. BAYESIAN OPTIMIZATION (intelligent) :
   Utilise les resultats precedents pour guider la recherche.
   Libraries : Optuna, Hyperopt, scikit-optimize
   → Converge plus vite que Random Search

4. HALVING GRID SEARCH (efficient) :
   Commence avec beaucoup de candidats et peu de donnees.
   Elimine progressivement les moins prometteurs.
   from sklearn.model_selection import HalvingGridSearchCV""",
                    "duration": "45 min"
                },
                {
                    "title": "Versioning des modeles MLflow",
                    "content": """MLflow est la plateforme open-source la plus populaire pour gerer le cycle de vie complet des modeles ML.

LES 4 COMPOSANTES DE MLFLOW :

1. MLFLOW TRACKING — journaliser les experiences :
   import mlflow

   with mlflow.start_run(run_name='exp_001'):
       mlflow.log_param('learning_rate', 0.001)
       mlflow.log_param('batch_size', 32)
       mlflow.log_metric('train_loss', 0.25)
       mlflow.log_metric('val_accuracy', 0.91)
       mlflow.log_artifact('confusion_matrix.png')
       mlflow.sklearn.log_model(model, 'model')

   Tableau de bord web : comparer toutes les runs cote a cote !
   → Filtrer par parametres, trier par metrique

2. MLFLOW PROJECTS — reproductibilite :
   Structure standardisee avec MLproject (YAML)
   → Definir l'environnement conda/docker, les entry points
   → mlflow run . -P alpha=0.5

3. MLFLOW MODELS — packaging :
   Format universel ("flavor") qui abstrait le framework :
   → sklearn, tensorflow, pytorch, onnx, spark...
   → mlflow.pyfunc : interface generique
   Deploiement :
   → mlflow models serve -m runs:/<run_id>/model -p 5000
   → mlflow.sagemaker.deploy() pour AWS SageMaker

4. MLFLOW MODEL REGISTRY — gouvernance :
   Etats du cycle de vie :
   → Staging : teste mais pas en production
   → Production : le modele actif en service
   → Archived : ancien modele garde en historique

   Actions :
   → Enregistrer un nouveau modele : mlflow.register_model()
   → Transitionner entre etapes avec approbations
   → Annotations et commentaires par l'equipe
   → Comparaison automatique ancien vs nouveau modele

INTEGRATION CI/CD :
→ Dans GitHub Actions : lancer les experiences, comparer, promouvoir si amelioration
→ MLflow Autologging : log automatique de tous les params/metriques pour sklearn""",
                    "duration": "50 min"
                },
                {
                    "title": "Conteneurisation avec Docker",
                    "content": """Docker permet d'encapsuler un modele ML et toutes ses dependances dans un conteneur portable et reproductible.

POURQUOI DOCKER POUR LE ML ?
"Ca marche sur ma machine !" → probleme classique en ML
→ Python 3.8 sur dev, 3.10 sur prod, versions differentes de numpy, CUDA...
→ Docker fige l'environnement complet : "build once, run anywhere"

CONCEPTS CLES :
• IMAGE : snapshot immuable (les couches)
• CONTENEUR : instance en cours d'execution de l'image
• REGISTRY : depot d'images (Docker Hub, ECR, GCR)

DOCKERFILE EXEMPLE (API ML) :
  # Image de base legere
  FROM python:3.10-slim

  # Definir le repertoire de travail
  WORKDIR /app

  # Copier et installer les dependances
  COPY requirements.txt .
  RUN pip install --no-cache-dir -r requirements.txt

  # Copier le code de l'application
  COPY ./app ./app
  COPY model.pkl .

  # Exposer le port
  EXPOSE 8000

  # Commande de demarrage
  CMD [\"uvicorn\", \"app.main:app\", \"--host\", \"0.0.0.0\", \"--port\", \"8000\"]

MULTI-STAGE BUILD (image legere) :
  # Stage 1 : Builder (installe tout)
  FROM python:3.10 AS builder
  RUN pip install --user torch scikit-learn fastapi

  # Stage 2 : Production (copie seulement le necessaire)
  FROM python:3.10-slim
  COPY --from=builder /root/.local /root/.local
  COPY app/ ./app/
  → Reduit la taille de l'image de 5 Go a 500 Mo !

DOCKER COMPOSE (plusieurs services) :
  version: '3.8'
  services:
    api:
      build: .
      ports: [\"8000:8000\"]
      depends_on: [redis]
    redis:
      image: redis:alpine
    nginx:
      image: nginx
      ports: ["80:80"]

BONNES PRATIQUES :
→ .dockerignore : exclure les fichiers inutiles (data/, __pycache__/)
→ Non-root user pour la securite
→ Healthcheck pour la robustesse
→ Variables d'environnement pour la config (pas dans l'image !)""",
                    "duration": "55 min"
                },
                {
                    "title": "Deploiement avec FastAPI",
                    "content": """FastAPI est le framework Python modern pour creer des APIs ML en production, avec validation automatique et documentation interactive.

POURQUOI FASTAPI POUR LE ML ?
→ RAPIDE : performance comparable a Node.js et Go (base sur Starlette + Pydantic)
→ ASYNC : supporte les requetes asynchrones (important pour le ML lent)
→ VALIDATION AUTOMATIQUE via Pydantic : types Python → schema JSON
→ DOCUMENTATION AUTO : Swagger UI et ReDoc generes automatiquement

API ML COMPLETE :
  from fastapi import FastAPI, HTTPException
  from pydantic import BaseModel
  import pickle, numpy as np

  app = FastAPI(title="API Prediction ML", version="1.0")

  # Charger le modele au demarrage
  @app.on_event("startup")
  async def load_model():
      app.state.model = pickle.load(open('model.pkl', 'rb'))
      app.state.scaler = pickle.load(open('scaler.pkl', 'rb'))

  # Schema de validation automatique
  class PredictionInput(BaseModel):
      surface: float
      nb_chambres: int
      quartier: str
      class Config:
          schema_extra = {"example": {"surface": 80, "nb_chambres": 3, "quartier": "centre"}}

  class PredictionOutput(BaseModel):
      prix_predit: float
      intervalle_confiance: list[float]
      modele_version: str

  @app.post("/predict", response_model=PredictionOutput)
  async def predict(input: PredictionInput):
      try:
          features = np.array([[input.surface, input.nb_chambres,
                                1 if input.quartier == 'centre' else 0]])
          features_scaled = app.state.scaler.transform(features)
          prediction = app.state.model.predict(features_scaled)[0]
          return PredictionOutput(
              prix_predit=float(prediction),
              intervalle_confiance=[prediction*0.9, prediction*1.1],
              modele_version="v1.2.3"
          )
      except Exception as e:
          raise HTTPException(status_code=500, detail=str(e))

  @app.get("/health")
  async def health():
      return {"status": "ok", "model": "loaded"}

DEPLOIEMENT :
  # Developpement
  uvicorn main:app --reload

  # Production (plusieurs workers)
  gunicorn main:app -w 4 -k uvicorn.workers.UvicornWorker""",
                    "duration": "60 min"
                },
                {
                    "title": "Monitoring et drift detection",
                    "content": """Le monitoring ML en production detecte quand un modele commence a se degrader pour declencher un reentrainement.

POURQUOI LE MONITORING EST CRITIQUE ?
Un modele entraine en janvier peut se degrader en juillet :
→ Les donnees changent (comportement des utilisateurs, saison, evenements)
→ Le concept sous-jacent evolue
→ Sans monitoring, on ne sait pas quand le modele est devenu inutile !

TYPES DE DERIVE :

1. DATA DRIFT (derive des entrees) :
   La distribution P(X) change.
   Exemple : le modele de credit entraine avec des clients 25-45 ans
   commence a recevoir des demandes de 18-24 ans.
   Detection : tests statistiques KS (Kolmogorov-Smirnov), PSI

2. CONCEPT DRIFT (derive du concept) :
   La relation P(Y|X) change.
   Exemple : les mots qui signalaient le spam ont change.
   Detection : degradation des metriques sur des donnees etiquetees

3. PREDICTION DRIFT :
   La distribution des predictions change.
   Exemple : le modele predit de plus en plus souvent "fraude".
   Detection : surveiller la distribution des sorties

4. DATA QUALITY :
   Valeurs nulles, hors-range, types incorrects...
   → Souvent dus a des changements dans le pipeline amont

OUTILS :
• Evidently AI (open-source) :
  import evidently
  from evidently.report import Report
  from evidently.metric_preset import DataDriftPreset
  report = Report(metrics=[DataDriftPreset()])
  report.run(reference_data=X_train, current_data=X_prod)
  report.save_html("drift_report.html")

• WhyLabs, Arize : plateformes SaaS
• MLflow + Grafana + Prometheus : stack open-source

REENTRAINEMENT :
Strategies :
→ Planifie : reentrainer toutes les semaines/mois
→ Declenche : reentrainer si derive detectee ou metrique < seuil
→ Online learning : mise a jour continue (streaming)""",
                    "duration": "55 min"
                },
                {
                    "title": "CI/CD pour le ML",
                    "content": """MLOps applique les pratiques DevOps au ML pour automatiser le deploiement de modeles de bout en bout.

LES 3 NIVEAUX DE MATURITE MLOps :

Niveau 0 — ML Manuel :
→ Data scientists travaillent en notebooks Jupyter
→ Deploiement manuel (exporter le pickle, copier sur le serveur)
→ Pas de monitoring, pas de tests
→ Typique au debut d'un projet ML

Niveau 1 — Pipeline ML automatise :
→ Pipeline de donnees + entrainement automatise
→ Declenchement automatique si nouvelles donnees
→ Monitoring basique
→ Feature Store partage entre equipes

Niveau 2 — CI/CD pour le ML :
→ Tests automatiques (donnees, modele, performance)
→ Pipeline CI/CD declenche a chaque commit
→ Deploiement automatique si les tests passent
→ Monitoring avance + alertes + reentrainement auto

PIPELINE CI/CD ML (GitHub Actions) :
  name: ML Pipeline
  on: push
  jobs:
    test-and-deploy:
      steps:
      - name: Tests donnees
        run: python test_data_quality.py
      - name: Entrainement
        run: python train.py
      - name: Validation modele
        run: python validate.py --min-accuracy=0.90
      - name: Build Docker
        run: docker build -t ml-api:${{ github.sha }} .
      - name: Push et Deploy
        run: kubectl apply -f k8s/deployment.yaml

TYPES DE TESTS ML :
→ Tests de donnees : schema, valeurs nulles, distributions (Great Expectations)
→ Tests de code : fonctions de preprocessing (pytest)
→ Tests de modele : performance > seuil, pas de regression
→ Tests de l'API : latence < 200ms, erreur < 0.1%

PLATEFORMES MLOps :
• Kubeflow (Google) : ML sur Kubernetes, tres flexible
• SageMaker (AWS) : service manage complet
• Azure ML (Microsoft) : integration Azure, AutoML
• Vertex AI (Google Cloud) : pipeline unifie
• Weights & Biases : experimentation + monitoring

FEATURE STORE :
→ Partager et reutiliser les features entre modeles
→ Eviter le double calcul, garantir la coherence
→ Feast (open-source), Tecton, Hopsworks""",
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
                    "content": """Machine Learning (ML) is a branch of Artificial Intelligence that enables computers to learn automatically from data, without being explicitly programmed for each task.

🔑 THE KEY DISTINCTION:
Traditional programming: a developer writes explicit rules (IF temperature > 30 THEN display 'hot').
With ML: we show thousands of examples to a model, and it DISCOVERS the rules by itself.

Formal definition (Tom Mitchell, 1997):
"A computer program is said to learn from experience E with respect to some task T and performance measure P, if its performance on T, as measured by P, improves with experience E."

📊 THE 3 FUNDAMENTAL TYPES:

1. SUPERVISED LEARNING
   - Data: LABELED (input + correct answer)
   - Example: 10,000 cat/dog photos, each with its label
   - Goal: learn the mapping f(X) = Y
   - Use cases: email spam detection, price prediction, medical diagnosis

2. UNSUPERVISED LEARNING
   - Data: NO labels — the model finds hidden structures alone
   - Example: group customers by purchase behavior without pre-defining segments
   - Use cases: market segmentation, anomaly detection, data compression

3. REINFORCEMENT LEARNING
   - An AGENT learns by trial-and-error in an environment
   - Receives REWARDS (+) or PENALTIES (-) based on its actions
   - Example: AlphaGo learns chess by playing millions of games against itself
   - Use cases: robotics, video games, algorithmic trading

🌍 REAL-WORLD APPLICATIONS:
• Facial recognition (Face ID on iPhone)
• Netflix / Spotify / YouTube recommendations
• Real-time bank fraud detection
• Self-driving cars (Tesla Autopilot)
• Machine translation (Google Translate)
• Voice assistants (Siri, Alexa, Google Assistant)
• Medical imaging (detecting cancers in MRI scans)

💡 EDUCATIONAL ANALOGY:
ML is like teaching a child to recognize dogs. The child sees hundreds of dogs (data), progressively learns their characteristics (4 legs, snout, fur), and eventually recognizes a dog they have never seen before. That is exactly what an ML model does!""",
                    "duration": "45 min"
                },
                {
                    "title": "Types of Learning",
                    "content": """In this lesson we go deep into each learning paradigm with concrete examples and the algorithms associated with each.

🟢 SUPERVISED LEARNING — "Learning with a teacher"

How it works:
  Input data (X) + Correct labels (Y) → Model learns f(X) = Y

Two main categories:

  a) CLASSIFICATION: predict a DISCRETE category
     - Email → [spam, normal]
     - Photo → [cat, dog, bird]
     - Algorithms: KNN, SVM, Decision Tree, Random Forest, Neural Networks

  b) REGRESSION: predict a CONTINUOUS value
     - (area, neighbourhood) → house price in dollars
     - Yesterday's temperature → tomorrow's temperature
     - Algorithms: Linear Regression, Ridge, Lasso, Gradient Boosting

🟡 UNSUPERVISED LEARNING — "Learning without a teacher"

No labels! The model discovers hidden structures.

  a) CLUSTERING (Grouping):
     - K-Means: divides data into K compact groups
     - DBSCAN: finds arbitrarily-shaped clusters
     - Hierarchical: builds a similarity tree

  b) DIMENSIONALITY REDUCTION:
     - PCA: compresses data while preserving variance
     - t-SNE: visualises complex data in 2D/3D
     - Autoencoders: non-linear neural compression

  c) ASSOCIATION RULES:
     - Find correlations: "People who buy X also buy Y"
     - Apriori algorithm for market-basket analysis

🔴 REINFORCEMENT LEARNING — "Learning from experience"

Key components:
  • Agent: the model that makes decisions
  • Environment: the world the agent operates in
  • State (s): description of the current situation
  • Action (a): what the agent can do
  • Reward (r): feedback signal (+/-) after each action
  • Policy (π): the strategy the agent follows

Learning loop:
  Agent observes state → picks action → receives reward → updates strategy

Algorithms: Q-Learning, DQN (Deep Q-Network), PPO, A3C

📋 COMPARISON TABLE:
Type              | Data         | Objective              | Example
Supervised        | Labeled      | Predict output         | Spam or not?
Unsupervised      | Unlabeled    | Find patterns          | Segment customers
Reinforcement     | Interactions | Maximize reward        | Play chess""",
                    "duration": "50 min"
                },
                {
                    "title": "Linear Regression",
                    "content": """Linear regression is one of the most foundational ML algorithms. It models the relationship between an output variable (Y) and one or more input variables (X).

📐 THE MATH:

Simple linear regression (1 variable):
   y = mx + b
   • y = predicted value (e.g. house price)
   • x = input feature (e.g. area in m²)
   • m = slope (coefficient): how much y increases when x increases by 1
   • b = y-intercept (bias): value of y when x = 0

Multiple linear regression (several variables):
   y = w₁x₁ + w₂x₂ + ... + wₙxₙ + b
   e.g.: price = 2500 × area + 15000 × bedrooms − 5000 × age + 50000

🎯 HOW THE MODEL LEARNS — Ordinary Least Squares:

Objective: find the line that passes CLOSEST to all data points.

   Error = Σ (actual_value − predicted_value)²

We minimise this sum of squared errors (MSE) to find the best m and b.

Why SQUARED?
  1. Makes all errors positive
  2. Penalises large errors more heavily

📏 EVALUATION METRICS:

• R² (coefficient of determination): between 0 and 1
  - R² = 1 → perfect model, explains 100% of variance
  - R² = 0.85 → model explains 85% of data variation
  - R² < 0 → model is worse than simply predicting the mean!

• MAE (Mean Absolute Error): average absolute error
  - Easy to interpret: "on average, I'm off by $X"

• RMSE (Root Mean Square Error): penalises large errors more
  - Same unit as y, but more sensitive to outliers

💡 CONCRETE EXAMPLE — House price prediction:
   Dataset: 1,000 houses with area, bedrooms, neighbourhood, price

   After training, the model finds:
   price = 2800 × area + 12000 × bedrooms + 30000 × premium_area + 40000

   For an 80m², 3-bedroom house in a normal area:
   price = 2800×80 + 12000×3 + 0 + 40000 = 224000 + 36000 + 40000 = $300,000

⚠️ ASSUMPTIONS & LIMITATIONS:
   • Assumes a LINEAR relationship (if the true relationship is curved → problem)
   • Sensitive to OUTLIERS (extreme values)
   • Does not capture complex feature interactions
   • For non-linear relationships: Polynomial Regression, Random Forest, etc.

🐍 PYTHON CODE (scikit-learn):
   from sklearn.linear_model import LinearRegression
   from sklearn.metrics import r2_score, mean_absolute_error

   model = LinearRegression()
   model.fit(X_train, y_train)        # Training
   y_pred = model.predict(X_test)     # Prediction
   print(f"R² = {r2_score(y_test, y_pred):.3f}")""",
                    "duration": "55 min"
                },
                {
                    "title": "Classification with KNN",
                    "content": """K-Nearest Neighbors (KNN) is an intuitive algorithm that classifies a new element by looking at the K closest elements in the training data.

🧠 THE INTUITION:
"Tell me who your neighbours are, and I will tell you who you are."
→ A point is classified by MAJORITY VOTE among its K nearest neighbours.

📍 HOW IT WORKS (step by step):

1. For a new point to classify:
2. Compute the DISTANCE to every training point
3. Select the K closest points (neighbours)
4. VOTE: the majority class among the K neighbours is the prediction
5. (For regression: take the AVERAGE of the K neighbours' values)

📏 DISTANCES — How do we measure "closeness"?

• EUCLIDEAN distance (most common):
  d = √[(x₁−x₂)² + (y₁−y₂)²]
  → Straight-line ("as the crow flies") distance

• MANHATTAN distance:
  d = |x₁−x₂| + |y₁−y₂|
  → Moving along a grid of streets

• MINKOWSKI distance: generalisation of both

🔢 CHOOSING K — The most important hyperparameter:

• SMALL K (e.g. K=1):
  → Very complex model, memorises training noise
  → Risk of OVERFITTING: poor generalisation
  → Very jagged decision boundary

• LARGE K (e.g. K=100):
  → Too simple, ignores important details
  → Risk of UNDERFITTING
  → Overly smooth decision boundary

• OPTIMAL K: found by CROSS-VALIDATION
  → Test K = 1, 3, 5, 7, 11, … and keep the best

💡 PRACTICAL RULE: use an odd K to avoid ties in binary classification.

✅ ADVANTAGES:
• Very simple to understand and implement
• No training! ("lazy" algorithm)
• Naturally handles multi-class problems
• Can learn complex decision boundaries

❌ LIMITATIONS:
• SLOW at prediction: computes all distances each time O(n×d)
• Scale-sensitive: normalisation is MANDATORY
• Suffers from the curse of dimensionality
• Requires storing the ENTIRE dataset in memory

🔄 MANDATORY PREPROCESSING — Normalisation:
  Without it: if area = 80 and price = 200,000, distance is dominated by price!
  With StandardScaler: all features contribute equally.

🐍 PYTHON CODE:
  from sklearn.neighbors import KNeighborsClassifier
  from sklearn.preprocessing import StandardScaler

  scaler = StandardScaler()
  X_train_scaled = scaler.fit_transform(X_train)
  X_test_scaled  = scaler.transform(X_test)

  model = KNeighborsClassifier(n_neighbors=5, metric='euclidean')
  model.fit(X_train_scaled, y_train)
  y_pred = model.predict(X_test_scaled)""",
                    "duration": "50 min"
                },
                {
                    "title": "Clustering with K-Means",
                    "content": """K-Means is the most popular clustering algorithm. It partitions data into K groups such that points in the same cluster are as similar as possible.

🎯 OBJECTIVE:
Minimise the sum of distances from points to their cluster centre (centroid):
  Minimise: Σ Σ ||x − μₖ||²

💡 ANALOGY:
Imagine 1,000 students to be distributed into K classes. K-Means automatically finds the most homogeneous groupings based on their academic profiles.

🔄 ITERATIVE ALGORITHM (4 steps):

STEP 1 — INITIALISATION:
   Randomly pick K points as initial centroids.
   (Advanced: K-Means++ chooses well-spread initial centres)

STEP 2 — ASSIGNMENT:
   Assign each point to the cluster with the nearest centroid:
   cluster = argmin_k ||x − μₖ||²

STEP 3 — UPDATE:
   Recompute each centroid as the MEAN of all points in that cluster:
   μₖ = (1/|Cₖ|) × Σ x  for x in Cₖ

STEP 4 — CONVERGENCE:
   Repeat steps 2 & 3 until clusters stop changing (or max iterations reached).

🔢 CHOOSING K — The ELBOW METHOD:

Compute inertia (sum of squared internal distances) for K = 1, 2, …, 10.
Plot the curve and look for the "elbow" = where improvement slows down.

Example:
   K=1 : inertia = 1000
   K=2 : inertia = 500  (gain 500)
   K=3 : inertia = 280  (gain 220)
   K=4 : inertia = 200  (gain 80)  ← ELBOW here, K=3 or 4 optimal
   K=5 : inertia = 180  (gain 20)

✅ ADVANTAGES:
• Simple and fast O(n×K×i×d)
• Works well for spherical, well-separated clusters
• Scalable to large datasets

❌ LIMITATIONS:
• Must specify K in advance
• Sensitive to random initialisation → use K-Means++
• Struggles with non-spherical cluster shapes
• Sensitive to outliers (extreme values shift centroids)

🌍 REAL-WORLD APPLICATIONS:

1. MARKETING SEGMENTATION:
   Group customers by behaviour (purchase frequency, basket size…)
   → Tailor ad campaigns to each segment

2. IMAGE COMPRESSION:
   Replace each pixel colour with the nearest centroid colour
   → Reduce 16M colours to only K colours!

3. ANOMALY DETECTION:
   Points very far from any centroid are suspicious

4. FEATURE ENGINEERING:
   Use cluster assignments as new features

🐍 PYTHON CODE:
  from sklearn.cluster import KMeans

  # Find optimal K
  inertias = []
  for k in range(1, 11):
      km = KMeans(n_clusters=k, init='k-means++', n_init=10)
      km.fit(X)
      inertias.append(km.inertia_)

  # Final model
  kmeans = KMeans(n_clusters=4, init='k-means++', n_init=10, random_state=42)
  labels  = kmeans.fit_predict(X)
  centres = kmeans.cluster_centers_""",
                    "duration": "55 min"
                },
                {
                    "title": "Model Evaluation",
                    "content": """Model evaluation is a crucial step to ensure our model will generalise well to new, unseen data — not just memorise the training examples.

📂 SPLITTING DATA — The Golden Rule:

Always divide the dataset into 3 parts:
• TRAIN (70%): learn model parameters
• VALIDATION (15%): tune hyperparameters and compare models
• TEST (15%): final evaluation (touch it ONCE at the very end!)

⚠️ COMMON MISTAKE: using test data during tuning → results will be overly optimistic!

📊 CLASSIFICATION METRICS:

Example: cancer detection (Positive = sick, Negative = healthy)

Confusion Matrix (100 patients):
                  | Predicted Positive | Predicted Negative |
  True Positive   |   TP = 40         |   FN = 10         |
  True Negative   |   FP = 5          |   TN = 45         |

• ACCURACY = (TP+TN) / Total = 85/100 = 85%
  ⚠️ Problem: if 95% of emails are normal, a model that always predicts "normal" has 95% accuracy!

• PRECISION = TP / (TP + FP) = 40/45 = 88.9%
  "Of those I identified as sick, how many really were?"

• RECALL (Sensitivity) = TP / (TP + FN) = 40/50 = 80%
  "Of all truly sick patients, how many did I catch?"
  → Critical in medicine: missing a sick patient is very serious (dangerous FN)

• F1-SCORE = 2 × (Precision × Recall) / (Precision + Recall)
  → Balance between Precision and Recall, useful with imbalanced classes

• ROC-AUC: area under the ROC curve (true positive rate vs false positive rate)
  → AUC = 1.0: perfect model | AUC = 0.5: random model

🎭 OVERFITTING vs UNDERFITTING — The 2 enemies:

UNDERFITTING:
  → Model too SIMPLE to capture data complexity
  → Poor performance on both train AND test
  → Fix: more complex model, more features, less regularisation

OVERFITTING:
  → Model has MEMORISED training data (noise included)
  → Excellent on train, poor on test
  → Fix: more data, regularisation (L1/L2), Dropout, cross-validation

🔄 K-FOLD CROSS-VALIDATION:

Instead of a single train/test split, perform K rotations:
  Fold 1: [TEST] [TRAIN] [TRAIN] [TRAIN] [TRAIN]
  Fold 2: [TRAIN] [TEST] [TRAIN] [TRAIN] [TRAIN]
  …
  Final score = AVERAGE of K scores → more reliable estimate!

⚖️ BIAS-VARIANCE TRADEOFF:

• BIAS: systematic error (model too simple)
• VARIANCE: sensitivity to data fluctuations (model too complex)
• We seek the SWEET SPOT where both are low

🐍 PYTHON CODE:
  from sklearn.model_selection import cross_val_score, train_test_split
  from sklearn.metrics import classification_report, confusion_matrix

  X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

  # Cross-validation
  scores = cross_val_score(model, X_train, y_train, cv=5, scoring='f1')
  print(f"Mean F1: {scores.mean():.3f} ± {scores.std():.3f}")

  # Full report
  y_pred = model.predict(X_test)
  print(classification_report(y_test, y_pred))""",
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
                    "content": """The perceptron is the elementary building block of all neural networks. Understanding how it works is essential for mastering deep learning.

🧠 BIOLOGICAL INSPIRATION:
A biological neuron receives signals from its dendrites, accumulates them, and if the threshold is exceeded, fires a signal through its axon. The artificial perceptron is directly inspired by this mechanism.

📐 THE PERCEPTRON — COMPLETE FORMULA:

  output = f( w₁×x₁ + w₂×x₂ + ... + wₙ×xₙ + b )

Breakdown:
• x₁, x₂, ..., xₙ = inputs (problem features)
• w₁, w₂, ..., wₙ = weights (importance of each input)
• b = bias (allows shifting the decision boundary)
• f = activation function (introduces non-linearity)
• The sum w×x + b = LINEAR COMBINATION (dot product)

💡 CONCRETE EXAMPLE:
  Spam detection (2 features):
  - x₁ = number of suspicious keywords (e.g. "money", "free")
  - x₂ = email length in words

  After training: w₁ = 0.8, w₂ = -0.3, b = -1.5
  For an email (x₁=3, x₂=50):
  z = 0.8×3 + (-0.3)×50 + (-1.5) = 2.4 − 15 − 1.5 = -14.1
  output = sigmoid(-14.1) ≈ 0 → NOT SPAM

🏗️ MULTI-LAYER NETWORKS (MLP):

A single perceptron can only solve linearly separable problems.
The solution: stack multiple perceptrons in LAYERS:

  Input Layer → Hidden Layers → Output Layer

Typical architecture for image classification:
  784 inputs (28×28 pixels) → [256] → [128] → [64] → 10 outputs (digits 0–9)

FORWARD PROPAGATION:
  At each layer: z = W × a + b, then a = f(z)
  Activations flow layer by layer to the final output.

🌐 UNIVERSAL APPROXIMATION THEOREM:
An MLP with a single sufficiently large hidden layer can approximate ANY continuous function.
→ Theoretically, a neural network can learn anything!
→ In practice: DEEP networks (many layers) learn better representations with fewer neurons.

📊 VECTORISED REPRESENTATION:
Using matrices, computing an entire layer is:
   A[l] = f( W[l] × A[l-1] + b[l] )
→ Very efficient on GPU with NumPy/TensorFlow/PyTorch

🐍 PYTORCH CODE:
  import torch.nn as nn

  class MLP(nn.Module):
      def __init__(self):
          super().__init__()
          self.layers = nn.Sequential(
              nn.Linear(784, 256), nn.ReLU(),
              nn.Linear(256, 128), nn.ReLU(),
              nn.Linear(128, 10),  nn.Softmax(dim=1)
          )

      def forward(self, x):
          return self.layers(x)""",
                    "duration": "60 min"
                },
                {
                    "title": "Activation Function and Backpropagation",
                    "content": """Activation functions and backpropagation are the two mechanisms that enable neural networks to learn complex representations.

⚡ ACTIVATION FUNCTIONS — Why are they necessary?

Without activation functions, stacking linear layers always gives a LINEAR result (Ax + b). Non-linearity allows the network to model complex decision boundaries.

Main functions:

1. ReLU (Rectified Linear Unit) — most popular today:
   f(x) = max(0, x)
   • Derivative: 1 if x > 0, 0 otherwise
   ✅ Fast to compute, avoids vanishing gradient for x > 0
   ❌ "Dead neurons": if a neuron always receives negative input, its gradient = 0

2. Sigmoid:
   f(x) = 1 / (1 + e^{−x}) → output between 0 and 1
   ✅ Ideal for binary classification output (probability)
   ❌ Vanishing gradient for extreme values

3. Tanh:
   f(x) = (e^x − e^{−x}) / (e^x + e^{−x}) → output between −1 and 1
   ✅ Zero-centred (better convergence than Sigmoid)
   ❌ Same vanishing gradient problem

4. Modern variants:
   • Leaky ReLU: f(x) = max(0.01x, x) → fixes dead neurons
   • GELU: used in BERT, GPT → smoother than ReLU
   • Swish: f(x) = x × sigmoid(x) → often beats ReLU in practice

🔄 BACKPROPAGATION — How the network learns:

Backpropagation computes how to adjust each weight to reduce error. It uses the CHAIN RULE of calculus.

STEPS:

1. FORWARD PASS: compute prediction y_pred
2. COMPUTE LOSS:
   - Classification: Cross-Entropy = −Σ y × log(y_pred)
   - Regression: MSE = (1/n) × Σ (y − y_pred)²
3. BACKWARD PASS: compute ∂Loss/∂w for every weight w
4. WEIGHT UPDATE:
   w = w − α × ∂Loss/∂w
   (α = learning rate)

📉 GRADIENT DESCENT:
Imagine a ball on a foggy mountain searching for the valley (loss minimum):
• Gradient = direction of steepest ascent
• We move in the OPPOSITE direction (downhill)
• Learning rate α = step size

Optimiser variants:
• SGD: one example at a time
• Mini-batch SGD: batches of 32/64/128 (the standard)
• Momentum: accumulates past gradients to accelerate
• Adam (Adaptive Moment Estimation): combines Momentum + per-weight adaptive rate
  → Adam is the most widely used in practice!

🐍 PYTORCH CODE:
  criterion = nn.CrossEntropyLoss()
  optimizer = torch.optim.Adam(model.parameters(), lr=0.001)

  for epoch in range(100):
      optimizer.zero_grad()         # reset gradients
      y_pred = model(X_batch)       # forward pass
      loss = criterion(y_pred, y)   # compute loss
      loss.backward()               # backpropagation
      optimizer.step()              # update weights""",
                    "duration": "65 min"
                },
                {
                    "title": "Convolutional Neural Networks CNN",
                    "content": """Convolutional Neural Networks (CNNs) revolutionised computer vision. They exploit the spatial structure of images to learn hierarchical representations.

🖼️ WHY CNNs FOR IMAGES?

A classic MLP for a 224×224×3 image = 150,528 inputs!
→ Problems: too many parameters, ignores spatial structure, not translation-invariant.

CNNs solve this with 3 key ideas: locality, weight sharing, and hierarchy.

🔩 THE 3 FUNDAMENTAL OPERATIONS:

1. CONVOLUTION (Conv2D layer):
   A FILTER (kernel) slides over the image computing dot products.
   • 3×3 filter = 9 weights (shared across the entire image!)
   • The same filter detects the same pattern everywhere
   • 32 filters → 32 "feature maps"

   What different filters detect:
   • Early layers: edges, corners, colours (universal)
   • Middle layers: textures, simple shapes
   • Deep layers: face parts, wheels, eyes…

2. POOLING (Max Pooling):
   Reduces spatial size while keeping the most important information.
   • MaxPool 2×2: takes the MAXIMUM in each 2×2 region
   • Halves the size → fewer computations, more robust to small shifts

3. ReLU ACTIVATION:
   After each convolution: f(x) = max(0, x) → non-linearity

📐 TYPICAL FULL ARCHITECTURE:

  Image (224×224×3)
  → Conv2D(32 filters, 3×3) + ReLU → (222×222×32)
  → MaxPool(2×2)              → (111×111×32)
  → Conv2D(64 filters, 3×3) + ReLU → (109×109×64)
  → MaxPool(2×2)              → (54×54×64)
  → Flatten                   → (186,624,)
  → Dense(256) + ReLU         → (256,)
  → Dense(10) + Softmax       → (10,) [10 classes]

🏗️ FAMOUS ARCHITECTURES:

• LeNet (1998): first CNN, MNIST handwritten digits
• AlexNet (2012): the revolution! ImageNet, 5 conv layers, Dropout
• VGG (2014): very deep, only 3×3 filters, 138M parameters
• ResNet (2015): residual (skip) connections → train 152-layer networks!
  Key innovation: y = F(x) + x → eliminates vanishing gradient
• EfficientNet (2019): optimal width/depth/resolution scaling

💡 PARAMETER COUNT — Conv vs Dense:
   Conv2D(64, 3×3) on 32 input channels:
   Params = 64 × (3×3×32 + 1) = 64 × 289 = 18,496
   (far fewer than a Dense layer over the same data!)

🐍 KERAS CODE:
  from tensorflow.keras import layers, models

  model = models.Sequential([
      layers.Conv2D(32, (3,3), activation='relu', input_shape=(224,224,3)),
      layers.MaxPooling2D(2,2),
      layers.Conv2D(64, (3,3), activation='relu'),
      layers.MaxPooling2D(2,2),
      layers.Conv2D(128, (3,3), activation='relu'),
      layers.Flatten(),
      layers.Dense(512, activation='relu'),
      layers.Dropout(0.5),
      layers.Dense(10, activation='softmax')
  ])""",
                    "duration": "70 min"
                },
                {
                    "title": "Recurrent Networks RNN/LSTM",
                    "content": """Recurrent networks (RNN) and LSTMs are designed to process SEQUENCES: text, audio, time series, DNA…

🔄 WHY RNNs?

An MLP or CNN treats every input INDEPENDENTLY.
But to understand "The cat caught the mouse that it had been chasing", the word "it" depends on "cat" much earlier in the sentence.
→ RNNs have MEMORY: they maintain a hidden state h_t that encodes history.

📐 RNN FORMULA:

At each time step t:
   h_t = tanh( W_hh × h_{t-1} + W_xh × x_t + b )
   y_t = W_hy × h_t + b_y

• h_t = current hidden state (the network's "memory")
• h_{t-1} = previous hidden state
• x_t = input at time t (e.g. embedding of the current word)
• W_hh = recurrence matrix (how the past influences the present)
• W_xh = input matrix (how the input influences the state)

💡 ANALOGY:
A reader reading word by word. At each word, they update their understanding (h_t) by combining what they just read (x_t) with what they understood up to now (h_{t-1}).

⚠️ THE VANISHING GRADIENT PROBLEM:

During backpropagation through time (BPTT), gradients are multiplied by W_hh at every step.
• |W_hh| < 1: gradients VANISH → network forgets long-range dependencies
• |W_hh| > 1: gradients EXPLODE → unstable training

🔮 LSTM — Long Short-Term Memory (the solution):

LSTM adds a MEMORY CELL c_t and 3 GATES:

1. FORGET GATE f_t:
   f_t = σ(W_f × [h_{t-1}, x_t] + b_f)
   → Decides what to FORGET from previous memory
   → 0 = forget everything, 1 = keep everything

2. INPUT GATE i_t:
   i_t = σ(W_i × [h_{t-1}, x_t] + b_i)
   c̃_t = tanh(W_c × [h_{t-1}, x_t] + b_c)
   → Decides what to ADD to memory

3. CELL UPDATE:
   c_t = f_t ⊙ c_{t-1} + i_t ⊙ c̃_t
   (⊙ = element-wise multiplication)

4. OUTPUT GATE o_t:
   o_t = σ(W_o × [h_{t-1}, x_t] + b_o)
   h_t = o_t ⊙ tanh(c_t)

🔵 GRU (Gated Recurrent Unit):
Simplified LSTM with only 2 gates (reset and update).
→ Fewer parameters, often same performance, trains faster.

📊 COMPARISON:
   RNN   : simple, fast, quickly forgets long dependencies
   LSTM  : powerful, long memory, many parameters
   GRU   : good speed/performance trade-off

🌍 APPLICATIONS:
• Machine translation (seq2seq with attention)
• Text generation (GPT predecessors used LSTMs)
• Speech recognition
• Time-series forecasting (stock markets, weather)
• Sentiment analysis

🐍 PYTORCH CODE:
  class LSTMModel(nn.Module):
      def __init__(self, vocab_size, embed_dim, hidden_dim):
          super().__init__()
          self.embedding = nn.Embedding(vocab_size, embed_dim)
          self.lstm = nn.LSTM(embed_dim, hidden_dim, batch_first=True)
          self.fc = nn.Linear(hidden_dim, vocab_size)

      def forward(self, x, hidden):
          x = self.embedding(x)
          out, hidden = self.lstm(x, hidden)
          return self.fc(out), hidden""",
                    "duration": "65 min"
                },
                {
                    "title": "Introduction to Transformers",
                    "content": """Transformers revolutionised NLP in 2017 ("Attention Is All You Need") and now dominate all of deep learning, including computer vision.

🎯 THE PROBLEM TRANSFORMERS SOLVE:

RNNs/LSTMs process sequences WORD BY WORD → slow, hard to parallelise.
Transformers process the entire sequence IN PARALLEL → much faster!

⚡ THE SELF-ATTENTION MECHANISM:

The central idea: every word can "look at" all other words in the sentence to understand its context.

For each word, 3 vectors are created:
• Q (Query):  "What am I looking for?"
• K (Key):    "What do I offer?"
• V (Value):  "What information do I carry?"

Attention computation:
   Attention(Q, K, V) = softmax( Q × Kᵀ / √d_k ) × V

• Q × Kᵀ = compatibility score between every pair of words
• / √d_k = normalisation to prevent very small gradients
• softmax = converts scores to probabilities (sum = 1)
• × V = weighted sum of values by attention weights

💡 EXAMPLE:
Sentence: "The bank refused my loan because they ran out of money."
For "they" → attention will be HIGH on "bank" (not "loan") → disambiguation!

🎭 MULTI-HEAD ATTENTION:

Instead of one attention, run H IN PARALLEL (e.g. H=8 or H=16).
Each "head" learns to focus on different relationships:
• Head 1: syntactic relations (subject–verb)
• Head 2: semantic relations (synonyms)
• Head 3: co-reference ("it" → "the president")
…
Result: concatenate all heads → final linear projection.

🏗️ FULL TRANSFORMER ARCHITECTURE:

ENCODER (understanding):
  For each layer (×N):
  → Multi-Head Self-Attention
  → Add & Norm (residual connection + layer norm)
  → Feed-Forward Network (2 dense layers)
  → Add & Norm

DECODER (generating):
  For each layer:
  → Masked Multi-Head Self-Attention (can only see past)
  → Cross-Attention (attends to encoder output)
  → Feed-Forward Network

POSITIONAL ENCODING:
  Unlike RNNs, Transformers have no inherent ordering.
  → ADD positional encodings to embeddings to inject position information.

🌟 LANDMARK MODELS:

• BERT (2018, Google): encoder only, bidirectional
  → Pre-trained on MLM and NSP | excels at understanding, QA, classification

• GPT (OpenAI): decoder only, unidirectional
  → Pre-trained to predict next token
  → GPT-2 (1.5B), GPT-3 (175B), GPT-4 (multimodal)

• T5 (Google): encoder + decoder, everything as "text-to-text"

• Vision Transformer (ViT): applies Transformers to images!
  → Splits image into 16×16 pixel patches treated as "words"

✅ ADVANTAGES:
• Full parallelisation → highly efficient on GPU
• Captures very long-range dependencies
• Transfer learning via massive pre-training

❌ LIMITATIONS:
• Memory: O(n²) for attention → limits very long sequences
• Requires enormous data and compute for pre-training""",
                    "duration": "70 min"
                },
                {
                    "title": "Fine-tuning and Transfer Learning",
                    "content": """Transfer learning is one of the most powerful techniques in modern deep learning: reusing knowledge acquired on one task to accelerate learning on another.

🧠 WHY TRANSFER LEARNING WORKS:

Problem: training ResNet-50 on ImageNet from scratch takes weeks on 8 GPUs.
Solution: download the pre-trained weights and adapt them to our specific task.

Intuition: an expert photographer (pre-trained on millions of images) learns to distinguish diseases on X-rays faster than a complete beginner.

🔑 WHAT THE MODEL ALREADY KNOWS:

For a CNN like ResNet pre-trained on ImageNet:
• Early layers: edge, corner, and colour detectors (universal)
• Middle layers: textures and patterns (semi-universal)
• Late layers: ImageNet-specific object parts (less universal)

→ Early and middle layers are REUSABLE for almost any vision task!

📋 TWO MAIN APPROACHES:

1. FEATURE EXTRACTION:
   → FREEZE all pre-trained weights
   → Only add and train new classification layers at the top
   → When to use: very small dataset (<1,000 images), task similar to source

2. FULL FINE-TUNING:
   → Load pre-trained weights
   → "Unfreeze" all or part of the model
   → Train with a VERY small learning rate (e.g. 1e-5 vs 1e-3 normal)
   → When to use: medium to large dataset, task different from source

🔧 GRADUAL UNFREEZING:
   Step 1: train only the classification head
   Step 2: unfreeze last 2 layers + train
   Step 3: unfreeze entire model + train with very low lr

📊 ADVANCED TECHNIQUES:

• LoRA (Low-Rank Adaptation):
  Instead of modifying all weights, inject small low-rank matrices.
  → Reduces trainable parameters by 99%!
  → Very popular for LLMs (GPT, LLaMA)

• Prompt Engineering:
  Guide the model via instructions in the prompt, no weight updates.
  → Zero-shot: "Translate this text to Spanish: ..."
  → Few-shot: provide 3–5 examples in the prompt

• RLHF (Reinforcement Learning from Human Feedback):
  Technique used to align ChatGPT, Claude, Gemini…
  → Human evaluators rate responses
  → A reward model is trained
  → The LLM is then optimised via PPO

🐍 KERAS CODE (Feature Extraction):
  from tensorflow.keras.applications import ResNet50
  from tensorflow.keras import layers, models

  base_model = ResNet50(weights='imagenet', include_top=False, input_shape=(224,224,3))
  base_model.trainable = False  # FREEZE

  model = models.Sequential([
      base_model,
      layers.GlobalAveragePooling2D(),
      layers.Dense(256, activation='relu'),
      layers.Dropout(0.5),
      layers.Dense(num_classes, activation='softmax')
  ])

  model.compile(optimizer='adam', loss='categorical_crossentropy', metrics=['accuracy'])""",
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
                    "content": """Before feeding an NLP model, raw text must be transformed into a numerical representation. This preprocessing step is crucial and directly impacts model quality.

📝 COMPLETE PREPROCESSING PIPELINE:

Raw text → Cleaning → Tokenisation → Normalisation → Stop-word removal → Lemmatisation → Numerical vectors

1️⃣ TEXT CLEANING:
• Remove HTML tags: <p>Hello</p> → "Hello"
• Remove URLs: "visit https://example.com" → "visit"
• Remove special characters: "Wow!!!" → "Wow"
• Handle emojis: keep (sentiment), remove, or convert to text

2️⃣ TOKENISATION — Split text into units:

a) WORD-LEVEL:
   "The cat eats" → ["The", "cat", "eats"]
   ✅ Intuitive | ❌ Huge vocabulary, unknown words (OOV)

b) CHARACTER-LEVEL:
   "cat" → ["c", "a", "t"]
   ✅ No unknown tokens | ❌ Very long sequences, less semantic meaning

c) SUBWORD (THE MODERN STANDARD):
   BPE (Byte Pair Encoding): "running" → ["run", "ning"]
   → Start with characters, merge most-frequent pairs
   → Used by GPT-2, RoBERTa

   WordPiece: "playing" → ["play", "##ing"]
   → Similar to BPE, ## signals continuation
   → Used by BERT

   SentencePiece: multilingual, handles spaces differently
   → Used by T5, LLaMA

3️⃣ NORMALISATION:
• Lowercasing: "Twitter" → "twitter"
  ⚠️ Caution: "Apple" (company) vs "apple" (fruit) → information loss!
• Accent removal: "café" → "cafe" (sometimes useful)
• Contraction expansion: "don't" → "do not"

4️⃣ STOP-WORD REMOVAL:
Very frequent words with little meaning: "the", "a", "is", "of", "in"…
✅ Reduces noise for information retrieval
❌ Can hurt tasks where syntax matters (sentiment, translation)

5️⃣ STEMMING vs LEMMATISATION:

STEMMING (fast, approximate):
   "running", "runs", "runner" → "run" (brute truncation)
   Porter Stemmer, Snowball Stemmer

LEMMATISATION (slower, precise):
   "running", "runs", "runner" → "run" (dictionary base form)
   Requires morphological analysis — SpaCy, NLTK with dictionaries

6️⃣ NUMERICAL ENCODING:
• One-Hot: binary vector of size |vocabulary| — very sparse, no semantic meaning
• TF-IDF: term frequency × log(N/df) — upweights rare, distinctive words
• Word Embeddings: dense vectors of 50–300 dimensions (Word2Vec, GloVe)

🐍 PYTHON CODE (SpaCy):
  import spacy
  nlp = spacy.load("en_core_web_sm")

  text = "Cats have been hunting mice for centuries."
  doc = nlp(text)
  tokens = [token.lemma_.lower() for token in doc
            if not token.is_stop and not token.is_punct]
  print(tokens)  # ['cat', 'hunt', 'mouse', 'century']""",
                    "duration": "45 min"
                },
                {
                    "title": "Word Embeddings Word2Vec GloVe",
                    "content": """Word embeddings transform words into dense numerical vectors that capture semantic meaning. This is one of the most important advances in modern NLP.

🧩 WHY EMBEDDINGS?

One-Hot: "cat" = [1,0,0,...], "dog" = [0,1,0,...], "king" = [0,0,1,...]
Problem: vectors are orthogonal → the model has no idea that "cat" and "dog" are similar!

Word Embeddings: similar words have NEARBY vectors in the embedding space!
   "cat"  → [0.2, -0.4, 0.7, ...]  (300 dimensions)
   "dog"  → [0.3, -0.3, 0.8, ...]  (close to "cat"!)
   "king" → [0.9,  0.1, 0.2, ...]  (far away)

📐 WORD2VEC — The original architecture (2013, Google):

Distributional hypothesis: "a word is defined by its neighbours."
→ "cat" and "dog" appear in similar contexts → they will have similar vectors.

TWO ARCHITECTURES:

1. CBOW (Continuous Bag of Words):
   INPUT: context words → OUTPUT: central word
   "The ___ eats a mouse" → predict "cat"
   ✅ Faster, better for frequent words

2. SKIP-GRAM:
   INPUT: central word → OUTPUT: context words
   "cat" → predict ["The", "eats", "a", "mouse"]
   ✅ Better for rare words, more semantically precise
   ✅ The standard in practice

NEGATIVE SAMPLING trick:
Instead of computing probability over the entire vocabulary, train a binary classifier (true neighbour vs random word).
→ Drastically reduces computational cost!

🌐 GLOVE — Global Vectors (2014, Stanford):

Unlike Word2Vec using local windows, GloVe exploits the GLOBAL CO-OCCURRENCE MATRIX.

For each word pair (i, j):
   X_ij = number of times j appears in the context of i

Objective: embeddings such that wᵢ · w̃ⱼ + bᵢ + b̃ⱼ ≈ log(X_ij)

✅ Captures global corpus statistics | ✅ Excellent for analogies

⚡ FASTTEXT (2016, Facebook):

Innovation: decomposes words into CHARACTER N-GRAMS
   "cat" → ["<ca", "cat", "at>", "<cat>"]

✅ Handles OUT-OF-VOCABULARY (OOV) words: "catfish" unknown → composed from n-grams
✅ Better for morphologically rich languages (Arabic, Turkish, German…)
✅ Can represent misspellings!

🔮 FASCINATING PROPERTIES:

Vector arithmetic (analogies):
   king − man + woman ≈ queen  ✨
   Paris − France + Germany ≈ Berlin  ✨
   big − small + slow ≈ fast  ✨

These properties EMERGE NATURALLY from training!

📊 COMPARISON:
   Method    | Fixed vocab | OOV | Context  | Strengths
   Word2Vec  | Yes         | No  | Local    | Fast, quality embeddings
   GloVe     | Yes         | No  | Global   | Analogies, global stats
   FastText  | Infinite    | Yes | Local+char | Morphology, rare words
   BERT      | Yes         | No  | Contextual | Same word = different vector per context!

🐍 PYTHON CODE:
  from gensim.models import Word2Vec

  sentences = [["the", "cat", "eats"], ["the", "dog", "runs"], ...]
  model = Word2Vec(sentences, vector_size=100, window=5, min_count=1, workers=4)

  print(model.wv.similarity("cat", "dog"))   # 0.82
  print(model.wv.most_similar("king"))        # [("queen", 0.91), ...]""",
                    "duration": "55 min"
                },
                {
                    "title": "Sequence Models Seq2Seq",
                    "content": """The Seq2Seq (sequence-to-sequence) architecture transforms one variable-length sequence into another. It is the foundation of machine translation, text summarisation, and chatbots.

🔄 THE PROBLEM TO SOLVE:

Input: variable-length sequence (French sentence)
Output: variable-length sequence (English translation)
→ Lengths differ, words do not correspond 1-to-1!

🏗️ ENCODER-DECODER ARCHITECTURE:

ENCODER:
• Reads the input sequence WORD BY WORD (via LSTM/GRU)
• Progressively builds an understanding of the meaning
• Produces a CONTEXT VECTOR (h_T final state)
→ This vector is a compressed representation of the entire source sentence

DECODER:
• Takes the context vector as its initial state
• Generates the output sequence WORD BY WORD
• At each step, uses its own prediction as the next input

⚠️ BOTTLENECK PROBLEM:
All meaning must fit in ONE vector (e.g. 256 dimensions).
For long sentences → information loss!

✨ ATTENTION MECHANISM — The Solution:

Instead of only using h_T, the decoder can "look at" ALL encoder states.

At each decoding step t:
1. Compute score between decoder state s_t and each encoder state h_i:
   e_ti = score(s_t, h_i)

2. Apply softmax to get attention weights:
   α_ti = softmax(e_ti)  → sum = 1

3. Compute dynamic context vector:
   c_t = Σ α_ti × h_i  (weighted sum of encoder states)

4. Use c_t + s_t to predict the next word

💡 INTUITION:
To generate "cat" in English, the decoder will strongly attend to the source word "cat" in French (high α), ignoring other words.

📊 TEACHER FORCING:
During training, provide the TRUE word (not the prediction) as decoder input at each step.
✅ Converges faster | ❌ Train/inference mismatch (exposure bias)

🔍 BEAM SEARCH (decoding):
Instead of always picking the most probable word (greedy), maintain the K best partial sequences.
K=5 (beam width) → 5 candidate sequences in parallel → pick the best at the end.
✅ Better than greedy | ❌ Slower

🌍 APPLICATIONS:
• Translation: FR → EN, AR → FR
• Summarisation: long article → short summary
• Chatbots: question → answer
• Code generation: natural language → Python code
• Grammar correction: erroneous → corrected text""",
                    "duration": "60 min"
                },
                {
                    "title": "BERT and Pre-trained Models",
                    "content": """BERT (Bidirectional Encoder Representations from Transformers) redefined NLP benchmarks in 2018. It uses the Transformer encoder to create bidirectional contextual representations.

🎯 THE KEY INNOVATION: BIDIRECTIONALITY

GPT (before BERT): reads text LEFT TO RIGHT only.
BERT: considers context on BOTH LEFT AND RIGHT simultaneously!
   "The ___ refused my loan" → "bank" (thanks to full context)

→ The same word gets DIFFERENT representations depending on context:
   "bank" in "bank account" ≠ "bank" in "river bank"
   (CONTEXTUAL embeddings vs static Word2Vec)

📚 PRE-TRAINING — 2 TASKS:

1. MLM (Masked Language Model):
   • Randomly mask 15% of tokens with [MASK]
   • "The cat [MASK] a mouse" → predict "ate"
   • Forces the model to understand complete context

   The 15% masked tokens are treated as:
   • 80%: replaced by [MASK]
   • 10%: replaced by a random word
   • 10%: kept unchanged (robust learning)

2. NSP (Next Sentence Prediction):
   • Predict whether sentence B NATURALLY follows sentence A
   • Sentence A: "The dog barked loudly."
   • Sentence B (positive, 50%): "Its owner told it to be quiet."
   • Sentence B (negative, 50%): "Stars shine at night."
   → Forces BERT to understand inter-sentence relationships

📐 BERT ARCHITECTURE:

BERT uses ONLY the Transformer encoder.

Special tokens:
• [CLS]: start of every sequence (its final representation = whole-sentence feature)
• [SEP]: separator between two sentences
• [PAD]: padding to uniform length

BERT-Base: 12 layers, 12 attention heads, hidden=768, 110M parameters
BERT-Large: 24 layers, 16 heads, hidden=1024, 340M parameters
BERT processes up to 512 tokens.

🌍 IMPORTANT VARIANTS:

• RoBERTa (Facebook, 2019):
  - Trained longer with more data
  - Removes NSP (deemed unhelpful)
  - Larger batch sizes → outperforms BERT on most benchmarks

• ALBERT (Google, 2019):
  - Weight sharing across layers → far fewer parameters
  - ALBERT-Base: 12M params (vs 110M for BERT-Base)
  → Same performance, 10× less memory

• DistilBERT (HuggingFace, 2019):
  - Knowledge distillation: student trained to mimic BERT
  - 40% fewer parameters, 60% faster
  - Retains 97% of performance → ideal for production/mobile

🐍 HUGGINGFACE CODE:
  from transformers import BertTokenizer, BertModel
  import torch

  tokenizer = BertTokenizer.from_pretrained('bert-base-uncased')
  model = BertModel.from_pretrained('bert-base-uncased')

  inputs = tokenizer("The cat eats a mouse", return_tensors='pt', padding=True)

  with torch.no_grad():
      outputs = model(**inputs)

  # Contextual representation of each token
  hidden_states = outputs.last_hidden_state  # (batch, seq_len, 768)
  # Full sentence representation ([CLS] token)
  sentence_emb = hidden_states[:, 0, :]      # (batch, 768)""",
                    "duration": "65 min"
                },
                {
                    "title": "Fine-tuning for Classification",
                    "content": """Fine-tuning BERT adapts the pre-trained model to a specific task with a relatively small dataset (thousands, not millions of examples).

🎯 WHY FINE-TUNING WORKS SO WELL?

BERT has already learned:
• Grammar and syntax of the language
• Semantic relationships between words
• Contextual meaning of sentences
• Factual world knowledge

We only need to learn the SPECIFIC TASK on top of this solid foundation!

🏗️ ARCHITECTURE FOR TEXT CLASSIFICATION:

  Text → Tokenise → [CLS] token1 token2 ... [SEP]
            ↓
       BERT (12 layers)
            ↓
  [CLS] representation (768 dimensions)
            ↓
       Dense Layer (num_classes)
            ↓
       Softmax → Class probabilities

Why the [CLS] token?
→ Designed to aggregate information from the entire sequence (via bidirectional attention)

⚙️ CRITICAL HYPERPARAMETERS:

• LEARNING RATE: the most important!
  - Too large: overwrites pre-trained weights ("catastrophic forgetting")
  - Optimal range: 2e-5 to 5e-5 (much smaller than the standard 1e-3)
  - Recommended scheduler: linear warmup + cosine decay

• BATCH SIZE: 16 or 32 (limited by GPU VRAM)

• EPOCHS: 2 to 4 (beyond that → overfitting since BERT is already very capable)

• MAX_LENGTH: up to 512 tokens, but 128 or 256 usually suffices

🔧 ADVANCED STRATEGIES:

1. GRADUAL UNFREEZING:
   Epoch 1: train only the classification head
   Epoch 2: unfreeze last 2 BERT layers + head
   Epoch 3: unfreeze all of BERT + head
   → Prevents destroying low-level representations

2. DISCRIMINATIVE LEARNING RATES:
   Output layer: lr = 5e-5
   Middle layers: lr = 3e-5
   Lower layers:  lr = 1e-5
   → Universal low-level representations change more slowly

📊 COMPLETE EVALUATION (5 sentiment classes):

  Classification Report:
                  Precision  Recall  F1-Score  Support
  Very Negative     0.91      0.88    0.89       200
  Negative          0.84      0.86    0.85       180
  Neutral           0.78      0.80    0.79       150
  Positive          0.87      0.85    0.86       190
  Very Positive     0.92      0.91    0.91       180
  Macro avg         0.86      0.86    0.86       900

🐍 COMPLETE HUGGINGFACE CODE:
  from transformers import BertForSequenceClassification, TrainingArguments, Trainer

  model = BertForSequenceClassification.from_pretrained(
      'bert-base-uncased', num_labels=5
  )
  training_args = TrainingArguments(
      output_dir='./results',
      num_train_epochs=3,
      per_device_train_batch_size=16,
      learning_rate=2e-5,
      warmup_steps=500,
      weight_decay=0.01,
      evaluation_strategy="epoch"
  )
  trainer = Trainer(
      model=model, args=training_args,
      train_dataset=train_dataset, eval_dataset=val_dataset
  )
  trainer.train()""",
                    "duration": "55 min"
                },
                {
                    "title": "Text Generation with GPT",
                    "content": """GPT (Generative Pre-trained Transformer) is a family of text-generation models developed by OpenAI. Unlike BERT, GPT is a unidirectional AUTOREGRESSIVE model.

🤖 GPT ARCHITECTURE — TRANSFORMER DECODER:

GPT uses ONLY Transformer decoder layers.
At each position, the model can only see PREVIOUS tokens (causal attention).

Pre-training: predict the next token!
   P(token_t | token_1, token_2, ..., token_{t-1})

📈 THE GPT FAMILY:

• GPT-1 (2018): 117M parameters, 12 layers
  First model to demonstrate the power of pre-training + fine-tuning

• GPT-2 (2019): 1.5B parameters, 48 layers
  "Too dangerous to release" (OpenAI initially withheld it)
  First emergence of strong zero-shot capabilities

• GPT-3 (2020): 175B parameters (175 billion!)
  Remarkable few-shot capabilities
  Basis of ChatGPT (+ RLHF on top)

• GPT-4 (2023): unknown architecture, multimodal (text + images)
  Human-level performance on many benchmarks

🎲 DECODING STRATEGIES — How to generate text:

1. GREEDY DECODING:
   Pick the highest-probability token at each step.
   ❌ Often repetitive: "The cat sat on the mat. The cat sat on the mat…"

2. BEAM SEARCH (k=5):
   Maintain the k best sequences in parallel.
   ✅ Better than greedy | ❌ Tends to produce short, generic sentences

3. TOP-K SAMPLING:
   Sample from the K most probable tokens.
   K=50: "The cat ___" → among {eats, sleeps, runs, plays, …}
   ✅ More variety | ❌ Fixed K can include improbable tokens

4. NUCLEUS SAMPLING (Top-p):
   Sample from the smallest set covering probability ≥ p.
   p=0.9: take tokens representing 90% of total probability
   ✅ Adaptive to the distribution | ✅ The industry standard

5. TEMPERATURE:
   Controls the model's "creativity".
   • T < 1: more deterministic (factual text)
   • T = 1: original distribution
   • T > 1: more random, more creative (poetry, storytelling)

   modified_logits = logits / temperature
   → T=0.7 for assistants, T=1.2 for creative writing

🎨 PROMPT ENGINEERING — Guiding GPT without changing weights:

ZERO-SHOT:
  "Translate this sentence to Spanish: The cat is on the mat."
  → GPT translates without being trained on this specific task!

FEW-SHOT (In-Context Learning):
  "EN: The cat eats. FR: Le chat mange.
   EN: The dog runs. FR: Le chien court.
   EN: The bird sings. FR:"
  → GPT understands the task from examples and completes it!

CHAIN-OF-THOUGHT:
  "Solve this step by step:
   If Jean has 3 apples and Marie gives him 5 more, how many does he have?
   Step 1: Jean starts with 3 apples.
   Step 2: Marie gives 5 more.
   Step 3: Total = 3 + 5 = 8 apples."
  ✅ Significantly improves complex reasoning tasks

🐍 HUGGINGFACE CODE:
  from transformers import GPT2LMHeadModel, GPT2Tokenizer

  tokenizer = GPT2Tokenizer.from_pretrained('gpt2')
  model = GPT2LMHeadModel.from_pretrained('gpt2')

  prompt = "The future of artificial intelligence is"
  inputs = tokenizer.encode(prompt, return_tensors='pt')

  outputs = model.generate(
      inputs, max_length=100,
      do_sample=True, temperature=0.8, top_p=0.9,
      num_return_sequences=3
  )
  for i, out in enumerate(outputs):
      print(f"--- Generation {i+1} ---")
      print(tokenizer.decode(out, skip_special_tokens=True))""",
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
                    "content": "OpenCV is the world's most-used computer vision library (2500+ functions).\n\nCore image operations:\n• Read/write: cv2.imread(), cv2.imwrite(), cv2.VideoCapture()\n• Resize: cv2.resize(img, (width, height))\n• Rotate: cv2.rotate() or cv2.getRotationMatrix2D()\n• Crop: img[y1:y2, x1:x2]  (NumPy slicing)\n• Colour conversion: cv2.cvtColor(img, cv2.COLOR_BGR2RGB)\n  (⚠️ OpenCV reads images as BGR, not RGB!)\n\nSmoothing filters:\n• GaussianBlur: gentle blur, removes Gaussian noise\n  cv2.GaussianBlur(img, (5,5), 0)\n• medianBlur: excellent for salt-and-pepper noise\n  cv2.medianBlur(img, 5)\n• bilateralFilter: smooths while preserving edges\n  cv2.bilateralFilter(img, 9, 75, 75)\n\nMorphological operations:\nA structuring element (kernel) slides across the image.\n• Erosion: shrinks white regions, removes noise\n• Dilation: expands white regions, fills holes\n• Opening = Erosion then Dilation: removes noise\n• Closing = Dilation then Erosion: fills holes\n\nHistograms:\n• Distribution of pixel intensities\n• Equalisation: uniform distribution → better contrast\n  cv2.equalizeHist(grey_img)\n• CLAHE: adaptive equalisation by tiles (best for medical images)\n\nSample code:\n  import cv2\n  img = cv2.imread('photo.jpg')\n  img_rgb = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)\n  img_blur = cv2.GaussianBlur(img, (5,5), 0)\n  edges = cv2.Canny(img_blur, 100, 200)\n  cv2.imshow('Edges', edges); cv2.waitKey(0)",
                    "duration": "50 min"
                },
                {
                    "title": "Contour and Feature Detection",
                    "content": "Edge and feature detection are fundamental to classical computer vision.\n\nEdge detection:\n\n1. Sobel (first-order gradient):\n   Computes partial derivatives in each direction.\n   Gx = [[-1,0,1],[-2,0,2],[-1,0,1]]  (horizontal)\n   Gy = [[1,2,1],[0,0,0],[-1,-2,-1]]  (vertical)\n   Magnitude = sqrt(Gx² + Gy²)\n   → Detects edges but sensitive to noise.\n\n2. Canny (industry standard):\n   4-step pipeline:\n   a) GaussianBlur to reduce noise\n   b) Gradient computation (Sobel)\n   c) Non-maximum suppression: keep only local maxima\n   d) Hysteresis thresholding: two thresholds (low/high)\n      - Pixel > high threshold → definite edge\n      - Pixel < low threshold → discard\n      - Between thresholds → edge only if connected to a definite edge\n   cv2.Canny(img, low=100, high=200)\n\nCorner detection:\n3. Harris Corner Detector:\n   Detects regions where gradient changes in all directions.\n   Structure matrix M = Σ [Ix², IxIy; IxIy, Iy²]\n   Score R = det(M) − k × trace(M)²\n   R >> 0 → corner | R << 0 → edge | |R| ≈ 0 → flat\n\nInvariant interest points:\n4. SIFT (Scale-Invariant Feature Transform):\n   Detects keypoints invariant to: scale (zoom), rotation, illumination.\n   Descriptor: histogram of local gradients (128 dimensions).\n   ✅ Very robust | ❌ Slow; was patented (now free)\n\n5. ORB (Oriented FAST and Rotated BRIEF):\n   Fast, free alternative to SIFT.\n   FAST detector + oriented BRIEF descriptor.\n   ✅ Real-time capable | ✅ Free to use\n\nContour extraction:\n6. findContours:\n   Finds contours of connected regions.\n   contours, _ = cv2.findContours(mask, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)\n   Then: cv2.boundingRect(c), cv2.contourArea(c), cv2.arcLength(c, True)",
                    "duration": "55 min"
                },
                {
                    "title": "Image Classification with CNN",
                    "content": "Image classification assigns a category label to an entire image — the foundational computer vision task.\n\nPre-trained CNN approach (Transfer Learning):\n\nChoose a backbone:\n  Architecture  | Params | Top-5 Acc | Speed\n  MobileNetV2   | 3.4M   | 91%       | Very fast (mobile)\n  ResNet50      | 25.6M  | 93%       | Fast\n  EfficientNetB4| 19M    | 98%       | Medium\n  ViT-B/16      | 86M    | 99%       | Slow but SOTA\n\nData augmentation — essential to prevent overfitting:\n  Label-preserving transforms:\n  • Random rotation: [-15°, +15°]\n  • Horizontal flip (context-dependent!)\n  • Random zoom: [0.8, 1.2]\n  • Horizontal/vertical shift\n  • Brightness / contrast jitter\n  • CutMix / MixUp: modern techniques, very effective\n\n  Keras code:\n  datagen = ImageDataGenerator(rotation_range=15, horizontal_flip=True, zoom_range=0.2)\n\nProgressive fine-tuning:\n  Phase 1: freeze entire ResNet50, train classification head only\n  Phase 2: unfreeze last 50 layers, lr=1e-5\n  Phase 3: unfreeze everything, lr=1e-6\n\nEvaluation and interpretation:\n  → Confusion matrix: which classes are confused with which?\n  → Grad-CAM: visualise the regions the CNN focused on for each prediction!\n     Crucial for explainability (especially in medicine).\n\nDeployment:\n  TensorFlow Lite → mobile | ONNX → cross-framework | TensorRT → production GPU",
                    "duration": "65 min"
                },
                {
                    "title": "Object Detection YOLO SSD",
                    "content": "Object detection simultaneously localises AND classifies multiple objects in one image.\n\nTwo-stage vs one-stage:\n\nTwo-stage (more accurate, slower):\n• R-CNN: region proposals → CNN → classification\n• Faster R-CNN: integrated Region Proposal Network (RPN)\n  → ~5-15 FPS, excellent accuracy\n\nOne-stage (real-time):\n\n1. YOLO (You Only Look Once):\n   Image divided into S×S grid.\n   Each cell predicts B bounding boxes + class probabilities.\n   Single forward pass → very fast!\n   YOLOv1 (2016) → v5 → v8 (2023): constant improvements.\n   YOLOv8: ~80 FPS on GPU, 53% mAP on COCO.\n\n2. SSD (Single Shot MultiBox Detector):\n   Uses feature maps at multiple scales.\n   Anchor boxes of different sizes per cell.\n   → Detects small and large objects better than YOLOv1.\n\nKey metrics:\n\nIoU (Intersection over Union):\n   IoU = Area(Intersection) / Area(Union)\n   Measures overlap between predicted and ground-truth box.\n   IoU > 0.5 → correct detection (PASCAL VOC convention)\n\nPrecision-Recall:\n   For each class, compute the Precision vs Recall curve.\n   AP (Average Precision) = area under the PR curve.\n\nmAP (mean Average Precision):\n   mAP = average of AP across all classes.\n   mAP@0.5: IoU threshold = 0.5\n   mAP@0.5:0.95: averaged from 0.5 to 0.95 (COCO standard)\n\nNMS (Non-Maximum Suppression):\n   Removes redundant overlapping boxes.\n   → Keeps only the highest-scoring box per object.\n\nYOLOv8 code:\n  from ultralytics import YOLO\n  model = YOLO('yolov8n.pt')  # nano model\n  results = model('image.jpg')\n  results[0].show()",
                    "duration": "70 min"
                },
                {
                    "title": "Semantic Segmentation",
                    "content": "Image segmentation assigns a class label to EVERY PIXEL.\n\nThree types:\n\n1. SEMANTIC SEGMENTATION:\n   Every pixel gets a class (cat, car, road…)\n   All pixels of the same type get the same colour.\n   Problem: cannot distinguish two separate cars!\n\n2. INSTANCE SEGMENTATION:\n   Detects AND segments each object individually.\n   Car #1 ≠ Car #2 (different colours). More useful, harder.\n\n3. PANOPTIC SEGMENTATION:\n   Combines both: semantic for background, instances for objects.\n   Modern standard for autonomous driving.\n\nKey architectures:\n\nFCN (Fully Convolutional Network, 2015):\n   Replaces dense layers with convolutions.\n   Output same size as input.\n\nU-Net (2015, medical segmentation):\n   U-shaped architecture with skip connections:\n   → Encoder arm (left): downsampling, capture context\n   → Decoder arm (right): upsampling, precise localisation\n   → Skip connections: bridge encoder and decoder for fine details\n   ✅ Excellent with VERY FEW images (medical: a few hundred)\n\nMask R-CNN (2017):\n   Faster R-CNN + parallel mask branch.\n   For each detected object: predicts a pixel-level binary mask.\n   ✅ High-quality instance segmentation | ❌ Slow (~5 FPS)\n\nDeepLab v3+ (Google):\n   Atrous (dilated) convolutions for multi-scale context.\n   ASPP (Atrous Spatial Pyramid Pooling).\n   ✅ SOTA for semantic segmentation.\n\nApplications:\n   Autonomous driving: detect road, lanes, pedestrians, vehicles\n   Medical imaging: tumour, organ boundaries\n   Satellite imagery: land cover mapping",
                    "duration": "60 min"
                },
                {
                    "title": "Image Generation GANs",
                    "content": "GANs (Generative Adversarial Networks) learn to create new realistic data by pitting two networks against each other.\n\nThe adversarial game (Goodfellow, 2014):\n\nTwo networks in competition:\n• GENERATOR G: takes random noise z and generates a fake image\n• DISCRIMINATOR D: distinguishes real images from fake ones\n\nObjectives:\n  G wants to FOOL D (maximise probability that D calls fakes real)\n  D wants to DETECT fakes (minimise its own classification error)\n\nMin-max loss:\n  min_G max_D E[log D(x)] + E[log(1 − D(G(z)))]\n\nTraining: alternate updating D (on real+fake), then G.\nNash equilibrium: G generates perfect images, D always predicts 0.5.\n\nKey architectures:\n\nDCGAN (2015):\n  → Transposed convolutions in generator, BatchNorm.\n  ✅ Reasonable image quality for its time.\n\nStyleGAN (NVIDIA, 2019):\n  → Generates photorealistic human faces (thispersondoesnotexist.com)\n  → Style control: hairstyle, age, expression at different scales\n  → Mapping network + synthesis network architecture\n  ✅ Photographic quality, fine-grained style control\n\nCycleGAN (2017):\n  → Unsupervised style transfer between domains\n  → No paired images needed!\n  → Horse ↔ Zebra, Summer ↔ Winter, Photo ↔ Painting\n  → 2 GANs + 2 cycle-consistency losses\n\nConditional GAN (cGAN):\n  → Condition on an input: text → image (early DALL-E)\n  → pix2pix: image → image (sketch → realistic photo)\n\nChallenges:\n• Mode collapse: G generates the same image over and over\n• Training instability: both networks must stay balanced\n• Hard to evaluate: use FID (Fréchet Inception Distance)\n\nApplications:\n• Synthetic face generation (deepfakes, avatars)\n• Medical data augmentation (scarce real data)\n• Super-resolution: low quality → high quality image\n• Photo editing: inpainting, colourising B&W photos\n• Generative art and design",
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
                    "content": "The Markov Decision Process (MDP) is the formal mathematical framework for modelling Reinforcement Learning problems.\n\nThe 5 components of an MDP:\n• S: state space (everything the agent can observe)\n• A: action space (what the agent can do)\n• P(s'|s,a): transition probability (environment dynamics)\n• R(s,a,s'): reward function (feedback signal)\n• γ (gamma): discount factor [0,1] (importance of future rewards)\n\nThe Markov property:\n  The future depends ONLY on the current state, not on history:\n  P(s_{t+1} | s_t, a_t) = P(s_{t+1} | s_0, a_0, ..., s_t, a_t)\n\nThe agent's objective:\n  Maximise the DISCOUNTED cumulative reward:\n  G_t = R_t + γ×R_{t+1} + γ²×R_{t+2} + ...\n  → γ near 0: myopic agent (only immediate rewards)\n  → γ near 1: far-sighted agent (long-term planning)\n\nValue functions:\n\nV^π(s) = state value under policy π:\n  V^π(s) = E[G_t | S_t = s, policy π]\n  → Expected cumulative reward starting from state s\n\nQ^π(s,a) = action-state value (Q-function):\n  Q^π(s,a) = E[G_t | S_t = s, A_t = a, policy π]\n  → Expected cumulative reward taking action a in state s\n\nThe Bellman equation (theoretical foundation):\n  Decomposes value recursively:\n  V^π(s) = Σ_a π(a|s) × Σ_{s'} P(s'|s,a) × [R(s,a,s') + γ × V^π(s')]\n  → Value now = immediate reward + discounted future value\n\nOptimal policy:\n  V*(s) = max_a Q*(s,a)\n  Q*(s,a) = R(s,a) + γ × Σ_{s'} P(s'|s,a) × V*(s')\n  π*(s) = argmax_a Q*(s,a)\n  → Knowing Q* gives us the optimal policy directly!",
                    "duration": "55 min"
                },
                {
                    "title": "Q-Learning and SARSA",
                    "content": "Q-Learning and SARSA are the two foundational tabular RL algorithms.\n\nQ-LEARNING (Watkins, 1989):\n\nQ-table update rule:\n  Q(s,a) ← Q(s,a) + α × [R + γ × max_{a'} Q(s',a') − Q(s,a)]\n  • α = learning rate\n  • R = reward received\n  • γ × max Q(s',a') = estimate of optimal future value\n  • The bracket = TD error (Temporal Difference error)\n\nOFF-POLICY: always uses max Q for the update,\nregardless of the action actually taken.\n→ Learns the OPTIMAL policy even while exploring!\n\nSARSA (State-Action-Reward-State-Action):\n\nUpdate rule:\n  Q(s,a) ← Q(s,a) + α × [R + γ × Q(s',a') − Q(s,a)]\n  (a' is the action ACTUALLY TAKEN in s')\n\nON-POLICY: the future value used matches the CURRENT policy\n(not necessarily optimal).\n→ More conservative, follows the exact exploration policy.\n\nExploration vs Exploitation — the fundamental dilemma:\n→ EXPLOITATION: pick the known best action → no new learning\n→ EXPLORATION: try unknown actions → risky but potentially better\n\nStrategies:\n• Epsilon-greedy: with probability ε, random action; else max Q.\n  Decay ε over time (more exploration early on).\n• UCB (Upper Confidence Bound): pick action with best upper bound.\n• Thompson Sampling: Bayesian sampling.\n\nComparison:\n  Criterion      | Q-Learning        | SARSA\n  Type           | Off-policy        | On-policy\n  Update uses    | max Q(s',a')      | actual Q(s',a')\n  Behaviour      | More aggressive   | More conservative\n  Best for       | Deterministic env | Environments with risk\n\nLimitation: only works if state space is SMALL and DISCRETE.\n  4×4 grid world → 16-entry table ✅\n  Atari pixels → 10^100 states ✗ → need DQN!",
                    "duration": "60 min"
                },
                {
                    "title": "Deep Q-Networks DQN",
                    "content": "DQN (Deep Q-Network) combines Q-Learning with deep neural networks to solve large state-space problems.\n\nThe tabular RL problem:\n  For Atari (84×84 images, 4 channels): 4^(84×84) = 10^21000 states!\n  Impossible to maintain a Q-table.\n\nDQN solution (DeepMind, 2013/2015):\n  Approximate Q(s,a) with a NEURAL NETWORK:\n  Q(s, a; θ) ≈ Q*(s, a)\n  → Input: state s (e.g. 84×84 image)\n  → Output: Q-value for each possible action\n\nThree key innovations:\n\n1. EXPERIENCE REPLAY:\n   Problem: consecutive transitions are highly correlated → instability.\n   Solution: store transitions (s, a, r, s') in a REPLAY BUFFER.\n   → Sample random MINI-BATCHES for training\n   → Breaks temporal correlations\n   → Reuses each experience multiple times (sample efficiency)\n\n2. TARGET NETWORK:\n   Problem: the Q* target changes every step → unstable feedback loop.\n   Solution: use a separate TARGET NETWORK θ⁻ to compute the target.\n   → Copy weights to θ⁻ every N steps (e.g. N=1,000)\n   → Target is stable for N steps\n\n3. DOUBLE DQN (2016):\n   Problem: vanilla DQN systematically overestimates Q-values.\n   Solution: use the ONLINE NETWORK to choose the action,\n   and the TARGET NETWORK to evaluate it:\n     y = R + γ × Q(s', argmax_{a'} Q(s',a'; θ); θ⁻)\n\n4. DUELING DQN (2016):\n   Decompose Q(s,a) into two streams:\n   Q(s,a) = V(s) + A(s,a)\n   → V(s): state value (action-independent)\n   → A(s,a): advantage of the action (relative to others)\n   → Learns more efficiently: V(s) is easier to estimate\n\nHistoric result:\n   DQN reached HUMAN LEVEL on 49 Atari games (2015),\n   learning purely from raw pixel inputs!\n\nPyTorch code:\n  class DQN(nn.Module):\n      def __init__(self, n_states, n_actions):\n          super().__init__()\n          self.net = nn.Sequential(nn.Linear(n_states,128), nn.ReLU(), nn.Linear(128,n_actions))\n      def forward(self, x): return self.net(x)",
                    "duration": "65 min"
                },
                {
                    "title": "Policy Gradient Methods",
                    "content": "Policy Gradient methods learn the policy π(a|s;θ) DIRECTLY, without an intermediate Q-function.\n\nWhy Policy Gradient?\n  Q-Learning/DQN → learn Q(s,a), derive π* as argmax.\n  Limitations:\n  → Requires DISCRETE action space (how to argmax over continuous actions?)\n  → Cannot represent stochastic policies naturally\n  → Hard to use for parameterised, differentiable policies\n\n  Policy Gradient: learn θ so that π(a|s;θ) maximises return G.\n  ✅ Works with continuous action spaces (robotics!)\n  ✅ Converges to a local optimum (theoretical guarantees)\n  ✅ Naturally learns stochastic policies\n\nThe Policy Gradient Theorem:\n  ∇_θ J(θ) = E[∇_θ log π(a|s;θ) × Q^π(s,a)]\n\n  → ∇_θ log π: how to change θ to make action a more/less likely from s\n  → Q^π(s,a): how good was this action?\n  → Increase probability of actions that yielded good returns!\n\nREINFORCE algorithm:\n  1. Play a full episode with policy π_θ\n  2. Compute returns G_t for each step\n  3. Update: θ ← θ + α × Σ_t [G_t × ∇_θ log π(a_t|s_t;θ)]\n\nProblem: HIGH VARIANCE\n  G_t can vary enormously between episodes.\n  → Unstable training and slow convergence.\n\nSolution: BASELINE\n  Subtract a baseline b(s) to reduce variance WITHOUT bias:\n  ∇_θ J(θ) = E[∇_θ log π(a|s;θ) × (Q^π(s,a) − b(s))]\n\n  Common baselines:\n  → Average return\n  → Value function V(s) → leads to the ACTOR-CRITIC algorithm!\n\nAdvantage A(s,a) = Q(s,a) − V(s):\n  → > 0: this action was BETTER than average\n  → < 0: this action was WORSE than average\n  → ≈ 0: this action was typical",
                    "duration": "60 min"
                },
                {
                    "title": "Actor-Critic A2C PPO",
                    "content": "Actor-Critic and PPO represent the state of the art in modern RL, used in both robots and LLMs.\n\nActor-Critic:\n\nTwo networks:\n→ ACTOR π(a|s;θ): the policy (decides what to do)\n→ CRITIC V(s;φ): the value function (evaluates the situation)\n\nUpdates:\n  Advantage: A(s,a) = R + γ×V(s') − V(s)  [TD error]\n  Actor:  θ ← θ + α × A(s,a) × ∇_θ log π(a|s;θ)\n  Critic: φ ← φ − α × [R + γ×V(s') − V(s)]² × ∇_φ\n\nA2C (Advantage Actor-Critic):\n→ Synchronous version of A3C (Asynchronous A3C)\n→ Multiple parallel environments → less correlated gradients\n→ More stable than REINFORCE thanks to the Critic baseline\n\nTRPO (Trust Region Policy Optimization, 2015):\n→ Key problem: too-large policy updates → catastrophic performance collapse\n→ Constraint: KL divergence between old and new policy ≤ δ\n→ Guarantees monotonic improvement (in theory)\n→ Hard to implement (constrained optimisation)\n\nPPO (Proximal Policy Optimization, OpenAI 2017):\n  Simpler solution to TRPO → becomes the industry standard!\n\n  Clip the probability ratio to limit large updates:\n  r(θ) = π(a|s;θ) / π(a|s;θ_old)\n  L_CLIP(θ) = E[min(r×A, clip(r, 1−ε, 1+ε)×A)]\n  (ε typically 0.1 or 0.2)\n\n  → Good action (A > 0): increase probability, but NOT too much (cap at 1+ε)\n  → Bad action (A < 0): decrease probability, but NOT too much (floor at 1−ε)\n\nPPO applications:\n  ✅ OpenAI Five (Dota 2), AlphaGo\n  ✅ Robotics (locomotion)\n  ✅ RLHF for aligning LLMs (ChatGPT, Claude!)\n\nSAC (Soft Actor-Critic, 2018):\n→ Maximises reward + policy ENTROPY → encourages exploration\n→ Standard for continuous robotics control",
                    "duration": "70 min"
                },
                {
                    "title": "Real-world Applications",
                    "content": "RL has moved from theory to real-world applications with spectacular successes in recent years.\n\nLandmark applications:\n\n1. Games and simulation:\n• AlphaGo (DeepMind, 2016):\n  Defeated world Go champion Lee Sedol 4-1.\n  → MCTS + CNN to evaluate board positions + self-play.\n\n• AlphaStar (StarCraft II, 2019):\n  Grandmaster level without any information restrictions.\n  → Handles fog of war, micromanagement, long-term strategy.\n\n• OpenAI Five (Dota 2, 2019):\n  Defeated world champion team OG.\n  → 5 coordinated agents trained for 10 months.\n\n2. Robotics:\n  Learning to walk, run, jump (Boston Dynamics, OpenAI)\n  → SAC or PPO with thousands of hours of simulation.\n  Object manipulation: grasp unfamiliar objects.\n  → Key challenge: generalisation to unseen objects.\n\n3. Sim-to-Real:\n  Train in simulation (free, parallelisable) then deploy in the real world.\n  Challenge: the domain gap (simulation ≠ reality exactly).\n  Solutions:\n  → Domain randomisation: vary physical parameters in simulation\n  → Domain adaptation: fine-tune the model on real data\n\n4. Algorithmic trading:\n  Agent learns to buy/sell to maximise profit.\n  Challenge: non-stationarity of markets, transaction costs.\n\n5. Energy management:\n  DeepMind applied RL to Google data-centre cooling: −40% energy!\n\nMajor challenges in RL:\n• Sample efficiency: RL needs ENORMOUS numbers of interactions\n  (DQN Atari: ~200M frames = 38 human days of gameplay)\n• Safety: avoid dangerous behaviours during exploration\n• Generalisation: performance on unseen scenarios\n• Credit assignment: link rewards to the right past actions\n• Reward shaping: designing the right reward function\n\nFuture directions:\n→ RL + LLMs: foundation models for decision-making\n→ World models: learn a model of the world to plan ahead",
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
                    "content": "Scikit-learn pipelines chain all ML steps cleanly and prevent data leakage.\n\nWhy pipelines?\n\nWithout pipeline — data leakage risk:\n  scaler.fit(X_train)               # OK\n  X_test_scaled = scaler.transform(X_test)  # potential leakage!\n  → If scaler is fit on all data → test statistics leak into training\n\nWith pipeline: fit() on the scaler runs ONLY on training data.\n\nBuilding a pipeline:\n  from sklearn.pipeline import Pipeline\n  from sklearn.preprocessing import StandardScaler\n  from sklearn.svm import SVC\n\n  pipe = Pipeline([\n      ('scaler', StandardScaler()),\n      ('feature_selection', SelectKBest(k=20)),\n      ('classifier', SVC(kernel='rbf'))\n  ])\n  pipe.fit(X_train, y_train)   # fits every step\n  y_pred = pipe.predict(X_test)\n\nHyperparameter optimisation:\n\n1. Grid Search (exhaustive):\n   Tests ALL combinations. Guarantees best result. Slow with many params.\n   param_grid = {'classifier__C': [0.1, 1, 10], 'classifier__gamma': ['scale', 0.1, 0.01]}\n   search = GridSearchCV(pipe, param_grid, cv=5, scoring='f1', n_jobs=-1)\n\n2. Random Search (fast):\n   Samples N random combinations. Often finds 90% of performance in 10% of time.\n   search = RandomizedSearchCV(pipe, param_grid, n_iter=20, cv=5)\n\n3. Bayesian Optimisation (smart):\n   Uses previous results to guide the search.\n   Libraries: Optuna, Hyperopt, scikit-optimize\n   → Converges faster than Random Search.\n\n4. Halving Grid Search (efficient):\n   Starts with many candidates and few data.\n   Progressively eliminates the least promising.\n   from sklearn.model_selection import HalvingGridSearchCV",
                    "duration": "45 min"
                },
                {
                    "title": "Model Versioning with MLflow",
                    "content": "MLflow is the most popular open-source platform for managing the full ML model lifecycle.\n\nThe 4 components of MLflow:\n\n1. MLflow Tracking — log experiments:\n   import mlflow\n   with mlflow.start_run(run_name='exp_001'):\n       mlflow.log_param('learning_rate', 0.001)\n       mlflow.log_param('batch_size', 32)\n       mlflow.log_metric('train_loss', 0.25)\n       mlflow.log_metric('val_accuracy', 0.91)\n       mlflow.log_artifact('confusion_matrix.png')\n       mlflow.sklearn.log_model(model, 'model')\n   Web dashboard: compare all runs side by side!\n\n2. MLflow Projects — reproducibility:\n   Standard structure with MLproject (YAML).\n   → Define conda/docker environment, entry points.\n   → mlflow run . -P alpha=0.5\n\n3. MLflow Models — packaging:\n   Universal format ('flavour') that abstracts the framework:\n   → sklearn, tensorflow, pytorch, onnx, spark…\n   → mlflow.pyfunc: generic Python function interface\n   Deployment:\n   → mlflow models serve -m runs:/<run_id>/model -p 5000\n   → mlflow.sagemaker.deploy() for AWS SageMaker\n\n4. MLflow Model Registry — governance:\n   Model lifecycle stages:\n   → Staging: tested but not yet in production\n   → Production: the live model serving traffic\n   → Archived: previous model kept in history\n\n   Actions:\n   → Register a new model: mlflow.register_model()\n   → Transition between stages with approvals\n   → Team annotations and comments\n   → Automatic old vs new model comparison\n\nCI/CD integration:\n→ In GitHub Actions: run experiments, compare, promote if improved.\n→ MLflow Autologging: automatic param/metric logging for sklearn.",
                    "duration": "50 min"
                },
                {
                    "title": "Containerization with Docker",
                    "content": "Docker encapsulates an ML model and all its dependencies into a portable, reproducible container.\n\nWhy Docker for ML?\n  'It works on my machine!' — the classic ML problem.\n  → Python 3.8 on dev, 3.10 on prod; different numpy/CUDA versions…\n  → Docker freezes the complete environment: 'build once, run anywhere'\n\nKey concepts:\n• IMAGE: immutable snapshot (layers)\n• CONTAINER: running instance of an image\n• REGISTRY: image repository (Docker Hub, ECR, GCR)\n\nSample Dockerfile (ML API):\n  FROM python:3.10-slim\n  WORKDIR /app\n  COPY requirements.txt .\n  RUN pip install --no-cache-dir -r requirements.txt\n  COPY ./app ./app\n  COPY model.pkl .\n  EXPOSE 8000\n  CMD [\"uvicorn\", \"app.main:app\", \"--host\", \"0.0.0.0\", \"--port\", \"8000\"]\n\nMulti-stage build (lightweight image):\n  FROM python:3.10 AS builder\n  RUN pip install --user torch scikit-learn fastapi\n\n  FROM python:3.10-slim\n  COPY --from=builder /root/.local /root/.local\n  COPY app/ ./app/\n  → Reduces image size from 5 GB to 500 MB!\n\nDocker Compose (multiple services):\n  version: '3.8'\n  services:\n    api:\n      build: .\n      ports: [\"8000:8000\"]\n      depends_on: [redis]\n    redis:\n      image: redis:alpine\n\nBest practices:\n→ .dockerignore: exclude unnecessary files (data/, __pycache__/)\n→ Non-root user for security\n→ Healthcheck for robustness\n→ Environment variables for config (never hard-code in image!)",
                    "duration": "55 min"
                },
                {
                    "title": "Deployment with FastAPI",
                    "content": "FastAPI: modern Python framework for production ML APIs.\n\nWhy FastAPI for ML?\n- FAST (Starlette+Pydantic), ASYNC, auto-validation, auto-Swagger docs\n\nComplete ML API:\n  from fastapi import FastAPI, HTTPException\n  from pydantic import BaseModel\n  import pickle, numpy as np\n\n  app = FastAPI()\n\n  @app.on_event('startup')\n  async def load_model():\n      app.state.model = pickle.load(open('model.pkl', 'rb'))\n\n  class PredictionInput(BaseModel):\n      area: float\n      bedrooms: int\n      neighbourhood: str\n\n  @app.post('/predict')\n  async def predict(inp: PredictionInput):\n      try:\n          X = [[inp.area, inp.bedrooms, 1 if inp.neighbourhood=='city-centre' else 0]]\n          pred = app.state.model.predict(X)[0]\n          return {'predicted_price': float(pred), 'version': 'v1.2.3'}\n      except Exception as e:\n          raise HTTPException(status_code=500, detail=str(e))\n\n  @app.get('/health')\n  async def health():\n      return {'status': 'ok'}\n\nDeployment:\n  uvicorn main:app --reload   # development\n  gunicorn main:app -w 4 -k uvicorn.workers.UvicornWorker  # production",
                    "duration": "60 min"
                },
                {
                    "title": "Monitoring and Drift Detection",
                    "content": "ML monitoring in production detects when a model starts to degrade so retraining can be triggered.\n\nWhy monitoring is critical?\n  A model trained in January may degrade by July:\n  → Data changes (user behaviour, seasons, world events)\n  → The underlying concept evolves\n  → Without monitoring you don't know when the model is useless!\n\nTypes of drift:\n\n1. DATA DRIFT (input drift):\n   Distribution P(X) changes.\n   Example: credit model trained on 25–45 year-olds starts receiving\n   applications from 18–24 year-olds.\n   Detection: KS test (Kolmogorov-Smirnov), PSI (Population Stability Index)\n\n2. CONCEPT DRIFT:\n   The relationship P(Y|X) changes.\n   Example: the words that signalled spam have changed.\n   Detection: metric degradation on labelled holdout data\n\n3. PREDICTION DRIFT:\n   Distribution of model outputs changes.\n   Example: model predicts 'fraud' more and more often.\n   Detection: monitor output distribution\n\n4. DATA QUALITY:\n   Null values, out-of-range values, incorrect types…\n   → Often caused by upstream pipeline changes\n\nTools:\n• Evidently AI (open-source):\n  from evidently.report import Report\n  from evidently.metric_preset import DataDriftPreset\n  report = Report(metrics=[DataDriftPreset()])\n  report.run(reference_data=X_train, current_data=X_prod)\n  report.save_html('drift_report.html')\n• WhyLabs, Arize: SaaS platforms\n• MLflow + Grafana + Prometheus: open-source stack\n\nRetraining strategies:\n→ Scheduled: retrain weekly/monthly\n→ Triggered: retrain if drift detected or metric < threshold\n→ Online learning: continuous update (streaming)",
                    "duration": "55 min"
                },
                {
                    "title": "CI/CD for ML",
                    "content": "MLOps applies DevOps practices to ML to automate end-to-end model deployment.\n\nMLOps maturity levels:\n\nLevel 0 — Manual ML:\n  → Data scientists work in Jupyter notebooks\n  → Manual deployment (export pickle, copy to server)\n  → No monitoring, no tests\n  → Typical at the start of an ML project\n\nLevel 1 — Automated ML pipeline:\n  → Automated data + training pipeline\n  → Automatic triggering on new data\n  → Basic monitoring\n  → Shared Feature Store\n\nLevel 2 — CI/CD for ML:\n  → Automated tests (data, model, performance)\n  → CI/CD pipeline triggered on every commit\n  → Automatic deployment if tests pass\n  → Advanced monitoring + alerts + auto-retraining\n\nML CI/CD Pipeline (GitHub Actions):\n  name: ML Pipeline\n  on: push\n  jobs:\n    test-and-deploy:\n      steps:\n      - name: Data tests\n        run: python test_data_quality.py\n      - name: Training\n        run: python train.py\n      - name: Model validation\n        run: python validate.py --min-accuracy=0.90\n      - name: Docker build\n        run: docker build -t ml-api:${{ github.sha }} .\n      - name: Push and Deploy\n        run: kubectl apply -f k8s/deployment.yaml\n\nML testing types:\n→ Data tests: schema, nulls, distributions (Great Expectations)\n→ Code tests: preprocessing functions (pytest)\n→ Model tests: performance > threshold, no regression\n→ API tests: latency < 200ms, error rate < 0.1%\n\nMLOps platforms:\n• Kubeflow (Google): ML on Kubernetes, very flexible\n• SageMaker (AWS): fully managed end-to-end service\n• Azure ML (Microsoft): Azure integration, AutoML\n• Vertex AI (Google Cloud): unified pipeline\n• Weights & Biases: experimentation + monitoring\n\nFeature Store:\n→ Share and reuse features across models\n→ Avoid double computation, guarantee consistency\n→ Feast (open-source), Tecton, Hopsworks",
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
                    "content": """تعلم الآلة (Machine Learning) هو فرع من فروع الذكاء الاصطناعي يُمكّن الحواسيب من التعلم تلقائياً من البيانات دون برمجة صريحة لكل مهمة.

🔑 المفهوم الأساسي:
في البرمجة التقليدية: يكتب المبرمج قواعد صريحة (إذا كانت درجة الحرارة > 30 فاعرض "حار").
في تعلم الآلة: نُقدّم آلاف الأمثلة للنموذج، فيكتشف القواعد بنفسه!

التعريف الرسمي (توم ميتشل 1997):
"يُقال إن برنامج حاسوبياً يتعلم من الخبرة E فيما يتعلق بالمهمة T ومقياس الأداء P، إذا تحسّن أداؤه في المهمة T، وفقاً للمقياس P، مع اكتساب المزيد من الخبرة E."

📊 الأنواع الثلاثة الرئيسية:

1. التعلم الخاضع للإشراف (Supervised Learning):
   - البيانات: مُعلَّمة (مدخلات + إجابات صحيحة)
   - المثال: 10,000 صورة كلب وقطة مع تصنيفاتها
   - الهدف: تعلّم الدالة f(X) = Y
   - التطبيقات: تصفية البريد المزعج، التنبؤ بالأسعار، تشخيص الأمراض

2. التعلم غير الخاضع للإشراف (Unsupervised Learning):
   - البيانات: بدون تصنيفات
   - المثال: تجميع العملاء حسب سلوك الشراء تلقائياً
   - الهدف: اكتشاف الأنماط والهياكل المخفية
   - التطبيقات: تجزئة السوق، كشف الشذوذات، ضغط البيانات

3. التعلم المعزز (Reinforcement Learning):
   - وكيل يتعلم بالتجربة والخطأ في بيئة معينة
   - يحصل على مكافآت (+) أو عقوبات (-) بعد كل إجراء
   - المثال: AlphaGo يتعلم الشطرنج بلعب ملايين الأدوار ضد نفسه
   - التطبيقات: الروبوتات، الألعاب، التداول الخوارزمي

🌍 تطبيقات واقعية:
• التعرف على الوجوه (Face ID في iPhone)
• توصيات Netflix وSpotify وYouTube
• كشف الاحتيال البنكي في الوقت الفعلي
• السيارات ذاتية القيادة (Tesla Autopilot)
• الترجمة الآلية (Google Translate)
• المساعدون الصوتيون (Siri, Alexa)
• التشخيص الطبي (كشف السرطان من صور الأشعة)

💡 تشبيه تعليمي:
تعلم الآلة يشبه تعليم طفل التعرف على الكلاب. يرى الطفل مئات الكلاب، يتعلم تدريجياً خصائصها (أربعة أرجل، أنف، فراء)، وفي النهاية يتعرف على كلب لم يره من قبل. هذا بالضبط ما يفعله نموذج تعلم الآلة!""",
                    "duration": "45 دقيقة"
                },
                {
                    "title": "أنواع التعلم",
                    "content": """في هذا الدرس نتعمق في كل نوع من أنواع التعلم مع أمثلة عملية والخوارزميات المرتبطة بها.

🟢 التعلم الخاضع للإشراف — "التعلم مع مُعلّم"

آلية العمل:
  بيانات الإدخال (X) + التصنيفات الصحيحة (Y) → النموذج يتعلم f(X) = Y

فئتان رئيسيتان:

أ) التصنيف (Classification): التنبؤ بفئة منفصلة
   - مثال: بريد إلكتروني → [مزعج، عادي]
   - مثال: صورة → [قطة، كلب، طائر]
   - الخوارزميات: KNN، SVM، شجرة القرار، الغابات العشوائية، الشبكات العصبية

ب) الانحدار (Regression): التنبؤ بقيمة مستمرة
   - مثال: المساحة + الحي → سعر الشقة
   - مثال: درجة حرارة الأمس → درجة حرارة الغد
   - الخوارزميات: الانحدار الخطي، Ridge، Lasso، Gradient Boosting

🟡 التعلم غير الخاضع للإشراف — "التعلم بدون مُعلّم"

لا توجد تصنيفات! النموذج يكتشف الأنماط المخفية في البيانات.

أ) التجميع (Clustering):
   - K-Means: يقسم البيانات إلى K مجموعات متجانسة
   - DBSCAN: يجد مجموعات بأشكال عشوائية
   - التجميع الهرمي: يبني شجرة تشابه

ب) تقليل الأبعاد (Dimensionality Reduction):
   - PCA: يضغط البيانات مع الحفاظ على المعلومات الأساسية
   - t-SNE: يُصوِّر البيانات المعقدة في 2D/3D
   - المشفرات التلقائية (Autoencoders): ضغط عصبوني غير خطي

ج) قواعد الارتباط (Association Rules):
   - إيجاد العلاقات: "من يشتري X يشتري أيضاً Y"
   - خوارزمية Apriori لتحليل سلال التسوق

🔴 التعلم المعزز — "التعلم بالتجربة"

المكونات الأساسية:
  • الوكيل (Agent): النموذج الذي يتخذ القرارات
  • البيئة (Environment): العالم الذي يعمل فيه الوكيل
  • الحالة (State s): وصف الوضع الحالي
  • الإجراء (Action a): ما يمكن للوكيل فعله
  • المكافأة (Reward r): إشارة ردود الفعل (+/-) بعد كل إجراء
  • السياسة (Policy π): الاستراتيجية التي يتبعها الوكيل

حلقة التعلم:
  الوكيل يلاحظ الحالة → يختار إجراءً → يحصل على مكافأة → يحدّث استراتيجيته

الخوارزميات: Q-Learning، DQN، PPO، A3C

📋 جدول مقارن:
النوع              | البيانات        | الهدف                 | مثال
الخاضع للإشراف    | مُصنَّفة        | التنبؤ بالمخرجات     | هل هذا بريد مزعج؟
غير الخاضع        | غير مُصنَّفة    | إيجاد الأنماط        | تجزئة العملاء
التعلم المعزز     | تفاعلات         | تعظيم المكافأة       | تعلم لعب الشطرنج""",
                    "duration": "50 دقيقة"
                },
                {
                    "title": "الانحدار الخطي",
                    "content": """الانحدار الخطي هو أحد أكثر خوارزميات تعلم الآلة أساسيةً وشيوعاً. يُنمذج العلاقة بين متغير الإخراج (Y) ومتغير أو أكثر من متغيرات الإدخال (X).

📐 الصيغة الرياضية:

الانحدار الخطي البسيط (متغير واحد):
   y = mx + b
   • y = القيمة المتوقعة (مثال: سعر منزل)
   • x = متغير الإدخال (مثال: المساحة بالمتر المربع)
   • m = الميل (المعامل): كم يرتفع y عند ارتفاع x بمقدار 1
   • b = نقطة التقاطع (الانحياز): قيمة y عندما x = 0

الانحدار الخطي المتعدد (عدة متغيرات):
   y = w₁x₁ + w₂x₂ + ... + wₙxₙ + b
   مثال: السعر = 2500 × المساحة + 15000 × عدد_الغرف - 5000 × العمر + 50000

🎯 كيف يتعلم النموذج — طريقة المربعات الصغرى:

الهدف: إيجاد الخط الذي يمر الأقرب إلى جميع النقاط.

   الخطأ = Σ (القيمة_الحقيقية - القيمة_المتوقعة)²

نُقلّل هذا المجموع (MSE) لإيجاد أفضل m وb.

لماذا نربّع الخطأ؟
  1. لجعل جميع الأخطاء موجبة
  2. لمعاقبة الأخطاء الكبيرة بشكل أكبر

📏 مقاييس التقييم:

• R² (معامل التحديد): بين 0 و1
  - R² = 1 → نموذج مثالي يشرح 100% من التباين
  - R² = 0.85 → النموذج يشرح 85% من تغيرات البيانات
  - R² < 0 → النموذج أسوأ من المتوسط!

• MAE (متوسط الخطأ المطلق): الخطأ المتوسط بالقيمة المطلقة
  - سهل التفسير: "في المتوسط، أخطأت بـ X درهم"

• RMSE (جذر متوسط مربع الخطأ): يعاقب الأخطاء الكبيرة أكثر
  - نفس وحدة y، لكن أكثر حساسية للقيم الشاذة

💡 مثال عملي — التنبؤ بسعر منزل:
   البيانات: 1000 منزل بمساحتها وعدد غرفها وحيّها وسعرها

   بعد التدريب، يجد النموذج:
   السعر = 2800 × المساحة + 12000 × عدد_الغرف + 30000 × (حي_راقي) + 40000

   لمنزل مساحته 80م²، 3 غرف، حي عادي:
   السعر = 2800×80 + 12000×3 + 0 + 40000 = 224000 + 36000 + 40000 = 300,000 درهم

⚠️ الافتراضات والقيود:
   • يفترض وجود علاقة خطية (إذا كانت العلاقة الحقيقية منحنية → مشكلة)
   • حساس للقيم الشاذة (Outliers)
   • لا يلتقط التفاعلات المعقدة بين المتغيرات
   • للعلاقات غير الخطية: استخدم Polynomial Regression أو Random Forest

🐍 كود Python (scikit-learn):
   from sklearn.linear_model import LinearRegression
   from sklearn.metrics import r2_score, mean_absolute_error

   model = LinearRegression()
   model.fit(X_train, y_train)        # التدريب
   y_pred = model.predict(X_test)     # التنبؤ
   print(f"R² = {r2_score(y_test, y_pred):.3f}")""",
                    "duration": "55 دقيقة"
                },
                {
                    "title": "التصنيف باستخدام KNN",
                    "content": """خوارزمية أقرب الجيران (K-Nearest Neighbors) هي خوارزمية بديهية تُصنّف عنصراً جديداً بالنظر إلى أقرب K عناصر إليه في بيانات التدريب.

🧠 الحدس:
"أخبرني من هم جيرانك، أخبرك من أنت"
→ يُصنَّف النقطة بالتصويت الأغلبي بين أقرب K جيران لها.

📍 خطوات العمل:

1. لنقطة جديدة نريد تصنيفها:
2. احسب المسافة بينها وبين جميع نقاط التدريب
3. اختر أقرب K نقطة (الجيران)
4. قم بتصويت: الفئة الأغلبية بين K جيران هي التنبؤ
5. (للانحدار: احسب متوسط قيم K جيران)

📏 المسافات — كيف نقيس "القرب"؟

• المسافة الإقليدية (الأكثر شيوعاً):
  d = √[(x₁-x₂)² + (y₁-y₂)²]
  → المسافة "الهوائية" في الهندسة الكلاسيكية

• مسافة مانهاتن:
  d = |x₁-x₂| + |y₁-y₂|
  → كالتنقل في شبكة شوارع متقاطعة

• مسافة مينكوفسكي: تعميم للنوعين السابقين

🔢 اختيار K — المعامل الأهم:

• K صغير (مثل K=1):
  → نموذج معقد جداً، يتكيف مع ضوضاء التدريب
  → خطر الإفراط في التخصيص (Overfitting)

• K كبير (مثل K=100):
  → نموذج بسيط جداً، يتجاهل التفاصيل المهمة
  → خطر الإفراط في التبسيط (Underfitting)

• K الأمثل: يُحدَّد بالتحقق المتقاطع (Cross-Validation)
  → اختبر K = 1, 3, 5, 7, 11, ... واختر الأفضل

💡 قاعدة عملية: اختر K فردي لتجنب التعادل في التصنيف الثنائي.

✅ المزايا:
• بسيط جداً في الفهم والتطبيق
• لا تدريب! (خوارزمية "كسولة")
• مناسب طبيعياً للمسائل متعددة الفئات
• يتعلم حدود قرار معقدة

❌ القيود:
• بطيء في التنبؤ: يحسب جميع المسافات في كل مرة O(n×d)
• حساس للمقياس: التطبيع الإجباري ضروري
• حساس للأبعاد غير ذات الصلة
• يحتاج تخزين كل قاعدة البيانات في الذاكرة

🔄 المعالجة المسبقة الإجبارية — التطبيع:
  بدون تطبيع: إذا كانت المساحة = 80 والسعر = 200,000، تهيمن المسافة بالسعر!
  مع StandardScaler: جميع الميزات لها نفس الأهمية.

🐍 كود Python:
  from sklearn.neighbors import KNeighborsClassifier
  from sklearn.preprocessing import StandardScaler

  scaler = StandardScaler()
  X_train_scaled = scaler.fit_transform(X_train)
  X_test_scaled = scaler.transform(X_test)

  model = KNeighborsClassifier(n_neighbors=5, metric='euclidean')
  model.fit(X_train_scaled, y_train)
  y_pred = model.predict(X_test_scaled)""",
                    "duration": "50 دقيقة"
                },
                {
                    "title": "التجميع باستخدام K-Means",
                    "content": """K-Means هي أكثر خوارزميات التجميع (Clustering) شيوعاً. تقسّم البيانات إلى K مجموعات بحيث تكون النقاط ضمن المجموعة الواحدة متشابهة قدر الإمكان.

🎯 الهدف:
تقليل مجموع مسافات النقاط إلى مراكز مجموعاتها:
  التقليل: Σ Σ ||x - μₖ||²

💡 تشبيه:
تخيّل 1000 طالب نريد توزيعهم على K فصول دراسية. K-Means يجد التوزيعات الأكثر تجانساً تلقائياً بناءً على ملفاتهم الأكاديمية.

🔄 الخوارزمية التكرارية (4 خطوات):

الخطوة 1 — التهيئة:
   اختر K نقطة عشوائية كمراكز أولية (Centroids)
   (الطريقة المتقدمة: K-Means++ تختار مراكز متباعدة بشكل جيد)

الخطوة 2 — التعيين:
   عيّن كل نقطة للمجموعة ذات المركز الأقرب إليها:
   المجموعة = argmin_k ||x - μₖ||²

الخطوة 3 — التحديث:
   أعد حساب المراكز كمتوسط جميع نقاط المجموعة:
   μₖ = (1/|Cₖ|) × Σ x  لكل x في Cₖ

الخطوة 4 — التقارب:
   كرر الخطوتين 2 و3 حتى لا تتغير المجموعات
   (أو بعد عدد أقصى من التكرارات)

🔢 اختيار K — طريقة المرفق (Elbow Method):

نحسب الجمود الداخلي (Inertia) لـ K = 1, 2, 3, ..., 10 ونرسم المنحنى ونبحث عن "المرفق".

مثال:
   K=1 : الجمود = 1000
   K=2 : الجمود = 500  (ربح 500)
   K=3 : الجمود = 280  (ربح 220)
   K=4 : الجمود = 200  (ربح 80)  ← المرفق هنا، K=3 أو 4 مثالي
   K=5 : الجمود = 180  (ربح 20)

✅ المزايا:
• بسيط وسريع O(n×K×i×d)
• يعمل جيداً مع المجموعات الكروية المتباينة
• قابل للتوسع مع البيانات الكبيرة

❌ القيود:
• يجب تحديد K مسبقاً
• حساس للتهيئة العشوائية → استخدم K-Means++
• لا يتعامل مع المجموعات غير الكروية الشكل
• حساس للقيم الشاذة

🌍 التطبيقات العملية:

1. تجزئة السوق:
   تجميع العملاء حسب سلوكهم (تكرار الشراء، متوسط الإنفاق...)
   → تخصيص الحملات الإعلانية لكل شريحة

2. ضغط الصور:
   استبدال كل لون بلون المركز الأقرب إليه
   → تقليل 16 مليون لون إلى K لون فقط!

3. كشف الشذوذات:
   النقاط البعيدة عن أي مركز مشبوهة

4. إعداد البيانات:
   استخدام تعيينات المجموعات كميزات جديدة

🐍 كود Python:
  from sklearn.cluster import KMeans

  # إيجاد K الأمثل
  inertias = []
  for k in range(1, 11):
      kmeans = KMeans(n_clusters=k, init='k-means++', n_init=10)
      kmeans.fit(X)
      inertias.append(kmeans.inertia_)

  # النموذج النهائي
  kmeans = KMeans(n_clusters=4, init='k-means++', n_init=10, random_state=42)
  labels = kmeans.fit_predict(X)
  centers = kmeans.cluster_centers_""",
                    "duration": "55 دقيقة"
                },
                {
                    "title": "تقييم النماذج",
                    "content": """تقييم النماذج خطوة حاسمة للتأكد من أن نموذجنا سيُعمّم بشكل جيد على البيانات الجديدة، لا يحفظ فقط ما رآه.

📂 تقسيم البيانات — القاعدة الذهبية:

نقسّم دائماً مجموعة البيانات إلى 3 أجزاء:
• التدريب (70%): تعلّم معاملات النموذج
• التحقق (15%): اختيار المعاملات الفائقة ومقارنة النماذج
• الاختبار (15%): التقييم النهائي (استخدمه مرة واحدة فقط في النهاية!)

⚠️ خطأ شائع: استخدام بيانات الاختبار للتحسين → النتائج ستكون متفائلة جداً!

📊 مقاييس التصنيف:

مثال: كشف السرطان (إيجابي = مريض، سلبي = سليم)

مصفوفة الارتباك (لـ 100 مريض):
                   | تنبؤ إيجابي | تنبؤ سلبي |
  إيجابي حقيقي   |   TP = 40  |  FN = 10  |
  سلبي حقيقي     |   FP = 5   |  TN = 45  |

• الدقة الكلية (Accuracy) = (TP+TN) / الإجمالي = 85/100 = 85%
  ⚠️ مشكلة: إذا كان 95% من الرسائل عادية، نموذج يتنبأ بـ"عادي" دائماً دقته 95%!

• الدقة (Precision) = TP / (TP + FP) = 40/45 = 88.9%
  "من بين من حددتهم كمرضى، كم كانوا مرضى فعلاً؟"

• الاستدعاء (Recall) = TP / (TP + FN) = 40/50 = 80%
  "من بين جميع المرضى الحقيقيين، كم اكتشفتُ؟"
  → حرج في الطب: إغفال مريض خطير جداً (FN خطير)

• F1-Score = 2 × (Precision × Recall) / (Precision + Recall)
  → توازن بين الدقة والاستدعاء، مفيد مع فئات غير متوازنة

• ROC-AUC: المساحة تحت منحنى ROC
  → AUC = 1.0: نموذج مثالي | AUC = 0.5: نموذج عشوائي

🎭 الإفراط في التخصيص vs الإفراط في التبسيط:

الإفراط في التبسيط (Underfitting):
  → النموذج بسيط جداً ليلتقط تعقيد البيانات
  → أداء سيئ على التدريب والاختبار معاً
  → الحل: نموذج أكثر تعقيداً، ميزات أكثر

الإفراط في التخصيص (Overfitting):
  → النموذج حفظ بيانات التدريب (بما فيها الضوضاء)
  → ممتاز على التدريب، سيئ على الاختبار
  → الحل: بيانات أكثر، تنظيم (L1/L2)، Dropout

🔄 التحقق المتقاطع K-Fold:

بدلاً من تقسيم واحد، نقوم بـ K دورات متناوبة:
  Fold 1: [اختبار] [تدريب] [تدريب] [تدريب] [تدريب]
  Fold 2: [تدريب] [اختبار] [تدريب] [تدريب] [تدريب]
  ...
  النتيجة النهائية = متوسط K نتائج → تقدير أكثر موثوقية!

⚖️ مقايضة الانحياز-التباين:
• الانحياز (Bias): خطأ منهجي (نموذج بسيط جداً)
• التباين (Variance): حساسية لتقلبات البيانات (نموذج معقد جداً)
• نبحث عن التوازن المثالي بين الاثنين

🐍 كود Python:
  from sklearn.model_selection import cross_val_score
  from sklearn.metrics import classification_report, confusion_matrix

  # التحقق المتقاطع
  scores = cross_val_score(model, X_train, y_train, cv=5, scoring='f1')
  print(f"F1 المتوسط: {scores.mean():.3f} ± {scores.std():.3f}")

  # تقرير كامل
  y_pred = model.predict(X_test)
  print(classification_report(y_test, y_pred))""",
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
                    "content": """البيرسبترون هو اللبنة الأساسية لجميع الشبكات العصبية. فهم آليته ضروري لإتقان التعلم العميق.

🧠 الإلهام البيولوجي:
الخلية العصبية البيولوجية تستقبل إشارات من تشعباتها، تتراكمها، وإذا تجاوز العتبة، ترسل إشارة عبر محورها. البيرسبترون الاصطناعي مستوحى من هذه الآلية.

📐 البيرسبترون — الصيغة الكاملة:

  المخرج = f( w₁×x₁ + w₂×x₂ + ... + wₙ×xₙ + b )

التوضيح:
• x₁, x₂, ..., xₙ = المدخلات (ميزات المسألة)
• w₁, w₂, ..., wₙ = الأوزان (أهمية كل مدخل)
• b = الانحياز (يسمح بإزاحة حد القرار)
• f = دالة التفعيل (تُدخل اللاخطية)
• مجموع w×x + b = التركيب الخطي (الضرب النقطي)

💡 مثال عملي:
  كشف البريد المزعج (ميزتان):
  - x₁ = عدد الكلمات المشبوهة (مثال: "مال"، "مجاني")
  - x₂ = عدد كلمات الرسالة

  بعد التدريب: w₁ = 0.8, w₂ = -0.3, b = -1.5
  لرسالة (x₁=3, x₂=50):
  z = 0.8×3 + (-0.3)×50 + (-1.5) = 2.4 - 15 - 1.5 = -14.1
  المخرج = sigmoid(-14.1) ≈ 0 → ليس بريداً مزعجاً

🏗️ الشبكات متعددة الطبقات (MLP):

بيرسبترون واحد يحل فقط المسائل القابلة للفصل الخطي.
الحل: تكديس عدة بيرسبترونات في طبقات:

  طبقة الإدخال → طبقات مخفية → طبقة الإخراج

بنية نموذجية لتصنيف الصور:
  784 مدخل (28×28 بكسل) → [256] → [128] → [64] → 10 مخرجات (أرقام 0-9)

الانتشار للأمام (Forward Propagation):
  في كل طبقة: z = W × a + b، ثم a = f(z)
  تنتشر التفعيلات من طبقة إلى أخرى حتى الإخراج.

🌐 نظرية التقريب العالمي:
شبكة MLP ذات طبقة مخفية واحدة كبيرة بما يكفي يمكنها تقريب أي دالة مستمرة!
→ نظرياً، الشبكة العصبية تستطيع تعلم أي شيء.
→ عملياً: الشبكات العميقة (طبقات متعددة) تتعلم بشكل أفضل بعدد أقل من النيورونات.

📊 التمثيل المتجهي:
مع المصفوفات، حساب طبقة كاملة هو:
   A[l] = f( W[l] × A[l-1] + b[l] )
→ فعّال جداً مع GPU ومكتبات TensorFlow/PyTorch

🐍 كود PyTorch:
  import torch.nn as nn

  class MLP(nn.Module):
      def __init__(self):
          super().__init__()
          self.layers = nn.Sequential(
              nn.Linear(784, 256),
              nn.ReLU(),
              nn.Linear(256, 128),
              nn.ReLU(),
              nn.Linear(128, 10),
              nn.Softmax(dim=1)
          )

      def forward(self, x):
          return self.layers(x)""",
                    "duration": "60 دقيقة"
                },
                {
                    "title": "دالة التفعيل والانتشار العكسي",
                    "content": """دوال التفعيل والانتشار العكسي هما الآليتان اللتان تُمكّنان الشبكات العصبية من تعلم تمثيلات معقدة.

⚡ دوال التفعيل — لماذا هي ضرورية؟

بدون دالة تفعيل، تكديس طبقات خطية سيُعطي دائماً نتيجة خطية (Ax + b). اللاخطية تسمح بنمذجة حدود قرار معقدة.

الدوال الرئيسية:

1. ReLU (الوحدة الخطية المُصحَّحة) — الأكثر شيوعاً اليوم:
   f(x) = max(0, x)
   • المشتقة: 1 إذا x > 0، 0 في غير ذلك
   ✅ سريعة الحساب، تتجنب التدرج المتلاشي لـ x > 0
   ❌ "النيورونات الميتة": إذا كان مدخل نيورون سالباً دائماً، تدرجه = 0

2. Sigmoid:
   f(x) = 1 / (1 + e^{-x}) → مخرج بين 0 و1
   ✅ مثالية للإخراج في التصنيف الثنائي (الاحتمالية)
   ❌ التدرج المتلاشي للقيم المتطرفة

3. Tanh (المماس الزائدي):
   f(x) = (e^x - e^{-x}) / (e^x + e^{-x}) → مخرج بين -1 و1
   ✅ مركزة حول الصفر (تقارب أفضل من Sigmoid)
   ❌ نفس مشكلة التدرج المتلاشي

4. المتغيرات الحديثة:
   • Leaky ReLU: f(x) = max(0.01x, x) → تحل مشكلة النيورونات الميتة
   • GELU: مستخدمة في BERT، GPT → أكثر نعومة من ReLU
   • Swish: f(x) = x × sigmoid(x) → غالباً أفضل من ReLU عملياً

🔄 الانتشار العكسي — كيف تتعلم الشبكة:

الانتشار العكسي هو الخوارزمية التي تحسب كيفية تعديل كل وزن لتقليل الخطأ. تستخدم قاعدة السلسلة في حساب التفاضل.

الخطوات:

1. الانتشار الأمامي: حساب التنبؤ y_pred
2. حساب دالة الخسارة (Loss):
   - التصنيف: Cross-Entropy = -Σ y × log(y_pred)
   - الانحدار: MSE = (1/n) × Σ (y - y_pred)²
3. الانتشار العكسي: حساب ∂Loss/∂w لكل وزن w
4. تحديث الأوزان:
   w = w - α × ∂Loss/∂w
   (α = معدل التعلم، Learning Rate)

📉 النزول التدريجي:
تخيل كرة على جبل ضبابي تبحث عن الوادي (أدنى خسارة):
• التدرج = اتجاه أشد انحدار (للأعلى)
• نسير في الاتجاه المعاكس للتدرج (للأسفل)
• معدل التعلم α = حجم الخطوة

متغيرات المُحسِّن:
• SGD: مثال واحد في كل مرة
• Mini-batch SGD: دفعات من 32/64/128 مثال (المعيار)
• Momentum: يجمع التدرجات السابقة للتسريع
• Adam: يجمع Momentum + معدل تكيفي لكل وزن
  → Adam هو الأكثر استخداماً عملياً!

🐍 كود PyTorch:
  criterion = nn.CrossEntropyLoss()
  optimizer = torch.optim.Adam(model.parameters(), lr=0.001)

  for epoch in range(100):
      optimizer.zero_grad()         # إعادة تهيئة التدرجات
      y_pred = model(X_batch)       # الانتشار الأمامي
      loss = criterion(y_pred, y)   # حساب الخسارة
      loss.backward()               # الانتشار العكسي
      optimizer.step()              # تحديث الأوزان""",
                    "duration": "65 دقيقة"
                },
                {
                    "title": "الشبكات التلافيفية CNN",
                    "content": """الشبكات التلافيفية (CNN) ثورت رؤية الحاسوب. تستغل البنية المكانية للصور لتعلم تمثيلات هرمية.

🖼️ لماذا CNN للصور؟

شبكة MLP كلاسيكية لصورة 224×224×3 بكسل = 150,528 مدخل!
→ مشاكل: معاملات كثيرة جداً، تتجاهل البنية المكانية، غير ثابتة للانزياح.

CNN تحل كل هذا بـ 3 أفكار أساسية: المحلية، الأوزان المشتركة، الهرمية.

🔩 العمليات الثلاث الأساسية:

1. التلافيف (Convolution — طبقة Conv2D):
   مرشح (Kernel) يُحرَّك على الصورة ويحسب الضربات النقطية.
   • مرشح 3×3 = 9 أوزان (مشتركة على كامل الصورة!)
   • نفس المرشح يكتشف نفس النمط في كل مكان
   • 32 مرشحاً → 32 "خريطة ميزات" (Feature Maps)
   
   ما الذي تكتشفه المرشحات؟
   • الطبقات الأولى: الحواف والزوايا والألوان (عامة)
   • الطبقات الوسطى: القوام والأشكال البسيطة
   • الطبقات العليا: أجزاء الوجوه، العجلات، العيون...

2. التجميع (Pooling — Max Pooling):
   يُقلّل الحجم المكاني مع الحفاظ على المعلومات الأهم.
   • MaxPool 2×2: يأخذ الحد الأقصى في كل منطقة 2×2
   • يُقسّم الحجم على 2 → حسابات أقل، أكثر متانة

3. تفعيل ReLU:
   بعد كل تلافيف: f(x) = max(0, x) → اللاخطية

📐 البنية الكاملة النموذجية:

  صورة (224×224×3)
  → Conv2D(32 مرشح, 3×3) + ReLU → (222×222×32)
  → MaxPool(2×2)              → (111×111×32)
  → Conv2D(64 مرشح, 3×3) + ReLU → (109×109×64)
  → MaxPool(2×2)              → (54×54×64)
  → Flatten                   → (186,624)
  → Dense(256) + ReLU         → (256)
  → Dense(10) + Softmax       → (10) [10 فئات]

🏗️ البنى الشهيرة:

• LeNet (1998): أول CNN، أرقام MNIST المكتوبة بخط اليد
• AlexNet (2012): الثورة! ImageNet، 5 طبقات تلافيف، Dropout
• VGG (2014): عميق جداً، مرشحات 3×3 فقط، 138M معامل
• ResNet (2015): روابط متبقية → تدريب شبكات 152 طبقة!
  الابتكار: skip connections: y = F(x) + x → تتجنب التدرج المتلاشي
• EfficientNet (2019): تحجيم مثالي للعرض/العمق/الدقة

🐍 كود Keras/TensorFlow:
  from tensorflow.keras import layers, models

  model = models.Sequential([
      layers.Conv2D(32, (3,3), activation='relu', input_shape=(224,224,3)),
      layers.MaxPooling2D(2,2),
      layers.Conv2D(64, (3,3), activation='relu'),
      layers.MaxPooling2D(2,2),
      layers.Conv2D(128, (3,3), activation='relu'),
      layers.Flatten(),
      layers.Dense(512, activation='relu'),
      layers.Dropout(0.5),
      layers.Dense(10, activation='softmax')
  ])""",
                    "duration": "70 دقيقة"
                },
                {
                    "title": "الشبكات المتكررة RNN/LSTM",
                    "content": "RNN تحافظ على حالة مخفية لمعالجة التسلسلات.\n\nالصيغة: h_t = tanh(W_hh*h_{t-1} + W_xh*x_t + b)\n\nمشكلة التدرج المتلاشي: عند الانتشار العكسي عبر الزمن، تتضاءل التدرجات أو تنفجر.\n\nLSTM — الحل: تضيف خلية ذاكرة c_t و3 بوابات:\n• بوابة النسيان: f_t = σ(W_f × [h_{t-1}, x_t] + b_f) → ماذا تنسى من الذاكرة\n• بوابة الإدخال: i_t = σ(W_i × [h_{t-1}, x_t] + b_i) → ماذا تضيف للذاكرة\n• بوابة الإخراج: o_t = σ(W_o × [h_{t-1}, x_t] + b_o) → ماذا تخرج\nتحديث الخلية: c_t = f_t ⊙ c_{t-1} + i_t ⊙ c̃_t\n\nGRU: نسخة مبسطة من LSTM ببوابتين فقط (إعادة الضبط والتحديث). معاملات أقل، غالباً نفس الأداء.\n\nمقارنة:\n• RNN: بسيط وسريع، لكن ذاكرة قصيرة\n• LSTM: قوي وذاكرة طويلة، لكن معاملات كثيرة\n• GRU: توازن جيد بين السرعة والأداء\n\nالتطبيقات: الترجمة الآلية (seq2seq مع الانتباه)، توليد النصوص، التعرف على الكلام، التنبؤ بالسلاسل الزمنية (البورصة، الطقس)، تحليل المشاعر.\n\nكود PyTorch:\n  lstm = nn.LSTM(input_size=100, hidden_size=256, num_layers=2, batch_first=True)\n  output, (hn, cn) = lstm(x, (h0, c0))",
                    "duration": "65 دقيقة"
                },
                {
                    "title": "مقدمة في Transformers",
                    "content": "ثورة Transformers (2017 - ورقة 'Attention Is All You Need'): تعالج المتسلسلات بالكامل في وقت واحد بدلاً من كلمة بكلمة.\n\nآلية الانتباه الذاتي (Self-Attention):\nلكل كلمة 3 متجهات: Q (ما أبحث عنه)، K (ما أقدمه)، V (المعلومة التي أحملها).\nالحساب: Attention(Q,K,V) = softmax(Q×Kᵀ / √d_k) × V\nمثال: في 'رفض البنك قرضي لأنها ليس لديها مال'، كلمة 'هي' تنتبه بقوة لـ'البنك'.\n\nMulti-Head Attention: عدة انتباهات بالتوازي، كل رأس يتعلم علاقات مختلفة:\n• الرأس 1: علاقات نحوية (فاعل-فعل)\n• الرأس 2: علاقات دلالية (مترادفات)\n• الرأس 3: مرجعية الضمائر\n\nبنية Transformer الكاملة:\nالمشفر (لكل طبقة): Multi-Head Attention → Add&Norm → Feed-Forward → Add&Norm\nفك المشفر: Masked Attention → Cross-Attention → Feed-Forward\nالترميز الموضعي (Positional Encoding): يضيف معلومات الترتيب لأن المحول لا يعرف الترتيب تلقائياً.\n\nالنماذج الكبرى:\n• BERT (2018، Google): مشفر فقط، ثنائي الاتجاه، 110M-340M معامل\n• GPT-3 (2020، OpenAI): فك مشفر فقط، 175 مليار معامل\n• T5 (Google): مشفر + فك مشفر، كل شيء نص-إلى-نص\n• Vision Transformer (ViT): يطبق المحولات على الصور!\n\nالمزايا: معالجة موازية كاملة، يلتقط الاعتمادات البعيدة جداً.\nالقيود: ذاكرة O(n²) → صعوبة مع المتسلسلات الطويلة جداً.",
                    "duration": "70 دقيقة"
                },
                {
                    "title": "الضبط الدقيق ونقل التعلم",
                    "content": "التعلم بالنقل (Transfer Learning): إعادة استخدام المعرفة المكتسبة في مهمة لتسريع التعلم في مهمة أخرى.\n\nلماذا يعمل؟ نموذج ResNet المُدرَّب على ImageNet تعلّم بالفعل:\n• الطبقات الأولى: كاشفات حواف وزوايا وألوان (عامة لكل الصور)\n• الطبقات الوسطى: أنماط وقوام (شبه عامة)\n• الطبقات العليا: أجزاء كائنات ImageNet (أقل عمومية)\n\nمقاربتان رئيسيتان:\n1. استخراج الميزات (Feature Extraction):\n   → تجميد كل أوزان النموذج المُدرَّب مسبقاً\n   → إضافة طبقات تصنيف جديدة فقط في النهاية\n   → مناسب: بيانات قليلة جداً، مهمة مشابهة للمصدر\n\n2. الضبط الدقيق الكامل (Full Fine-tuning):\n   → تحميل الأوزان المُدرَّبة مسبقاً\n   → تدريب كل النموذج بمعدل تعلم صغير جداً (1e-5 إلى 5e-5)\n   → مناسب: بيانات متوسطة إلى كبيرة\n\nالضبط الدقيق التدريجي (Gradual Unfreezing):\n   المرحلة 1: تدريب رأس التصنيف فقط\n   المرحلة 2: فك تجميد آخر 2 طبقات + التدريب\n   المرحلة 3: فك تجميد كل النموذج + التدريب\n\nتقنيات متقدمة:\n• LoRA: إضافة مصفوفات رتبة منخفضة بدلاً من تعديل كل الأوزان → 99% أقل معاملات قابلة للتدريب\n• Prompt Engineering: توجيه النموذج بتعليمات بدون تعديل الأوزان\n• Zero-shot: 'ترجم هذا النص إلى الإسبانية: ...'\n• Few-shot: تقديم 3-5 أمثلة في الـ prompt\n• RLHF: تقوية التعلم من ردود فعل البشر (ChatGPT، Claude)\n\nكود Keras:\n  base = ResNet50(weights='imagenet', include_top=False)\n  base.trainable = False  # تجميد\n  model = Sequential([base, GlobalAveragePooling2D(), Dense(num_classes, activation='softmax')])",
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
                    "content": "قبل تغذية نموذج NLP، يجب تحويل النص الخام إلى تمثيل رقمي. هذه المرحلة حاسمة وتؤثر مباشرة على جودة النموذج.\n\nخط أنابيب المعالجة المسبقة الكاملة:\nنص خام → تنظيف → تجزئة → تطبيع → حذف كلمات التوقف → ليمتة → متجهات رقمية\n\n1. تنظيف النص:\n• إزالة وسوم HTML: <p>مرحبا</p> → 'مرحبا'\n• إزالة الروابط: 'زر https://example.com' → 'زر'\n• إزالة الأحرف الخاصة، معالجة الإيموجي\n\n2. التجزئة (Tokenization):\nأ) مستوى الكلمة: 'القط يأكل' → ['القط', 'يأكل']\n  ✅ بديهي | ❌ مفردات ضخمة، كلمات خارج المفردات (OOV)\nب) مستوى الحرف: 'قطة' → ['ق','ط','ة']\n  ✅ لا كلمات مجهولة | ❌ تسلسلات طويلة\nج) تجزئة فرعية (Subword) — المعيار الحديث:\n  BPE: 'يلعبون' → ['يلعب','ون'] → مستخدم في GPT-2، RoBERTa\n  WordPiece: مشابه، '##' للمقطع الداخلي → مستخدم في BERT\n  SentencePiece: متعدد اللغات → مستخدم في T5، LLaMA\n\n3. التطبيع:\n• تحويل للحروف الصغيرة: 'تويتر' → 'تويتر' (⚠️ 'Apple' الشركة vs 'apple' التفاحة)\n• إزالة التشكيل في العربية (أحياناً)\n• توحيد الهمزات: 'إبراهيم' = 'ابراهيم'\n\n4. حذف كلمات التوقف (Stop Words):\nكلمات شائعة جداً: 'في'، 'من'، 'على'، 'هو'، 'هي'...\n✅ يقلل الضوضاء للبحث عن المعلومات\n❌ قد يضر مهام تحليل المشاعر والترجمة\n\n5. الليمتة (Lemmatization) vs التجذير (Stemming):\nالتجذير (سريع، تقريبي): 'يلعبون', 'لعب', 'لاعب' → 'لعب' (قطع مباشر)\nالليمتة (أبطأ، دقيق): 'يلعبون', 'لعب', 'لاعب' → 'لعب' (الشكل القاموسي)\n\n6. الترميز الرقمي:\n• TF-IDF: تكرار الكلمة × log(N/df) → يعطي وزناً أكبر للكلمات النادرة المميزة\n• Word Embeddings: متجهات كثيفة 50-300 بُعد (Word2Vec، GloVe)\n\nكود Python (SpaCy):\n  import spacy\n  nlp = spacy.load('ar_core_news_sm')\n  doc = nlp('القطط تصطاد الفئران منذ قرون')\n  tokens = [t.lemma_ for t in doc if not t.is_stop and not t.is_punct]",
                    "duration": "45 دقيقة"
                },
                {
                    "title": "تضمينات الكلمات Word2Vec و GloVe",
                    "content": "تُحوّل تضمينات الكلمات (Word Embeddings) الكلمات إلى متجهات رقمية كثيفة تلتقط المعنى الدلالي.\n\nلماذا التضمينات؟\nOne-Hot: 'قطة' = [1,0,0,...] و'كلب' = [0,1,0,...] → متعامدتان! النموذج لا يعلم أنهما متشابهتان.\nWord Embeddings: الكلمات المتشابهة لها متجهات قريبة:\n  'قطة'   → [0.2, -0.4, 0.7, ...] (300 بُعد)\n  'كلب'  → [0.3, -0.3, 0.8, ...] (قريب من قطة!)\n  'ملك'  → [0.9,  0.1, 0.2, ...] (بعيد)\n\nWord2Vec (2013، Google):\nالفرضية التوزيعية: 'الكلمة تُعرَّف بجيرانها'\nبنيتان:\n• CBOW: السياق → الكلمة المركزية. 'القط ___ فأراً' → 'أكل'. أسرع، أفضل للكلمات الشائعة.\n• Skip-gram: الكلمة المركزية → السياق. 'أكل' → ['القط', 'فأراً']. أفضل للكلمات النادرة.\nالحيلة — Negative Sampling: بدلاً من حساب الاحتمال على كل المفردات، نتدرب على مصنّف ثنائي (جار حقيقي vs عشوائي).\n\nGloVe (2014، Stanford):\nيستغل مصفوفة الترافق العالمية: X_ij = عدد مرات ظهور j في سياق i.\nالهدف: w_i · w̃_j + b_i + b̃_j ≈ log(X_ij)\nيلتقط الإحصاءات العالمية، ممتاز للتماثلات.\n\nFastText (2016، Facebook):\nابتكار: يحلّل الكلمات إلى n-grammes من الأحرف:\n  'قطة' → ['<قط', 'قطة', 'طة>'] (3-grammes)\nيتعامل مع الكلمات خارج المفردات!\nأفضل للغات الصرفية الغنية (العربية، التركية...).\n\nخصائص رائعة — الحساب المتجهي:\n  ملك - رجل + امرأة ≈ ملكة  ✨\n  باريس - فرنسا + ألمانيا ≈ برلين  ✨\n\nكود Python:\n  from gensim.models import Word2Vec\n  model = Word2Vec(sentences, vector_size=100, window=5, min_count=1)\n  print(model.wv.similarity('قطة', 'كلب'))  # 0.82\n  print(model.wv.most_similar('ملك'))         # [('ملكة', 0.91), ...]",
                    "duration": "55 دقيقة"
                },
                {
                    "title": "نماذج التسلسل Seq2Seq",
                    "content": "بنية المشفر-فك المشفر (Encoder-Decoder) تُحوّل متسلسلة بطول متغير إلى أخرى بطول مختلف.\n\nالمشكلة: جملة عربية من 8 كلمات قد تُترجم لـ 10 كلمات فرنسية، والكلمات لا تتطابق 1:1.\n\nالمشفر (Encoder):\n• يقرأ الجملة المصدر كلمة بكلمة (بـ LSTM/GRU)\n• يبني تدريجياً فهماً للمعنى\n• ينتج متجه السياق (Context Vector) = h_T النهائي\n→ هذا المتجه تمثيل مضغوط للجملة كاملة\n\nفك المشفر (Decoder):\n• يأخذ متجه السياق كحالة أولية\n• يُولّد الجملة الهدف كلمة بكلمة\n• كل تنبؤ يُستخدم كمدخل للخطوة التالية\n\nمشكلة عنق الزجاجة:\nكل معنى الجملة يجب أن يتسع في متجه واحد (مثلاً 256 بُعداً).\nللجمل الطويلة → فقدان المعلومات!\n\nآلية الانتباه — الحل:\nبدلاً من متجه سياق واحد، يستطيع فك المشفر 'النظر' إلى كل حالات المشفر:\nفي كل خطوة t:\n1. حساب درجة التوافق: e_ti = score(s_t, h_i)\n2. تطبيق softmax: α_ti = softmax(e_ti) → مجموعها 1\n3. متجه السياق الديناميكي: c_t = Σ α_ti × h_i\n4. استخدام c_t + s_t للتنبؤ بالكلمة التالية\n\nالحدس: لتوليد 'قطة' بالإنجليزية، يُركّز فك المشفر على الكلمة المصدر 'قطة' (وزن عالٍ).\n\nTeacher Forcing:\nأثناء التدريب: تغذية الكلمة الحقيقية (لا التنبؤ) كمدخل لفك المشفر.\n✅ تقارب أسرع | ❌ تباين بين التدريب والاستدلال\n\nBeam Search (K=5):\nبدلاً من أخذ الكلمة الأكثر احتمالاً (Greedy)، نحتفظ بأفضل K تسلسلات جزئية.\n✅ نتائج أفضل من Greedy | ❌ أبطأ\n\nالتطبيقات: الترجمة، التلخيص، Chatbots، توليد الكود، تصحيح القواعد.",
                    "duration": "60 دقيقة"
                },
                {
                    "title": "BERT والنماذج المُدرّبة مسبقاً",
                    "content": "BERT (تمثيلات المشفر ثنائية الاتجاه من Transformer) أعاد تعريف معايير NLP عام 2018.\n\nالابتكار الرئيسي — ثنائية الاتجاه:\nGPT (قبل BERT): يقرأ من اليسار لليمين فقط.\nBERT: يأخذ السياق من اليسار واليمين في آنٍ واحد!\n'رفض البنك ___ لي' → 'القرض' (بفضل السياق الكامل)\nنفس الكلمة = تمثيل مختلف حسب السياق (تضمينات سياقية).\n\nمرحلة التدريب المسبق — مهمتان:\n1. MLM (نموذج اللغة المقنّع):\n   • إخفاء 15% عشوائياً بـ[MASK]: 'القط [MASK] فأراً' → التنبؤ بـ'يأكل'\n   • الـ15% المخفية: 80% [MASK]، 10% كلمة عشوائية، 10% الكلمة نفسها\n2. NSP (التنبؤ بالجملة التالية):\n   جملة A + جملة B → 'متتاليتان؟' (نعم 50% / لا 50%)\n   يُجبر BERT على فهم العلاقات بين الجمل.\n\nالبنية:\nيستخدم BERT فقط طبقات المشفر من Transformer.\nرموز خاصة:\n• [CLS]: بداية كل تسلسل (تمثيله النهائي = خاصية الجملة كاملة)\n• [SEP]: فاصل بين جملتين\n• [PAD]: تعبئة لتوحيد الطول\n\nBERT-Base: 12 طبقة، 12 رأس انتباه، hidden=768، 110M معامل\nBERT-Large: 24 طبقة، 16 رأس، hidden=1024، 340M معامل\n\nمتغيرات مهمة:\n• RoBERTa: BERT مُدرَّب أطول وأكثر بيانات، يحذف NSP → يتفوق على BERT\n• ALBERT: مشاركة الأوزان بين الطبقات → 12M معامل فقط بنفس الأداء!\n• DistilBERT: تقطير BERT → 40% أقل معاملات، 60% أسرع، 97% من الأداء\n• AraBERT: BERT مُدرَّب على نصوص عربية ضخمة → أفضل للعربية\n• CAMeL-BERT: متخصص للعربية الفصحى والعامية\n\nكود HuggingFace:\n  from transformers import BertTokenizer, BertModel\n  tokenizer = BertTokenizer.from_pretrained('bert-base-multilingual-cased')\n  model = BertModel.from_pretrained('bert-base-multilingual-cased')\n  inputs = tokenizer('القط يجلس على السجادة', return_tensors='pt')\n  outputs = model(**inputs)\n  sentence_emb = outputs.last_hidden_state[:, 0, :]  # رمز [CLS]",
                    "duration": "65 دقيقة"
                },
                {
                    "title": "الضبط الدقيق للتصنيف",
                    "content": "الضبط الدقيق لـBERT يُكيّف النموذج لمهمة محددة ببيانات صغيرة نسبياً (آلاف لا ملايين المثال).\n\nلماذا يعمل الضبط الدقيق جيداً؟\nBERT تعلّم بالفعل:\n• قواعد اللغة والنحو\n• العلاقات الدلالية بين الكلمات\n• المعنى السياقي للجمل\n→ نحتاج فقط تعلّم المهمة المحددة!\n\nبنية تصنيف النصوص:\n  نص → تجزئة → [CLS] + رموز → BERT (12 طبقة) → تمثيل [CLS] (768 بُعد) → Dense(num_classes) → Softmax\n\nلماذا رمز [CLS]؟\n→ مصمم لتجميع معلومات التسلسل كاملاً (بفضل الانتباه الثنائي الاتجاه)\n\nمعاملات فائقة حرجة:\n• معدل التعلم: الأهم!\n  - كبير جداً: يمحو الأوزان المُدرَّبة ('نسيان كارثي')\n  - الأمثل: 2e-5 إلى 5e-5 (أصغر بكثير من 1e-3 المعتاد)\n• حجم الدفعة: 16 أو 32 (محدود بذاكرة GPU)\n• عدد الحقب: 2 إلى 4 (أكثر → إفراط في التخصيص)\n\nاستراتيجيات متقدمة:\n1. Gradual Unfreezing:\n   الحقبة 1: تدريب رأس التصنيف فقط\n   الحقبة 2: فك تجميد آخر طبقتين + التدريب\n   الحقبة 3: فك تجميد كل BERT + التدريب\n2. معدلات تعلم تمييزية:\n   طبقة الإخراج: lr = 5e-5 | طبقات وسطى: lr = 3e-5 | طبقات أولى: lr = 1e-5\n\nتقييم شامل:\n  مصفوفة الارتباك لـ5 فئات مشاعر:\n  → نحدد أي الفئات تُخلَط مع بعضها\n  تقرير التصنيف: Precision، Recall، F1-Score لكل فئة\n\nكود HuggingFace:\n  from transformers import BertForSequenceClassification, TrainingArguments, Trainer\n  model = BertForSequenceClassification.from_pretrained('aubmindlab/bert-base-arabertv2', num_labels=5)\n  training_args = TrainingArguments(num_train_epochs=3, learning_rate=2e-5, per_device_train_batch_size=16)\n  trainer = Trainer(model=model, args=training_args, train_dataset=train_ds, eval_dataset=val_ds)\n  trainer.train()",
                    "duration": "55 دقيقة"
                },
                {
                    "title": "توليد النصوص باستخدام GPT",
                    "content": "GPT (Generative Pre-trained Transformer) عائلة نماذج توليد النصوص من OpenAI. على عكس BERT، هو نموذج ذاتي الانحدار أحادي الاتجاه.\n\nبنية GPT — طبقات فك المشفر فقط:\nيستخدم فقط طبقات Decoder من Transformer.\nفي كل موضع، لا يرى النموذج إلا الرموز السابقة (انتباه سببي).\nالتدريب: التنبؤ بالرمز التالي! P(token_t | token_1, ..., token_{t-1})\n\nتطور عائلة GPT:\n• GPT-1 (2018): 117M معامل، 12 طبقة - أول نموذج يُظهر قوة التدريب المسبق + الضبط الدقيق\n• GPT-2 (2019): 1.5B معامل، 48 طبقة - 'خطير جداً للنشر' (OpenAI احتجزته مبدئياً)\n• GPT-3 (2020): 175 مليار معامل! قدرات Few-shot مذهلة، أساس ChatGPT\n• GPT-4 (2023): متعدد الوسائط (نص + صور)، أداء بشري على معظم المعايير\n\nاستراتيجيات التوليد — كيف نولّد النص؟\n1. Greedy Decoding: اختر الرمز الأعلى احتمالاً دائماً.\n   ❌ غالباً متكرر: 'القط جلس على... القط جلس على...'\n\n2. Beam Search (k=5): احتفظ بأفضل k تسلسلات جزئية.\n   ✅ أفضل من Greedy | ❌ جمل قصيرة وعامة\n\n3. Top-K Sampling: اختر عشوائياً من أفضل K رموز.\n   K=50: من بين الكلمات الأكثر احتمالاً\n   ✅ تنوع أكثر | ❌ K ثابت قد يتضمن رموزاً غير مناسبة\n\n4. Nucleus Sampling (Top-p) — المعيار في الإنتاج:\n   اختر عشوائياً من أصغر مجموعة تغطي احتمال ≥ p.\n   p=0.9: الرموز التي تمثل 90% من إجمالي الاحتمال\n   ✅ تكيفي حسب التوزيع | ✅ الأفضل عملياً\n\n5. Temperature — يتحكم في 'إبداعية' النموذج:\n   T < 1: أكثر حتمية (مناسب للنصوص الوقائعية)\n   T = 1: التوزيع الأصلي\n   T > 1: أكثر عشوائية وإبداعاً (القصص والشعر)\n   logits_معدّلة = logits / temperature\n\nهندسة الأوامر (Prompt Engineering):\n• Zero-shot: 'ترجم هذه الجملة للإسبانية: القط يجلس على السجادة.'\n• Few-shot: تقديم أمثلة في الـ prompt → النموذج يفهم المهمة!\n• Chain-of-Thought: 'حل المسألة خطوة بخطوة...' → يحسّن التفكير المعقد بشكل كبير\n\nكود HuggingFace:\n  from transformers import GPT2LMHeadModel, GPT2Tokenizer\n  tokenizer = GPT2Tokenizer.from_pretrained('gpt2')\n  model = GPT2LMHeadModel.from_pretrained('gpt2')\n  inputs = tokenizer.encode('مستقبل الذكاء الاصطناعي', return_tensors='pt')\n  outputs = model.generate(inputs, max_length=100, do_sample=True, temperature=0.8, top_p=0.9)\n  print(tokenizer.decode(outputs[0], skip_special_tokens=True))",
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
                    "content": "OpenCV أكثر مكتبات رؤية الحاسوب استخداماً (2500+). العمليات: cv2.imread()، cv2.resize()، cv2.cvtColor() (⚠️ BGR وليس RGB!). الفلاتر: GaussianBlur (ضوضاء غاوسية)، medianBlur (ملح وفلفل)، bilateralFilter (يحافظ على الحواف). المورفولوجيا: التآكل يُقلّص، التوسع يُوسّع، الفتح=تآكل+توسع يزيل الضوضاء، الإغلاق=توسع+تآكل يملأ الثقوب. الهيستوغرام: cv2.equalizeHist() لتحسين التباين، CLAHE للصور الطبية.",
                    "duration": "50 دقيقة"
                },
                {
                    "title": "كشف الحواف والميزات",
                    "content": "كشف الحواف والميزات أساسيٌ لرؤية الحاسوب الكلاسيكية.\n\nكشف الحواف:\n\n1. Sobel (تدرج الدرجة الأولى):\n   يحسب المشتقات الجزئية في كل اتجاه.\n   Gx = [[-1,0,1],[-2,0,2],[-1,0,1]]  (أفقي)\n   Gy = [[1,2,1],[0,0,0],[-1,-2,-1]]  (عمودي)\n   الحجم = sqrt(Gx² + Gy²)\n   → يكتشف الحواف لكنه حساس للضوضاء.\n\n2. Canny (المعيار الصناعي):\n   خطوارزمية من 4 خطوات:\n   أ) GaussianBlur لتقليل الضوضاء\n   ب) حساب التدرج (Sobel)\n   ج) قمع غير القصوى: الاحتفاظ بالحد الأقصى المحلي فقط\n   د) العتبة الهسترية: عتبتان (منخفضة/عالية)\n      - بكسل > عتبة عالية → حافة مؤكدة\n      - بكسل < عتبة منخفضة → يُحذف\n      - بين العتبتين → حافة إذا متصلة بحافة مؤكدة\n   cv2.Canny(img, low=100, high=200)\n\nكشف الزوايا:\n3. Harris Corner Detector:\n   يكتشف المناطق التي يتغير فيها التدرج في كل الاتجاهات.\n   مصفوفة البنية M = Σ [Ix², IxIy; IxIy, Iy²]\n   النتيجة R = det(M) - k × trace(M)²\n   R >> 0 → زاوية | R << 0 → حافة | |R| ≈ 0 → مستو\n\nnقاط الاهتمام الثابتة:\n4. SIFT (Scale-Invariant Feature Transform):\n   يكتشف نقاط اهتمام ثابتة للتغييرات: الحجم (التكبير)، الدوران، الإضاءة.\n   الواصف: هيستوغرام التدرجات المحلية (128 بُعداً).\n   ✅ قوي جداً | ❌ بطيء، كان محمياً ببراءة اختراع (الآن مجاني)\n\n5. ORB (Oriented FAST and Rotated BRIEF):\n   بديل سريع ومجاني لـ SIFT.\n   كاشف FAST + واصف BRIEF الموجّه.\n   ✅ الوقت الفعلي | ✅ مجاني\n\nاستخراج الكفوف:\n6. findContours:\n   يجد كفوف المناطق المتصلة.\n   contours, _ = cv2.findContours(mask, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)\n   ثم: cv2.boundingRect(c)، cv2.contourArea(c)، cv2.arcLength(c, True)",
                    "duration": "55 دقيقة"
                },
                {
                    "title": "تصنيف الصور باستخدام CNN",
                    "content": "تصنيف الصور: تعيين فئة لصورة كاملة. اختيار النموذج (Transfer Learning): MobileNetV2 (3.4M، سريع/موبايل)، ResNet50 (25.6M، 93%)، EfficientNetB4 (98%). زيادة البيانات: دوران [-15,+15]، انعكاس، تكبير [0.8,1.2]، CutMix/MixUp. الضبط التدريجي: مرحلة 1 تجميد+رأس فقط، مرحلة 2 آخر 50 طبقة lr=1e-5، مرحلة 3 الكل lr=1e-6. Grad-CAM: تصوير ما ركّز عليه CNN، أساسي للشرح الطبي.",
                    "duration": "65 دقيقة"
                },
                {
                    "title": "كشف الأجسام YOLO و SSD",
                    "content": "YOLO: تمريرة واحدة فقط → سريع! YOLOv8 (~80 FPS، 53% mAP). SSD: خرائط ميزات متعددة المقاييس. المقاييس: IoU=مساحة(تقاطع)/مساحة(اتحاد)، IoU>0.5 كشف صحيح. AP=مساحة تحت منحنى PR. mAP=متوسط AP لكل الفئات. NMS يحذف الصناديق المتكررة. كود: from ultralytics import YOLO; YOLO('yolov8n.pt')('img.jpg')[0].show()",
                    "duration": "70 دقيقة"
                },
                {
                    "title": "التجزئة الدلالية",
                    "content": "تجزئة الصور: فئة لكل بكسل. الأنواع: 1) الدلالية: فئة لكل بكسل (لا يميز مثيلين) 2) المثيلات: كل جسم منفرد 3) الشاملة (Panoptic): معيار القيادة الذاتية. U-Net (2015): بنية U مع skip connections، مشفر (downsampling) + فاك مشفر (upsampling)، ✅ ممتاز مع 100-200 صورة طبية. Mask R-CNN: Faster RCNN + فرع قناع، ✅ جودة عالية، ❌ بطيء (~5 FPS). DeepLab v3+: تلافيفات منتشرة للسياق متعدد المقاييس.",
                    "duration": "60 دقيقة"
                },
                {
                    "title": "توليد الصور GANs",
                    "content": "GANs: المولّد G (يأخذ ضوضاء z ويولّد صورة) والمميِّز D (يُميّز الحقيقي من المزيف) في منافسة. min_G max_D E[logD(x)]+E[log(1-D(G(z)))]. البنى: DCGAN (تلافيفات منقولة+BatchNorm)، StyleGAN NVIDIA2019 (وجوه واقعية=thispersondoesnotexist.com)، CycleGAN (نقل أسلوب بدون صور مقترنة: حصان↔حمار وحشي)، Conditional GAN (نص→صورة، pix2pix: رسم→صورة). التحديات: انهيار الوضع، عدم الاستقرار. التقييم: FID. التطبيقات: deepfakes، تعزيز البيانات الطبية، super-resolution.",
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
                    "content": "MDP الإطار الرياضي للتعلم المعزز. المكونات: S (حالات)، A (إجراءات)، P(s'|s,a) (انتقال)، R (مكافأة)، γ (خصم [0,1]). الهدف: G_t=R_t+γR_{t+1}+... (γ صغير→قصير النظر، γ كبير→بعيد النظر). دوال القيمة: V^π(s)=E[G_t|S_t=s] وQ^π(s,a)=E[G_t|S_t=s,A_t=a]. معادلة بيلمان: V^π(s)=Σ_a π(a|s)Σ_{s'} P(s'|s,a)[R+γV^π(s')]. السياسة المثلى: π*(s)=argmax_a Q*(s,a). معرفة Q* تعطي السياسة المثلى مباشرة!",
                    "duration": "55 دقيقة"
                },
                {
                    "title": "Q-Learning و SARSA",
                    "content": "Q-Learning: Q(s,a)←Q(s,a)+α[R+γ max Q(s',a')-Q(s,a)]. OFF-POLICY: يتعلم السياسة المثلى حتى أثناء الاستكشاف. SARSA: Q(s,a)←Q(s,a)+α[R+γQ(s',a')-Q(s,a)] (a' فعلي). ON-POLICY: أكثر تحفظاً. Epsilon-greedy: باحتمال ε إجراء عشوائي وإلا max Q (ε يتناقص). القيد: فضاء حالات صغير فقط. شبكة 4×4 ✅ | بكسلات Atari=10^100 حالة ✗ → نحتاج DQN!",
                    "duration": "60 دقيقة"
                },
                {
                    "title": "Deep Q-Networks DQN",
                    "content": "DQN تجمع Q-Learning مع الشبكات العصبية. Atari: 10^21000 حالة! Q(s,a;θ)≈Q*(s,a) بشبكة. 3 ابتكارات: 1) Experience Replay: تخزين (s,a,r,s') وأخذ عينات عشوائية يكسر الترابطات الزمنية. 2) Target Network θ⁻: ثابتة N خطوة للاستقرار. 3) Double DQN: الشبكة الرئيسية تختار، الهدف يُقيّم → يقلّل المبالغة. Dueling: Q(s,a)=V(s)+A(s,a). النتيجة التاريخية: مستوى الإنسان في 49 لعبة Atari من البكسلات الخام 2015!",
                    "duration": "65 دقيقة"
                },
                {
                    "title": "طرق تدرج السياسة",
                    "content": "طرق تدرج السياسة تتعلم السياسة π(a|s;θ) مباشرة دون المرور بدالة Q.\n\nلماذا تدرج السياسة؟\n  Q-Learning/DQN → يتعلم Q(s,a)، يشتق π* كـ argmax.\n  القيود:\n  → يتطلب فضاء إجراءات منفصل (كيف نحسب argmax على إجراءات مستمرة؟)\n  → لا يُمثّل السياسات العشوائية بشكل طبيعي\n  → صعب مع السياسات المُعامَلة القابلة للاشتقاق\n\n  تدرج السياسة: تعلّم θ بحيث π(a|s;θ) تُعظّم العائد G.\n  ✅ يعمل مع فضاءات الإجراءات المستمرة (الروبوتات!)\n  ✅ يتقارب إلى حد أدنى محلي (ضمانات نظرية)\n  ✅ يتعلم السياسات العشوائية بشكل طبيعي\n\nنظرية تدرج السياسة:\n  ∇_θ J(θ) = E[∇_θ log π(a|s;θ) × Q^π(s,a)]\n  → ∇_θ log π: كيف نغيّر θ لجعل الإجراء a أكثر/أقل احتمالاً\n  → Q^π(s,a): كم كان هذا الإجراء جيداً؟\n  → زيادة احتمالية الإجراءات التي أعطت مكافآت جيدة!\n\nخوارزمية REINFORCE:\n  1. العب حلقة كاملة بالسياسة π_θ\n  2. احسب العوائد G_t لكل خطوة\n  3. تحديث: θ ← θ + α × Σ_t [G_t × ∇_θ log π(a_t|s_t;θ)]\n\nالمشكلة: تباين عالٍ\n  G_t قد يتفاوت كثيراً بين الحلقات.\n  → عدم استقرار وتقارب بطيء.\n\nالحل: خط الأساس (Baseline)\n  طرح خط أساس b(s) لتقليل التباين دون انحياز:\n  ∇_θ J(θ) = E[∇_θ log π(a|s;θ) × (Q^π(s,a) - b(s))]\n\n  خطوط الأساس الشائعة:\n  → متوسط العوائد\n  → دالة القيمة V(s) → يؤدي إلى خوارزمية Actor-Critic!\n\nالميزة A(s,a) = Q(s,a) - V(s):\n  → > 0: هذا الإجراء كان أفضل من المتوسط\n  → < 0: هذا الإجراء كان أسوأ من المتوسط\n  → ≈ 0: هذا الإجراء كان نموذجياً",
                    "duration": "60 دقيقة"
                },
                {
                    "title": "Actor-Critic A2C و PPO",
                    "content": "Actor-Critic: ACTOR π(a|s;θ) + CRITIC V(s;φ). الميزة A(s,a)=R+γV(s')-V(s). Actor: θ←θ+α A ∇_θ logπ. TRPO: يضمن تحسناً رتيباً (KL≤δ) لكن صعب. PPO (OpenAI 2017) المعيار: r(θ)=π/π_old، L_CLIP=E[min(r×A, clip(r,1-ε,1+ε)×A)] (ε=0.1-0.2) → حد للتحديثات بدون تعقيد. ✅ OpenAI Five، AlphaGo، الروبوتات، RLHF (ChatGPT، Claude!). SAC: يعظّم المكافأة+الإنتروبيا → المعيار للتحكم المستمر.",
                    "duration": "70 دقيقة"
                },
                {
                    "title": "تطبيقات واقعية",
                    "content": "نجاحات: AlphaGo 2016 (هزم لي سيدول 4-1، MCTS+CNN+تعلم ذاتي)، AlphaStar 2019 (Grand Master في StarCraft II)، OpenAI Five 2019 (هزم OG في Dota 2 بـ5 وكلاء). الروبوتات: مشي وجري وقفز (SAC/PPO+محاكاة). Sim-to-Real: تدريب مجاني في محاكاة→نشر حقيقي (Domain Randomization). إدارة الطاقة: DeepMind خفّض تبريد Google بـ40%! التحديات: كفاءة العينات (DQN Atari=200M إطار=38 يوم بشري!)، السلامة، التعميم، إسناد الفضل.",
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
                    "content": "Pipelines scikit-learn تمنع تسرب البيانات وتربط الخطوات. pipe=Pipeline([('scaler',StandardScaler()),('clf',SVC())]); pipe.fit(X_train,y_train); pipe.predict(X_test). تحسين المعاملات الفائقة: 1) Grid Search: كل التركيبات (مضمون لكن بطيء). 2) Random Search: N تركيبة عشوائية (90% الأداء بـ10% الوقت). 3) Bayesian Optimization (Optuna): يوجّه البحث بالنتائج السابقة. 4) Halving Grid Search: يبدأ بمرشحين كثيرين ويُزيل الأضعف تدريجياً.",
                    "duration": "45 دقيقة"
                },
                {
                    "title": "إدارة إصدارات النماذج بـ MLflow",
                    "content": "MLflow: 4 مكونات. 1) Tracking: with mlflow.start_run(): log_param، log_metric، log_model → لوحة تحكم لمقارنة التشغيلات. 2) Projects: MLproject YAML، تشغيل محمول. 3) Models: تغليف عالمي (sklearn،pytorch،onnx)، النشر: mlflow models serve. 4) Registry: Staging→Production→Archived، انتقالات بموافقات+مقارنة تلقائية. Autologging: تسجيل تلقائي لكل المعاملات.",
                    "duration": "50 دقيقة"
                },
                {
                    "title": "الحاويات باستخدام Docker",
                    "content": "Docker يُغلّف النموذج ومتطلباته في حاوية محمولة. Dockerfile: FROM python:3.10-slim | WORKDIR /app | COPY requirements.txt . && RUN pip install -r requirements.txt | COPY app/ . && COPY model.pkl . | EXPOSE 8000 | CMD [uvicorn...]. Multi-stage Build: FROM builder→pip install → FROM slim→COPY --from=builder → يُقلّص من 5GB إلى 500MB! Docker Compose: api+redis في ملف واحد. أفضل الممارسات: .dockerignore، مستخدم غير جذر، Healthcheck، متغيرات البيئة.",
                    "duration": "55 دقيقة"
                },
                {
                    "title": "النشر باستخدام FastAPI",
                    "content": "FastAPI: سريع (مثل Go)، ASYNC، تحقق Pydantic تلقائي، Swagger تلقائي. مثال: app=FastAPI(); class Input(BaseModel): area: float; bedrooms: int; @app.on_event('startup') async def load(): app.state.model=pickle.load(...); @app.post('/predict') async def predict(inp: Input): X=np.array([[inp.area,inp.bedrooms]]); return {'price': float(app.state.model.predict(X)[0])}; @app.get('/health') async def health(): return {'status':'ok'}. النشر: uvicorn main:app --reload (تطوير) | gunicorn main:app -w 4 -k uvicorn.workers.UvicornWorker (إنتاج).",
                    "duration": "60 دقيقة"
                },
                {
                    "title": "المراقبة وكشف الانحراف",
                    "content": "المراقبة تكتشف تدهور النموذج. أنواع الانحراف: 1) انحراف البيانات: P(X) يتغير، الكشف: KS test، PSI. 2) انحراف المفهوم: P(Y|X) يتغير، الأصعب. 3) انحراف التنبؤ: توزيع المخرجات يتغير. 4) جودة البيانات: قيم فارغة، خارج النطاق. Evidently: Report(metrics=[DataDriftPreset()]).run(X_train,X_prod).save_html(). أدوات: WhyLabs، Arize، MLflow+Grafana. إعادة التدريب: مجدولة (أسبوعياً)، مُشغَّلة (عند انحراف)، Online Learning (مستمر).",
                    "duration": "55 دقيقة"
                },
                {
                    "title": "CI/CD للتعلم الآلي",
                    "content": "MLOps: أتمتة نشر نماذج التعلم الآلي. مستوى 0: يدوي (Notebooks، لا مراقبة). مستوى 1: خط أنابيب آلي (تدريب تلقائي). مستوى 2: CI/CD (اختبارات+نشر+مراقبة+إعادة تدريب آلي). GitHub Actions: test_data.py→train.py→validate.py→docker build→kubectl apply. أنواع الاختبارات: بيانات (Great Expectations)، كود (pytest)، نموذج (الأداء>عتبة)، API (كمون<200ms). المنصات: Kubeflow (K8s)، SageMaker (AWS)، Azure ML، Vertex AI، W&B. Feature Store: Feast، Tecton، Hopsworks.",
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

        # Groq API Key input in sidebar - PROMINENT VERSION
        st.markdown(f"""
        <div style="background: rgba(102,126,234,0.15); border: 1px solid rgba(102,126,234,0.3); 
                    border-radius: 12px; padding: 12px; margin: 8px 0;">
            <div style="color: #667eea; font-size: 12px; font-weight: 600; margin-bottom: 6px;">
                🔑 {t['groq_key_label']}
            </div>
        </div>
        """, unsafe_allow_html=True)

        current_key = st.session_state.get("groq_api_key", "")

        # Use a visible text input with label
        new_key = st.text_input(
            "API Key", 
            value=current_key, 
            type="password",
            placeholder="gsk_xxxxxxxxxxxxxxxxxxxxxxxx",
            key="groq_key_input",
            label_visibility="collapsed"
        )

        col_save, col_clear = st.columns(2)
        with col_save:
            if st.button("💾 Save", key="save_api_key", use_container_width=True):
                if new_key != current_key:
                    st.session_state.groq_api_key = new_key
                    st.success("✅ Key saved!" if lang != "ar" else "✅ تم حفظ المفتاح!")
                    st.rerun()
                else:
                    st.info("No changes" if lang != "ar" else "لا توجد تغييرات")

        with col_clear:
            if st.button("🗑️ Clear", key="clear_api_key", use_container_width=True):
                st.session_state.groq_api_key = ""
                st.success("Cleared!" if lang != "ar" else "تم المسح!")
                st.rerun()

        st.markdown(f"<div style='color: #888; font-size: 10px; margin: 8px 0;'>{t['groq_key_help']}</div>", unsafe_allow_html=True)

        # Show mentor status with visual indicator
        mentor = CloudAIClient()
        if mentor.is_available:
            st.markdown(f"""
            <div style="background: rgba(76,175,80,0.15); border: 1px solid rgba(76,175,80,0.3); 
                        border-radius: 8px; padding: 8px; margin: 8px 0; text-align: center;">
                <div style="color: #4CAF50; font-size: 12px; font-weight: 600;">
                    🟢 {t['mentor_online']}
                </div>
            </div>
            """, unsafe_allow_html=True)
        else:
            st.markdown(f"""
            <div style="background: rgba(255,152,0,0.15); border: 1px solid rgba(255,152,0,0.3); 
                        border-radius: 8px; padding: 8px; margin: 8px 0; text-align: center;">
                <div style="color: #FF9800; font-size: 12px; font-weight: 600;">
                    🟡 {t['mentor_demo']}
                </div>
            </div>
            """, unsafe_allow_html=True)

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
        st.markdown(f"""
        <div style="background: rgba(76,175,80,0.1); border-left: 4px solid #4CAF50; 
                    padding: 12px; margin: 8px 0; border-radius: 0 8px 8px 0;">
            <div style="color: #4CAF50; font-size: 14px; font-weight: 600;">
                🟢 {t['mentor_online']}
            </div>
        </div>
        """, unsafe_allow_html=True)
    else:
        st.markdown(f"""
        <div style="background: rgba(255,152,0,0.1); border-left: 4px solid #FF9800; 
                    padding: 12px; margin: 8px 0; border-radius: 0 8px 8px 0;">
            <div style="color: #FF9800; font-size: 14px; font-weight: 600; margin-bottom: 8px;">
                🟡 {t['mentor_demo']}
            </div>
            <div style="color: #666; font-size: 12px; line-height: 1.5;">
                {t['groq_key_help']}
            </div>
            <div style="margin-top: 8px;">
                <a href="https://console.groq.com" target="_blank" 
                   style="color: #667eea; text-decoration: none; font-size: 12px; font-weight: 600;">
                   🔗 Get Free API Key →
                </a>
            </div>
        </div>
        """, unsafe_allow_html=True)

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
        st.markdown(f"""
        <div style="background: rgba(76,175,80,0.1); border: 1px solid rgba(76,175,80,0.3); 
                    padding: 12px; margin: 8px 0 16px 0; border-radius: 8px; text-align: center;">
            <div style="color: #4CAF50; font-size: 14px; font-weight: 600;">
                🟢 {t['mentor_online']}
            </div>
        </div>
        """, unsafe_allow_html=True)
    else:
        st.markdown(f"""
        <div style="background: rgba(255,152,0,0.1); border: 1px solid rgba(255,152,0,0.3); 
                    padding: 12px; margin: 8px 0 16px 0; border-radius: 8px; text-align: center;">
            <div style="color: #FF9800; font-size: 14px; font-weight: 600; margin-bottom: 8px;">
                🟡 {t['mentor_demo']}
            </div>
            <div style="color: #666; font-size: 12px; margin-bottom: 8px;">
                {t['groq_key_help']}
            </div>
            <a href="https://console.groq.com" target="_blank" 
               style="color: #667eea; text-decoration: none; font-size: 12px; font-weight: 600;">
               🔗 Get Free API Key →
            </a>
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
