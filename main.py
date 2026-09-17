from fastapi import FastAPI
from fastapi.responses import HTMLResponse
from pydantic import BaseModel

app = FastAPI(title="Mary Agent - Visual", version="2.4.0")

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
                background-color: #0f172a;
                color: #f8fafc;
                font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
                margin: 0;
                padding: 0;
                display: flex;
                flex-direction: column;
                height: 100vh;
            }
            header {
                background-color: #1e293b;
                padding: 1rem;
                text-align: center;
                border-bottom: 1px solid #334155;
            }
            h1 { margin: 0; color: #38bdf8; font-size: 1.4rem; }
            #chat {
                flex: 1;
                overflow-y: auto;
                padding: 1rem;
                display: flex;
                flex-direction: column;
                gap: 0.8rem;
                max-width: 700px;
                width: 100%;
                margin: 0 auto;
                box-sizing: border-box;
            }
            .msg {
                padding: 0.8rem 1rem;
                border-radius: 8px;
                max-width: 85%;
                word-break: break-word;
                line-height: 1.4;
            }
            .mary {
                background-color: #1e293b;
                border: 1px solid #334155;
                align-self: flex-start;
            }
            .user {
                background-color: #2563eb;
                color: white;
                align-self: flex-end;
            }
            pre {
                background: #090d16;
                padding: 0.6rem;
                border-radius: 4px;
                color: #38bdf8;
                overflow-x: auto;
                font-family: monospace;
            }
            .input-box {
                background-color: #1e293b;
                padding: 1rem;
                display: flex;
                gap: 0.5rem;
                max-width: 700px;
                width: 100%;
                margin: 0 auto;
                box-sizing: border-box;
                border-top: 1px solid #334155;
            }
            input {
                flex: 1;
                background: #0f172a;
                border: 1px solid #334155;
                border-radius: 6px;
                padding: 0.7rem;
                color: white;
                outline: none;
            }
            button {
                background: #38bdf8;
                color: #0f172a;
                border: none;
                padding: 0 1.2rem;
                font-weight: bold;
                border-radius: 6px;
                cursor: pointer;
            }
        </style>
    </head>
    <body>
        <header>
            <h1>🤖 Mary - Agente Autónomo</h1>
        </header>

        <div id="chat">
            <div class="msg mary">¡Hola, jefe! Estoy en línea y lista. Escribe abajo lo que quieres que programe.</div>
        </div>

        <div class="input-box">
            <input type="text" id="userInput" placeholder="Ej: Crea un script de análisis..." autofocus>
            <button onclick="send()">Enviar</button>
        </div>

        <script>
            const chat = document.getElementById('chat');
            const input = document.getElementById('userInput');

            input.addEventListener('keypress', (e) => { if (e.key === 'Enter') send(); });

            async function send() {
                const text = input.value.trim();
                if (!text) return;

                appendMsg(text, 'user');
                input.value = '';

                const loadId = appendMsg('Mary está procesando...', 'mary');

                try {
                    const res = await fetch('/build', {
                        method: 'POST',
                        headers: { 'Content-Type': 'application/json' },
                        body: JSON.stringify({ instruction: text, language: 'python' })
                    });
                    const data = await res.json();
                    
                    document.getElementById(loadId).remove();
                    appendMsg(`<strong>Resultado:</strong><br><pre>${data.codigo_generado}</pre>`, 'mary', true);
                } catch (err) {
                    document.getElementById(loadId).remove();
                    appendMsg('Error de comunicación con Mary.', 'mary');
                }
            }

            function appendMsg(html, sender, isHtml = false) {
                const div = document.createElement('div');
                div.className = `msg ${sender}`;
                const id = 'msg-' + Math.random();
                div.id = id;
                if (isHtml) div.innerHTML = html;
                else div.textContent = html;
                chat.appendChild(div);
                chat.scrollTop = chat.scrollHeight;
                return id;
            }
        </script>
    </body>
    </html>
    """

@app.post("/build")
def build_program(req: PromptRequest):
    return {
        "agente": "Mary",
        "instruccion": req.instruction,
        "codigo_generado": f"# Programa autónomo generado por Mary\n# Solicitud: {req.instruction}\n\ndef run_task():\n    print('Ejecutando tarea solicitada con éxito')\n\nif __name__ == '__main__':\n    run_task()"
    }
    
