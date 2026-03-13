import uuid
import os
import tempfile
import logging
from fastapi import FastAPI, UploadFile, File, HTTPException
from botocore.exceptions import ClientError
from .storage import upload_file, download_file
from .parser import parse_pdf, DOCLING_AVAILABLE
from .analyzer import CVAnalyzer

# Configuration du logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

app = FastAPI(title="Sourcing RH API")

# Instance globale de l'analyzer
analyzer = None

@app.on_event("startup")
async def startup_event():
    """
    Diagnostic au démarrage pour vérifier les dépendances critiques.
    """
    global analyzer
    logger.info("Démarrage du serveur Sourcing RH...")
    if DOCLING_AVAILABLE:
        logger.info("Diagnostic : Docling est disponible.")
    else:
        logger.error("Diagnostic : Docling est INDISPONIBLE. Le parsing de CV ne fonctionnera pas.")
    
    try:
        analyzer = CVAnalyzer()
        logger.info("Diagnostic : Analyzer IA initialisé.")
    except Exception as e:
        logger.warning(f"Diagnostic : Analyzer IA non initialisé (OPENAI_API_KEY manquante ?) : {str(e)}")

@app.get("/api/health")
async def health_check():
    return {"status": "ok", "message": "Le moteur de Sourcing RH est prêt."}

@app.post("/api/cv/analyze/{file_id}")
async def analyze_cv_endpoint(file_id: str):
    """
    Extrait le texte via Docling et l'analyse via l'IA pour générer un dossier augmenté.
    """
    if not analyzer:
        raise HTTPException(status_code=503, detail="Service d'analyse IA non configuré.")

    object_name = f"{file_id}.pdf"
    with tempfile.NamedTemporaryFile(delete=False, suffix=".pdf") as tmp_file:
        tmp_path = tmp_file.name
    
    try:
        download_file(object_name, tmp_path)
        markdown_text = parse_pdf(tmp_path)
        
        analysis_data, augmented_markdown = analyzer.analyze_cv(markdown_text)
        
        return {
            "id": file_id,
            "analysis": analysis_data,
            "dossier_markdown": augmented_markdown
        }
    except Exception as e:
        logger.exception(f"Erreur lors de l'analyse du CV {file_id}")
        raise HTTPException(status_code=500, detail=str(e))
    finally:
        if os.path.exists(tmp_path):
            os.remove(tmp_path)

@app.post("/api/cv/upload")
async def upload_cv(file: UploadFile = File(...)):
    if file.content_type != "application/pdf":
        raise HTTPException(status_code=400, detail="Seuls les fichiers PDF sont acceptés.")
    
    file_id = str(uuid.uuid4())
    filename = file.filename or "unnamed.pdf"
    
    # Simple check for extension if filename is present
    if not filename.lower().endswith(".pdf"):
         raise HTTPException(status_code=400, detail="Seuls les fichiers PDF sont acceptés.")

    object_name = f"{file_id}.pdf"
    
    content = await file.read()
    storage_path = upload_file(content, object_name)
    
    return {
        "id": file_id,
        "filename": filename,
        "path": storage_path
    }

@app.post("/api/cv/parse/{file_id}")
async def parse_cv(file_id: str):
    """
    Récupère un CV depuis MinIO et extrait son contenu textuel structuré via Docling.
    """
    object_name = f"{file_id}.pdf"
    
    # Créer un fichier temporaire pour Docling
    with tempfile.NamedTemporaryFile(delete=False, suffix=".pdf") as tmp_file:
        tmp_path = tmp_file.name
    
    try:
        # Téléchargement depuis MinIO
        download_file(object_name, tmp_path)
        
        # Parsing avec Docling
        markdown_content = parse_pdf(tmp_path)
        
        return {
            "id": file_id,
            "format": "markdown",
            "content": markdown_content
        }
    except ClientError as e:
        # Gestion propre des erreurs MinIO/S3 (ex: 404 Not Found)
        logger.error(f"Erreur de stockage pour {file_id}: {str(e)}")
        if e.response['Error']['Code'] in ['404', 'NoSuchKey']:
            raise HTTPException(status_code=404, detail="Fichier non trouvé dans le stockage.")
        raise HTTPException(status_code=500, detail="Erreur lors de la communication avec le stockage.")
    except Exception as e:
        # Log de l'exception complète pour l'observabilité
        logger.exception(f"Erreur interne lors du parsing du CV {file_id}")
        raise HTTPException(status_code=500, detail="Une erreur interne est survenue lors du parsing.")
    finally:
        # Nettoyage du fichier temporaire
        if os.path.exists(tmp_path):
            os.remove(tmp_path)
