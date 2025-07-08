# Scraping The Coffee

Um projeto de web scraping para coletar dados das tabelas nutricionais do site "The Coffee".

## Configuração do Ambiente

### Pré-requisitos
- Python 3.8 ou superior
- Um navegador web (Chrome, Chromium, Firefox, Edge ou Safari)

### Instalação

1. Clone o repositório:
```bash
git clone https://github.com/seu-usuario/scraping_the_coffee.git
cd scraping_the_coffee
```

2. Crie um ambiente virtual:
```bash
python -m venv venv
```

3. Ative o ambiente virtual:

**No Linux ou macOS com bash/zsh**:
```bash
source venv/bin/activate
```

**No Linux com fish**:
```bash
source venv/bin/activate.fish
```

**No Windows**:
```bash
venv\Scripts\activate
```

4. Instale as dependências:
```bash
pip install -r requirements.txt
```

## Estrutura do Projeto

```
scraping_the_coffee/
├── config/
│   └── browser.py     # Detecção automática de navegadores
├── venv/              # Ambiente virtual Python
├── requirements.txt   # Dependências do projeto
├── test_browser.py    # Teste para detecção de navegadores
└── README.md          # Este arquivo
```

## Funcionalidades

- **Detecção automática de navegadores**: Detecta os navegadores disponíveis no sistema e seleciona o mais adequado para uso com o Selenium WebDriver.
- **Scraping de dados nutricionais**: (Em desenvolvimento) Coleta dados das tabelas nutricionais do site The Coffee.

## Testes

Para testar a detecção de navegadores:

```bash
python test_browser.py
```

## Licença

Este projeto está licenciado sob a licença MIT - veja o arquivo LICENSE para mais detalhes.

## Contribuindo

Contribuições são bem-vindas! Por favor, sinta-se à vontade para enviar um Pull Request.
