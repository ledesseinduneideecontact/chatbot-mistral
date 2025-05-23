from fastapi import FastAPI
from fastapi.responses import HTMLResponse, JSONResponse
import httpx
import os
from dotenv import load_dotenv

# Charger les variables d'environnement
load_dotenv()

# Clé API Mistral depuis les variables d'environnement
API_KEY = os.getenv("MISTRAL_API_KEY")

app = FastAPI()

# Interface HTML simple
HTML_CONTENT = """
<!DOCTYPE html>
<html>
<head>
    <title>Chat Mistral</title>
    <style>
        body { 
            font-family: Arial; 
            max-width: 800px; 
            margin: 20px auto; 
            padding: 20px;
            background-color: #f0f2f5;
        }
        #chat { 
            height: 400px; 
            border: 1px solid #ddd; 
            overflow-y: auto; 
            padding: 20px; 
            margin-bottom: 20px;
            background: white;
            border-radius: 10px;
            box-shadow: 0 2px 4px rgba(0,0,0,0.1);
        }
        .message {
            margin-bottom: 15px;
            padding: 10px;
            border-radius: 8px;
        }
        .user-message {
            background-color: #e3f2fd;
            margin-left: 20%;
        }
        .bot-message {
            background-color: #f5f5f5;
            margin-right: 20%;
        }
        #input { 
            width: 80%; 
            padding: 10px;
            border: 1px solid #ddd;
            border-radius: 5px;
            margin-right: 10px;
        }
        button { 
            padding: 10px 20px;
            background-color: #0084ff;
            color: white;
            border: none;
            border-radius: 5px;
            cursor: pointer;
        }
        button:hover {
            background-color: #0066cc;
        }
    </style>
</head>
<body>
    <h1>Chat avec Mistral AI</h1>
    <div id="chat"></div>
    <div style="display: flex; gap: 10px;">
        <input type="text" id="input" placeholder="Écrivez votre message...">
        <button onclick="sendMessage()">Envoyer</button>
    </div>

    <script>
        async function sendMessage() {
            const input = document.getElementById('input');
            const message = input.value.trim();
            if (!message) return;

            // Afficher le message de l'utilisateur
            addMessage(message, 'user');
            input.value = '';

            try {
                const response = await fetch('/chat', {
                    method: 'POST',
                    headers: {'Content-Type': 'application/json'},
                    body: JSON.stringify({message: message})
                });
                const data = await response.json();
                addMessage(data.response, 'bot');
            } catch (error) {
                addMessage('Erreur: ' + error, 'bot');
            }
        }

        function addMessage(text, sender) {
            const chat = document.getElementById('chat');
            const div = document.createElement('div');
            div.className = `message ${sender}-message`;
            div.textContent = sender === 'user' ? 'Vous: ' + text : 'Mistral: ' + text;
            chat.appendChild(div);
            chat.scrollTop = chat.scrollHeight;
        }

        // Permettre l'envoi avec Entrée
        document.getElementById('input').addEventListener('keypress', function(e) {
            if (e.key === 'Enter') sendMessage();
        });
    </script>
</body>
</html>
"""

@app.get("/", response_class=HTMLResponse)
async def root():
    return HTML_CONTENT

@app.post("/chat")
async def chat(message: dict):
    if not API_KEY:
        return JSONResponse(
            status_code=500,
            content={"response": "Erreur: Clé API non configurée"}
        )
    
    try:
        async with httpx.AsyncClient() as client:
            response = await client.post(
                "https://api.mistral.ai/v1/chat/completions",
                headers={
                    "Content-Type": "application/json",
                    "Authorization": f"Bearer {API_KEY}"
                },
                json={
                    "model": "mistral-tiny",
                    "messages": [{"role": "user", "content": message["message"]}]
                }
            )
            
            if response.status_code == 200:
                data = response.json()
                return {"response": data['choices'][0]['message']['content']}
            else:
                return JSONResponse(
                    status_code=500,
                    content={"response": f"Erreur API Mistral: {response.text}"}
                )
            
    except Exception as e:
        return JSONResponse(
            status_code=500,
            content={"response": f"Erreur: {str(e)}"}
        ) 