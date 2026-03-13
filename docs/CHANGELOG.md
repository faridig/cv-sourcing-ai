# 📜 CHANGELOG

L'historique des modifications apportées au projet, classé par Sprints et par Version.

## [Unreleased]

### Added
- Pipeline de Parsing haute fidélité via Docling (`/api/cv/parse/{file_id}`). (Sprint 2)
- Endpoint d'Upload vers MinIO (`/api/cv/upload`) avec validation PDF. (Sprint 1)
- Infrastructure locale via Docker Compose (MinIO, Qdrant).
- Squelette Backend FastAPI avec point de terminaison `/api/health`.
- Squelette Frontend React/Vite (TypeScript).
- Makefile pour automatiser le setup et les tests.

## 💡 LEÇONS APPRISES

### Sprint 1
- Le Lead-Dev a géré efficacement l'intégration de MinIO avec `boto3`.
- La double validation (MIME type + extension) renforce la sécurité de l'upload.
- L'utilisation de `python-multipart` est indispensable pour gérer les fichiers avec FastAPI.
- **Isolation des tests** : Utilisation de fixtures pytest pour nettoyer le stockage MinIO, garantissant des tests reproductibles.
- **Industrialisation** : Création de `make seed` et `make clean-storage` pour faciliter la démo.

### Sprint 2
- **Pivot Technologique** : Passage de PyMuPDF à **Docling (IBM)**. Ce choix améliore radicalement l'extraction des CV multi-colonnes, réduisant le risque de "mélange sémantique" pour l'IA.
- **Poids des Dépendances** : Docling est une librairie puissante mais lourde (Torch). Il est crucial de monitorer l'espace disque et la mémoire en environnement local.
- **Mocking Stratégique** : L'utilisation de mocks pour Docling dans les tests unitaires permet de valider la logique API sans subir les temps de calcul du modèle.
- **Observabilité & Diagnostic** : L'audit a révélé l'importance de ne pas masquer les erreurs d'importation sur les dépendances critiques. L'ajout de logs d'exception (`logger.exception`) et d'un test d'intégrité de dépendance assure une maintenance simplifiée.
- **Gestion Fine des Erreurs S3** : L'utilisation de `ClientError` (404) permet désormais de distinguer un fichier manquant d'une panne serveur, améliorant l'expérience utilisateur finale.

### Sprint 3
- **Structuration IA via 8 Axes** : L'utilisation de Pydantic V2 pour typer les retours de l'IA garantit une intégrité totale des données avant l'insertion en base vectorielle.
- **Robustesse des Prompts** : L'introduction d'un séparateur explicite (`---MARKDOWN---`) et de fallbacks de nettoyage de code blocks JSON permet de compenser les variabilités de formatage des LLM.
- **Hygiène Technique (Lifespan)** : La migration vers `lifespan` (FastAPI) a permis de supprimer des avertissements d'obsolescence et de centraliser la gestion des ressources (Analyzer).
- **Consistance des Environnements de Test** : Le Lead-Dev a dû harmoniser les imports (`app` vs `backend.app`) pour assurer la compatibilité entre l'exécution locale et la CI GitHub Actions. Une racine de projet mal définie peut paralyser les automates de test.
