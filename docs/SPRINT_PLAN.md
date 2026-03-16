# 🚀 SPRINT EN COURS : Sprint 3 (Intelligence Latente & Augmentation)

**Objectif du Sprint** : Transformer le texte brut des CV en dossiers structurés "augmentés" selon 8 axes d'analyse RH pour optimiser le matching IA.

---

### [PBI-003] Structuration IA & Intelligence Latente (8 Axes)
**Priorité** : High | **Estimation** : M

**User Story** : "En tant que Système, je veux soumettre le texte extrait par Docling à un LLM avec un prompt d'expert RH, afin de générer une fiche candidat augmentée (Markdown) et des métadonnées (JSON) couvrant 8 axes d'analyse."

**Les 8 Axes à extraire** :
1. Dynamique de Carrière (Séniorité/Progression)
2. Culture Fit (Startup/Grand Compte/Agile)
3. Rayonnement (Open Source/Side Projects/Engagement)
4. Langues (Usage contextuel)
5. Soft Skills (Scores 0-10 sur Leadership, Autonomie, etc.)
6. Stack Technologique Hiérarchisée (Main/Secondary/Veille)
7. Mobilité & Télétravail
8. Signaux Faibles (Audit de cohérence par l'IA)

**Critères d'Acceptation (Gherkin)** :
- [ ] **Scenario 1** : Génération de la fiche augmentée
  - **GIVEN** Un texte structuré issu de Docling (PBI-002)
  - **WHEN** Le service d'analyse IA traite le texte
  - **THEN** Un fichier Markdown est généré suivant le template "Dossier Augmenté".
  - **AND** Les 8 axes sont présents et documentés.

- [ ] **Scenario 2** : Préparation des métadonnées pour Qdrant
  - **GIVEN** Un CV analysé
  - **WHEN** Le système prépare l'objet final
  - **THEN** Un objet JSON contenant les scores et les tags (Payload) est créé parallèlement au Markdown.

- [ ] **Scenario 3** : Robustesse du prompt
  - **GIVEN** Un CV très court ou incomplet
  - **WHEN** L'IA tente l'analyse
  - **THEN** L'IA ne doit pas inventer d'informations (hallucination) mais marquer l'axe comme "Non déterminé" ou "Données insuffisantes".

- [ ] **Scenario 4** : Gestion des coûts et tokens
  - **GIVEN** L'utilisation de GPT-4o-mini
  - **WHEN** L'appel API est effectué
  - **THEN** Le prompt doit être optimisé pour minimiser la consommation de tokens tout en respectant la structure de sortie.
