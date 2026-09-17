from fastapi import FastAPI
from fastapi.responses import HTMLResponse
from pydantic import BaseModel

app = FastAPI(title="Mary Agent", version="2.2.0")

class PromptRequest(BaseModel):
    instruction: str
    language: str = "python"

@app.get("/", response_class=HTMLResponse)
def home():
    html_content = """
    <!DOCTYPE html>
    <html lang="es">
    <head>
        <meta charset="UTF-8">
        <title>Mary Agent - En Línea</title>
        <style>
            body { background: #0f172a; color: #f8fafc; font-family: sans-serif; text-align: center; padding-top: 50px; }
            h1 { color: #38bdf8; }
            .box { background: #1e293b; max-width: 500px; margin: auto; padding: 20px; border-radius: 8px; }
            textarea { width: 90%; height: 60px; background: #0f172a; color: #fff; border: 1px solid #334155; padding: 10px; border-radius: 4px; }
            button { background: #38bdf8; color: #0f172a; border: none; padding: 10px 20px; font-weight: bold; margin-top: 10px; border-radius: 4px; cursor: pointer; }
            pre { background: #090d16; color: #38bdf8; padding: 10px; text-align: left; border-radius: 4px; margin-top: 15px; overflow-x: auto; }
        </style>
    </head>
    <body>
        <div class="box">
            <h1>🤖 Mary Agent</h1>
            <p>Estado: Operativo</p>
            <textarea id="txt" placeholder="Pídele algo a Mary..."></textarea><br>
            <button onclick="enviar()">Enviar</button>
            <pre id="out">Esperando...</pre>
        </div>
        <script>
            async function enviar() {
                let text = document.getElementById('txt').value;
                document.getElementById('out').textContent = 'Procesando...';
                try {
                    let res = await fetch('/build', {
                        method: 'POST',
                        headers: {'Content-Type': 'application/json'},
                        body: JSON.stringify({instruction: text})
                    });
                    let data = await res.json();
                    document.getElementById('out').textContent = data.codigo_generado;
                } catch(e) {
                    document.getElementById('out').textContent = 'Error de conexión';
                }
            }
        </script>
    </body>
    </html>
    """
    return html_content

@app.post("/build")
def build_program(req: PromptRequest):
    return {
        "agente": "Mary",
        "codigo_generado": f"# Código generado por Mary para:\n# {req.instruction}\n\ndef ejecutar():\n    print('¡Listo!')\n\nejecutar()"
    }
