# 📜 CHANGELOG

L'historique des modifications apportées au projet, classé par Sprints et par Version.

## [Unreleased]

### Added
- Infrastructure locale via Docker Compose (MinIO, Qdrant).
- Squelette Backend FastAPI avec point de terminaison `/api/health`.
- Squelette Frontend React/Vite (TypeScript).
- Makefile pour automatiser le setup et les tests.

## 💡 LEÇONS APPRISES

### Sprint 0
- Le Lead-Dev a correctement structuré les environnements, facilitant le lancement via le Makefile. 
- Attention à la configuration du PYTHONPATH pour le backend lors des tests locaux (nécessite d'inclure le dossier `app`).
- L'utilisation de `uvicorn` en direct nécessite une bonne gestion des chemins de modules.
- L'infrastructure Docker est robuste mais nécessite une vérification manuelle des ports au premier lancement.