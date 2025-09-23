from fastapi import FastAPI, Request
from fastapi.responses import HTMLResponse, JSONResponse
from fastapi.staticfiles import StaticFiles
from fastapi.middleware.cors import CORSMiddleware
from dotenv import load_dotenv
import os
from openai import OpenAI

# Cargar variables de entorno (.env)
load_dotenv()
api_key = os.getenv("OPENAI_API_KEY")

# Inicializar cliente de OpenAI
client = OpenAI(api_key=api_key)

# Inicializar FastAPI
app = FastAPI()

# Middleware CORS (opcional)
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Reemplazar con tu dominio en producción
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Montar carpeta de archivos estáticos
app.mount("/static", StaticFiles(directory="app/static"), name="static")

# Cargar contexto desde archivos .txt
def cargar_contexto():
    glosario_path = "data/glosario_final_para_indexar.txt"
    preguntas_path = "data/Preguntas_Consejo_con_respuestas.txt"

    contexto = ""
    if os.path.exists(glosario_path):
        with open(glosario_path, "r", encoding="utf-8") as f:
            contexto += f.read() + "\n"

    if os.path.exists(preguntas_path):
        with open(preguntas_path, "r", encoding="utf-8") as f:
            contexto += f.read() + "\n"

    return contexto.strip()

# Contexto cargado en memoria
contexto_base = cargar_contexto()

@app.get("/", response_class=HTMLResponse)
async def serve_home():
    """Carga la interfaz visual principal."""
    with open("app/static/index.html", "r", encoding="utf-8") as f:
        return HTMLResponse(content=f.read())

@app.get("/preguntar")
async def preguntar(pregunta: str):
    """Procesa la pregunta y responde con GPT-4 Turbo contextualizado."""
    if not pregunta:
        return JSONResponse(content={"respuesta": "Por favor escribe una pregunta válida."})

    try:
        response = client.chat.completions.create(
            model="gpt-4-1106-preview",
            messages=[
                {
                    "role": "system",
                    "content": "Eres un asistente experto en neurocirugía. Responde con base en el siguiente contexto proporcionado por el usuario:\n\n" + contexto_base
                },
                {
                    "role": "user",
                    "content": pregunta
                }
            ],
            max_tokens=1000,
            temperature=0.3
        )
        respuesta = response.choices[0].message.content.strip()
        return JSONResponse(content={"respuesta": respuesta})
    except Exception as e:
        return JSONResponse(content={"respuesta": f"Error al procesar la pregunta: {str(e)}"})

@app.get("/status")
async def status():
    """Verifica si la API está en línea."""
    return {"message": "Red Neuronal del Consejo de Neurocirugía funcionando correctamente."}