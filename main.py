from fastapi import FastAPI
from fastapi.responses import HTMLResponse
from pydantic import BaseModel

app = FastAPI(title="Mary Agent", version="2.1.0")

class PromptRequest(BaseModel):
    instruction: str
    language: str = "python"

@app.get("/", response_class=HTMLResponse)
def home():
    return """
    <!DOCTYPE html>
    <html lang="es">
    <head>
        <meta charset="UTF-8">
        <meta name="viewport" content="width=device-width, initial-scale=1.0">
        <title>Mary - Centro de Control</title>
        <style>
            body {
                font-family: Arial, sans-serif;
                background-color: #0f172a;
                color: #f8fafc;
                margin: 0;
                padding: 20px;
                display: flex;
                flex-direction: column;
                align-items: center;
            }
            h1 { color: #38bdf8; }
            .chat-box {
                width: 100%;
                max-width: 600px;
                background: #1e293b;
                padding: 20px;
                border-radius: 8px;
                box-shadow: 0 4px 6px rgba(0,0,0,0.3);
            }
            textarea {
                width: 100%;
                height: 80px;
                background: #0f172a;
                color: #fff;
                border: 1px solid #334155;
                border-radius: 4px;
                padding: 10px;
                margin-bottom: 10px;
                box-sizing: border-box;
            }
            button {
                background: #38bdf8;
                color: #0f172a;
                border: none;
                padding: 10px 20px;
                font-weight: bold;
                border-radius: 4px;
                cursor: pointer;
            }
            pre {
                background: #090d16;
                padding: 10px;
                border-radius: 4px;
                overflow-x: auto;
                color: #38bdf8;
                margin-top: 15px;
            }
        </style>
    </head>
    <body>
        <h1>🤖 Mary Agent</h1>
        <div class="chat-box">
            <p>Escribe lo que quieres que Mary programe:</p>
            <textarea id="instruction" placeholder="Ej: Crea una calculadora..."></textarea>
            <br>
            <button onclick="enviar()">Generar Programa</button>
            <pre id="result">Esperando instrucciones...</pre>
        </div>

        <script>
            async function enviar() {
                const text = document.getElementById('instruction').value;
                document.getElementById('result').textContent = 'Procesando...';
                
                try {
                    const res = await fetch('/build', {
                        method: 'POST',
                        headers: { 'Content-Type': 'application/json' },
                        body: JSON.stringify({ instruction: text, language: 'python' })
                    });
                    const data = await res.json();
                    document.getElementById('result').textContent = data.codigo_generado;
                } catch (e) {
                    document.getElementById('result').textContent = 'Error de conexión.';
                }
            }
        </script>
    </body>
    </html>
    """

@app.post("/build")
def build_program(req: PromptRequest):
    codigo = f"# Generado por Mary para: {req.instruction}\n\ndef run():\n    print('¡Programa ejecutándose con éxito!')\n\nif __name__ == '__main__':\n    run()"
    return {
        "agente": "Mary",
        "codigo_generado": codigo,
        "estado": "Éxito"
    }
