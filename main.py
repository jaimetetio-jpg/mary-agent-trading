from fastapi import FastAPI
import os

app = FastAPI(title="Mary Agent API", version="1.0")

@app.get("/")
def leer_raiz():
    return {
        "mensaje": "¡Hola, jefe! Mary está en línea y lista para operar.",
        "estado": "Operativo",
        "conexion_nube": "Exitosa"
    }

@app.get("/api/estado")
def estado_sistema():
    return {
        "agente": "Mary",
        "modo": "Desarrollo y Trading",
        "supabase_conectado": os.getenv("SUPABASE_DB_URL") is not None
    }
  
