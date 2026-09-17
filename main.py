from fastapi import FastAPI, HTTPException
from fastapi.responses import HTMLResponse
from pydantic import BaseModel
import os
import requests

app = FastAPI(title="Mary Autonomous AI", version="3.2.0")

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
        <title>Mary - 3D AI Neural Engine</title>
        <style>
            :root {
                --bg-gradient: linear-gradient(135deg, #090d16 0%, #1a1c29 50%, #0f172a 100%);
                --accent-neon: #06b6d4;
                --accent-purple: #8b5cf6;
                --text-main: #f8fafc;
            }
            body {
                background: var(--bg-gradient);
                color: var(--text-main);
                font-family: 'Segoe UI', Roboto, Helvetica, sans-serif;
                margin: 0;
                padding: 0;
                display: flex;
                flex-direction: column;
                height: 100vh;
                overflow: hidden;
            }
            header {
                background: linear-gradient(90deg, #1e293b, #0f172a);
                padding: 15px 20px;
                text-align: center;
                border-bottom: 2px solid rgba(6, 182, 212, 0.3);
                box-shadow: 0 10px 25px -5px rgba(0, 0, 0, 0.5);
                z-index: 10;
            }
            h1 {
                margin: 0;
                font-size: 1.3rem;
                background: linear-gradient(to right, #38bdf8, #c084fc);
                -webkit-background-clip: text;
                -webkit-text-fill-color: transparent;
                text-shadow: 0 2px 10px rgba(56, 189, 248, 0.3);
            }
            #chat {
                flex: 1;
                overflow-y: auto;
                padding: 20px;
                display: flex;
                flex-direction: column;
                gap: 15px;
                max-width: 750px;
                width: 100%;
                margin: 0 auto;
                box-sizing: border-box;
            }
            .msg {
                padding: 14px 18px;
                border-radius: 16px;
                max-width: 85%;
                word-break: break-word;
                line-height: 1.5;
            }
            .mary {
                background: linear-gradient(145deg, #1e293b, #0f172a);
                border: 1px solid rgba(139, 92, 246, 0.3);
                align-self: flex-start;
                box-shadow: 0 10px 25px -5px rgba(0, 0, 0, 0.4);
            }
            .user {
                background: linear-gradient(135deg, #2563eb, #1d4ed8);
                color: white;
                align-self: flex-end;
                box-shadow: 0 10px 20px -5px rgba(37, 99, 235, 0.5);
            }
            pre {
                background: #05070c;
                padding: 12px;
                border-radius: 8px;
                color: #38bdf8;
                overflow-x: auto;
                font-family: 'Courier New', Courier, monospace;
                border: 1px solid rgba(56, 189, 248, 0.2);
            }
            .input-container {
                background: rgba(15, 23, 42, 0.9);
                backdrop-filter: blur(10px);
                padding: 15px 20px;
                display: flex;
                gap: 12px;
                max-width: 750px;
                width: 100%;
                margin: 0 auto;
                box-sizing: border-box;
                border-top: 2px solid rgba(139, 92, 246, 0.2);
            }
            input {
                flex: 1;
                background: #0b0f19;
                border: 1px solid #334155;
                border-radius: 12px;
                padding: 12px 16px;
                color: white;
                font-size: 1rem;
                outline: none;
            }
            input:focus {
                border-color: #8b5cf6;
                box-shadow: 0 0 12px rgba(139, 92, 246, 0.4);
            }
            button {
                background: linear-gradient(135deg, #06b6d4, #3b82f6);
                color: #090d16;
                border: none;
                padding: 0 22px;
                font-weight: bold;
                border-radius: 12px;
                cursor: pointer;
            }
        </style>
    </head>
    <body>
        <header>
            <h1>🔮 Mary - IA Autónoma en Línea</h1>
        </header>

        <div id="chat">
            <div class="msg mary">¡Hola, jefe! Cerebro reconectado con éxito. Pregúntame lo que quieras o pídeme código.</div>
        </div>

        <div class="input-container">
            <input type="text" id="userInput" placeholder="Escribe tu instrucción aquí..." autofocus>
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

                const loadId = appendMsg('Mary está procesando con IA...', 'mary');

                try {
                    const res = await fetch('/build', {
                        method: 'POST',
                        headers: { 'Content-Type': 'application/json' },
                        body: JSON.stringify({ instruction: text, language: 'python' })
                    });
                    const data = await res.json();
                    
                    document.getElementById(loadId).remove();
                    // AQUÍ ESTÁ LA CORRECCIÓN CLAVE: leemos data.respuesta_ia con seguridad
                    const replyText = data.respuesta_ia || "Error: Respuesta vacía del servidor.";
                    appendMsg(replyText, 'mary', true);
                } catch (err) {
                    document.getElementById(loadId).remove();
                    appendMsg('Error de comunicación con el núcleo de IA.', 'mary');
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
    api_key = os.environ.get("GEMINI_API_KEY")
    if not api_key:
        raise HTTPException(status_code=500, detail="Falta configurar la GEMINI_API_KEY en Render")
    
    url = f"https://generativelanguage.googleapis.com/v1beta/models/gemini-2.5-flash:generateContent?key={api_key}"
    
    payload = {
        "contents": [{
            "parts": [{"text": f"Eres Mary, una agente de software autónoma y asistente de trading experta. Tu jefe te habla. Responde de forma inteligente, conversacional y redacta código funcional limpio en bloques cuando sea necesario. Instrucción: {req.instruction}"}]
        }]
    }
    
    try:
        response = requests.post(url, json=payload)
        res_data = response.json()
        
        # Extraer con seguridad el texto de la respuesta de Google
        if "candidates" in res_data and len(res_data["candidates"]) > 0:
            ai_text = res_data["candidates"][0]["content"]["parts"][0]["text"]
        else:
            ai_text = f"Respuesta cruda: {str(res_data)}"
            
        ai_reply = ai_text.replace("\n", "<br>").replace("```python", "<pre><code>").replace("```", "</code></pre>")
        
        return {
            "agente": "Mary",
            "respuesta_ia": ai_reply
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
