From fastapi import FastAPI, HTTPExceptionFrom fastapi import FastAPI, HTTPException
from fastapi.responses import HTMLResponse
from pydantic import BaseModel
import os
import time
import requests

app = FastAPI(title="Mary Autonomous AI", version="3.7.0")

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
        <title>Mary - Smart Neural Engine</title>
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
            <h1>🔮 Mary - Smart Autonomous Engine</h1>
        </header>

        <div id="chat">
            <div class="msg mary">¡Hola, jefe! Memoria inteligente y núcleo optimizado activos. ¿En qué proyecto o estrategia avanzamos hoy?</div>
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

                // Guardar en el historial local
                conversationHistory.push({ role: "user", content: text });

                const loadId = appendMsg('Mary procesando con memoria activa...', 'mary');

                try {
                    const res = await fetch('/build', {
                        method: 'POST',
                        headers: { 'Content-Type': 'application/json' },
                        body: JSON.stringify({ instruction: text, history: conversationHistory })
                    });
                    const data = await res.json();
                    
                    document.getElementById(loadId).remove();
                    const replyText = data.respuesta_ia || "Error: Respuesta vacía del servidor.";
                    
                    appendMsg(replyText, 'mary', true);
                    
                    // Guardar respuesta de la IA en el historial
                    conversationHistory.push({ role: "model", content: replyText });

                } catch (err) {
                    document.getElementById(loadId).remove();
                    appendMsg('Error de comunicación con el núcleo inteligente.', 'mary');
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
        return {"agente": "Mary", "respuesta_ia": "Error: Falta configurar la GEMINI_API_KEY en Render."}
    
    url = f"https://generativelanguage.googleapis.com/v1beta/models/gemini-3.6-flash:generateContent?key={api_key}"
    
    # Instrucción de sistema experta (Smart Training)
    system_instruction = (
        "Eres Mary, una agente de software autónoma de élite y asistente de trading experta. "
        "Posees un razonamiento avanzado, alta capacidad de análisis técnico y destreza en programación web y Python. "
        "Sé directa, inteligente, clara y concisa. Estructura el código de manera impecable y limpia."
    )
    
    # Construir contents formateando todo el historial de la conversación para darle memoria real
    contents = []
    
    # Inyectar prompt del sistema como contexto inicial
    contents.append({
        "role": "user",
        "parts": [{"text": f"[Instrucción del Sistema]: {system_instruction}"}]
    })
    contents.append({
        "role": "model",
        "parts": [{"text": "Entendido, jefe. Mantendré un perfil inteligente, técnico, directo y con memoria activa de nuestra sesión."}]
    })

    # Añadir todo el historial previo recibido desde el navegador
    for msg in req.history:
        # La API de Gemini espera los roles como 'user' y 'model'
        api_role = "user" if msg.role == "user" else "model"
        # Limpiamos etiquetas HTML previas del historial del modelo para enviarlas limpias
        clean_content = msg.content.replace("<br>", "\n").replace("<pre><code>", "```").replace("</code></pre>", "```")
        contents.append({
            "role": api_role,
            "parts": [{"text": clean_content}]
        })

    payload = {
        "contents": contents
    }
    
    max_retries = 3
    backoff_factor = 2

    for attempt in range(max_retries):
        try:
            response = requests.post(url, json=payload, timeout=35)
            res_data = response.json()
            
            if "error" in res_data:
                error_msg = res_data["error"].get("message", "Error desconocido de API")
                if "high demand" in error_msg.lower() or "resourceexhausted" in error_msg.lower() or "429" in str(response.status_code):
                    if attempt < max_retries - 1:
                        time.sleep(backoff_factor ** (attempt + 1))
                        continue
                return {"agente": "Mary", "respuesta_ia": f"⚠️ Error de Google AI: {error_msg}"}
            
            if "candidates" in res_data and len(res_data["candidates"]) > 0:
                ai_text = res_data["candidates"][0]["content"]["parts"][0]["text"]
            else:
                ai_text = f"Respuesta inesperada de Google: {str(res_data)}"
                
            ai_reply = ai_text.replace("\n", "<br>").replace("```python", "<pre><code>").replace("```", "</code></pre>")
            
            return {
                "agente": "Mary",
                "respuesta_ia": ai_reply
            }
        except Exception as e:
            if attempt < max_retries - 1:
                time.sleep(backoff_factor ** (attempt + 1))
                continue
            return {"agente": "Mary", "respuesta_ia": f"⚠️ Excepción en el servidor tras {max_retries} intentos: {str(e)}"}
    
    return {"agente": "Mary", "respuesta_ia": "⚠️ El servidor de Google está saturado temporalmente. Por favor, intenta de nuevo en unos segundos."}


Recupere el código viejo que funcionó la última vez sin dañar nada puedes agregar que ella me diga Hola Jaime Soy Mary Tu Mentora De Negocio En Que Puedo Ayudarte?  Y aparte agregar un historial que guarde nuestras conversaciones?
from fastapi.responses import HTMLResponse
from pydantic import BaseModel
import os
import time
import requests

app = FastAPI(title="Mary Autonomous AI", version="3.7.0")

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
        <title>Mary - Smart Neural Engine</title>
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
            <h1>🔮 Mary - Smart Autonomous Engine</h1>
        </header>

        <div id="chat">
            <div class="msg mary">¡Hola, jefe! Memoria inteligente y núcleo optimizado activos. ¿En qué proyecto o estrategia avanzamos hoy?</div>
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

                // Guardar en el historial local
                conversationHistory.push({ role: "user", content: text });

                const loadId = appendMsg('Mary procesando con memoria activa...', 'mary');

                try {
                    const res = await fetch('/build', {
                        method: 'POST',
                        headers: { 'Content-Type': 'application/json' },
                        body: JSON.stringify({ instruction: text, history: conversationHistory })
                    });
                    const data = await res.json();
                    
                    document.getElementById(loadId).remove();
                    const replyText = data.respuesta_ia || "Error: Respuesta vacía del servidor.";
                    
                    appendMsg(replyText, 'mary', true);
                    
                    // Guardar respuesta de la IA en el historial
                    conversationHistory.push({ role: "model", content: replyText });

                } catch (err) {
                    document.getElementById(loadId).remove();
                    appendMsg('Error de comunicación con el núcleo inteligente.', 'mary');
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
        return {"agente": "Mary", "respuesta_ia": "Error: Falta configurar la GEMINI_API_KEY en Render."}
    
    url = f"https://generativelanguage.googleapis.com/v1beta/models/gemini-3.6-flash:generateContent?key={api_key}"
    
    # Instrucción de sistema experta (Smart Training)
    system_instruction = (
        "Eres Mary, una agente de software autónoma de élite y asistente de trading experta. "
        "Posees un razonamiento avanzado, alta capacidad de análisis técnico y destreza en programación web y Python. "
        "Sé directa, inteligente, clara y concisa. Estructura el código de manera impecable y limpia."
    )
    
    # Construir contents formateando todo el historial de la conversación para darle memoria real
    contents = []
    
    # Inyectar prompt del sistema como contexto inicial
    contents.append({
        "role": "user",
        "parts": [{"text": f"[Instrucción del Sistema]: {system_instruction}"}]
    })
    contents.append({
        "role": "model",
        "parts": [{"text": "Entendido, jefe. Mantendré un perfil inteligente, técnico, directo y con memoria activa de nuestra sesión."}]
    })

    # Añadir todo el historial previo recibido desde el navegador
    for msg in req.history:
        # La API de Gemini espera los roles como 'user' y 'model'
        api_role = "user" if msg.role == "user" else "model"
        # Limpiamos etiquetas HTML previas del historial del modelo para enviarlas limpias
        clean_content = msg.content.replace("<br>", "\n").replace("<pre><code>", "```").replace("</code></pre>", "```")
        contents.append({
            "role": api_role,
            "parts": [{"text": clean_content}]
        })

    payload = {
        "contents": contents
    }
    
    max_retries = 3
    backoff_factor = 2

    for attempt in range(max_retries):
        try:
            response = requests.post(url, json=payload, timeout=35)
            res_data = response.json()
            
            if "error" in res_data:
                error_msg = res_data["error"].get("message", "Error desconocido de API")
                if "high demand" in error_msg.lower() or "resourceexhausted" in error_msg.lower() or "429" in str(response.status_code):
                    if attempt < max_retries - 1:
                        time.sleep(backoff_factor ** (attempt + 1))
                        continue
                return {"agente": "Mary", "respuesta_ia": f"⚠️ Error de Google AI: {error_msg}"}
            
            if "candidates" in res_data and len(res_data["candidates"]) > 0:
                ai_text = res_data["candidates"][0]["content"]["parts"][0]["text"]
            else:
                ai_text = f"Respuesta inesperada de Google: {str(res_data)}"
                
            ai_reply = ai_text.replace("\n", "<br>").replace("```python", "<pre><code>").replace("```", "</code></pre>")
            
            return {
                "agente": "Mary",
                "respuesta_ia": ai_reply
            }
        except Exception as e:
            if attempt < max_retries - 1:
                time.sleep(backoff_factor ** (attempt + 1))
                continue
            return {"agente": "Mary", "respuesta_ia": f"⚠️ Excepción en el servidor tras {max_retries} intentos: {str(e)}"}
    
    return {"agente": "Mary", "respuesta_ia": "⚠️ El servidor de Google está saturado temporalmente. Por favor, intenta de nuevo en unos segundos."}


Recupere el código viejo que funcionó la última vez sin dañar nada puedes agregar que ella me diga Hola Jaime Soy Mary Tu Mentora De Negocio En Que Puedo Ayudarte?  Y aparte agregar un historial que guarde nuestras conversaciones?
