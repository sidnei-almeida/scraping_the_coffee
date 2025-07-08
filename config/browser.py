#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import os
import subprocess
import platform
from typing import Dict, List, Optional

def check_browser_exists(browser_name: str) -> bool:
    """
    Verifica se um navegador específico está instalado no sistema.
    
    Args:
        browser_name: Nome do navegador para verificar
        
    Returns:
        True se o navegador estiver instalado, False caso contrário
    """
    system = platform.system()
    
    # Para Linux
    if system == 'Linux':
        try:
            # Tenta executar o comando which para verificar se o executável existe
            subprocess.run(['which', browser_name], 
                          stdout=subprocess.PIPE, 
                          stderr=subprocess.PIPE, 
                          check=True)
            return True
        except subprocess.CalledProcessError:
            return False
    
    # Para Windows
    elif system == 'Windows':
        # Caminhos comuns para navegadores no Windows
        paths = {
            'chrome': [
                r'C:\Program Files\Google\Chrome\Application\chrome.exe',
                r'C:\Program Files (x86)\Google\Chrome\Application\chrome.exe'
            ],
            'firefox': [
                r'C:\Program Files\Mozilla Firefox\firefox.exe',
                r'C:\Program Files (x86)\Mozilla Firefox\firefox.exe'
            ],
            'chromium': [
                r'C:\Program Files\Chromium\Application\chrome.exe',
                r'C:\Program Files (x86)\Chromium\Application\chrome.exe'
            ],
            'edge': [
                r'C:\Program Files (x86)\Microsoft\Edge\Application\msedge.exe',
                r'C:\Program Files\Microsoft\Edge\Application\msedge.exe'
            ],
        }
        
        browser_paths = paths.get(browser_name.lower(), [])
        return any(os.path.exists(path) for path in browser_paths)
    
    # Para MacOS
    elif system == 'Darwin':
        paths = {
            'chrome': ['/Applications/Google Chrome.app/Contents/MacOS/Google Chrome'],
            'firefox': ['/Applications/Firefox.app/Contents/MacOS/firefox'],
            'chromium': ['/Applications/Chromium.app/Contents/MacOS/Chromium'],
            'safari': ['/Applications/Safari.app/Contents/MacOS/Safari']
        }
        
        browser_paths = paths.get(browser_name.lower(), [])
        return any(os.path.exists(path) for path in browser_paths)
    
    return False

def get_installed_browsers() -> Dict[str, bool]:
    """
    Detecta quais navegadores estão instalados no sistema.
    
    Returns:
        Dicionário com nome do navegador e status de instalação
    """
    browsers = ['chrome', 'chromium', 'firefox', 'edge', 'safari']
    installed_browsers = {}
    
    for browser in browsers:
        installed_browsers[browser] = check_browser_exists(browser)
    
    return installed_browsers

def get_preferred_browser() -> Optional[str]:
    """
    Retorna o nome do navegador preferido disponível no sistema.
    Ordem de preferência: Chrome > Chromium > Firefox > Edge > Safari
    
    Returns:
        Nome do navegador preferido ou None se nenhum navegador for encontrado
    """
    preference_order = ['chrome', 'chromium', 'firefox', 'edge', 'safari']
    installed = get_installed_browsers()
    
    for browser in preference_order:
        if installed.get(browser, False):
            return browser
            
    return None

if __name__ == "__main__":
    # Teste simples para verificar a detecção de navegadores
    browsers = get_installed_browsers()
    print("Navegadores instalados:")
    for browser, installed in browsers.items():
        status = "Instalado" if installed else "Não instalado"
        print(f"- {browser.capitalize()}: {status}")
    
    preferred = get_preferred_browser()
    if preferred:
        print(f"\nNavegador preferido: {preferred.capitalize()}")
    else:
        print("\nNenhum navegador compatível encontrado.") 