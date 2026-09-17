from fastapi import FastAPI, UploadFile, File, Form
from fastapi.responses import HTMLResponse
import requests
import os
import re
import sqlite3
import base64

app = FastAPI(title="Mary Autonomous AI - Neural Engine Pro", version="5.8")

DB_FILE = "mary_memory.db"

def init_db():
    try:
        conn = sqlite3.connect(DB_FILE)
        cursor = conn.cursor()
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS history (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                role TEXT,
                content TEXT
            )
        ''')
        conn.commit()
        conn.close()
    except Exception as e:
        print(f"Error inicializando BD: {e}")

init_db()

def get_db_history():
    try:
        conn = sqlite3.connect(DB_FILE)
        cursor = conn.cursor()
        cursor.execute("SELECT role, content FROM history ORDER BY id ASC")
        rows = cursor.fetchall()
        conn.close()
        return [{"role": row[0], "content": row[1]} for row in rows]
    except Exception:
        return []

def save_to_db(role: str, content: str):
    try:
        conn = sqlite3.connect(DB_FILE)
        cursor = conn.cursor()
        cursor.execute("INSERT INTO history (role, content) VALUES (?, ?)", (role, content))
        conn.commit()
        conn.close()
    except Exception as e:
        print(f"Error guardando en BD: {e}")

def clear_db_history():
    try:
        conn = sqlite3.connect(DB_FILE)
        cursor = conn.cursor()
        cursor.execute("DELETE FROM history")
        conn.commit()
        conn.close()
    except Exception as e:
        print(f"Error limpiando BD: {e}")

@app.get("/", response_class=HTMLResponse)
def home():
    return """
    <!DOCTYPE html>
    <html lang="es">
    <head>
        <meta charset="UTF-8">
        <meta name="viewport" content="width=device-width, initial-scale=1.0">
        <title>Mary - Neural Engine Pro v5.8</title>
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
                padding: 12px 20px;
                display: flex;
                justify-content: space-between;
                align-items: center;
                border-bottom: 2px solid rgba(16, 185, 129, 0.3);
                box-shadow: 0 10px 25px -5px rgba(0, 0, 0, 0.5);
                z-index: 10;
            }
            h1 {
                margin: 0;
                font-size: 1.2rem;
                background: linear-gradient(to right, #34d399, #60a5fa);
                -webkit-background-clip: text;
                -webkit-text-fill-color: transparent;
            }
            .btn-clear {
                background: #ef4444;
                color: white;
                border: none;
                padding: 6px 12px;
                border-radius: 8px;
                font-size: 0.8rem;
                cursor: pointer;
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
                flex-direction: column;
                gap: 8px;
                max-width: 750px;
                width: 100%;
                margin: 0 auto;
                box-sizing: border-box;
                border-top: 2px solid rgba(16, 185, 129, 0.2);
            }
            .input-row {
                display: flex;
                gap: 10px;
            }
            input[type="text"] {
                flex: 1;
                background: #0b0f19;
                border: 1px solid #334155;
                border-radius: 12px;
                padding: 12px 16px;
                color: white;
                font-size: 1rem;
                outline: none;
            }
            input[type="text"]:focus {
                border-color: #10b981;
                box-shadow: 0 0 12px rgba(16, 185, 129, 0.4);
            }
            .file-upload-btn {
                background: #334155;
                color: white;
                padding: 0 14px;
                border-radius: 12px;
                display: flex;
                align-items: center;
                justify-content: center;
                cursor: pointer;
                font-size: 1.2rem;
                transition: background 0.2s;
            }
            .file-upload-btn:hover {
                background: #475569;
            }
            input[type="file"] {
                display: none;
            }
            button.send-btn {
                background: linear-gradient(135deg, #10b981, #059669);
                color: white;
                border: none;
                padding: 0 20px;
                font-weight: bold;
                border-radius: 12px;
                cursor: pointer;
            }
            #fileNameDisplay {
                font-size: 0.8rem;
                color: #34d399;
                padding-left: 5px;
                display: none;
            }
        </style>
    </head>
    <body>
        <header>
            <h1>⚡ Mary Pro v5.8</h1>
            <button class="btn-clear" onclick="clearMemory()">Borrar Memoria</button>
        </header>

        <div id="chat"></div>

        <div class="input-container">
            <div id="fileNameDisplay">📎 Archivo adjunto seleccionado</div>
            <div class="input-row">
                <label class="file-upload-btn" title="Adjuntar foto o archivo">
                    📁 <input type="file" id="fileInput" accept="image/*,text/*,.py,.txt,.csv" onchange="showFileName()">
                </label>
                <input type="text" id="userInput" placeholder="Escribe tu instrucción o pregunta..." autofocus>
                <button class="send-btn" onclick="send()">Enviar</button>
            </div>
        </div>

        <script>
            const chat = document.getElementById('chat');
            const input = document.getElementById('userInput');
            const fileInput = document.getElementById('fileInput');
            const fileNameDisplay = document.getElementById('fileNameDisplay');

            input.addEventListener('keypress', (e) => { if (e.key === 'Enter') send(); });

            async function loadHistory() {
                try {
                    const res = await fetch('/history');
                    const data = await res.json();
                    chat.innerHTML = '';
                    if (!data.history || data.history.length === 0) {
                        appendMsg('¡Hola, Jaime! Soy Mary, tu mentora de negocios. Estoy aquí para ayudarte a optimizar tus operaciones, maximizar oportunidades y tomar decisiones estratégicas con enfoque en resultados. ¿En qué aspecto de tu negocio necesitas avanzar hoy?', 'mary', true);
                    } else {
                        data.history.forEach(msg => {
                            appendMsg(msg.content, msg.role === 'user' ? 'user' : 'mary', true);
                        });
                    }
                } catch(e) {
                    appendMsg('Error cargando historial.', 'mary');
                }
            }

            function showFileName() {
                if (fileInput.files.length > 0) {
                    fileNameDisplay.textContent = '📎 ' + fileInput.files[0].name;
                    fileNameDisplay.style.display = 'block';
                } else {
                    fileNameDisplay.style.display = 'none';
                }
            }

            async function send() {
                const text = input.value.trim();
                const file = fileInput.files[0];
                if (!text && !file) return;

                let displayText = text;
                if (file) displayText += `<br><em>[Archivo adjunto: ${file.name}]</em>`;
                
                appendMsg(displayText, 'user', true);
                
                input.value = '';
                const loadId = appendMsg('Mary procesando...', 'mary');

                const formData = new FormData();
                formData.append('instruction', text || "Analiza este archivo adjunto.");
                if (file) {
                    formData.append('file', file);
                }

                try {
                    const res = await fetch('/build', {
                        method: 'POST',
                        body: formData
                    });
                    const data = await res.json();
                    
                    document.getElementById(loadId).remove();
                    const replyText = data.respuesta_ia || "Error de respuesta.";
                    
                    appendMsg(replyText, 'mary', true);
                    
                    fileInput.value = '';
                    fileNameDisplay.style.display = 'none';

                } catch (err) {
                    document.getElementById(loadId).remove();
                    appendMsg('Error de comunicación con el núcleo.', 'mary');
                }
            }

            async function clearMemory() {
                if(confirm('¿Deseas reiniciar toda la memoria de conversaciones?')) {
                    await fetch('/clear', { method: 'POST' });
                    loadHistory();
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

            loadHistory();
        </script>
    </body>
    </html>
    """

@app.get("/history")
def get_history():
    return {"history": get_db_history()}

@app.post("/clear")
def clear_history():
    clear_db_history()
    return {"status": "success"}

@app.post("/build")
async def build_program(instruction: str = Form(""), file: UploadFile = File(None)):
    api_key = os.environ.get("OPENROUTER_API_KEY")
    if not api_key:
        return {"agente": "Mary", "respuesta_ia": "⚠️ Error: Falta configurar la variable OPENROUTER_API_KEY en Render."}
    
    url = "https://openrouter.ai/api/v1/chat/completions"
    
    file_content_text = ""
    image_payload = None

    if file:
        contents = await file.read()
        mime = file.content_type or ""
        if "image" in mime:
            encoded_image = base64.b64encode(contents).decode('utf-8')
            image_payload = f"data:{mime};base64,{encoded_image}"
        else:
            try:
                file_content_text = f"\n\n--- Contenido del archivo {file.filename} ---\n" + contents.decode('utf-8')
            except:
                file_content_text = f"\n\n[Archivo recibido: {file.filename}]"

    full_user_input = instruction + file_content_text
    save_to_db("user", full_user_input)

    db_history = get_db_history()
    
    system_instruction = (
        "Eres Mary, la mentora de negocio de Jaime. Te diriges a él siempre por su nombre (Jaime) con un tono profesional, estratégico y enfocado en el éxito de sus proyectos y operaciones. "
        "Posees memoria completa de todas las iteraciones previas. Analiza con precisión cualquier imagen o archivo que te adjunten."
    )
    
    messages = [{"role": "system", "content": system_instruction}]
    
    for h in db_history:
        role = "user" if h["role"] == "user" else "assistant"
        content = h["content"]
        
        if h == db_history[-1] and image_payload and role == "user":
            messages.append({
                "role": "user",
                "content": [
                    {"type": "text", "text": content},
                    {"type": "image_url", "image_url": {"url": image_payload}}
                ]
            })
        else:
            messages.append({"role": role, "content": content})

    model_to_use = "deepseek/deepseek-chat"
    if image_payload:
        model_to_use = "openai/gpt-4o-mini"

    payload = {
        "model": model_to_use,
        "messages": messages,
        "temperature": 0.3
    }

    headers = {
        "Authorization": f"Bearer {api_key}",
        "HTTP-Referer": "https://trading.onrender.com",
        "X-Title": "Mary AI Assistant Pro",
        "Content-Type": "application/json"
    }

    try:
        response = requests.post(url, json=payload, headers=headers, timeout=45)
        res_data = response.json()
        
        if "error" in res_data:
            error_msg = res_data["error"].get("message", "Error desconocido en OpenRouter")
            return {"agente": "Mary", "respuesta_ia": f"⚠️ Nota de sistema: {error_msg}"}
        
        if "choices" in res_data and len(res_data["choices"]) > 0:
            ai_text = res_data["choices"][0]["message"]["content"]
        else:
            ai_text = f"Respuesta inesperada: {str(res_data)}"
            
        save_to_db("assistant", ai_text)

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
