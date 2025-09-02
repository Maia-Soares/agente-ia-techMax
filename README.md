# Assistente Virtual TechMax
Este projeto é um assistente virtual para uma loja de eletrônicos (TechMax) que utiliza a API do Google Gemini para responder perguntas dos clientes sobre produtos, promoções e suporte. A interface gráfica foi desenvolvida em Python com Tkinter e suporta renderização de markdown.
## Funcionalidades
- Interface gráfica amigável com histórico de conversa.
- Integração com a API do Google Gemini para geração de respostas.
- Suporte a markdown nas respostas.
- Carregamento de dados de produtos a partir de uma planilha Excel.
## Pré-requisitos
- Python 3.7 ou superior
- Conta no Google AI Studio para obter uma chave de API do Gemini
- Tkinter para interface gráfica
- tkinterweb para renderização de HTML/Markdown
- Pandas para manipulação de planilhas Excel
- python-dotenv para gerenciamento de variáveis de ambiente
## Instalação
1. Clone o repositório ou baixe os arquivos do projeto.
2. Instale as dependências necessárias:
```bash
pip install -r requirements.txt
```
3. Crie um arquivo `.env` na raiz do projeto e adicione sua chave de API do Gemini:
```
GEMINI_API_KEY=sua_chave_aqui
```
4. Crie uma planilha `produtos.xlsx` com as colunas: nome, categoria, preco, estoque, descricao. Você pode usar o script `dados_produtos.py` para gerar um exemplo.
## Uso
Execute o aplicativo com o comando:
```bash
python TechMax.py
```
A janela do assistente virtual será aberta. Digite suas perguntas no campo de entrada e pressione Enter ou clique no botão "Enviar".
## Estrutura do Projeto
- `TechMax.py`: Arquivo principal com a interface gráfica e lógica de integração com a API.
- `.env`: Arquivo de configuração para variáveis de ambiente (não versionado).
- `produtos.xlsx`: Planilha com informações dos produtos (não versionada).
- `dados_produtos.py`: Script opcional para gerar a planilha de produtos.
## Personalização
- **Prompt do Assistente**: Edite a variável `prompt_inicial` no código para alterar o comportamento e as respostas do assistente.
- **Produtos**: Atualize a planilha `produtos.xlsx` para refletir os produtos e estoques atuais.
- **Estilo**: Modifique o CSS embutido no código para alterar a aparência da interface.
## Limitações
- A planilha de produtos é carregada apenas no início da execução.
- A API do Gemini tem limites de uso gratuito. Monitorar o consumo para evitar custos inesperados.
