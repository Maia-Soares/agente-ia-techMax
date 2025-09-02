import pandas as pd

# Dados dos produtos
produtos = [
    {
        "nome": "Smartphone Samsung Galaxy A54 5G",
        "categoria": "Smartphones",
        "preco": 1799.90,
        "estoque": 15,
        "descricao": "Smartphone Samsung Galaxy A54 5G, 128GB, 8GB RAM, Tela 6.4\", Câmera Tripla 50MP, Android 13"
    },
    {
        "nome": "Notebook Gamer Acer Nitro 5",
        "categoria": "Notebooks",
        "preco": 4299.90,
        "estoque": 8,
        "descricao": "Notebook Gamer Acer Nitro 5, Intel i5-11400H, GTX 1650, 8GB RAM, SSD 512GB, 15.6\" FHD 144Hz"
    },
    {
        "nome": "Teclado Mecânico Redragon Kumara",
        "categoria": "Periféricos",
        "preco": 229.90,
        "estoque": 42,
        "descricao": "Teclado Mecânico Redragon Kumara, RGB, Switch Outemu Blue, ABNT2, Preto"
    },
    {
        "nome": "Mouse Gamer Logitech G502 HERO",
        "categoria": "Periféricos",
        "preco": 299.90,
        "estoque": 36,
        "descricao": "Mouse Gamer Logitech G502 HERO, 25600 DPI, RGB, 11 Botões, Ajuste de Peso"
    },
    {
        "nome": "Headset Gamer HyperX Cloud Stinger",
        "categoria": "Áudio",
        "preco": 299.90,
        "estoque": 28,
        "descricao": "Headset Gamer HyperX Cloud Stinger, Drivers 50mm, Microfone com Cancelamento de Ruído"
    },
    {
        "nome": "Monitor Gamer AOC Hero 24\"",
        "categoria": "Monitores",
        "preco": 899.90,
        "estoque": 12,
        "descricao": "Monitor Gamer AOC 24\" LED, 144Hz, 1ms, FHD, HDMI/DisplayPort, FreeSync"
    },
    {
        "nome": "SSD Kingston NV2 1TB NVMe",
        "categoria": "Armazenamento",
        "preco": 399.90,
        "estoque": 50,
        "descricao": "SSD Kingston NV2 1TB, M.2 NVMe, PCIe 4.0, Leitura 3500MB/s, Gravação 2100MB/s"
    },
    {
        "nome": "Memória RAM Kingston Fury 8GB",
        "categoria": "Memória",
        "preco": 199.90,
        "estoque": 75,
        "descricao": "Memória RAM Kingston Fury Beast, 8GB, 3200MHz, DDR4, CL16"
    },
    {
        "nome": "Processador AMD Ryzen 5 5600G",
        "categoria": "Processadores",
        "preco": 899.90,
        "estoque": 18,
        "descricao": "Processador AMD Ryzen 5 5600G, 6-Core, 12-Threads, 3.9GHz, Video Integrado Radeon"
    },
    {
        "nome": "Placa de Vídeo RTX 3060 Galax",
        "categoria": "Placas de Vídeo",
        "preco": 2199.90,
        "estoque": 6,
        "descricao": "Placa de Vídeo Galax GeForce RTX 3060, 12GB GDDR6, 192-bit, LHR"
    },
    {
        "nome": "Fonte Gamemax 600W 80 Plus Bronze",
        "categoria": "Fontes",
        "preco": 299.90,
        "estoque": 25,
        "descricao": "Fonte Gamemax 600W, 80 Plus Bronze, PFC Ativo, Cabos Flat"
    },
    {
        "nome": "Webcam Logitech C920x",
        "categoria": "Webcams",
        "preco": 499.90,
        "estoque": 20,
        "descricao": "Webcam Logitech C920x, Full HD 1080p, Microfone Embutido, Compatível com Skype/Zoom"
    },
    {
        "nome": "Roteador TP-Link Archer C6",
        "categoria": "Redes",
        "preco": 249.90,
        "estoque": 30,
        "descricao": "Roteador TP-Link Archer C6, Wi-Fi Dual Band, 1200Mbps, 4 Antenas, Gigabit"
    },
    {
        "nome": "Tablet Samsung Galaxy Tab S6 Lite",
        "categoria": "Tablets",
        "preco": 1499.90,
        "estoque": 10,
        "descricao": "Tablet Samsung Galaxy Tab S6 Lite, 64GB, Tela 10.4\", S Pen Inclusa, Android"
    },
    {
        "nome": "Smartwatch Samsung Galaxy Watch 4",
        "categoria": "Wearables",
        "preco": 899.90,
        "estoque": 14,
        "descricao": "Smartwatch Samsung Galaxy Watch 4, 40mm, Bluetooth, Monitor de Saúde, Android Wear"
    },
    {
        "nome": "Caixa de Som JBL Flip 6",
        "categoria": "Áudio",
        "preco": 699.90,
        "estoque": 22,
        "descricao": "Caixa de Som JBL Flip 6, Bluetooth, À Prova D'água, 12 Horas de Bateria"
    },
    {
        "nome": "Impressora Multifuncional Epson EcoTank L3210",
        "categoria": "Impressoras",
        "preco": 1299.90,
        "estoque": 9,
        "descricao": "Impressora Multifuncional Epson EcoTank L3210, Tanque de Tinta, Wi-Fi"
    },
    {
        "nome": "Smart TV LED 50\" Samsung 50CU7700",
        "categoria": "TVs",
        "preco": 2199.90,
        "estoque": 7,
        "descricao": "Smart TV LED 50\" Samsung, 4K UHD, Crystal Processor, Tizen, 3 HDMI"
    },
    {
        "nome": "Console PlayStation 5",
        "categoria": "Consoles",
        "preco": 3899.90,
        "estoque": 3,
        "descricao": "Console PlayStation 5, SSD 825GB, Controle DualSense, Edição Digital"
    },
    {
        "nome": "Xbox Series S",
        "categoria": "Consoles",
        "preco": 2299.90,
        "estoque": 5,
        "descricao": "Console Xbox Series S, 512GB SSD, 1440p, Ray Tracing, Carbon Black"
    }
]

# Criar DataFrame e salvar como Excel
df = pd.DataFrame(produtos)
df.to_excel("produtos.xlsx", index=False)

print("Arquivo produtos.xlsx criado com sucesso!")
