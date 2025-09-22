from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from app.faiss_loader import get_answer

app = FastAPI()

# Configuración CORS para permitir peticiones desde cualquier origen
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.get("/")
def home():
    return {"message": "🚀 Red Neuronal Consejo de Neurocirugía funcionando correctamente."}

@app.get("/preguntar/")
def preguntar(pregunta: str):
    respuesta = get_answer(pregunta)
    return {"pregunta": pregunta, "respuesta": respuesta}