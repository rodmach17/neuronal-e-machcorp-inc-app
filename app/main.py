from fastapi import FastAPI, Request
from fastapi.responses import HTMLResponse
from fastapi.staticfiles import StaticFiles
from fastapi.middleware.cors import CORSMiddleware
from app.faiss_loader import obtener_respuesta

app = FastAPI()

# Configurar CORS para permitir conexiones desde cualquier origen
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Puedes restringirlo a tu dominio si lo deseas
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Montar carpeta estática donde está index.html
app.mount("/static", StaticFiles(directory="app/static"), name="static")

# Ruta raíz que devuelve la interfaz visual HTML
@app.get("/", response_class=HTMLResponse)
async def serve_index():
    with open("app/static/index.html", "r", encoding="utf-8") as file:
        return HTMLResponse(content=file.read(), status_code=200)

# Endpoint de prueba de vida
@app.get("/ping")
async def ping():
    return {"message": "Red Neuronal Consejo de Neurocirugía funcionando correctamente."}

# Endpoint que recibe la pregunta y devuelve la respuesta
@app.get("/preguntar")
async def preguntar(pregunta: str):
    respuesta = obtener_respuesta(pregunta)
    return {"respuesta": respuesta}