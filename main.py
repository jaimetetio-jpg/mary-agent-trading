from fastapi import FastAPI, UploadFile, File, Form
from fastapi.responses import HTMLResponse, JSONResponse
import requests
import os
import json
import sqlite3
import base64

app = FastAPI(title="Mary Autonomous AI - Neural Engine Pro", version="6.19")

DB_FILE = "mary_memory_v19.db"

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
        
        cursor.execute("SELECT COUNT(*) FROM history")
        count = cursor.fetchone()[0]
        if count == 0:
            greeting = "¡Hola, Jaime! Soy Mary, tu mentora de negocio. ¿En qué puedo ayudarte?"
            cursor.execute("INSERT INTO history (role, content) VALUES (?, ?)", ("assistant", greeting))
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

@app.get("/", response_class=HTMLResponse)
def home():
    history = get_db_history()
    chat_html = ""
    for msg in history:
        role_class = "user" if msg["role"] == "user" else "mary"
        content_formatted = msg["content"].replace("\n", "<br>")
        chat_html += f'<div class="msg {role_class}">{content_formatted}</div>'

    html_template = """<!DOCTYPE html>
<html lang="es">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Mary - Neural Engine Pro v6.19</title>
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
            height: 100dvh;
            overflow: hidden;
        }
        header {
            background: linear-gradient(90deg, #1e293b, #0f172a);
            padding: 10px 15px;
            display: flex;
            justify-content: space-between;
            align-items: center;
            border-bottom: 2px solid rgba(16, 185, 129, 0.3);
            box-shadow: 0 4px 15px rgba(0, 0, 0, 0.5);
            flex-shrink: 0;
            z-index: 10;
        }
        h1 {
            margin: 0;
            font-size: 1.1rem;
            background: linear-gradient(to right, #34d399, #60a5fa);
            -webkit-background-clip: text;
            -webkit-text-fill-color: transparent;
            cursor: pointer;
        }
        .header-actions {
            display: flex;
            gap: 8px;
        }
        .btn-nav {
            background: rgba(16, 185, 129, 0.2);
            color: #34d399;
            border: 1px solid rgba(16, 185, 129, 0.4);
            padding: 5px 10px;
            border-radius: 8px;
            font-size: 0.8rem;
            cursor: pointer;
        }
        .btn-nav:hover {
            background: rgba(16, 185, 129, 0.4);
        }
        
        .view-container {
            flex: 1;
            display: none;
            flex-direction: column;
            overflow: hidden;
            max-width: 750px;
            width: 100%;
            margin: 0 auto;
            box-sizing: border-box;
        }
        .view-container.active {
            display: flex;
        }

        #homeView {
            justify-content: center;
            align-items: center;
            padding: 20px;
            text-align: center;
            gap: 20px;
        }
        .home-card {
            background: linear-gradient(145deg, #1e293b, #0f172a);
            border: 1px solid rgba(16, 185, 129, 0.4);
            border-radius: 16px;
            padding: 25px;
            max-width: 400px;
            width: 100%;
            box-shadow: 0 10px 25px rgba(0,0,0,0.5);
        }
        .home-card h2 {
            margin-top: 0;
            color: #34d399;
            font-size: 1.3rem;
        }
        .home-card p {
            color: #94a3b8;
            font-size: 0.9rem;
            margin-bottom: 20px;
        }
        .home-btn-group {
            display: flex;
            flex-direction: column;
            gap: 10px;
        }
        .btn-primary-action {
            background: linear-gradient(135deg, #10b981, #059669);
            color: white;
            border: none;
            padding: 12px;
            border-radius: 10px;
            font-weight: bold;
            cursor: pointer;
            font-size: 0.95rem;
        }

        #chat {
            flex: 1;
            overflow-y: auto;
            padding: 15px;
            display: flex;
            flex-direction: column;
            gap: 12px;
            width: 100%;
            box-sizing: border-box;
        }
        .msg {
            padding: 12px 16px;
            border-radius: 14px;
            max-width: 88%;
            word-break: break-word;
            line-height: 1.4;
            font-size: 0.95rem;
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
        .input-container {
            background: rgba(15, 23, 42, 0.98);
            padding: 10px 15px;
            display: flex;
            flex-direction: column;
            gap: 6px;
            width: 100%;
            box-sizing: border-box;
            border-top: 2px solid rgba(16, 185, 129, 0.3);
            flex-shrink: 0;
        }
        .input-row {
            display: flex;
            gap: 8px;
            align-items: center;
        }
        input[type="text"] {
            flex: 1;
            min-width: 0;
            background: #0b0f19;
            border: 1px solid #334155;
            border-radius: 10px;
            padding: 10px 12px;
            color: white;
            font-size: 1rem;
            outline: none;
        }
        input[type="text"]:focus {
            border-color: #10b981;
            box-shadow: 0 0 10px rgba(16, 185, 129, 0.4);
        }
        .file-upload-btn {
            background: #334155;
            color: white;
            padding: 0 10px;
            height: 42px;
            border-radius: 10px;
            display: flex;
            align-items: center;
            justify-content: center;
            cursor: pointer;
            font-size: 1.1rem;
            flex-shrink: 0;
        }
        input[type="file"] {
            display: none;
        }
        button.send-btn {
            background: linear-gradient(135deg, #10b981, #059669);
            color: white;
            border: none;
            padding: 0 14px;
            height: 42px;
            font-weight: bold;
            border-radius: 10px;
            cursor: pointer;
            flex-shrink: 0;
            font-size: 0.9rem;
        }
        #fileNameDisplay {
            font-size: 0.75rem;
            color: #34d399;
            padding-left: 2px;
            display: none;
        }

        #historyModal {
            display: none;
            position: fixed;
            top: 0; left: 0; width: 100%; height: 100%;
            background: rgba(0,0,0,0.85);
            z-index: 100;
            justify-content: center;
            align-items: center;
        }
        .modal-content {
            background: #1e293b;
            border: 1px solid #10b981;
            border-radius: 14px;
            width: 92%;
            max-width: 550px;
            max-height: 80vh;
            display: flex;
            flex-direction: column;
            overflow: hidden;
        }
        .modal-header {
            padding: 12px 16px;
            background: #0f172a;
            display: flex;
            justify-content: space-between;
            align-items: center;
            border-bottom: 1px solid #334155;
        }
        .modal-header h3 {
            margin: 0;
            color: #34d399;
            font-size: 1rem;
        }
        .close-modal {
            background: transparent;
            border: none;
            color: #94a3b8;
            font-size: 1.4rem;
            cursor: pointer;
        }
        .modal-body {
            padding: 15px;
            overflow-y: auto;
            flex: 1;
            font-size: 0.85rem;
            display: flex;
            flex-direction: column;
            gap: 10px;
        }
        .history-item {
            padding: 10px 12px;
            border-radius: 8px;
            background: #0f172a;
            border-left: 3px solid #10b981;
            cursor: pointer;
            transition: background 0.2s;
        }
        .history-item:hover {
            background: #162032;
        }
        .history-item.user-item {
            border-left-color: #3b82f6;
        }
        .history-role {
            font-weight: bold;
            font-size: 0.7rem;
            color: #94a3b8;
            margin-bottom: 3px;
        }
        .history-hint {
            font-size: 0.7rem;
            color: #34d399;
            margin-top: 5px;
            text-align: right;
        }
        .modal-footer {
            padding: 10px 16px;
            background: #0f172a;
            display: flex;
            justify-content: flex-end;
            border-top: 1px solid #334155;
        }
    </style>
</head>
<body>
    <header>
        <h1 onclick="switchView('home')">⚡ Mary Pro v6.19</h1>
        <div class="header-actions">
            <button class="btn-nav" type="button" onclick="switchView('home')">🏠 Inicio</button>
            <button class="btn-nav" type="button" onclick="startNewChatSession()">➕ Nuevo Chat</button>
            <button class="btn-nav" type="button" onclick="openHistoryModal()">📜 Historial</button>
        </div>
    </header>

    <div id="homeView" class="view-container active">
        <div class="home-card">
            <h2>Panel de Control</h2>
            <p>Bienvenida general de Mary, tu mentora de negocio e IA autónoma.</p>
            <div class="home-btn-group">
                <button class="btn-primary-action" type="button" onclick="switchView('chat')">💬 Ir al Chat Actual</button>
                <button class="btn-nav" type="button" onclick="startNewChatSession()" style="padding: 12px;">➕ Iniciar Nuevo Chat</button>
                <button class="btn-nav" type="button" onclick="openHistoryModal()" style="padding: 12px;">📜 Ver Historial de Conversación</button>
            </div>
        </div>
    </div>

    <div id="chatView" class="view-container">
        <div id="chat">
            __CHAT_CONTENT__
        </div>
        <div class="input-container">
            <div id="fileNameDisplay">📎 Archivo adjunto seleccionado</div>
            <div class="input-row">
                <label class="file-upload-btn" title="Adjuntar">
                    📁 <input type="file" id="fileInput" accept="image/*,text/*,.py,.txt,.csv" onchange="showFileName()">
                </label>
                <input type="text" id="userInput" placeholder="Escribe tu instrucción..." autocomplete="off">
                <button type="button" class="send-btn" id="sendButton" onclick="sendMsg()">Enviar</button>
            </div>
        </div>
    </div>

    <div id="historyModal">
        <div class="modal-content">
            <div class="modal-header">
                <h3>📜 Historial Permanente (Base de Datos)</h3>
                <button class="close-modal" type="button" onclick="closeHistoryModal()">&times;</button>
            </div>
            <div class="modal-body" id="modalHistoryBody">
                Cargando registros...
            </div>
            <div class="modal-footer">
                <button class="btn-nav" type="button" onclick="closeHistoryModal()">Cerrar</button>
            </div>
        </div>
    </div>

    <script>
        function switchView(viewName) {
            document.getElementById('homeView').classList.remove('active');
            document.getElementById('chatView').classList.remove('active');

            if (viewName === 'home') {
                document.getElementById('homeView').classList.add('active');
            } else if (viewName === 'chat') {
                document.getElementById('chatView').classList.add('active');
                const chat = document.getElementById('chat');
                chat.scrollTop = chat.scrollHeight;
            }
        }

        function startNewChatSession() {
            document.getElementById('chat').innerHTML = `
                <div class="msg mary">¡Hola, Jaime! Nuevo chat iniciado. ¿En qué puedo ayudarte hoy?</div>
            `;
            switchView('chat');
        }

        const chat = document.getElementById('chat');
        chat.scrollTop = chat.scrollHeight;

        const input = document.getElementById('userInput');
        const fileInput = document.getElementById('fileInput');
        const fileNameDisplay = document.getElementById('fileNameDisplay');
        const sendButton = document.getElementById('sendButton');

        input.addEventListener('keypress', (e) => {
            if (e.key === 'Enter') {
                e.preventDefault();
                sendMsg();
            }
        });

        async function sendMsg() {
            const text = input.value.trim();
            const file = fileInput.files[0];
            if (!text && !file) return;

            sendButton.disabled = true;
            sendButton.textContent = 'Enviando...';

            let userDisplay = text;
            if (file) userDisplay += `<br><em>[Archivo adjunto: ${file.name}]</em>`;
            appendMessage(userDisplay, 'user');

            input.value = '';
            fileInput.value = '';
            fileNameDisplay.style.display = 'none';

            const formData = new FormData();
            formData.append('instruction', text || "Analiza este archivo adjunto.");
            if (file) formData.append('file', file);

            const maryDiv = appendMessage('Pensando...', 'mary');

            try {
                const response = await fetch('/build', {
                    method: 'POST',
                    body: formData
                });

                const data = await response.json();
                
                if (!response.ok || data.error) {
                    maryDiv.innerHTML = '⚠️ Error: ' + (data.error || 'No se pudo procesar la solicitud.');
                } else {
                    let formatted = data.reply.replace(/&/g, '&amp;').replace(/</g, '&lt;').replace(/>/g, '&gt;');
                    formatted = formatted.replace(/\\n/g, '<br>');
                    maryDiv.innerHTML = formatted;
                }
            } catch (err) {
                maryDiv.innerHTML = '⚠️ Error de conexión con el servidor.';
            } finally {
                sendButton.disabled = false;
                sendButton.textContent = 'Enviar';
                chat.scrollTop = chat.scrollHeight;
                input.focus();
            }
        }

        function appendMessage(html, sender) {
            const div = document.createElement('div');
            div.className = `msg ${sender}`;
            div.innerHTML = html;
            chat.appendChild(div);
            chat.scrollTop = chat.scrollHeight;
            return div;
        }

        async function openHistoryModal() {
            document.getElementById('historyModal').style.display = 'flex';
            const modalBody = document.getElementById('modalHistoryBody');
            modalBody.innerHTML = 'Cargando registros...';
            try {
                const res = await fetch('/history');
                const data = await res.json();
                modalBody.innerHTML = '';
                if (!data.history || data.history.length === 0) {
                    modalBody.innerHTML = '<em style="color: #94a3b8;">No hay registros guardados todavía.</em>';
                    return;
                }
                data.history.forEach(item => {
                    const div = document.createElement('div');
                    div.className = `history-item ${item.role === 'user' ? 'user-item' : ''}`;
                    
                    const cleanContent = item.content.replace(/<br>/g, '\\n');
                    div.innerHTML = `
                        <div class="history-role">${item.role.toUpperCase()}</div>
                        <div>${item.content}</div>
                        <div class="history-hint">👆 Toca para continuar el tema con Mary</div>
                    `;
                    
                    div.onclick = async () => {
                        const textToResume = cleanContent.replace(/<[^>]*>?/gm, '');
                        closeHistoryModal();
                        switchView('chat');
                        
                        input.value = `Continuando sobre esto: "${textToResume}" -> `;
                        input.focus();
                    };
                    
                    modalBody.appendChild(div);
                });
            } catch(e) {
                modalBody.innerHTML = 'Error al cargar el historial.';
            }
        }

        function closeHistoryModal() {
            document.getElementById('historyModal').style.display = 'none';
        }

        function showFileName() {
            if (fileInput.files.length > 0) {
                fileNameDisplay.textContent = '📎 ' + fileInput.files[0].name;
                fileNameDisplay.style.display = 'block';
            } else {
                fileNameDisplay.style.display = 'none';
            }
        }
    </script>
</body>
</html>
"""
    return html_template.replace("__CHAT_CONTENT__", chat_html)

@app.get("/history")
def get_history():
    return {"history": get_db_history()}

@app.post("/build")
async def build_program(instruction: str = Form(""), file: UploadFile = File(None)):
    api_key = os.environ.get("OPENROUTER_API_KEY")
    if not api_key:
        err_msg = "Falta configurar la variable OPENROUTER_API_KEY en Render."
        save_to_db("user", instruction)
        save_to_db("assistant", f"⚠️ Error: {err_msg}")
        return JSONResponse(status_code=400, content={"error": err_msg})
    
    url = "https://openrouter.ai/api/v1/chat/completions"
    
    file_content_text = ""
    image_payload = None

    if file and file.filename:
        try:
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
        except Exception as e:
            print(f"Error leyendo archivo: {e}")

    full_user_input = instruction + file_content_text
    save_to_db("user", full_user_input)

    db_history = get_db_history()
    
    system_instruction = (
        "Eres Mary, la mentora de negocio de Jaime. Te diriges a él siempre por su nombre (Jaime) con un tono profesional, estratégico y enfocado en el éxito de sus proyectos y operaciones."
    )
    
    messages = [{"role": "system", "content": system_instruction}]
    
    # Tomamos solo los últimos 6 mensajes para evitar sobrepasar límites de tokens en OpenRouter
    recent_history = db_history[-7:] if len(db_history) > 7 else db_history
    
    for h in recent_history[:-1]:
        role = "user" if h["role"] == "user" else "assistant"
        messages.append({"role": role, "content": h["content"]})
        
    last_content = recent_history[-1]["content"]
    if image_payload:
        messages.append({
            "role": "user",
            "content": [
                {"type": "text", "text": last_content},
                {"type": "image_url", "image_url": {"url": image_payload}}
            ]
        })
    else:
        messages.append({"role": "user", "content": last_content})

    model_to_use = "deepseek/deepseek-chat"
    if image_payload:
        model_to_use = "openai/gpt-4o-mini"

    payload = {
        "model": model_to_use,
        "messages": messages,
        "max_tokens": 1000,
        "temperature": 0.3
    }

    headers = {
        "Authorization": f"Bearer {api_key}",
        "HTTP-Referer": "https://trading.onrender.com",
        "X-Title": "Mary AI Assistant Pro",
        "Content-Type": "application/json"
    }

    try:
        resp = requests.post(url, json=payload, headers=headers, timeout=50)
        res_data = resp.json()
        
        if resp.status_code != 200:
            error_message = res_data.get("error", {}).get("message", "Error desconocido de OpenRouter")
            full_response = f"⚠️ Error en API externa: {error_message}"
        else:
            full_response = res_data.get("choices", [{}])[0].get("message", {}).get("content", "Sin respuesta de la IA.")
            
    except Exception as e:
        full_response = f"⚠️ Error de conexión con el proveedor de IA: {str(e)}"
    
    save_to_db("assistant", full_response)
    return {"reply": full_response}
