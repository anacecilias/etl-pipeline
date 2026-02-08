# api.py
from fastapi import FastAPI, UploadFile, File, HTTPException
from fastapi.responses import JSONResponse
import shutil
import os

from etl.etl import run_etl
from fastapi.responses import FileResponse
from fastapi.staticfiles import StaticFiles

UPLOAD_DIR = "uploads"

app = FastAPI(title="ETL API", version="1.0")

# Serve arquivos da pasta de saída
app.mount("/saida", StaticFiles(directory="saida"), name="saida")

@app.get("/download/{nome_arquivo}")
async def download_arquivo(nome_arquivo: str):
    caminho = f"saida/{nome_arquivo}"
    if os.path.exists(caminho):
        return FileResponse(caminho, media_type='text/csv', filename=nome_arquivo)
    else:
        return {"erro": "Arquivo não encontrado"}

@app.get("/health")
def health_check():
    return {"status": "ok"}

@app.post("/upload")
async def upload_arquivo(file: UploadFile = File(...)):
    os.makedirs(UPLOAD_DIR, exist_ok=True)

    caminho_arquivo = os.path.join(UPLOAD_DIR, file.filename)

    with open(caminho_arquivo, "wb") as buffer:
        shutil.copyfileobj(file.file, buffer)

    return {
        "mensagem": "Arquivo enviado com sucesso",
        "arquivo": caminho_arquivo
    }

@app.post("/run-etl")
def executar_etl():
    try:
        resultado = run_etl()
        return JSONResponse(content=resultado)
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

# api.py (adicione isso)

from fastapi.responses import FileResponse

@app.get("/download")
def download(caminho: str):
    if not os.path.exists(caminho):
        raise HTTPException(status_code=404, detail="Arquivo não encontrado")
    return FileResponse(caminho, filename=os.path.basename(caminho))
