"""
API própria para verificação de vazamentos de dados
Busca em múltiplas fontes e mostra resultados diretamente no site
"""
import requests
import json
import os
from typing import Dict, List, Optional
from urllib.parse import quote_plus, quote
import re

try:
    from dotenv import load_dotenv
    load_dotenv()
except ImportError:
    pass

class VazamentosAPIClient:
    def __init__(self):
        self.headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36',
            'Accept': 'application/json, text/html, */*',
            'Accept-Language': 'pt-BR,pt;q=0.9,en-US;q=0.8,en;q=0.7'
        }
        
        # API Keys (opcionais - podem ser configuradas via variáveis de ambiente)
        self.hibp_api_key = os.getenv('HIBP_API_KEY', '')
        self.intelx_api_key = os.getenv('INTELX_API_KEY', '')
        self.leakcheck_api_key = os.getenv('LEAKCHECK_API_KEY', '')
        
    def verificar_hibp(self, email: str) -> Dict:
        """
        Verifica vazamentos usando Have I Been Pwned API
        """
        resultado = {
            'fonte': 'Have I Been Pwned',
            'comprometido': False,
            'breaches': [],
            'senhas': [],
            'erro': None
        }
        
        try:
            email_encoded = quote_plus(email)
            
            # Tentar API v3 primeiro (requer key)
            if self.hibp_api_key:
                url = f'https://haveibeenpwned.com/api/v3/breachedaccount/{email_encoded}?truncateResponse=false'
                headers = {
                    **self.headers,
                    'hibp-api-key': self.hibp_api_key
                }
                response = requests.get(url, headers=headers, timeout=15)
                
                if response.status_code == 200:
                    breaches = response.json()
                    resultado['comprometido'] = True
                    
                    for breach in breaches:
                        breach_info = {
                            'nome': breach.get('Name', ''),
                            'titulo': breach.get('Title', ''),
                            'data': breach.get('BreachDate', ''),
                            'dominio': breach.get('Domain', ''),
                            'total_contas': breach.get('PwnCount', 0),
                            'dados_vazados': breach.get('DataClasses', []),
                            'descricao': breach.get('Description', ''),
                            'verificado': breach.get('IsVerified', False),
                            'logo': breach.get('LogoPath', '')
                        }
                        resultado['breaches'].append(breach_info)
                
                elif response.status_code == 404:
                    resultado['comprometido'] = False
                elif response.status_code == 429:
                    resultado['erro'] = 'Rate limit atingido'
                    
            # Se não tiver key ou falhar, tentar método alternativo via scraping
            if not self.hibp_api_key or resultado.get('erro'):
                # Fazer busca na página pública
                public_url = f'https://haveibeenpwned.com/api/v2/breachedaccount/{email_encoded}'
                response = requests.get(public_url, headers=self.headers, timeout=15)
                
                if response.status_code == 200:
                    breaches = response.json()
                    resultado['comprometido'] = True
                    resultado['erro'] = None
                    
                    for breach in breaches:
                        breach_info = {
                            'nome': breach.get('Name', ''),
                            'titulo': breach.get('Title', ''),
                            'data': breach.get('BreachDate', ''),
                            'dominio': breach.get('Domain', ''),
                            'total_contas': breach.get('PwnCount', 0),
                            'dados_vazados': breach.get('DataClasses', []),
                            'descricao': breach.get('Description', ''),
                            'verificado': breach.get('IsVerified', False),
                            'logo': breach.get('LogoPath', '')
                        }
                        resultado['breaches'].append(breach_info)
                        
        except Exception as e:
            resultado['erro'] = str(e)
            
        return resultado
    
    def verificar_pastebin(self, email: str) -> Dict:
        """
        Busca email em vazamentos do Pastebin via Google
        """
        resultado = {
            'fonte': 'Pastebin (via Google)',
            'comprometido': False,
            'breaches': [],
            'senhas': [],
            'resultados': []
        }
        
        try:
            email_encoded = quote_plus(email)
            query = f'site:pastebin.com "{email}"'
            url = f'https://www.google.com/search?q={quote_plus(query)}'
            
            response = requests.get(url, headers=self.headers, timeout=15)
            
            if response.status_code == 200:
                # Verificar se encontrou resultados
                if 'pastebin.com' in response.text.lower() and email.lower() in response.text.lower():
                    resultado['comprometido'] = True
                    resultado['resultados'].append({
                        'url': url,
                        'descricao': f'Email encontrado em posts do Pastebin',
                        'tipo': 'Pastebin Leak'
                    })
                    
        except Exception as e:
            resultado['erro'] = str(e)
            
        return resultado
    
    def verificar_github(self, email: str) -> Dict:
        """
        Busca email em repositórios públicos do GitHub
        """
        resultado = {
            'fonte': 'GitHub (via Google)',
            'comprometido': False,
            'breaches': [],
            'senhas': [],
            'resultados': []
        }
        
        try:
            email_encoded = quote_plus(email)
            query = f'site:github.com "{email}"'
            url = f'https://www.google.com/search?q={quote_plus(query)}'
            
            response = requests.get(url, headers=self.headers, timeout=15)
            
            if response.status_code == 200:
                if 'github.com' in response.text.lower() and email.lower() in response.text.lower():
                    resultado['comprometido'] = True
                    resultado['resultados'].append({
                        'url': url,
                        'descricao': f'Email encontrado em repositórios do GitHub',
                        'tipo': 'GitHub Leak'
                    })
                    
        except Exception as e:
            resultado['erro'] = str(e)
            
        return resultado
    
    def verificar_multiplas_fontes(self, email: str) -> Dict:
        """
        Verifica email em múltiplas fontes de vazamentos
        Retorna resultado consolidado
        """
        resultados_consolidados = {
            'email': email,
            'comprometido': False,
            'total_breaches': 0,
            'total_senhas': 0,
            'fontes_verificadas': [],
            'breaches': [],
            'senhas': [],
            'resultados_adicionais': [],
            'resumo': ''
        }
        
        # Verificar Have I Been Pwned
        hibp_result = self.verificar_hibp(email)
        resultados_consolidados['fontes_verificadas'].append(hibp_result)
        
        if hibp_result['comprometido']:
            resultados_consolidados['comprometido'] = True
            resultados_consolidados['breaches'].extend(hibp_result.get('breaches', []))
            resultados_consolidados['total_breaches'] += len(hibp_result.get('breaches', []))
        
        # Verificar Pastebin
        pastebin_result = self.verificar_pastebin(email)
        resultados_consolidados['fontes_verificadas'].append(pastebin_result)
        
        if pastebin_result['comprometido']:
            resultados_consolidados['comprometido'] = True
            resultados_consolidados['resultados_adicionais'].extend(pastebin_result.get('resultados', []))
        
        # Verificar GitHub
        github_result = self.verificar_github(email)
        resultados_consolidados['fontes_verificadas'].append(github_result)
        
        if github_result['comprometido']:
            resultados_consolidados['comprometido'] = True
            resultados_consolidados['resultados_adicionais'].extend(github_result.get('resultados', []))
        
        # Calcular totais
        resultados_consolidados['total_breaches'] = len(resultados_consolidados['breaches'])
        
        # Gerar resumo
        if resultados_consolidados['comprometido']:
            resultados_consolidados['resumo'] = f"Email '{email}' foi encontrado em {resultados_consolidados['total_breaches']} vazamento(s) confirmado(s) e {len(resultados_consolidados['resultados_adicionais'])} ocorrência(s) adicionais."
        else:
            resultados_consolidados['resumo'] = f"Email '{email}' não foi encontrado em vazamentos conhecidos nas fontes verificadas."
        
        return resultados_consolidados
    
    def formatar_resultado_para_frontend(self, resultado: Dict) -> Dict:
        """
        Formata resultado para exibição no frontend
        """
        formatado = {
            'email': resultado['email'],
            'comprometido': resultado['comprometido'],
            'total_breaches': resultado['total_breaches'],
            'breaches': [],
            'resultados_adicionais': resultado.get('resultados_adicionais', []),
            'resumo': resultado.get('resumo', ''),
            'aviso': ''
        }
        
        # Formatar breaches
        for breach in resultado.get('breaches', []):
            formatado['breaches'].append({
                'nome': breach.get('nome', 'Desconhecido'),
                'titulo': breach.get('titulo', breach.get('nome', 'Sem título')),
                'data': breach.get('data', 'N/A'),
                'dominio': breach.get('dominio', 'N/A'),
                'total_contas': breach.get('total_contas', 0),
                'dados_vazados': breach.get('dados_vazados', []),
                'descricao': breach.get('descricao', ''),
                'verificado': breach.get('verificado', False),
                'logo': breach.get('logo', '')
            })
        
        # Gerar aviso
        if formatado['comprometido']:
            formatado['aviso'] = f"⚠️ ATENÇÃO: Este email foi encontrado em {formatado['total_breaches']} vazamento(s) de dados!"
        else:
            formatado['aviso'] = "✅ Este email NÃO foi encontrado em vazamentos conhecidos."
        
        return formatado

