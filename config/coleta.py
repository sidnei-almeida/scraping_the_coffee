#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import sys
import os
import time
import pandas as pd
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.chrome.service import Service as ChromeService
from selenium.webdriver.firefox.service import Service as FirefoxService
from selenium.webdriver.edge.service import Service as EdgeService
from webdriver_manager.chrome import ChromeDriverManager
from webdriver_manager.firefox import GeckoDriverManager
from webdriver_manager.microsoft import EdgeChromiumDriverManager
from typing import Optional, Dict, List
from datetime import datetime

# Adiciona o diretório raiz ao path para importação
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
from config.browser import get_preferred_browser

def get_webdriver() -> Optional[webdriver.Remote]:
    """
    Retorna uma instância do WebDriver configurada para o navegador preferido.
    
    Returns:
        Uma instância do WebDriver ou None se nenhum navegador compatível for encontrado.
    """
    preferred_browser = get_preferred_browser()
    driver = None

    if preferred_browser == 'chrome':
        try:
            service = ChromeService(ChromeDriverManager().install())
            driver = webdriver.Chrome(service=service)
            print("WebDriver Chrome inicializado com sucesso.")
        except Exception as e:
            print(f"Erro ao inicializar WebDriver Chrome: {e}")
    elif preferred_browser == 'chromium':
        try:
            service = ChromeService(ChromeDriverManager(chrome_type="chromium").install())
            driver = webdriver.Chrome(service=service)
            print("WebDriver Chromium inicializado com sucesso.")
        except Exception as e:
            print(f"Erro ao inicializar WebDriver Chromium: {e}")
    elif preferred_browser == 'firefox':
        try:
            service = FirefoxService(GeckoDriverManager().install())
            driver = webdriver.Firefox(service=service)
            print("WebDriver Firefox inicializado com sucesso.")
        except Exception as e:
            print(f"Erro ao inicializar WebDriver Firefox: {e}")
    elif preferred_browser == 'edge':
        try:
            service = EdgeService(EdgeChromiumDriverManager().install())
            driver = webdriver.Edge(service=service)
            print("WebDriver Edge inicializado com sucesso.")
        except Exception as e:
            print(f"Erro ao inicializar WebDriver Edge: {e}")
    else:
        print("Nenhum navegador compatível encontrado para inicializar o WebDriver.")
        print("Por favor, instale Chrome, Chromium, Firefox ou Edge.")

    return driver

def extrair_dados_tabela_nutricional(driver: webdriver.Remote) -> Dict[str, str]:
    """
    Extrai os dados da tabela nutricional do popup aberto.
    
    Args:
        driver: Instância do WebDriver
        
    Returns:
        Dicionário com os dados nutricionais
    """
    dados = {
        'NOME_PRODUTO': '',
        'URL': driver.current_url,
        'CATEGORIA': 'N/A',  # Será determinada dinamicamente
        'PORCAO (g)': '0',  # Nota: mantém (g) no nome da coluna, mas aceita qualquer unidade
        'CALORIAS (kcal)': '0',
        'CARBOIDRATOS (g)': '0',
        'PROTEINAS (g)': '0',
        'GORDURAS_TOTAIS (g)': '0',
        'GORDURAS_SATURADAS (g)': '0',
        'GORDURAS_TRANS (g)': '0',
        'FIBRAS (g)': '0',
        'ACUCARES (g)': '0',
        'SODIO (mg)': '0'
    }
    
    try:
        # Aguarda o popup aparecer e localiza o popup específico
        wait = WebDriverWait(driver, 10)
        
        # Aguarda um pouco para o popup carregar completamente
        time.sleep(2)
        
        # Determina a categoria antes de abrir o popup
        categoria = determinar_categoria(driver)
        dados['CATEGORIA'] = categoria
        print(f"Categoria determinada: {categoria}")
        
        # Localiza o popup específico pela classe
        popup = None
        try:
            popup = wait.until(EC.presence_of_element_located((By.CSS_SELECTOR, ".styles_popup__nejKE")))
            print("Popup encontrado com sucesso!")
        except:
            print("Não foi possível localizar o popup específico, tentando busca geral...")
            # Fallback para qualquer popup visível
            popups = driver.find_elements(By.CSS_SELECTOR, "[class*='popup'], [class*='modal'], [class*='dialog']")
            for p in popups:
                if p.is_displayed():
                    popup = p
                    break
        
        if not popup:
            print("Nenhum popup encontrado!")
            return dados
        
        # Extrai o nome do produto - busca especificamente no h4 dentro do popup
        try:
            nome_elemento = popup.find_element(By.CSS_SELECTOR, "h4")
            dados['NOME_PRODUTO'] = nome_elemento.text.strip()
            print(f"Nome do produto encontrado: {dados['NOME_PRODUTO']}")
        except Exception as e:
            print(f"Erro ao buscar nome do produto no popup: {e}")
            # Fallback: busca por qualquer título dentro do popup
            try:
                titulos = popup.find_elements(By.CSS_SELECTOR, "h1, h2, h3, h4, h5")
                for titulo in titulos:
                    texto = titulo.text.strip()
                    if texto and len(texto) > 3:
                        dados['NOME_PRODUTO'] = texto
                        print(f"Nome do produto encontrado (fallback): {texto}")
                        break
            except:
                pass
        
        # Extrai a porção - busca especificamente por "Porção:" dentro do popup
        # Aceita qualquer tipo de unidade: copos, fatias, unidades, ml, g, etc.
        try:
            # Busca por qualquer elemento <p> dentro do popup que contenha "Porção:"
            elementos_porcao = popup.find_elements(By.XPATH, ".//p[contains(text(), 'Porção:')]")
            
            print(f"Encontrados {len(elementos_porcao)} elementos com 'Porção:'")
            
            for elemento in elementos_porcao:
                try:
                    texto = elemento.text.strip()
                    print(f"Texto da porção encontrado: '{texto}'")
                    
                    # Verifica se é "Porção:" e não "Porções por embalagem"
                    if "Porção:" in texto and "embalagem" not in texto.lower():
                        porcao_info = texto.split("Porção:")[1].strip()
                        dados['PORCAO (g)'] = porcao_info  # Aceita qualquer unidade (copo, fatia, unidade, ml, g)
                        print(f"✅ Porção encontrada: '{porcao_info}' (pode ser: copo, fatia, unidade, ml, g, etc.)")
                        break
                    else:
                        print(f"❌ Elemento descartado (contém 'embalagem' ou não é 'Porção:'): {texto}")
                except Exception as e:
                    print(f"Erro ao processar elemento de porção: {e}")
                    continue
                    
            # Se ainda não encontrou, tenta busca mais geral
            if not dados['PORCAO (g)'] or dados['PORCAO (g)'] == '0':
                print("Tentando busca alternativa para porção...")
                todos_p = popup.find_elements(By.TAG_NAME, "p")
                for p in todos_p:
                    texto = p.text.strip()
                    # Busca por padrões mais amplos de porção
                    if any(palavra in texto.lower() for palavra in ["porção", "unidade", "fatia", "pedaço"]) and "embalagem" not in texto.lower():
                        print(f"Texto alternativo encontrado: '{texto}'")
                        if ":" in texto:
                            porcao_info = texto.split(":")[1].strip()
                            dados['PORCAO (g)'] = porcao_info
                            print(f"✅ Porção encontrada (método alternativo): '{porcao_info}'")
                            break
                            
        except Exception as e:
            print(f"Erro ao buscar porção: {e}")
        
        # Mapeia os nomes dos nutrientes para as chaves do nosso dicionário
        # Nomes exatos como aparecem na tabela
        nutrientes_map = {
            'Valor energético (kcal)': 'CALORIAS (kcal)',
            'Carboidratos (g)': 'CARBOIDRATOS (g)', 
            'Proteínas (g)': 'PROTEINAS (g)',
            'Gorduras totais (g)': 'GORDURAS_TOTAIS (g)',
            'Gorduras saturadas (g)': 'GORDURAS_SATURADAS (g)',
            'Gorduras trans (g)': 'GORDURAS_TRANS (g)',
            'Fibra alimentar (g)': 'FIBRAS (g)',
            'Sódio (mg)': 'SODIO (mg)'
        }
        
        # Busca por linhas da tabela nutricional dentro do popup
        try:
            # Localiza a tabela especificamente dentro do popup
            tabela = popup.find_element(By.CSS_SELECTOR, "table")
            linhas = tabela.find_elements(By.CSS_SELECTOR, "tr")
            
            print(f"Encontradas {len(linhas)} linhas na tabela")
            
            for i, linha in enumerate(linhas):
                texto_linha = linha.text.strip()
                print(f"Linha {i}: '{texto_linha}'")
                
                # Processa cada nutriente
                for nutriente_nome, chave_dados in nutrientes_map.items():
                    if nutriente_nome.lower() in texto_linha.lower():
                        print(f"🔍 Processando nutriente: {nutriente_nome}")
                        
                        # Procura pelas células da linha (td)
                        celulas = linha.find_elements(By.TAG_NAME, "td")
                        print(f"   Encontradas {len(celulas)} células")
                        
                        if len(celulas) >= 3:  # Nome do nutriente + 100ml + porção + %VD
                            try:
                                # A primeira célula numérica (índice 1) contém o valor para 100ml
                                valor_100ml = celulas[1].text.strip()
                                print(f"   Valor da célula 100ml: '{valor_100ml}'")
                                
                                # Extrai números incluindo decimais (aceita tanto vírgula quanto ponto)
                                import re
                                match = re.search(r'(\d+(?:[.,]\d+)?)', valor_100ml)
                                if match:
                                    valor_limpo = match.group(1).replace(',', '.')  # Converte vírgula para ponto
                                    dados[chave_dados] = valor_limpo  # Mantém como string para preservar decimais
                                    print(f"✅ {nutriente_nome}: {valor_limpo}")
                                else:
                                    print(f"❌ Não foi possível extrair valor numérico de '{valor_100ml}'")
                            except Exception as e:
                                print(f"❌ Erro ao processar células: {e}")
                        else:
                            # Fallback: extrai valores usando regex como antes
                            import re
                            valores = re.findall(r'(\d+(?:[.,]\d+)?)', texto_linha)
                            print(f"   Valores encontrados via regex: {valores}")
                            if valores and len(valores) >= 1:
                                # Pega o primeiro valor (coluna 100ml)
                                valor = valores[0].replace(',', '.')
                                dados[chave_dados] = valor
                                print(f"✅ {nutriente_nome} (fallback): {valor}")
                        break  # Sai do loop de nutrientes após encontrar o correto
                        
        except Exception as e:
            print(f"Erro ao extrair dados da tabela: {e}")
        
        print(f"Dados extraídos para {dados['NOME_PRODUTO']}")
        
    except Exception as e:
        print(f"Erro ao extrair dados nutricionais: {e}")
    
    return dados

def determinar_categoria(driver: webdriver.Remote) -> str:
    """
    Determina a categoria do produto baseado na seção da página onde o botão foi clicado.
    
    Args:
        driver: Instância do WebDriver
        
    Returns:
        Nome da categoria
    """
    try:
        # Busca por títulos de seção visíveis na página
        titulos_secoes = [
            "BEBIDAS PURISTAS", "BEBIDAS AUTORAIS", "COADOS", "COMIDAS", 
            "OUTRAS BEBIDAS", "SHOP", "DOCES", "PADOCA", "SOBREMESAS"
        ]
        
        for titulo in titulos_secoes:
            elementos = driver.find_elements(By.XPATH, f"//*[contains(text(), '{titulo}')]")
            for elemento in elementos:
                if elemento.is_displayed():
                    # Verifica se o elemento está próximo de onde clicamos
                    return titulo
                    
        return "PRODUTOS"  # Categoria genérica como fallback
    except:
        return "PRODUTOS"

def coletar_produtos_the_coffee(url: str = "https://thecoffee.jp/shortcut/brasil/sao-paulo/the-coffee-vila-olimpia/menu", limite_produtos: int = None) -> List[Dict[str, str]]:
    """
    Coleta dados nutricionais de todos os produtos do site The Coffee.
    
    Args:
        url: URL do menu do The Coffee
        limite_produtos: Limite de produtos para coletar (None = todos)
        
    Returns:
        Lista de dicionários com dados dos produtos
    """
    driver = get_webdriver()
    if not driver:
        return []
    
    produtos_dados = []
    
    try:
        print(f"Navegando para: {url}")
        driver.get(url)
        
        # Aguarda a página carregar
        time.sleep(5)
        
        # Procura todos os botões "info nutricional"
        wait = WebDriverWait(driver, 15)
        
        print("Procurando botões de informação nutricional...")
        
        # Tenta diferentes seletores para encontrar os botões
        botoes_info = []
        seletores_possivel = [
            ".styles_btNutritionalInfo__3QtQz",
            "[class*='btNutritionalInfo']",
            "span:contains('info nutricional')",
            "button:contains('info nutricional')",
            "*[class*='nutritional']"
        ]
        
        for seletor in seletores_possivel:
            try:
                botoes_info = driver.find_elements(By.CSS_SELECTOR, seletor)
                if botoes_info:
                    print(f"Encontrados {len(botoes_info)} botões com seletor: {seletor}")
                    break
            except:
                continue
        
        if not botoes_info:
            # Fallback: procura por texto "info nutricional"
            try:
                botoes_info = driver.find_elements(By.XPATH, "//*[contains(text(), 'info nutricional')]")
                print(f"Encontrados {len(botoes_info)} botões via XPath")
            except:
                print("Não foi possível encontrar botões de informação nutricional")
                return []
        
        # Aplica limite se especificado
        if limite_produtos:
            botoes_info = botoes_info[:limite_produtos]
            print(f"Limitando coleta a {limite_produtos} produtos")
        
        print(f"Total de produtos a processar: {len(botoes_info)}")
        
        # Coleta dados de cada produto
        for i, botao in enumerate(botoes_info, 1):
            try:
                print(f"\nProcessando produto {i}/{len(botoes_info)}")
                
                # Scroll até o botão para garantir que está visível
                driver.execute_script("arguments[0].scrollIntoView(true);", botao)
                time.sleep(1)
                
                # Clica no botão
                driver.execute_script("arguments[0].click();", botao)
                time.sleep(3)
                
                # Extrai dados da tabela nutricional
                dados_produto = extrair_dados_tabela_nutricional(driver)
                produtos_dados.append(dados_produto)
                
                # Fecha o popup (tenta diferentes métodos)
                try:
                    # Procura botão de fechar (X)
                    botao_fechar = driver.find_element(By.CSS_SELECTOR, ".close, .modal-close, [class*='close'], button[aria-label='Close']")
                    botao_fechar.click()
                except:
                    # Se não encontrar botão, pressiona ESC
                    try:
                        from selenium.webdriver.common.keys import Keys
                        driver.find_element(By.TAG_NAME, 'body').send_keys(Keys.ESCAPE)
                    except:
                        # Como último recurso, clica fora do popup
                        driver.execute_script("document.body.click();")
                
                time.sleep(2)
                
            except Exception as e:
                print(f"Erro ao processar produto {i}: {e}")
                continue
        
    except Exception as e:
        print(f"Erro durante a coleta: {e}")
    
    finally:
        driver.quit()
        print("WebDriver fechado.")
    
    return produtos_dados

def salvar_dados_csv(dados: List[Dict[str, str]], pasta_dados: str = "dados") -> str:
    """
    Salva os dados coletados em um arquivo CSV.
    
    Args:
        dados: Lista de dicionários com dados dos produtos
        pasta_dados: Pasta onde salvar o arquivo
        
    Returns:
        Caminho do arquivo salvo
    """
    if not dados:
        print("Nenhum dado para salvar.")
        return ""
    
    # Cria a pasta se não existir
    os.makedirs(pasta_dados, exist_ok=True)
    
    # Nome do arquivo com timestamp
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    nome_arquivo = f"dados_nutricionais_the_coffee_{timestamp}.csv"
    caminho_arquivo = os.path.join(pasta_dados, nome_arquivo)
    
    # Cria DataFrame e salva
    df = pd.DataFrame(dados)
    df.to_csv(caminho_arquivo, index=False, encoding='utf-8-sig')
    
    print(f"Dados salvos em: {caminho_arquivo}")
    print(f"Total de produtos coletados: {len(dados)}")
    
    return caminho_arquivo

def main(modo_teste: bool = False):
    """
    Função principal para executar o scraping completo.
    
    Args:
        modo_teste: Se True, coleta apenas 3 produtos para teste
    """
    print("=== Iniciando coleta de dados nutricionais do The Coffee ===")
    
    if modo_teste:
        print("🧪 Modo TESTE: coletando apenas 3 produtos")
        limite = 3
    else:
        print("🚀 Modo COMPLETO: coletando todos os produtos")
        limite = None
    
    # Coleta os dados
    dados = coletar_produtos_the_coffee(limite_produtos=limite)
    
    # Salva em CSV
    if dados:
        arquivo_salvo = salvar_dados_csv(dados)
        print(f"\n✅ Coleta concluída com sucesso!")
        print(f"📁 Arquivo salvo: {arquivo_salvo}")
    else:
        print("\n❌ Nenhum dado foi coletado.")

if __name__ == "__main__":
    main()