import tkinter as tk
from tkinter import ttk, scrolledtext
import requests
import json

class ChatApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Chat Mistral AI")
        self.root.geometry("600x800")
        
        # Configuration de la clé API
        self.api_key = "k1T5pJrbwL5mdIPyeLgt44vBeS8qMdcF"
        
        # Création de l'interface
        self.create_widgets()
        
    def create_widgets(self):
        # Zone de chat
        self.chat_area = scrolledtext.ScrolledText(self.root, wrap=tk.WORD, width=60, height=30)
        self.chat_area.pack(padx=10, pady=10, expand=True, fill='both')
        
        # Frame pour l'entrée et le bouton
        input_frame = ttk.Frame(self.root)
        input_frame.pack(padx=10, pady=(0, 10), fill='x')
        
        # Zone de texte
        self.input_field = ttk.Entry(input_frame)
        self.input_field.pack(side='left', expand=True, fill='x', padx=(0, 10))
        
        # Bouton d'envoi
        send_button = ttk.Button(input_frame, text="Envoyer", command=self.send_message)
        send_button.pack(side='right')
        
        # Bind la touche Enter
        self.input_field.bind('<Return>', lambda e: self.send_message())
        
        # Style
        self.chat_area.tag_configure('user', foreground='blue')
        self.chat_area.tag_configure('bot', foreground='green')
        
    def send_message(self):
        message = self.input_field.get().strip()
        if not message:
            return
            
        # Afficher le message de l'utilisateur
        self.chat_area.insert(tk.END, "Vous: " + message + "\n", 'user')
        self.chat_area.see(tk.END)
        
        # Vider le champ de texte
        self.input_field.delete(0, tk.END)
        
        try:
            # Appel à l'API Mistral
            response = requests.post(
                "https://api.mistral.ai/v1/chat/completions",
                headers={
                    "Content-Type": "application/json",
                    "Authorization": f"Bearer {self.api_key}"
                },
                json={
                    "model": "mistral-tiny",
                    "messages": [{"role": "user", "content": message}]
                }
            )
            
            if response.status_code == 200:
                bot_response = response.json()['choices'][0]['message']['content']
                self.chat_area.insert(tk.END, "Mistral: " + bot_response + "\n\n", 'bot')
            else:
                self.chat_area.insert(tk.END, f"Erreur: {response.text}\n\n", 'bot')
                
        except Exception as e:
            self.chat_area.insert(tk.END, f"Erreur: {str(e)}\n\n", 'bot')
            
        self.chat_area.see(tk.END)

if __name__ == "__main__":
    root = tk.Tk()
    app = ChatApp(root)
    root.mainloop() 