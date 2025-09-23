import os
import openai
from dotenv import load_dotenv
from fastapi import FastAPI, Request
from fastapi.responses import HTMLResponse, JSONResponse
from fastapi.staticfiles import StaticFiles
from fastapi.middleware.cors import CORSMiddleware

# 1. Cargar clave API desde el archivo .env
load_dotenv()
openai.api_key = os.getenv("OPENAI_API_KEY")

# 2. Crear instancia de la app FastAPI
app = FastAPI()

# 3. Configuración de CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Reemplaza con tu dominio si lo deseas
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# 4. Montar carpeta estática
app.mount("/static", StaticFiles(directory="app/static"), name="static")

# 5. Ruta principal que carga el index.html
@app.get("/", response_class=HTMLResponse)
async def serve_home():
    try:
        with open("app/static/index.html", "r", encoding="utf-8") as file:
            html_content = file.read()
        return HTMLResponse(content=html_content)
    except FileNotFoundError:
        return HTMLResponse(content="<h1>Error: index.html no encontrado</h1>", status_code=404)

# 6. Ruta para procesar preguntas
@app.get("/preguntar")
async def preguntar(pregunta: str):
    if not pregunta or len(pregunta.strip()) < 3:
        return JSONResponse(content={"respuesta": "Por favor escribe una pregunta válida."})

    try:
        respuesta = await consultar_openai_gpt4(pregunta)
        return JSONResponse(content={"respuesta": respuesta})
    except Exception as e:
        return JSONResponse(content={"respuesta": f"Ocurrió un error: {str(e)}"})

# 7. Ruta de verificación de estado
@app.get("/status")
async def status():
    return {"message": "🧠 Red Neuronal Consejo de Neurocirugía funcionando correctamente con GPT-4 Turbo."}

# 8. Función que consulta a la API de OpenAI
async def consultar_openai_gpt4(pregunta: str) -> str:
    respuesta = openai.ChatCompletion.create(
        model="gpt-4-turbo",
        messages=[
            {"role": "system", "content": "Eres un neurocirujano experto entrenado para responder preguntas del examen de consejo de neurocirugía en México. Sé preciso, profesional y directo."},
            {"role": "user", "content": pregunta}
        ],
        temperature=0.3,
        max_tokens=800
    )
    return respuesta.choices[0].message['content'].strip()