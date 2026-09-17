from fastapi import FastAPI, HTTPException
from fastapi.responses import HTMLResponse
from pydantic import BaseModel
import os
import requests

app = FastAPI(title="Mary Autonomous AI", version="5.0.0")

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
        <title>Mary - Mentora de Negocios</title>
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
                padding: 12px 20px;
                display: flex;
                justify-content: space-between;
                align-items: center;
                border-bottom: 2px solid rgba(6, 182, 212, 0.3);
                box-shadow: 0 10px 25px -5px rgba(0, 0, 0, 0.5);
                z-index: 10;
            }
            h1 {
                margin: 0;
                font-size: 1.1rem;
                background: linear-gradient(to right, #38bdf8, #c084fc);
                -webkit-background-clip: text;
                -webkit-text-fill-color: transparent;
            }
            .history-btn {
                background: rgba(139, 92, 246, 0.2);
                border: 1px solid var(--accent-purple);
                color: #c084fc;
                padding: 6px 12px;
                border-radius: 8px;
                cursor: pointer;
                font-size: 0.9rem;
                font-weight: bold;
            }
            .history-btn:hover {
                background: rgba(139, 92, 246, 0.4);
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
            button.send-btn {
                background: linear-gradient(135deg, #06b6d4, #3b82f6);
                color: #090d16;
                border: none;
                padding: 0 22px;
                font-weight: bold;
                border-radius: 12px;
                cursor: pointer;
            }
            #modal {
                display: none;
                position: fixed;
                top: 0; left: 0; width: 100%; height: 100%;
                background: rgba(0,0,0,0.8);
                backdrop-filter: blur(5px);
                z-index: 100;
                justify-content: center;
                align-items: center;
            }
            .modal-content {
                background: #0f172a;
                border: 1px solid var(--accent-purple);
                width: 90%;
                max-width: 600px;
                max-height: 80vh;
                border-radius: 16px;
                display: flex;
                flex-direction: column;
                overflow: hidden;
                box-shadow: 0 20px 40px rgba(0,0,0,0.6);
            }
            .modal-header {
                padding: 15px 20px;
                background: #1e293b;
                display: flex;
                justify-content: space-between;
                align-items: center;
                border-bottom: 1px solid #334155;
            }
            .modal-header h3 { margin: 0; color: #38bdf8; }
            .close-btn { background: none; border: none; color: white; font-size: 1.5rem; cursor: pointer; }
            .modal-body { padding: 20px; overflow-y: auto; display: flex; flex-direction: column; gap: 10px; }
            .history-item { padding: 10px; border-radius: 8px; background: #1e293b; font-size: 0.9rem; border-left: 4px solid var(--accent-neon); }
            .history-item.model { border-left-color: var(--accent-purple); }
        </style>
    </head>
    <body>
        <header>
            <h1>🔮 Mary - Mentora</h1>
            <button class="history-btn" onclick="openHistory()">🗂️ Historial</button>
        </header>

        <div id="chat">
            <div class="msg mary">Hola Jaime soy Mary tu Mentora de Negocio en que puedo ayudarte?</div>
        </div>

        <div class="input-container">
            <input type="text" id="userInput" placeholder="Escribe tu consulta aquí, Jaime..." autofocus>
            <button class="send-btn" onclick="send()">Enviar</button>
        </div>

        <div id="modal">
            <div class="modal-content">
                <div class="modal-header">
                    <h3>Historial de Conversación</h3>
                    <button class="close-btn" onclick="closeHistory()">&times;</button>
                </div>
                <div class="modal-body" id="historyList">
                    <p style="color: #94a3b8; text-align: center;">No hay historial aún.</p>
                </div>
            </div>
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

                const loadId = appendMsg('Mary procesando...', 'mary');

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
                    conversationHistory.push({ role: "model", content: replyText });

                } catch (err) {
                    document.getElementById(loadId).remove();
                    appendMsg('⚠️ Error de conexión.', 'mary');
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

            function openHistory() {
                const list = document.getElementById('historyList');
                list.innerHTML = '';
                if (conversationHistory.length === 0) {
                    list.innerHTML = '<p style="color: #94a3b8; text-align: center;">El historial está vacío.</p>';
                } else {
                    conversationHistory.forEach(item => {
                        const div = document.createElement('div');
                        div.className = `history-item ${item.role}`;
                        div.innerHTML = `<strong>${item.role === 'user' ? 'Jaime' : 'Mary'}:</strong> ${item.content.substring(0, 150)}...`;
                        list.appendChild(div);
                    });
                }
                document.getElementById('modal').style.display = 'flex';
            }

            function closeHistory() {
                document.getElementById('modal').style.display = 'none';
            }
        </script>
    </body>
    </html>
    """

@app.post("/build")
def build_program(req: PromptRequest):
    api_key = os.environ.get("GEMINI_API_KEY")
    if not api_key:
        return {"agente": "Mary", "respuesta_ia": "Error: Falta GEMINI_API_KEY en Render."}
    
    # Usando gemini-2.5-flash y versión v1 estable para evitar conflictos
    url = f"https://generativelanguage.googleapis.com/v1/models/gemini-2.5-flash:generateContent?key={api_key}"
    
    system_instruction = (
        "Eres Mary, una agente de inteligencia artificial autónoma y experta Mentora de Negocios, desarrollo de software y trading algorítmico. "
        "Tu socio y usuario principal se llama JAIME. "
        "REGLA CRÍTICA: Debes dirigirte a él SIEMPRE por su nombre (Jaime) de forma natural y profesional. "
        "Sé directa, analítica, brillante y concisa."
    )
    
    contents = []
    contents.append({"role": "user", "parts": [{"text": f"Instrucción del sistema: {system_instruction}"}]})
    contents.append({"role": "model", "parts": [{"text": "Entendido. Hola Jaime, soy Mary, tu mentora de negocio. ¿En qué te puedo ayudar hoy?"}]})

    for msg in req.history:
        r = "user" if msg.role == "user" else "model"
        clean = msg.content.replace("<br>", "\n").replace("<pre><code>", "```").replace("</code></pre>", "```")
        contents.append({"role": r, "parts": [{"text": clean}]})

    payload = {"contents": contents}
    
    try:
        response = requests.post(url, json=payload, timeout=30)
        res_data = response.json()
        
        if "error" in res_data:
            error_msg = res_data["error"].get("message", "Error desconocido de API")
            return {"agente": "Mary", "respuesta_ia": f"⚠️ Error de Google AI: {error_msg}"}
        
        if "candidates" in res_data and len(res_data["candidates"]) > 0:
            ai_text = res_data["candidates"][0]["content"]["parts"][0]["text"]
        else:
            ai_text = "Respuesta vacía del modelo."
            
        ai_reply = ai_text.replace("\n", "<br>").replace("```python", "<pre><code>").replace("```", "</code></pre>")
        return {"agente": "Mary", "respuesta_ia": ai_reply}
        
    except Exception as e:
        return {"agente": "Mary", "respuesta_ia": f"⚠️ Excepción de conexión: {str(e)}"}
