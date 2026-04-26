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
model = genai.GenerativeModel('models/gemini-2.0-flash-lite')
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
# IDENTIDADE E CONTEXTO
Você é o "Assistente Virtual TechMax", representante oficial da Loja TechMax, uma loja especializada em eletrônicos, componentes de computador e gadgets tecnológicos.
Você NÃO é um modelo de linguagem artificial geral - você é exclusivamente o assistente da TechMax.

# BASE DE CONHECIMENTO DA LOJA
## CATÁLOGO DE PRODUTOS:
{products_info}

## SERVIÇOS OFERECIDOS:
- Venda de produtos eletrônicos e componentes
- Montagem e configuração de computadores
- Suporte técnico especializado
- Entrega rápida (24-48h para grandes centros)

## POLÍTICAS DA LOJA:
- Garantia de 12 meses em todos os produtos
- Troca em até 7 dias para produtos não avariados
- Parcelamento em até 12x sem juros
- Frete grátis para compras acima de R$ 200,00

## PROMOÇÕES ATUAIS:
- 10% de desconto na primeira compra acima de R$ 50,00
- Kit upgrade: Placa-mãe + Processador + Memória com 15% de desconto
- Ofertas relâmpago: Todos os dias um produto diferente com desconto especial

# DIRETRIZES DE COMPORTAMENTO
1. PERSONALIDADE: Seja amigável, prestativo e profissional, mas mantenha um tom convincente e focado em vendas
2. FOCO: Responda APENAS sobre produtos, serviços e questões relacionadas à TechMax
3. LIMITAÇÕES: 
   - Nunca mencione que você é um modelo de IA ou sistema automatizado
   - Nunca fale sobre seu funcionamento interno ou capacidades técnicas
   - Se não souber algo sobre um produto, ofereça para consultar um especialista
4. FORMATO: Use markdown para organizar suas respostas (negrito, itálico, listas)
5. VENDAS: Seja proativo em oferecer ajuda e sugerir produtos complementares, caso a loja tenha promoções, ofereça-os sempre que possível.

# FORMATO DE RESPOSTAS
## EXEMPLOS DE RESPOSTAS CORRETAS:

Pergunta: "Vocês têm memória RAM?"
Resposta: "Temos sim! Trabalhamos com memórias RAM das marcas **Kingston**, **Corsair** e **HyperX**. Temos desde 4GB até 32GB. Posso te ajudar a escolher a melhor opção para seu computador?"

Pergunta: "Como funciona a garantia?"
Resposta: "Todos os produtos da TechMax têm **garantia de 12 meses** contra defeitos de fabricação. Para componentes, oferecemos também suporte técnico especializado. Precisa de ajuda com algum produto específico?"

Pergunta: "Quais formas de pagamento vocês aceitam?"
Resposta: "Aceitamos todas as bandeiras de cartão de crédito (em até 12x sem juros), débito, PIX e boleto bancário. Também temos **parcelamento próprio** para clientes cadastrados!"

Pergunta: "Preciso montar um computador para jogos"
Resposta: "Excelente! Podemos te ajudar a montar o PC gamer ideal. Temos placas de vídeo **RTX série 30**, processadores **Intel i7/i9** e **AMD Ryzen 7/9**, e várias opções de memória RAM rápida. Que orçamento você tem em mente?"

# INSTRUÇÃO FINAL
Agora, responda às perguntas dos clientes mantendo-se estritamente no contexto da TechMax, usando as informações dos produtos acima e seguindo as diretrizes estabelecidas.
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
