from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
import os

app = FastAPI(title="Mary Agent - Code & Trading Engine", version="1.0.0")

class PromptRequest(BaseModel):
    instruction: str
    language: str = "python"

@app.get("/")
def home():
    return {
        "mensaje": "¡Hola, jefe! Mary está en línea y lista para operar y programar.",
        "estado": "Operativo",
        "conexion_nube": "Exitosa"
    }

@app.post("/build")
def build_program(req: PromptRequest):
    """
    Endpoint para que Mary reciba instrucciones y devuelva 
    la estructura o código fuente del programa solicitado.
    """
    instruction_lower = req.instruction.lower()
    
    # Lógica base para que Mary interprete y construya soluciones
    if "calculadora" in instruction_lower or "estructural" in instruction_lower:
        code_output = """
# Script autogenerado por Mary para cálculo estructural o de soportes
def calcular_espaciamiento(largo: float, divisiones: int):
    return largo / divisiones
        """.strip()
    elif "canvas" in instruction_lower or "juego" in instruction_lower:
        code_output = """
// HTML5 Canvas Base Script generado por Mary
const canvas = document.getElementById('appCanvas');
const ctx = canvas.getContext('2d');
function loop() {
    ctx.clearRect(0, 0, canvas.width, canvas.height);
    requestAnimationFrame(loop);
}
loop();
        """.strip()
    else:
        code_output = f"# Código base generado para: {req.instruction}\nprint('Ejecutando rutina de Mary')"

    return {
        "agente": "Mary",
        "lenguaje": req.language,
        "instruccion_recibida": req.instruction,
        "codigo_generado": code_output,
        "estado": "Programa compilado con éxito"
        }
    
