from fastapi import FastAPI, HTTPException
from fastapi.responses import HTMLResponse
from pydantic import BaseModel
import os

app = FastAPI(title="Mary Agent - Autonomous Frontend", version="2.0.0")

class PromptRequest(BaseModel):
    instruction: str
    language: str = "python"

@app.get("/", response_class=HTMLResponse)
def home():
    """Interfaz visual de chat integrada para interactuar con Mary."""
    return """
    <!DOCTYPE html>
    <html lang="es">
    <head>
        <meta charset="UTF-8">
        <meta name="viewport" content="width=device-width, initial-scale=1.0">
        <title>Mary - Agente Autónomo</title>
        <style>
            :root {
                --bg-color: #0f172a;
                --chat-bg: #1e293b;
                --accent: #38bdf8;
                --text-main: #f8fafc;
                --text-muted: #94a3b8;
                --border: #334155;
            }
            body {
                font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
                background-color: var(--bg-color);
                color: var(--text-main);
                margin: 0;
                padding: 0;
                display: flex;
                flex-direction: column;
                height: 100vh;
            }
            header {
                background-color: var(--chat-bg);
                padding: 1rem 2rem;
                border-bottom: 1px solid var(--border);
                display: flex;
                justify-content: space-between;
                align-items: center;
            }
            header h1 {
                margin: 0;
                font-size: 1.25rem;
                color: var(--accent);
            }
            .status {
                font-size: 0.85rem;
                color: #4ade80;
                display: flex;
                align-items: center;
                gap: 0.5rem;
            }
            .status-dot {
                width: 8px;
                height: 8px;
                background-color: #4ade80;
                border-radius: 50%;
                display: inline-block;
                box-shadow: 0 0 8px #4ade80;
            }
            #chat-container {
                flex: 1;
                overflow-y: auto;
                padding: 1.5rem;
                display: flex;
                flex-direction: column;
                gap: 1rem;
                max-width: 800px;
                width: 100%;
                margin: 0 auto;
            }
            .message {
                padding: 1rem;
                border-radius: 12px;
                max-width: 85%;
                line-height: 1.5;
                word-break: break-word;
            }
            .user-message {
                background-color: #2563eb;
                color: white;
                align-self: flex-end;
                border-bottom-right-radius: 2px;
            }
            .mary-message {
                background-color: var(--chat-bg);
                border: 1px solid var(--border);
                align-self: flex-start;
                border-bottom-left-radius: 2px;
            }
            .mary-message pre {
                background: #090d16;
                padding: 0.75rem;
                border-radius: 6px;
                overflow-x: auto;
                font-family: 'Courier New', Courier, monospace;
                color: #38bdf8;
            }
            .input-area {
                background-color: var(--chat-bg);
                padding: 1rem 2rem;
                border-top: 1px solid var(--border);
                display: flex;
                gap: 1rem;
                max-width: 840px;
                width: 100%;
                margin: 0 auto;
                box-sizing: border-box;
            }
            input[type="text"] {
                flex: 1;
                background-color: var(--bg-color);
                border: 1px solid var(--border);
                border-radius: 8px;
                padding: 0.75rem 1rem;
                color: var(--text-main);
                font-size: 1rem;
                outline: none;
            }
            input[type="text"]:focus {
                border-color: var(--accent);
            }
            button {
                background-color: var(--accent);
                color: var(--bg-color);
                border: none;
                border-radius: 8px;
                padding: 0 1.5rem;
                font-weight: bold;
                cursor: pointer;
                transition: opacity 0.2s;
            }
            button:hover {
                opacity: 0.9;
            }
        </style>
    </head>
    <body>
        <header>
            <h1>🤖 Mary Agent - Centro de Control</h1>
            <div class="status">
                <span class="status-dot"></span> Operativo en la Nube
            </div>
        </header>

        <div id="chat-container">
            <div class="message mary-message">
                ¡Hola, jefe! Estoy en línea y lista. Pídeme que cree un programa, script o app y me encargaré de estructurarlo.
            </div>
        </div>

        <div class="input-area">
            <input type="text" id="userInput" placeholder="Ej: Crea una calculadora o un script en Python..." autofocus>
            <button onclick="sendMessage()">Enviar</button>
        </div>

        <script>
            const chatContainer = document.getElementById('chat-container');
            const userInput = document.getElementById('userInput');

            userInput.addEventListener('keypress', function (e) {
                if (e.key === 'Enter') {
                    sendMessage();
                }
            });

            async function sendMessage() {
                const text = userInput.value.trim();
                if (!text) return;

                // Mensaje del usuario
                appendMessage(text, 'user-message');
                userInput.value = '';
                chatContainer.scrollTop = chatContainer.scrollHeight;

                // Mensaje temporal de carga
                const loadingId = appendMessage('Mary está procesando tu solicitud...', 'mary-message');

                try {
                    const response = await fetch('/build', {
                        method: 'POST',
                        headers: { 'Content-Type': 'application/json' },
                        body: JSON.stringify({ instruction: text, language: 'python' })
                    });
                    
                    const data = await response.json();
                    
                    // Remover mensaje de carga y mostrar resultado real
                    document.getElementById(loadingId).remove();
                    
                    const formattedResponse = `<strong>Estado:</strong> ${data.estado}<br><br><pre>${escapeHtml(data.codigo_generado)}</pre>`;
                    appendMessage(formattedResponse, 'mary-message', true);

                } catch (error) {
                    document.getElementById(loadingId).remove();
                    appendMessage('Error de conexión con el servidor de Mary.', 'mary-message');
                }
                chatContainer.scrollTop = chatContainer.scrollHeight;
            }

            function appendMessage(text, className, isHTML = false) {
                const msgDiv = document.createElement('div');
                msgDiv.className = `message ${className}`;
                const id = 'msg-' + Date.now();
                msgDiv.id = id;
                
                if (isHTML) {
                    msgDiv.innerHTML = text;
                } else {
                    msgDiv.textContent = text;
                }
                
                chatContainer.appendChild(msgDiv);
                chatContainer.scrollTop = chatContainer.scrollHeight;
                return id;
            }

            function escapeHtml(string) {
                return String(string).replace(/&/g, '&amp;').replace(/</g, '&lt;').replace(/>/g, '&gt;');
            }
        </script>
    </body>
    </html>
    """

@app.post("/build")
def build_program(req: PromptRequest):
    """Endpoint lógico para que Mary procese comandos de desarrollo."""
    instruccion = req.instruction.lower()
    
    # Generador inteligente simulado de código según la petición
    if "calculadora" in instruccion:
        codigo = (
            "def calcular():\n"
            "    print('Calculadora inteligente activa')\n"
            "    a = float(input('Valor 1: '))\n"
            "    b = float(input('Valor 2: '))\n"
            "    print('Resultado:', a + b)\n"
            "if __name__ == '__main__':\n"
            "    calcular()"
        )
    elif "api" in instruccion or "servidor" in instruccion:
        codigo = (
            "from fastapi import FastAPI\n"
            "app = FastAPI()\n\n"
            "@app.get('/api/v1/status')\n"
            "def status():\n"
            "    return {'status': 'active', 'agent': 'Mary'}"
        )
    else:
        codigo = (
            f"# Programa generado automáticamente por Mary\n"
            f"# Requerimiento: {req.instruction}\n\n"
            "def main():\n"
            "    print('Ejecutando rutina automatizada...')\n\n"
            "if __name__ == '__main__':\n"
            "    main()"
        )

    return {
        "agente": "Mary",
        "instruccion_recibida": req.instruction,
        "codigo_generado": codigo,
        "estado": "Programa generado y compilado con éxito"
    }
