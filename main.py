from fastapi import FastAPI, HTTPException
from fastapi.responses import HTMLResponse
from pydantic import BaseModel
import requests
import re

app = FastAPI(title="Mary Autonomous AI - Kimi Engine", version="3.9.9")

class ChatMessage(BaseModel):
    role: str
    content: str

class PromptRequest(BaseModel):
    instruction: str
    history: list[ChatMessage] = []

@app.get("/", response_class=HTMLResponse)
def home():
    return """
    <!DOCTYPE html>
    <html lang="es">
    <head>
        <meta charset="UTF-8">
        <meta name="viewport" content="width=device-width, initial-scale=1.0">
        <title>Mary - Kimi Neural Engine v3.9.9</title>
        <style>
            :root {
                --bg-gradient: linear-gradient(135deg, #090d16 0%, #1a1c29 50%, #0f172a 100%);
                --accent-neon: #10b981;
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
                border-bottom: 2px solid rgba(16, 185, 129, 0.3);
                box-shadow: 0 10px 25px -5px rgba(0, 0, 0, 0.5);
                z-index: 10;
            }
            h1 {
                margin: 0;
                font-size: 1.3rem;
                background: linear-gradient(to right, #34d399, #60a5fa);
                -webkit-background-clip: text;
                -webkit-text-fill-color: transparent;
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
                border: 1px solid rgba(16, 185, 129, 0.3);
                align-self: flex-start;
            }
            .user {
                background: linear-gradient(135deg, #059669, #047857);
                color: white;
                align-self: flex-end;
            }
            pre {
                background: #05070c;
                padding: 12px;
                border-radius: 8px;
                color: #34d399;
                overflow-x: auto;
                font-family: 'Courier New', Courier, monospace;
                border: 1px solid rgba(52, 211, 153, 0.2);
                white-space: pre-wrap;
            }
            .input-container {
                background: rgba(15, 23, 42, 0.9);
                padding: 15px 20px;
                display: flex;
                gap: 12px;
                max-width: 750px;
                width: 100%;
                margin: 0 auto;
                box-sizing: border-box;
                border-top: 2px solid rgba(16, 185, 129, 0.2);
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
                border-color: #10b981;
                box-shadow: 0 0 12px rgba(16, 185, 129, 0.4);
            }
            button {
                background: linear-gradient(135deg, #10b981, #059669);
                color: white;
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
            <h1>🔮 Mary - Kimi Neural Engine v3.9.9</h1>
        </header>

        <div id="chat">
            <div class="msg mary">¡Hola, Jaime! Núcleo Kimi v3.9.9 conectado con éxito. ¿Qué programa o cálculo hacemos hoy?</div>
        </div>

        <div class="input-container">
            <input type="text" id="userInput" placeholder="Escribe tu instrucción aquí..." autofocus>
            <button onclick="send()">Enviar</button>
        </div>

        <script>
            const chat = document.getElementById('chat');
            const input = document.getElementById('userInput');
            let conversationHistory = [];

            input.addEventListener('keypress', (e) => { if (e.key === 'Enter') send(); });

            async function send() {
                const text = input.value.trim();
                if (!text) return;

                appendMsg(text, 'user');
                input.value = '';
                conversationHistory.push({ role: "user", content: text });

                const loadId = appendMsg('Mary procesando con Kimi...', 'mary');

                try {
                    const res = await fetch('/build', {
                        method: 'POST',
                        headers: { 'Content-Type': 'application/json' },
                        body: JSON.stringify({ instruction: text, history: conversationHistory })
                    });
                    const data = await res.json();
                    
                    document.getElementById(loadId).remove();
                    const replyText = data.respuesta_ia || "Error: Respuesta vacía.";
                    
                    appendMsg(replyText, 'mary', true);
                    conversationHistory.push({ role: "assistant", content: replyText });

                } catch (err) {
                    document.getElementById(loadId).remove();
                    appendMsg('Error de comunicación con el núcleo.', 'mary');
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
    # API Key integrada directamente de forma segura
    api_key = "sk-r95hjSAMuoEJySjUPVsmV63EL0Yc8amx8G5qYYKl1ORqG2wP"
    
    url = "https://api.moonshot.cn/v1/chat/completions"
    
    system_instruction = (
        "Eres Mary, una agente de software autónoma de élite y asistente de construcción y trading experta. "
        "Posees un razonamiento avanzado, alta capacidad de cálculo técnico, diseño de estructuras (como PVC, drywall) y programación. "
        "Sé directa, inteligente, clara y concisa. Estructura el código de manera impecable y limpia."
    )
    
    messages = [{"role": "system", "content": system_instruction}]
    
    for msg in req.history:
        r = "user" if msg.role == "user" else "assistant"
        if msg.role == "model":
            r = "assistant"
        clean_content = msg.content.replace("<br>", "\n").replace("<pre><code>", "```").replace("</code></pre>", "```")
        messages.append({"role": r, "content": clean_content})

    payload = {
        "model": "moonshot-v1-8k",
        "messages": messages,
        "temperature": 0.3
    }
    
    headers = {
        "Authorization": f"Bearer {api_key}",
        "Content-Type": "application/json"
    }

    try:
        response = requests.post(url, json=payload, headers=headers, timeout=45)
        res_data = response.json()
        
        if "error" in res_data:
            error_msg = res_data["error"].get("message", "Error desconocido en Kimi API")
            return {"agente": "Mary", "respuesta_ia": f"⚠️ Nota de sistema: {error_msg}"}
        
        if "choices" in res_data and len(res_data["choices"]) > 0:
            ai_text = res_data["choices"][0]["message"]["content"]
        else:
            ai_text = f"Respuesta inesperada: {str(res_data)}"
            
        ai_reply = ai_text.replace("&", "&amp;").replace("<", "&lt;").replace(">", "&gt;")
        ai_reply = ai_reply.replace("\n", "<br>")
        ai_reply = re.sub(r'```([a-zA-Z]*)(.*?)```', r'<pre><code>\2</code></pre>', ai_reply, flags=re.DOTALL)
        ai_reply = ai_reply.replace("&lt;br&gt;", "<br>")

        return {
            "agente": "Mary",
            "respuesta_ia": ai_reply
        }
    except Exception as e:
        return {"agente": "Mary", "respuesta_ia": f"⚠️ Error de conexión: {str(e)}"}
