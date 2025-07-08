#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
🍵 SCRAPER THE COFFEE - Dados Nutricionais
==========================================
Sistema de coleta de dados nutricionais do site The Coffee
Desenvolvido para extrair informações completas de todos os produtos
"""

import os
import sys
import time
import glob
from datetime import datetime
from typing import List, Dict

# Adiciona o diretório config ao path
sys.path.append(os.path.dirname(os.path.abspath(__file__)))
from config.coleta import main as executar_coleta

# Cores ANSI para terminal
class Cores:
    RESET = '\033[0m'
    BOLD = '\033[1m'
    VERDE = '\033[92m'
    AZUL = '\033[94m'
    AMARELO = '\033[93m'
    VERMELHO = '\033[91m'
    CIANO = '\033[96m'
    MAGENTA = '\033[95m'
    BRANCO = '\033[97m'

def limpar_terminal():
    """Limpa o terminal"""
    os.system('clear' if os.name == 'posix' else 'cls')

def mostrar_banner():
    """Exibe o banner principal do programa"""
    banner = f"""
{Cores.CIANO}{Cores.BOLD}
╔══════════════════════════════════════════════════════════════╗
║                    🍵 SCRAPER THE COFFEE 🍵                   ║
║                                                              ║
║            Extrator de Dados Nutricionais v1.0              ║
║                                                              ║
║  📊 Coleta dados de todos os produtos do site The Coffee    ║
║  🎯 Informações nutricionais completas por 100ml            ║
║  📝 Exporta dados em formato CSV para análise               ║
╚══════════════════════════════════════════════════════════════╝
{Cores.RESET}"""
    print(banner)

def mostrar_barra_progresso(texto: str, duracao: float = 2.0):
    """Exibe uma barra de progresso animada"""
    print(f"\n{Cores.AMARELO}⏳ {texto}...{Cores.RESET}")
    barra_tamanho = 40
    for i in range(barra_tamanho + 1):
        progresso = i / barra_tamanho
        barra = "█" * i + "░" * (barra_tamanho - i)
        porcentagem = int(progresso * 100)
        print(f"\r{Cores.VERDE}[{barra}] {porcentagem}%{Cores.RESET}", end="", flush=True)
        time.sleep(duracao / barra_tamanho)
    print()

def mostrar_menu():
    """Exibe o menu principal"""
    menu = f"""
{Cores.AZUL}{Cores.BOLD}═══════════════════ MENU PRINCIPAL ═══════════════════{Cores.RESET}

{Cores.VERDE}📊 OPÇÕES DE COLETA:{Cores.RESET}
  {Cores.AMARELO}1.{Cores.RESET} 🧪 {Cores.BRANCO}Teste Rápido{Cores.RESET} - Coleta 3 produtos para verificação
  {Cores.AMARELO}2.{Cores.RESET} 🚀 {Cores.BRANCO}Coleta Completa{Cores.RESET} - Todos os produtos do site
  {Cores.AMARELO}3.{Cores.RESET} 📈 {Cores.BRANCO}Coleta Personalizada{Cores.RESET} - Escolha quantos produtos coletar

{Cores.VERDE}📁 GERENCIAR DADOS:{Cores.RESET}
  {Cores.AMARELO}4.{Cores.RESET} 📋 {Cores.BRANCO}Ver Arquivos Gerados{Cores.RESET} - Lista arquivos CSV criados
  {Cores.AMARELO}5.{Cores.RESET} 🗑️  {Cores.BRANCO}Limpar Dados Antigos{Cores.RESET} - Remove arquivos antigos

{Cores.VERDE}ℹ️  INFORMAÇÕES:{Cores.RESET}
  {Cores.AMARELO}6.{Cores.RESET} 📖 {Cores.BRANCO}Sobre o Programa{Cores.RESET} - Informações e estatísticas
  {Cores.AMARELO}7.{Cores.RESET} ❌ {Cores.BRANCO}Sair{Cores.RESET} - Encerrar programa

{Cores.AZUL}══════════════════════════════════════════════════════{Cores.RESET}
"""
    print(menu)

def obter_escolha() -> str:
    """Obtém a escolha do usuário"""
    try:
        escolha = input(f"{Cores.MAGENTA}👉 Digite sua opção (1-7): {Cores.RESET}").strip()
        return escolha
    except KeyboardInterrupt:
        print(f"\n\n{Cores.AMARELO}⚠️  Programa interrompido pelo usuário{Cores.RESET}")
        sys.exit(0)

def executar_teste_rapido():
    """Executa teste rápido com 3 produtos"""
    print(f"\n{Cores.CIANO}{Cores.BOLD}🧪 INICIANDO TESTE RÁPIDO{Cores.RESET}")
    print(f"{Cores.AZUL}━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━{Cores.RESET}")
    
    mostrar_barra_progresso("Preparando ambiente", 1.5)
    
    print(f"\n{Cores.VERDE}✅ Configurações:{Cores.RESET}")
    print(f"   📊 Produtos: {Cores.AMARELO}3 produtos{Cores.RESET}")
    print(f"   📁 Destino: {Cores.AMARELO}pasta dados/{Cores.RESET}")
    print(f"   🔄 Modo: {Cores.AMARELO}Teste e validação{Cores.RESET}")
    
    confirmar = input(f"\n{Cores.MAGENTA}🤔 Continuar com o teste? (s/N): {Cores.RESET}").lower()
    
    if confirmar in ['s', 'sim', 'y', 'yes']:
        try:
            print(f"\n{Cores.VERDE}🚀 Iniciando coleta...{Cores.RESET}")
            executar_coleta(modo_teste=True)
            print(f"\n{Cores.VERDE}✅ Teste concluído com sucesso!{Cores.RESET}")
        except Exception as e:
            print(f"\n{Cores.VERMELHO}❌ Erro durante o teste: {e}{Cores.RESET}")
    else:
        print(f"{Cores.AMARELO}⏭️  Teste cancelado{Cores.RESET}")

def executar_coleta_completa():
    """Executa coleta completa de todos os produtos"""
    print(f"\n{Cores.CIANO}{Cores.BOLD}🚀 COLETA COMPLETA - TODOS OS PRODUTOS{Cores.RESET}")
    print(f"{Cores.AZUL}━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━{Cores.RESET}")
    
    print(f"\n{Cores.AMARELO}⚠️  ATENÇÃO:{Cores.RESET}")
    print(f"   • Este processo pode demorar {Cores.VERMELHO}15-30 minutos{Cores.RESET}")
    print(f"   • Será coletado dados de {Cores.AMARELO}~61 produtos{Cores.RESET}")
    print(f"   • O navegador irá abrir automaticamente")
    print(f"   • {Cores.VERDE}NÃO feche o navegador manualmente{Cores.RESET}")
    
    confirmar = input(f"\n{Cores.MAGENTA}🤔 Tem certeza que deseja continuar? (s/N): {Cores.RESET}").lower()
    
    if confirmar in ['s', 'sim', 'y', 'yes']:
        try:
            mostrar_barra_progresso("Preparando para coleta completa", 2.0)
            print(f"\n{Cores.VERDE}🚀 Iniciando coleta completa...{Cores.RESET}")
            print(f"{Cores.CIANO}📱 Acompanhe o progresso no terminal{Cores.RESET}")
            
            executar_coleta(modo_teste=False)
            
            print(f"\n{Cores.VERDE}🎉 COLETA COMPLETA FINALIZADA COM SUCESSO!{Cores.RESET}")
            mostrar_estatisticas_coleta()
            
        except KeyboardInterrupt:
            print(f"\n{Cores.AMARELO}⚠️  Coleta interrompida pelo usuário{Cores.RESET}")
        except Exception as e:
            print(f"\n{Cores.VERMELHO}❌ Erro durante a coleta: {e}{Cores.RESET}")
    else:
        print(f"{Cores.AMARELO}⏭️  Coleta cancelada{Cores.RESET}")

def executar_coleta_personalizada():
    """Executa coleta com número personalizado de produtos"""
    print(f"\n{Cores.CIANO}{Cores.BOLD}📈 COLETA PERSONALIZADA{Cores.RESET}")
    print(f"{Cores.AZUL}━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━{Cores.RESET}")
    
    try:
        quantidade = input(f"\n{Cores.MAGENTA}📊 Quantos produtos coletar? (1-61): {Cores.RESET}").strip()
        
        if not quantidade.isdigit():
            print(f"{Cores.VERMELHO}❌ Por favor, digite um número válido{Cores.RESET}")
            return
            
        num = int(quantidade)
        if num < 1 or num > 61:
            print(f"{Cores.VERMELHO}❌ Número deve estar entre 1 e 61{Cores.RESET}")
            return
        
        print(f"\n{Cores.VERDE}✅ Configuração:{Cores.RESET}")
        print(f"   📊 Produtos: {Cores.AMARELO}{num} produtos{Cores.RESET}")
        print(f"   ⏱️  Tempo estimado: {Cores.AMARELO}~{num * 0.5:.1f} minutos{Cores.RESET}")
        
        confirmar = input(f"\n{Cores.MAGENTA}🤔 Continuar? (s/N): {Cores.RESET}").lower()
        
        if confirmar in ['s', 'sim', 'y', 'yes']:
            try:
                print(f"\n{Cores.VERDE}🚀 Iniciando coleta de {num} produtos...{Cores.RESET}")
                # Aqui você pode modificar a função para aceitar limite personalizado
                # executar_coleta_com_limite(num)
                print(f"{Cores.AMARELO}⚠️  Funcionalidade em desenvolvimento{Cores.RESET}")
            except Exception as e:
                print(f"\n{Cores.VERMELHO}❌ Erro durante a coleta: {e}{Cores.RESET}")
        else:
            print(f"{Cores.AMARELO}⏭️  Coleta cancelada{Cores.RESET}")
            
    except ValueError:
        print(f"{Cores.VERMELHO}❌ Por favor, digite um número válido{Cores.RESET}")

def listar_arquivos_gerados():
    """Lista todos os arquivos CSV gerados"""
    print(f"\n{Cores.CIANO}{Cores.BOLD}📋 ARQUIVOS GERADOS{Cores.RESET}")
    print(f"{Cores.AZUL}━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━{Cores.RESET}")
    
    if not os.path.exists("dados"):
        print(f"{Cores.AMARELO}📁 Pasta 'dados' não encontrada{Cores.RESET}")
        return
    
    arquivos = glob.glob("dados/*.csv")
    
    if not arquivos:
        print(f"{Cores.AMARELO}📄 Nenhum arquivo CSV encontrado na pasta 'dados'{Cores.RESET}")
        return
    
    print(f"\n{Cores.VERDE}📊 Total de arquivos: {len(arquivos)}{Cores.RESET}\n")
    
    for i, arquivo in enumerate(sorted(arquivos, reverse=True), 1):
        nome_arquivo = os.path.basename(arquivo)
        tamanho = os.path.getsize(arquivo)
        data_modificacao = datetime.fromtimestamp(os.path.getmtime(arquivo))
        
        # Calcula o tamanho em formato legível
        if tamanho < 1024:
            tamanho_str = f"{tamanho} B"
        elif tamanho < 1024 * 1024:
            tamanho_str = f"{tamanho / 1024:.1f} KB"
        else:
            tamanho_str = f"{tamanho / (1024 * 1024):.1f} MB"
        
        print(f"{Cores.AMARELO}{i:2d}.{Cores.RESET} {Cores.BRANCO}{nome_arquivo}{Cores.RESET}")
        print(f"     📅 {data_modificacao.strftime('%d/%m/%Y %H:%M:%S')}")
        print(f"     📏 {tamanho_str}")
        print()

def limpar_dados_antigos():
    """Remove arquivos CSV antigos"""
    print(f"\n{Cores.CIANO}{Cores.BOLD}🗑️  LIMPAR DADOS ANTIGOS{Cores.RESET}")
    print(f"{Cores.AZUL}━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━{Cores.RESET}")
    
    if not os.path.exists("dados"):
        print(f"{Cores.AMARELO}📁 Pasta 'dados' não encontrada{Cores.RESET}")
        return
    
    arquivos = glob.glob("dados/*.csv")
    
    if not arquivos:
        print(f"{Cores.VERDE}✅ Nenhum arquivo para limpar{Cores.RESET}")
        return
    
    print(f"\n{Cores.AMARELO}⚠️  ATENÇÃO:{Cores.RESET}")
    print(f"   • Serão removidos {Cores.VERMELHO}{len(arquivos)} arquivos{Cores.RESET}")
    print(f"   • Esta ação {Cores.VERMELHO}NÃO PODE ser desfeita{Cores.RESET}")
    
    confirmar = input(f"\n{Cores.MAGENTA}🤔 Tem certeza? Digite 'CONFIRMAR' para prosseguir: {Cores.RESET}")
    
    if confirmar == "CONFIRMAR":
        try:
            for arquivo in arquivos:
                os.remove(arquivo)
            print(f"\n{Cores.VERDE}✅ {len(arquivos)} arquivos removidos com sucesso!{Cores.RESET}")
        except Exception as e:
            print(f"\n{Cores.VERMELHO}❌ Erro ao remover arquivos: {e}{Cores.RESET}")
    else:
        print(f"{Cores.AMARELO}⏭️  Operação cancelada{Cores.RESET}")

def mostrar_sobre():
    """Exibe informações sobre o programa"""
    sobre = f"""
{Cores.CIANO}{Cores.BOLD}📖 SOBRE O SCRAPER THE COFFEE{Cores.RESET}
{Cores.AZUL}━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━{Cores.RESET}

{Cores.VERDE}🎯 OBJETIVO:{Cores.RESET}
   Extrair dados nutricionais completos de todos os produtos do site The Coffee
   para análise e pesquisa nutricional.

{Cores.VERDE}📊 DADOS COLETADOS:{Cores.RESET}
   • Nome do produto
   • URL de origem  
   • Categoria (Bebidas, Doces, Comidas, etc.)
   • Porção (flexível: copos, fatias, unidades, ml, g)
   • Calorias (kcal) por 100ml
   • Carboidratos (g) por 100ml
   • Proteínas (g) por 100ml
   • Gorduras Totais (g) por 100ml
   • Gorduras Saturadas (g) por 100ml
   • Gorduras Trans (g) por 100ml
   • Fibras (g) por 100ml
   • Açúcares (g) por 100ml
   • Sódio (mg) por 100ml

{Cores.VERDE}🛠️  TECNOLOGIAS:{Cores.RESET}
   • Python 3.8+
   • Selenium WebDriver (automação do navegador)
   • WebDriver Manager (gestão automática de drivers)
   • Pandas (manipulação e exportação de dados)
   • BeautifulSoup4 (parsing HTML)

{Cores.VERDE}📂 ARQUIVOS GERADOS:{Cores.RESET}
   • Formato: CSV (compatível com Excel, Google Sheets)
   • Codificação: UTF-8 com BOM
   • Localização: pasta 'dados/'
   • Nomenclatura: dados_nutricionais_the_coffee_YYYYMMDD_HHMMSS.csv

{Cores.VERDE}⚡ PERFORMANCE:{Cores.RESET}
   • ~61 produtos total no site
   • Tempo estimado: 15-30 minutos (coleta completa)
   • Detecção automática do navegador instalado
   • Suporte: Chrome, Chromium, Firefox, Edge

{Cores.VERDE}📝 DESENVOLVIDO POR:{Cores.RESET}
   • Claude (Anthropic) + Cursor
   • Versão: 1.0
   • Data: Janeiro 2025

{Cores.AZUL}━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━{Cores.RESET}
"""
    print(sobre)

def mostrar_estatisticas_coleta():
    """Mostra estatísticas da última coleta"""
    arquivos = glob.glob("dados/*.csv")
    if arquivos:
        arquivo_mais_recente = max(arquivos, key=os.path.getctime)
        tamanho = os.path.getsize(arquivo_mais_recente)
        
        print(f"\n{Cores.VERDE}📈 ESTATÍSTICAS DA COLETA:{Cores.RESET}")
        print(f"   📁 Arquivo: {Cores.AMARELO}{os.path.basename(arquivo_mais_recente)}{Cores.RESET}")
        print(f"   📏 Tamanho: {Cores.AMARELO}{tamanho / 1024:.1f} KB{Cores.RESET}")
        print(f"   💾 Local: {Cores.AMARELO}dados/{Cores.RESET}")

def pausar():
    """Pausa o programa aguardando input do usuário"""
    input(f"\n{Cores.CIANO}⏯️  Pressione Enter para continuar...{Cores.RESET}")

def main():
    """Função principal do programa"""
    try:
        while True:
            limpar_terminal()
            mostrar_banner()
            mostrar_menu()
            
            escolha = obter_escolha()
            
            if escolha == "1":
                executar_teste_rapido()
                pausar()
                
            elif escolha == "2":
                executar_coleta_completa()
                pausar()
                
            elif escolha == "3":
                executar_coleta_personalizada()
                pausar()
                
            elif escolha == "4":
                listar_arquivos_gerados()
                pausar()
                
            elif escolha == "5":
                limpar_dados_antigos()
                pausar()
                
            elif escolha == "6":
                mostrar_sobre()
                pausar()
                
            elif escolha == "7":
                print(f"\n{Cores.VERDE}👋 Obrigado por usar o Scraper The Coffee!{Cores.RESET}")
                print(f"{Cores.CIANO}🍵 Até a próxima análise nutricional!{Cores.RESET}\n")
                break
                
            else:
                print(f"\n{Cores.VERMELHO}❌ Opção inválida! Por favor, escolha entre 1-7{Cores.RESET}")
                time.sleep(2)
                
    except KeyboardInterrupt:
        print(f"\n\n{Cores.AMARELO}👋 Programa encerrado pelo usuário. Até logo!{Cores.RESET}\n")
    except Exception as e:
        print(f"\n{Cores.VERMELHO}❌ Erro inesperado: {e}{Cores.RESET}")

if __name__ == "__main__":
    main() 