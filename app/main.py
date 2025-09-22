from fastapi import FastAPI, Request
from fastapi.responses import HTMLResponse, JSONResponse
from fastapi.staticfiles import StaticFiles
from fastapi.middleware.cors import CORSMiddleware
from app.faiss_loader import obtener_respuesta

app = FastAPI()

# Permitir CORS (opcional, útil si accedes desde dominios externos)
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Puedes restringir esto a tu dominio
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Montar archivos estáticos (como index.html, CSS, JS)
app.mount("/static", StaticFiles(directory="app/static"), name="static")


@app.get("/", response_class=HTMLResponse)
async def serve_home():
    """Carga la interfaz visual (index.html)"""
    with open("app/static/index.html", "r", encoding="utf-8") as file:
        html_content = file.read()
    return HTMLResponse(content=html_content)


@app.get("/preguntar")
async def preguntar(pregunta: str):
    """Procesa la pregunta y devuelve respuesta del modelo"""
    if not pregunta:
        return JSONResponse(content={"respuesta": "Por favor escribe una pregunta válida."})
    respuesta = obtener_respuesta(pregunta)
    return JSONResponse(content={"respuesta": respuesta})


@app.get("/status")
async def status():
    """Verifica si la app está en línea"""
    return {"message": "Red Neuronal Consejo de Neurocirugía funcionando correctamente."}