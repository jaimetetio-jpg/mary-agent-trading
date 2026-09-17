from fastapi import FastAPI
from pydantic import BaseModel

app = FastAPI(title="Mary Agent", version="2.3.0")

class PromptRequest(BaseModel):
    instruction: str
    language: str = "python"

@app.get("/")
def home():
    return {
        "mensaje": "¡Hola, jefe! Mary está en línea y lista para operar.",
        "estado": "Operativo",
        "conexion_nube": "Exitosa"
    }

@app.post("/build")
def build_program(req: PromptRequest):
    return {
        "agente": "Mary",
        "instruccion": req.instruction,
        "codigo_generado": f"# Código generado para: {req.instruction}\nprint('¡Mary operando con éxito!')"
    }
    
