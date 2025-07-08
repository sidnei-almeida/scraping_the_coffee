# 🍵 Scraping The Coffee

Sistema profissional de web scraping para coletar dados nutricionais completos do site "The Coffee". Extrai informações de todos os 61 produtos disponíveis no cardápio com interface bonita e amigável.

## ✨ Características

- 🎯 **Interface profissional** com menu interativo colorido
- 🚀 **Coleta automatizada** de todos os produtos do site
- 📊 **Dados nutricionais completos** por 100ml
- 🧪 **Modo teste** para validação (3 produtos)
- 📝 **Exportação em CSV** com encoding UTF-8
- 🔧 **Detecção automática de navegador**
- 🛡️ **Tratamento robusto de erros**
- ⚡ **Feedback visual em tempo real**

## 📋 Dados Coletados

O sistema extrai as seguintes informações de cada produto:

- **Nome do produto**
- **URL de origem**
- **Categoria** (Bebidas, Doces, Comidas, etc.)
- **Porção** (flexível: copos, fatias, unidades, ml, g)
- **Valor energético** (kcal) por 100ml
- **Carboidratos** (g) por 100ml
- **Proteínas** (g) por 100ml
- **Gorduras totais** (g) por 100ml
- **Gorduras saturadas** (g) por 100ml
- **Gorduras trans** (g) por 100ml
- **Fibras alimentares** (g) por 100ml
- **Açúcares** (g) por 100ml
- **Sódio** (mg) por 100ml

## 🛠️ Configuração do Ambiente

### Pré-requisitos
- Python 3.8 ou superior
- Um navegador web (Chrome, Chromium, Firefox ou Edge)

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

## 🚀 Como Usar

### Execução Principal
```bash
python main.py
```

### Menu Interativo

O programa oferece uma interface bonita com as seguintes opções:

1. **🧪 Teste Rápido** - Coleta 3 produtos para verificação
2. **🚀 Coleta Completa** - Todos os ~61 produtos do site  
3. **📈 Coleta Personalizada** - Quantidade específica (em desenvolvimento)
4. **📋 Ver Arquivos** - Lista arquivos CSV gerados
5. **🗑️ Limpar Dados** - Remove arquivos antigos
6. **📖 Sobre o Programa** - Informações detalhadas
7. **❌ Sair** - Encerrar programa

### Exemplo de Uso Rápido

```bash
# Executar o programa
python main.py

# Escolher opção 1 para teste rápido
# Ou opção 2 para coleta completa
# Aguardar conclusão e verificar pasta dados/
```

## 📂 Estrutura do Projeto

```
scraping_the_coffee/
├── config/
│   ├── browser.py        # Detecção automática de navegadores
│   └── coleta.py         # Motor de scraping principal
├── dados/                # Arquivos CSV gerados
│   └── dados_nutricionais_the_coffee_YYYYMMDD_HHMMSS.csv
├── main.py              # Interface principal com menu bonito
├── requirements.txt     # Dependências do projeto
└── README.md           # Este arquivo
```

## 🎯 Funcionalidades Implementadas

### ✅ Scraping Completo
- Navegação automatizada no site The Coffee
- Detecção e clique em botões "info nutricional"
- Extração de dados de popups nutricionais
- Processamento de ~61 produtos disponíveis

### ✅ Interface Profissional
- Menu interativo com cores ANSI
- Barras de progresso animadas
- Confirmações de segurança
- Tratamento elegante de erros
- Feedback visual em tempo real

### ✅ Processamento de Dados
- Parsing inteligente de porções (copos, fatias, ml, g)
- Preservação de decimais nos valores
- Categorização automática por tipo de produto
- Exportação em CSV com timestamp

### ✅ Compatibilidade
- Suporte a Chrome, Chromium, Firefox, Edge
- Gestão automática de WebDrivers
- Multiplataforma (Windows, Linux, macOS)

## 📊 Resultados

### Dados de Exemplo (Teste com 3 produtos):

| Produto | Calorias (kcal) | Carboidratos (g) | Proteínas (g) | Porção |
|---------|-----------------|------------------|---------------|---------|
| Pure Black (Double Shot) | 25.0 | 4.2 | 1.9 | 1/2 copo pequeno |
| Americano | 5.6 | 0.9 | 0.4 | 1/2 copo médio |
| True White | 47.5 | 4.2 | 2.6 | 1 copo médio |

### Performance
- **Tempo estimado**: 15-30 minutos para coleta completa
- **Taxa de sucesso**: ~100% com internet estável
- **Produtos disponíveis**: ~61 itens no cardápio
- **Formato de saída**: CSV com encoding UTF-8-BOM

## 🔧 Configurações Avançadas

### Modo Teste vs Completo
```python
# Teste rápido (3 produtos)
python main.py → Opção 1

# Coleta completa (todos os produtos)
python main.py → Opção 2
```

### Personalização
O arquivo `config/coleta.py` permite ajustar:
- Timeouts de carregamento
- Seletores CSS específicos
- Mapeamento de nutrientes
- Categorias de produtos

## 🐛 Solução de Problemas

### Navegador não encontrado
```bash
# Instale um navegador compatível
sudo apt install chromium-browser  # Ubuntu/Debian
brew install --cask chrome         # macOS
```

### WebDriver desatualizado
```bash
# O sistema atualiza automaticamente via webdriver-manager
# Caso necessite, delete cache e execute novamente
rm -rf ~/.wdm/
python main.py
```

### Erro de conexão
- Verifique sua conexão com a internet
- Teste acessando o site manualmente
- Aguarde alguns minutos entre execuções

## 📈 Roadmap

- [ ] 📊 Coleta personalizada com limite de produtos
- [ ] 🔄 Modo atualização incremental
- [ ] 📋 Exportação para outros formatos (JSON, Excel)
- [ ] 🌐 Interface web opcional
- [ ] 📈 Análise estatística dos dados
- [ ] 🔔 Notificações de conclusão

## 🤝 Contribuindo

Contribuições são bem-vindas! Para contribuir:

1. Faça um fork do projeto
2. Crie uma branch para sua feature (`git checkout -b feature/nova-funcionalidade`)
3. Commit suas mudanças (`git commit -am 'Adiciona nova funcionalidade'`)
4. Push para a branch (`git push origin feature/nova-funcionalidade`)
5. Abra um Pull Request

## 📄 Licença

Este projeto está licenciado sob a licença MIT - veja o arquivo LICENSE para mais detalhes.

## 🏆 Créditos

- **Desenvolvimento**: Claude (Anthropic) + Cursor
- **Interface**: Sistema de cores ANSI e emojis
- **Dados**: Site The Coffee (https://thecoffee.jp/)
- **Versão**: 1.0 - Janeiro 2025

---

**🍵 Aproveite seus dados nutricionais do The Coffee!**
