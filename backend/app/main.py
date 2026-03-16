import uuid
import os
import tempfile
import logging
from fastapi import FastAPI, UploadFile, File, HTTPException
from contextlib import asynccontextmanager
from botocore.exceptions import ClientError
from .storage import upload_file, download_file
from .parser import parse_pdf, DOCLING_AVAILABLE
from .analyzer import CVAnalyzer

# Configuration du logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Instance globale de l'analyzer
analyzer = None

@asynccontextmanager
async def lifespan(app: FastAPI):
    """
    Gestionnaire de cycle de vie pour initialiser les ressources au démarrage
    et les nettoyer à la fermeture.
    """
    global analyzer
    logger.info("Démarrage du serveur Sourcing RH (via lifespan)...")
    
    # Diagnostics Docling
    if DOCLING_AVAILABLE:
        logger.info("Diagnostic : Docling est disponible.")
    else:
        logger.error("Diagnostic : Docling est INDISPONIBLE.")
    
    # Initialisation Analyzer
    try:
        analyzer = CVAnalyzer()
        logger.info("Diagnostic : Analyzer IA initialisé.")
    except Exception as e:
        logger.warning(f"Diagnostic : Analyzer IA non initialisé : {str(e)}")
    
    yield
    
    logger.info("Fermeture du serveur Sourcing RH...")

app = FastAPI(title="Sourcing RH API", lifespan=lifespan)

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
        
        # Sauvegarde locale du dossier augmenté (PBI-003)
        base_dir = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
        output_dir = os.path.join(base_dir, "data", "analyses")
        os.makedirs(output_dir, exist_ok=True)
        md_filename = f"{file_id}.md"
        md_path = os.path.join(output_dir, md_filename)
        
        with open(md_path, "w", encoding="utf-8") as f:
            f.write(augmented_markdown)
            
        logger.info(f"Dossier augmenté sauvegardé : {md_path}")
        
        return {
            "id": file_id,
            "analysis": analysis_data,
            "dossier_markdown": augmented_markdown,
            "dossier_path": md_path
        }
    except ClientError as e:
        # Gestion robuste des erreurs MinIO/S3 (PBI-003 Harmonisation)
        error_code = e.response.get('Error', {}).get('Code', 'Unknown')
        if error_code in ['404', 'NoSuchKey']:
            logger.warning(f"Fichier non trouvé pour l'analyse : {file_id}")
            raise HTTPException(status_code=404, detail=f"Fichier {file_id} non trouvé dans le stockage.")
        
        logger.error(f"Erreur stockage lors de l'analyse du CV {file_id} : {str(e)}")
        raise HTTPException(status_code=500, detail="Erreur de communication avec le stockage.")
    except Exception as e:
        logger.exception(f"Erreur interne lors de l'analyse du CV {file_id}")
        raise HTTPException(status_code=500, detail="Une erreur interne est survenue lors de l'analyse.")
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
