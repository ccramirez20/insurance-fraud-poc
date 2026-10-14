from fastapi import FastAPI, UploadFile, File, HTTPException, Request
from fastapi.responses import JSONResponse, HTMLResponse, FileResponse
from fastapi.staticfiles import StaticFiles
from openai import OpenAI
from dotenv import load_dotenv
from tempfile import NamedTemporaryFile
import os
from analisis_fraude import prompt_1, prompt_2
import json
from uuid import uuid4
from datetime import datetime

# Esto carga las variables de entorno como el OPENAI_API_KEY
load_dotenv()
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")
if not OPENAI_API_KEY:
    raise RuntimeError("OPENAI_API_KEY no encontrada en el entorno")

# Esta parte inicia el cliente de OpenAI
client = OpenAI(api_key=OPENAI_API_KEY)
# Inicia el app de FastAPI
app = FastAPI() 

# Se establece la carpeta static para el frontend en HTML
app.mount("/static", StaticFiles(directory="static"), name="static")

@app.get("/favicon.ico", include_in_schema=False)
async def favicon():
    return FileResponse("static/favicon.ico")

# A partir de esto se construye el frontend, se está usando una petición GET que lee información
@app.get("/", response_class=HTMLResponse)
#Cuando el navegador va localhost FAstAPI ejecuta index y devuelve el HTML
def index():
    with open("static/index.html", "r", encoding="utf-8") as f:
        return f.read()

DATA_DIR = "datos_analisis"
os.makedirs(DATA_DIR, exist_ok=True)


@app.post("/summarize")
async def summarize_audio(file: UploadFile = File(...)):
    print("Recibiendo archivo de audio...")
    if not file.content_type.startswith("audio/"):
        raise HTTPException(status_code=400, detail="El archivo debe ser de audio")

    _, ext = os.path.splitext(file.filename)
    if ext.lower() not in [".mp3", ".wav", ".m4a"]:
        raise HTTPException(status_code=400, detail="Formato de audio no soportado")

    with NamedTemporaryFile(delete=False, suffix=ext) as tmp:
        tmp.write(await file.read())
        tmp_path = tmp.name

    with open(tmp_path, "rb") as audio:
        transcription = client.audio.transcriptions.create(
            model="gpt-4o-transcribe",
            file=audio,
            prompt = f"""{prompt_2}""",
        )
 
    texto = transcription.text
    print(texto)

# Esto hace que el sistema vaya y busque el prompt directamente en la carpeta
    prompt = f"""{prompt_1} Este es el texto que debes analizar: {texto}"""

    chat = client.chat.completions.create(
        model="gpt-4o-mini-2024-07-18",
        messages=[{"role": "user", "content": prompt}]
    )
    resumen = chat.choices[0].message.content.strip()

    file_id = str(uuid4())
    entry = {
        "id": file_id,
        "filename": file.filename,
        "timestamp": datetime.now().isoformat(),
        "texto": texto,
        "resumen": resumen
    }

    with open(os.path.join(DATA_DIR, f"{file_id}.json"), "w", encoding="utf-8") as f:
        json.dump(entry, f, ensure_ascii=False, indent=4)

    return JSONResponse(
        {
            "summary": resumen,
            "id": file_id
        }
    )

# Esto para que el chat funcione y pueda enviar mensajes
@app.post("/chat")
async def chat_with_agent(request: Request): # async hace que no haya problema con multiples usuarios
    data = await request.json()
    messages = data.get("messages")
    if not messages:
        raise HTTPException(status_code=400, detail="Faltan los mensajes")
    
    
    file_id = data.get("file_id")
    if file_id:
        file_path = os.path.join(DATA_DIR, f"{file_id}.json")
        if os.path.exists(file_path):
            with open(file_path, "r", encoding="utf-8") as f:
                datos = json.load(f)
            # Agregar el contexto al inicio del chat
            context_msg = {
                "role": "system",
                "content": f"Este es el resumen de un audio procesado previamente:\n\nResumen: {datos['resumen']}\nTexto completo: {datos['texto'][:1000]}..."
            }
            messages.insert(0, context_msg)
        else:
            raise HTTPException(status_code=404, detail="Archivo no encontrado")
    
    
    chat = client.chat.completions.create(
        model="gpt-4o-mini-2024-07-18",
        messages=messages
    )
    reply = chat.choices[0].message.content.strip()
    return JSONResponse({"reply": reply})


@app.get("/analisis")
async def listar_analisis():
    archivos = []
    for nombre in os.listdir(DATA_DIR):
        if nombre.endswith(".json"):
            with open(os.path.join(DATA_DIR, nombre), "r", encoding="utf-8") as f:
                datos = json.load(f)
                archivos.append({
                    "id": datos["id"],
                    "filename": datos["filename"],
                    "timestamp": datos["timestamp"]
                })
    return JSONResponse({"analisis": archivos})

@app.get("/analisis/{file_id}")
async def obtener_analisis(file_id: str):
    ruta = os.path.join(DATA_DIR, f"{file_id}.json")
    if not os.path.exists(ruta):
        raise HTTPException(status_code=404, detail="No encontrado")
    return FileResponse(ruta, media_type="application/json")



if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
