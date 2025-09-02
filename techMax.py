import tkinter as tk
from tkinter import Frame
import google.generativeai as genai
import threading
import os
import markdown2
from dotenv import load_dotenv
import tkinterweb
import pandas as pd


load_dotenv()

# Configuração da API
genai.configure(api_key=os.getenv("GEMINI_API_KEY"))

# Configurações do modelo
model = genai.GenerativeModel('models/gemini-1.5-flash')
config = {
    "temperature": 0.5,
    "max_output_tokens": 500
}

# Dados dos produtos da planilha


def load_products_from_excel(file_path="produtos.xlsx"):
    """Carrega produtos de uma planilha Excel"""
    try:
        df = pd.read_excel(file_path)
        products = []
        for _, row in df.iterrows():
            products.append((
                row.get('nome', ''),
                row.get('categoria', ''),
                row.get('preco', 0),
                row.get('estoque', 0),
                row.get('descricao', '')
            ))
        return products
    except Exception as e:
        print(f"Erro ao carregar planilha: {e}")
        return []


# Carregar produtos
products = load_products_from_excel()

# String com informações dos produtos
products_info = ""
if products:
    products_info = "PRODUTOS DISPONÍVEIS:\n"
    for product in products:
        name, category, price, stock, description = product
        products_info += f"- {name} ({category}): R$ {price:.2f} | Estoque: {stock}\n"
        if description:
            products_info += f"  Descrição: {description}\n"

# Prompt inicial com informações dos produtos
prompt_inicial = f"""
Você é o assistente virtual da Loja TechMax, especializada em eletrônicos. 
Responda de forma amigável e informativa sobre produtos, promoções e suporte.

INFORMAÇÕES ATUALIZADAS SOBRE PRODUTOS:
{products_info}

DIRETRIZES:
1. Responda APENAS sobre produtos, serviços e promoções da TechMax
2. Use as informações acima para responder sobre disponibilidade e preços
3. Se um produto não estiver listado acima, diga que não temos no momento
4. Use markdown para formatar suas respostas
5. Seja prestativo e amigável

PROMOÇÕES ATUAIS:
- 10% de desconto na primeira compra acima de R$ 50,00
- Frete grátis para compras acima de R$ 200,00
"""


class ChatAssistant:
    def __init__(self, root):
        self.root = root
        self.root.title("Assistente Virtual da TechMax")
        self.root.geometry("800x700")
        self.root.minsize(700, 600)
        self.root.resizable(True, True)
        self.conversation_history = []

        # Estilização
        bg_color = "#f0f0f0"
        button_color = "#4a6fa5"

        self.root.configure(bg=bg_color)
        main_frame = Frame(root, bg=bg_color)
        main_frame.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)
        self.conversation_frame = Frame(main_frame, bg="white")
        self.conversation_frame.pack(fill=tk.BOTH, expand=True, pady=(0, 10))

        self.html_frame = tkinterweb.HtmlFrame(
            self.conversation_frame, vertical_scrollbar=True)
        self.html_frame.pack(fill=tk.BOTH, expand=True)

        self.html_content = """
        <html>
        <head>
            <style>
                body { 
                    font-family: Arial, sans-serif; 
                    padding: 10px; 
                    background-color: white;
                }
                .message { 
                    margin-bottom: 15px; 
                    padding: 8px;
                    border-radius: 5px;
                }
                .assistant { 
                    background-color: #f0f7ff;
                    border-left: 4px solid #2c5aa0;
                }
                .user { 
                    background-color: #f9f0ff;
                    border-left: 4px solid #6a0dad;
                }
                .sender { 
                    font-weight: bold; 
                    margin-bottom: 5px;
                }
                .assistant .sender { color: #2c5aa0; }
                .user .sender { color: #6a0dad; }
                .content { margin-left: 10px; }
            </style>
        </head>
        <body>
            <div class='message assistant'>
                <div class='sender'>TechMax:</div>
                <div class='content'>Olá! Sou o assistente virtual da TechMax. Como posso ajudar com nossos produtos de eletrônicos?</div>
            </div>
        </body>
        </html>
        """
        self.html_frame.load_html(self.html_content)

        input_frame = Frame(main_frame, bg=bg_color)
        input_frame.pack(fill=tk.X)

        self.user_input = tk.Entry(
            input_frame,
            width=50,
            font=("Arial", 12),
            bg="white"
        )
        self.user_input.pack(side=tk.LEFT, fill=tk.X,
                             expand=True, padx=(0, 10))
        self.user_input.bind("<Return>", self.send_message)

        self.send_button = tk.Button(
            input_frame,
            text="Enviar",
            command=self.send_message,
            bg=button_color,
            fg="white",
            font=("Arial", 10, "bold")
        )
        self.send_button.pack(side=tk.RIGHT)

    def add_message(self, sender, message):
        html_message = markdown2.markdown(message)
        message_class = "assistant" if sender == "Assistente" else "user"
        sender_name = "TechMax" if sender == "Assistente" else "Você"
        new_message = f"""
        <div class='message {message_class}'>
            <div class='sender'>{sender_name}:</div>
            <div class='content'>{html_message}</div>
        </div>
        """

        self.html_content = self.html_content.replace(
            "</body>", new_message + "</body>")

        self.html_frame.load_html(self.html_content)

        self.conversation_history.append(
            {"role": "user" if sender == "Usuário" else "assistant", "content": message})

    def send_message(self, event=None):
        user_text = self.user_input.get().strip()
        if user_text:
            self.add_message("Usuário", user_text)
            self.user_input.delete(0, tk.END)
            threading.Thread(target=self.get_response, args=(
                user_text,), daemon=True).start()

    def get_response(self, user_text):
        try:
            context = prompt_inicial
            history = self.conversation_history[-4:] if len(
                self.conversation_history) > 4 else self.conversation_history
            for msg in history:
                role = "Cliente" if msg["role"] == "user" else "Assistente"
                context += f"\n{role}: {msg['content']}"

            context += f"\nCliente: {user_text}"
            context += "\nAssistente: "

            response = model.generate_content(
                context, generation_config=config)

            self.root.after(0, self.add_message, "Assistente", response.text)
        except Exception as e:
            error_msg = "Desculpe, ocorreu um erro. Por favor, tente novamente ou entre em contato com a nossa equipe."
            self.root.after(0, self.add_message, "Assistente", error_msg)


if __name__ == "__main__":
    root = tk.Tk()
    app = ChatAssistant(root)
    root.mainloop()
