# 🚀 SPRINT EN COURS : Sprint 1 (Endpoint d'Upload)

**Objectif du Sprint** : Assurer la réception et le stockage sécurisé d'un PDF, ce qui est la porte d'entrée incontournable de tout le système.

*(Règle méthodologique : Un seul PBI par Sprint pour une livraison continue et maîtrisée)*

---

### [PBI-001] Endpoint d'Upload vers MinIO
**Priorité** : High | **Estimation** : S

**User Story** : "En tant que Système, je veux recevoir un fichier PDF via une API REST et le stocker en sécurité dans MinIO pour pouvoir le réafficher plus tard à l'utilisateur."

**Dépendances** : [PBI-000] (Infrastructure)

**Critères d'Acceptation (Gherkin)** :
- [ ] **Scenario 1** : Upload d'un fichier valide
  - **GIVEN** Le service backend et MinIO tournent
  - **WHEN** Je fais un POST sur `/api/cv/upload` avec un fichier au format PDF
  - **THEN** Le fichier est sauvegardé dans un bucket MinIO (ex: "resumes")
  - **AND** L'API me renvoie un code 200 avec l'ID unique ou le chemin du fichier stocké (ex: `{"id": "uuid-v4", "filename": "cv.pdf", "path": "resumes/uuid-v4.pdf"}`).

- [ ] **Scenario 2** : Rejet d'un fichier invalide
  - **GIVEN** Le service backend est prêt
  - **WHEN** Je fais un POST sur `/api/cv/upload` avec un fichier qui n'est pas un PDF (ex: une image ou un `.docx`)
  - **THEN** L'API rejette l'envoi
  - **AND** Elle renvoie un code d'erreur HTTP 400 avec un message clair : "Seuls les fichiers PDF sont acceptés."