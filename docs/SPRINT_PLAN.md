# 🚀 SPRINT EN COURS : Sprint 2 (Pipeline de Parsing haute fidélité)

**Objectif du Sprint** : Extraire le texte des PDF stockés dans MinIO en respectant la mise en page (colonnes, titres) grâce à Docling.

*(Règle méthodologique : Un seul PBI par Sprint pour une livraison continue et maîtrisée)*

---

### [CHORE] Dette Technique : Nettoyage du Git Cache
**Priorité** : Critical | **Estimation** : XS
**Tâche préalable obligatoire pour le Lead-Dev avant de commencer le PBI-002.**
- Exécuter la commande `git rm -r --cached .opencode openrtk` pour retirer ces dossiers du suivi Git (ils avaient été poussés lors d'un sprint précédent avant d'être ajoutés au `.gitignore`).
- Commiter cette correction (`fix(git): nettoyage du cache des dossiers ignorés`).

---

### [PBI-002] Pipeline de Parsing (Extraction haute fidélité via Docling)
**Priorité** : High | **Estimation** : S

**User Story** : "En tant que Système, je veux extraire le texte d'un fichier PDF (récupéré depuis MinIO) en conservant la structure logique du document (colonnes, hiérarchie) grâce à Docling, afin de faciliter l'analyse ultérieure par l'IA."

**Dépendances** : [PBI-001] (Upload MinIO)

**Critères d'Acceptation (Gherkin)** :
- [ ] **Scenario 1** : Extraction structurée réussie
  - **GIVEN** L'ID ou le chemin d'un PDF valide stocké dans MinIO
  - **WHEN** Le système (backend) appelle le service de parsing avec cet ID
  - **THEN** Le PDF est récupéré depuis MinIO
  - **AND** **Docling** l'analyse et retourne une représentation Markdown ou texte qui respecte l'ordre de lecture des colonnes.

- [ ] **Scenario 2** : Performance et Robustesse
  - **GIVEN** Un CV avec une mise en page complexe (2 ou 3 colonnes)
  - **WHEN** Docling traite le fichier
  - **THEN** Le texte extrait ne mélange pas les lignes des colonnes adjacentes.

- [ ] **Scenario 3** : Gestion des erreurs
  - **GIVEN** Un fichier PDF corrompu
  - **WHEN** Le système tente de l'extraire
  - **THEN** Une exception propre est levée et journalisée.