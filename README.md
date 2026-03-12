# CV Opti - Sourcing RH IA

Ce projet est un moteur de sourcing RH assisté par IA, utilisant FastAPI pour le backend, React pour le frontend, MinIO pour le stockage de documents et Qdrant pour la recherche vectorielle.

## 🚀 Installation Rapide

### 1. Pré-requis
- Docker et Docker Compose
- Python 3.10+
- Node.js & npm

### 2. Configuration
Copiez le fichier d'exemple des variables d'environnement et ajustez-le si nécessaire :
```bash
cp .env.example .env
```

### 3. Lancer les services (MinIO, Qdrant)
```bash
docker compose up -d
```

### 4. Backend
```bash
cd backend
python -m venv venv
source venv/bin/activate
pip install -r requirements.txt
uvicorn app.main:app --reload
```
Le backend est disponible sur [http://localhost:8000](http://localhost:8000).
La documentation Swagger est sur [http://localhost:8000/docs](http://localhost:8000/docs).

### 5. Frontend
```bash
cd frontend
npm install
npm run dev
```
Le frontend est disponible sur [http://localhost:5173](http://localhost:5173).

## ✅ Tests
Pour lancer les tests du backend :
```bash
PYTHONPATH=backend pytest backend/tests
```

## 🏗️ Architecture
- **Backend** : FastAPI (Python)
- **Frontend** : React / Vite (TypeScript)
- **Vector DB** : Qdrant
- **Object Storage** : MinIO
