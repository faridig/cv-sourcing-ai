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
- **Prompt Engineering RH** : L'utilisation de Structured Outputs (OpenAI `parse`) garantit une cohérence parfaite entre l'analyse IA et le modèle de données Pydantic, évitant les erreurs de format JSON.
- **Fiabilité des Soft Skills** : Le passage de scores numériques arbitraires à une extraction de preuves textuelles (ex: "A animé...") rend l'analyse RH auditable et moins sujette aux biais.
- **Chain of Thought (CoT) pour les Dates** : Forcer l'IA à lister explicitement les mois de début et de fin résout les hallucinations classiques sur les chevauchements d'expériences.
- **Filtrage de la Pollution Visuelle** : L'IA a été instruite pour ignorer les fautes d'orthographe sur les noms propres et les technologies, se concentrant uniquement sur la qualité rédactionnelle humaine.
- **Augmentation Multi-axes** : La structuration en 8 axes stratégiques prépare le terrain pour un RAG (Retrieval Augmented Generation) ultra-précis lors de la phase de sourcing.
