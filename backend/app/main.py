from fastapi import FastAPI, UploadFile, File, HTTPException
import uuid
import os
import tempfile
from botocore.exceptions import ClientError
from .storage import upload_file, download_file
from .parser import parse_pdf

app = FastAPI(title="Sourcing RH API")

@app.get("/api/health")
async def health_check():
    return {"status": "ok", "message": "Le moteur de Sourcing RH est prêt."}

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
        if e.response['Error']['Code'] in ['404', 'NoSuchKey']:
            raise HTTPException(status_code=404, detail="Fichier non trouvé dans le stockage.")
        raise HTTPException(status_code=500, detail="Erreur lors de la communication avec le stockage.")
    except Exception as e:
        # Éviter de renvoyer l'erreur brute (fuite d'information)
        raise HTTPException(status_code=500, detail="Une erreur interne est survenue lors du parsing.")
    finally:
        # Nettoyage du fichier temporaire
        if os.path.exists(tmp_path):
            os.remove(tmp_path)

