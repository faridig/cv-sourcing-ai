# 📜 CHANGELOG

L'historique des modifications apportées au projet, classé par Sprints et par Version.

## [Unreleased]

### Added
- Infrastructure locale via Docker Compose (MinIO, Qdrant).
- Squelette Backend FastAPI avec point de terminaison `/api/health`.
- Squelette Frontend React/Vite (TypeScript).
- Makefile pour automatiser le setup et les tests.

## 💡 LEÇONS APPRISES

### Sprint 1
- Le Lead-Dev a géré efficacement l'intégration de MinIO avec `boto3`.
- La double validation (MIME type + extension) renforce la sécurité de l'upload.
- L'utilisation de `python-multipart` est indispensable pour gérer les fichiers avec FastAPI, un oubli classique qui a été évité ici.
- L'automatisation de la création du bucket dans le code de stockage simplifie le déploiement.
- Pour les prochains tickets, conserver cette approche de "Single-Piece Flow" qui permet une validation technique très granulaire.
