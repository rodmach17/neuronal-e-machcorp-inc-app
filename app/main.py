from fastapi import FastAPI, Request
from fastapi.responses import HTMLResponse, JSONResponse
from fastapi.staticfiles import StaticFiles
from fastapi.middleware.cors import CORSMiddleware
import openai
import os
from dotenv import load_dotenv

# Cargar la API key desde el archivo .env
load_dotenv()
openai.api_key = os.getenv("OPENAI_API_KEY")

app = FastAPI()

# CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Puedes cambiarlo por tu dominio si gustas
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Servir archivos estáticos (index.html)
app.mount("/static", StaticFiles(directory="app/static"), name="static")


@app.get("/", response_class=HTMLResponse)
async def home():
    with open("app/static/index.html", "r", encoding="utf-8") as file:
        html = file.read()
    return HTMLResponse(content=html)


@app.get("/preguntar")
async def preguntar(pregunta: str):
    if not pregunta:
        return JSONResponse(content={"respuesta": "Por favor escribe una pregunta válida."})

    try:
        respuesta = openai.ChatCompletion.create(
            model="gpt-4-1106-preview",  # También puedes usar "gpt-3.5-turbo" si lo prefieres
            messages=[
                {"role": "system", "content": "Eres un neurocirujano experto respondiendo preguntas del examen de Consejo Mexicano de Cirugía Neurológica con precisión académica."},
                {"role": "user", "content": pregunta}
            ],
            temperature=0.2,
            max_tokens=800
        )
        texto = respuesta["choices"][0]["message"]["content"]
        return JSONResponse(content={"respuesta": texto})

    except Exception as e:
        return JSONResponse(content={"respuesta": f"Error al obtener respuesta: {str(e)}"})


@app.get("/status")
async def status():
    return {"message": "Asistente GPT-4 Turbo activo y funcionando correctamente."}