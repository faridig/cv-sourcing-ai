# 🚀 SPRINT EN COURS : Sprint 1 (Ingestion et Intelligence Profonde)

**Objectif du Sprint** : Mettre en place la mécanique de lecture des PDF et leur transformation en données intelligentes et structurées, avant de les envoyer dans la base vectorielle.

---

### [PBI-001] Endpoint d'Upload vers MinIO
**Priorité** : High | **Estimation** : S

**User Story** : "En tant que Système, je veux recevoir un fichier PDF via une API REST et le stocker en sécurité dans MinIO pour pouvoir le réafficher plus tard à l'utilisateur."

**Dépendances** : [PBI-000]

**Critères d'Acceptation (Gherkin)** :
- [ ] **Scenario 1** : Upload d'un CV
  - **GIVEN** Le service backend et MinIO tournent
  - **WHEN** Je fais un POST sur `/api/cv/upload` avec un fichier PDF
  - **THEN** Le fichier est sauvegardé dans un bucket MinIO "resumes" et l'API renvoie l'ID/Chemin du fichier stocké.

---

### [PBI-002] Pipeline de Parsing (Extraction de texte brute)
**Priorité** : High | **Estimation** : S

**User Story** : "En tant que Système, je veux extraire tout le texte d'un fichier PDF (récupéré depuis MinIO) de manière rapide et brute pour le préparer à l'analyse IA."

**Dépendances** : [PBI-001]

**Critères d'Acceptation (Gherkin)** :
- [ ] **Scenario 1** : Extraction de texte
  - **GIVEN** Un PDF valide stocké dans MinIO
  - **WHEN** Le pipeline déclenche l'extraction via PyMuPDF
  - **THEN** Je récupère une chaîne de caractères (string) contenant tout le texte du CV de manière lisible.

---

### [PBI-003] Structuration IA & Extraction des "Soft Skills Latentes"
**Priorité** : High | **Estimation** : M

**User Story** : "En tant que Système, je veux envoyer le texte brut à l'IA pour qu'elle le nettoie en Markdown, qu'elle isole les données de contact, et qu'elle déduise des compétences non explicites à partir des missions décrites."

**Dépendances** : [PBI-002]

**Critères d'Acceptation (Gherkin)** :
- [ ] **Scenario 1** : Nettoyage et enrichissement
  - **GIVEN** Une chaîne de texte brute issue d'un CV
  - **WHEN** Je l'envoie à l'API OpenAI (`gpt-4o-mini`) avec le prompt d'analyse approprié
  - **THEN** Je reçois un objet JSON standardisé contenant au minimum : `{"contact_info": {...}, "markdown_content": "...", "latent_soft_skills": ["...", "..."]}`.

---

### [PBI-004] Vectorisation (Intégration Qdrant)
**Priorité** : High | **Estimation** : M

**User Story** : "En tant que Système, je veux transformer le Markdown structuré en vecteur mathématique et l'insérer dans Qdrant avec ses métadonnées, pour pouvoir le rechercher par la suite."

**Dépendances** : [PBI-003]

**Critères d'Acceptation (Gherkin)** :
- [ ] **Scenario 1** : Stockage vectoriel
  - **GIVEN** L'objet JSON contenant le CV analysé (PBI-003)
  - **WHEN** Je demande la génération d'embeddings (via OpenAI ou local) et l'insertion dans Qdrant
  - **THEN** Qdrant confirme l'insertion du vecteur avec les métadonnées (ID MinIO, Soft Skills, etc.) associées.