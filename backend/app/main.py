from fastapi import FastAPI

app = FastAPI(title="Sourcing RH API")

@app.get("/api/health")
async def health_check():
    return {"status": "ok", "message": "Le moteur de Sourcing RH est prêt."}
