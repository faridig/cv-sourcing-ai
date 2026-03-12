# 🚀 SPRINT EN COURS : Sprint 2 (Pipeline de Parsing)

**Objectif du Sprint** : Extraire le texte brut des PDF stockés dans MinIO.

*(Règle méthodologique : Un seul PBI par Sprint pour une livraison continue et maîtrisée)*

---

### [CHORE] Dette Technique : Nettoyage du Git Cache
**Priorité** : Critical | **Estimation** : XS
**Tâche préalable obligatoire pour le Lead-Dev avant de commencer le PBI-002.**
- Exécuter la commande `git rm -r --cached .opencode openrtk` pour retirer ces dossiers du suivi Git (ils avaient été poussés lors d'un sprint précédent avant d'être ajoutés au `.gitignore`).
- Commiter cette correction (`fix(git): nettoyage du cache des dossiers ignorés`).

---

### [PBI-002] Pipeline de Parsing (Extraction de texte brute)
**Priorité** : High | **Estimation** : S

**User Story** : "En tant que Système, je veux extraire tout le texte d'un fichier PDF (récupéré depuis MinIO) de manière rapide et brute pour le préparer à l'analyse IA."

**Dépendances** : [PBI-001] (Upload MinIO)

**Critères d'Acceptation (Gherkin)** :
- [ ] **Scenario 1** : Extraction de texte réussie
  - **GIVEN** L'ID ou le chemin d'un PDF valide stocké dans MinIO (suite au PBI-001)
  - **WHEN** Le système (backend) appelle le service de parsing avec cet ID
  - **THEN** Le PDF est récupéré depuis MinIO
  - **AND** `PyMuPDF` (`fitz`) l'analyse et retourne une chaîne de caractères (string) contenant tout le texte du CV.

- [ ] **Scenario 2** : Gestion des erreurs de lecture
  - **GIVEN** Un PDF corrompu ou illisible
  - **WHEN** Le système tente de l'extraire
  - **THEN** Une exception propre est levée et journalisée, évitant le crash complet du système.