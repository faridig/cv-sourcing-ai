# 🚀 SPRINT EN COURS : Sprint 0 (Walking Skeleton)

**Objectif du Sprint** : Mettre en place les fondations techniques du projet (Base de données, Stockage, Backend, Frontend) pour que le développement fonctionnel puisse démarrer sereinement. 

---

### [PBI-000] Initialisation de l'Infrastructure (Docker & Services)
**Priorité** : High | **Estimation** : M

**User Story** : "En tant que Développeur, je veux une infrastructure locale conteneurisée (MinIO, Qdrant) et un squelette Back/Front qui communiquent, afin de commencer à coder la logique métier sans me soucier de l'environnement."

**Dépendances** : Aucune

**Critères d'Acceptation (Gherkin)** :
- [ ] **Scenario 1** : Lancement de l'environnement complet
  - **GIVEN** Un développeur vient de cloner le projet
  - **WHEN** Il exécute `docker compose up -d` (ou commande équivalente documentée dans un `Makefile`/`README`)
  - **THEN** Les conteneurs pour MinIO et Qdrant démarrent sans erreur sur leurs ports par défaut respectifs.

- [ ] **Scenario 2** : Squelette Backend (FastAPI)
  - **GIVEN** Le backend FastAPI est lancé (via Uvicorn/Docker)
  - **WHEN** Je fais un GET sur `/api/health`
  - **THEN** Je reçois une réponse JSON `{"status": "ok", "message": "Le moteur de Sourcing RH est prêt."}`.

- [ ] **Scenario 3** : Squelette Frontend (React/Vite)
  - **GIVEN** Le frontend React est lancé
  - **WHEN** J'accède à `http://localhost:5173` (ou port par défaut Vite)
  - **THEN** Je vois un titre "Dashboard RH - Sourcing IA" et l'interface s'affiche sans erreur console.

- [ ] **Scenario 4** : Sécurité des secrets
  - **GIVEN** Le projet nécessite des clés (OpenAI, MinIO admin/password)
  - **WHEN** Je regarde à la racine du projet
  - **THEN** Un fichier `.env.example` est présent et documente clairement les variables requises (OPENAI_API_KEY, MINIO_ROOT_USER, MINIO_ROOT_PASSWORD, etc.).

- [ ] **Scenario 5** : Documentation minimale
  - **GIVEN** Le squelette est en place
  - **WHEN** Je lis le `README.md`
  - **THEN** J'y trouve les instructions claires pour lancer le projet (Front, Back, et Services) et configurer le `.env`.