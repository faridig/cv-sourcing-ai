# 🎯 VISION DU PROJET : Dashboard RH - Sourcing IA Local

Un outil 100% local, souverain et sécurisé, destiné aux professionnels des Ressources Humaines. L'objectif est d'analyser un lot de CV (PDF), d'en extraire le sens avec une intelligence artificielle (LLM) et de les classer selon une offre d'emploi donnée, avec un dashboard d'aide à la décision hautement visuel et interactif.

---

# ⚙️ CONFIGURATION TECHNIQUE

*   **Type de projet** : Application Web Full-stack (Outil de Matching Intelligent / Dashboard Unique).
*   **Architecture** : Locale (Dockerisée pour un déploiement instantané).
*   **Langage Principal** : Python 3.11+.
*   **Framework Backend** : FastAPI (Asynchrone, performant, typage fort).
*   **Framework Frontend** : React (Vite) + Tailwind CSS + Recharts (Pour les graphiques Radar) + Web Speech API (Microphone natif).
*   **Parsing PDF** : PyMuPDF (Extraction rapide du texte brut).
*   **Structuration & Analyse IA** : OpenAI API (Modèles : `gpt-4o-mini` pour le texte, `whisper-1` pour la voix si nécessaire, ou l'API Web Speech native du navigateur).
*   **Stockage de Fichiers (CV)** : MinIO (S3-compatible, hébergé localement).
*   **Base de Données Vectorielle** : Qdrant (Recherche sémantique, hébergée localement).

---

# 🏛️ JOURNAL DES DÉCISIONS (ADR)

*   **Décision 1** : Utilisation de `gpt-4o-mini` pour transformer le texte brut issu de `PyMuPDF` en Markdown propre avec métadonnées.
*   **Décision 2** : Utilisation de MinIO en local pour stocker les PDF originaux afin de garantir la confidentialité des données RH.
*   **Décision 3** : Le scoring n'est plus un simple chiffre, mais une évaluation multi-critères (Radar "Culture Fit") générée par l'IA.
*   **Décision 4** : Interface en "Dashboard Unique" (Single Page Application) pour éviter les rechargements de page.
*   **Décision 5** : L'expérience de "Chat avec le CV" se fera par la voix (Speech-to-Text) pour une ergonomie maximale pour le recruteur.
*   **Décision 6 (Méthodologie)** : Adoption du modèle "Single-Piece Flow" : **1 seul ticket (PBI) par Sprint**. Cela garantit une maîtrise parfaite, une livraison continue et minimise les risques de régression technique.

---

# ✅ DEFINITION OF DONE (DoD)

Pour chaque ticket du Sprint Plan, le Lead-Dev ou l'UX doit valider :
*   [ ] **Qualité** : Le code est propre, formaté (Black/Ruff pour Python, Prettier pour JS) et typé (MyPy / TypeScript).
*   [ ] **Sécurité** : AUCUN secret en dur (clés API). Présence d'un `.env.example`.
*   [ ] **Testabilité** : Les dépendances permettent un lancement local immédiat (`docker compose up`).
*   [ ] **Documentation** : Le README est à jour.
*   [ ] **Fonctionnel** : Le ticket répond strictement aux critères d'acceptation (Gherkin).

---

# 📋 BACKLOG GLOBAL (EPICS & PBI)

## Epic 1 : Squelette & Infrastructure DevOps
*   **[DONE]** **[PBI-000]** Initialisation du projet (Walking Skeleton), Docker Compose (Qdrant, MinIO), squelettes FastAPI et React.

## Epic 2 : Ingestion et Intelligence Profonde (Parsing) (Sprint 1 - En Cours)
*   **[PBI-001]** Endpoint d'Upload : Envoyer un PDF, le stocker dans MinIO.
*   **[PBI-002]** Pipeline de Parsing : Extraire le texte brut via PyMuPDF.
*   **[PBI-003]** Structuration IA & Extraction des "Soft Skills Latentes" : L'IA lit les missions, déduit les compétences non écrites (ex: "A organisé un salon de 500p" -> "Gestion de projet événementiel"), et génère le Markdown structuré avec ces métadonnées enrichies.
*   **[PBI-004]** Vectorisation : Convertir le Markdown enrichi en embeddings et les insérer dans Qdrant.

## Epic 3 : Moteur de Recherche RH et Radar Multi-critères
*   **[PBI-005]** Endpoint Sourcing : Prendre une annonce en input, chercher les Top 20 vecteurs les plus proches dans Qdrant.
*   **[PBI-006]** Évaluation IA (Radar) : Pour le Top 20, l'IA compare le CV et l'annonce sur 4 axes : Hard Skills, Séniorité, Secteur, Autonomie. Le backend renvoie ces 4 scores distincts et un avis textuel.

## Epic 4 : L'Interface (Dashboard Wow Effect)
*   **[PBI-007]** Maquette UX/UI : Définition du Dashboard (Stratégie UX).
*   **[PBI-008]** Zone de Dépôt (Drag & Drop) pour les CV et formulaire d'Annonce.
*   **[PBI-009]** Affichage des Résultats : Liste des candidats avec leurs badges de "Soft Skills Latentes" déduites par l'IA.
*   **[PBI-010]** Visualisation du Score : Intégration d'un composant Graphique en Radar (Recharts) pour comparer l'offre et le candidat sur les 4 axes évalués.

## Epic 5 : "L'Agent Recruteur" (Interactivité Vocale)
*   **[PBI-011]** Fenêtre de Chat Contextuel : Lorsqu'un recruteur clique sur un profil, un panneau latéral s'ouvre pour discuter spécifiquement de ce CV (RAG ciblé sur 1 document).
*   **[PBI-012]** Intégration Speech-to-Text : Le recruteur maintient un bouton "Micro" dans le chat, sa voix est transcrite en texte (via l'API native du navigateur ou `whisper-1` d'OpenAI) et envoyée comme question à l'IA concernant le CV ouvert.

## Epic 6 : Observabilité IA & Métriques (Dashboard Admin)
*   **[PBI-013]** Télémétrie "Human-in-the-Loop" : Ajouter un bouton "Shortlisté / Rejeté" (ou un simple 👍/👎 sur l'avis de l'IA) sur chaque CV dans les résultats pour recueillir le feedback réel des recruteurs.
*   **[PBI-014]** Dashboard Administrateur : Vue simple avec 3 indicateurs clés de performance (KPI) du RAG :
    *   *Taux d'Adéquation (Precision)* : Le nombre de profils proposés par l'IA qui ont été effectivement ouverts ou "shortlistés" par un humain.
    *   *Temps moyen de parsing* : Durée de traitement pour un lot de CV (pour surveiller les coûts et la performance locale).
    *   *Signalements "Hallucination"* : Un compteur des fois où le recruteur a signalé que l'IA avait inventé une compétence (via le bouton 👎).