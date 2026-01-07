from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
import json
from pathlib import Path

app = FastAPI(title="CV API", version="1.0")

# Permitir consumo desde Streamlit u otros frontends
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["GET"],
    allow_headers=["*"],
)

CV_FILE = Path("cv_data_en.json")


@app.get("/cv")
def get_cv():
    if not CV_FILE.exists():
        raise HTTPException(status_code=404, detail="cv_data no encontrado")

    try:
        with CV_FILE.open("r", encoding="utf-8") as f:
            return json.load(f)
    except json.JSONDecodeError:
        raise HTTPException(status_code=500, detail="JSON inválido")
