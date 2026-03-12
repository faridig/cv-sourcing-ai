from fastapi import FastAPI, UploadFile, File, HTTPException
import uuid
from .storage import upload_file

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
