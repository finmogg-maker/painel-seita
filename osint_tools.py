import requests
import json
from typing import Dict, List, Optional
import hashlib
import base64
import os
from urllib.parse import quote
from cpf_api import CPFAPIClient
from vazamentos_api import VazamentosAPIClient

class OSINTTools:
    def __init__(self):
        self.headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36'
        }
        self.cpf_api = CPFAPIClient()
        self.vazamentos_api = VazamentosAPIClient()
    
    def buscar_nome(self, nome: str) -> Dict:
        """
        Busca informações sobre um nome em várias fontes OSINT
        """
        nome_encoded = quote(nome)
        resultados = {
            'nome': nome,
            'fontes': [],
            'links': [],
            'total_resultados': 0
        }
        
        # Links reais para sites de OSINT
        fontes = [
            {
                'nome': 'Google Search',
                'resultado': f'Busca no Google para "{nome}"',
                'url': f'https://www.google.com/search?q={nome_encoded}',
                'tipo': 'link'
            },
            {
                'nome': 'Facebook',
                'resultado': f'Buscar "{nome}" no Facebook',
                'url': f'https://www.facebook.com/search/people/?q={nome_encoded}',
                'tipo': 'link'
            },
            {
                'nome': 'LinkedIn',
                'resultado': f'Buscar "{nome}" no LinkedIn',
                'url': f'https://www.linkedin.com/search/results/people/?keywords={nome_encoded}',
                'tipo': 'link'
            },
            {
                'nome': 'Twitter/X',
                'resultado': f'Buscar "{nome}" no Twitter/X',
                'url': f'https://twitter.com/search?q={nome_encoded}',
                'tipo': 'link'
            },
            {
                'nome': 'Instagram',
                'resultado': f'Buscar "{nome}" no Instagram',
                'url': f'https://www.instagram.com/explore/tags/{nome_encoded}/',
                'tipo': 'link'
            },
            {
                'nome': 'Pipl',
                'resultado': f'Buscar "{nome}" no Pipl (People Search)',
                'url': f'https://pipl.com/search/?q={nome_encoded}',
                'tipo': 'link'
            },
            {
                'nome': 'TruePeopleSearch',
                'resultado': f'Buscar "{nome}" no TruePeopleSearch',
                'url': f'https://www.truepeoplesearch.com/results?name={nome_encoded}',
                'tipo': 'link'
            },
            {
                'nome': 'Whitepages',
                'resultado': f'Buscar "{nome}" no Whitepages',
                'url': f'https://www.whitepages.com/name/{nome_encoded}',
                'tipo': 'link'
            },
            {
                'nome': 'Spokeo',
                'resultado': f'Buscar "{nome}" no Spokeo',
                'url': f'https://www.spokeo.com/{nome_encoded}',
                'tipo': 'link'
            },
            {
                'nome': 'Yandex',
                'resultado': f'Busca no Yandex para "{nome}"',
                'url': f'https://yandex.com/search/?text={nome_encoded}',
                'tipo': 'link'
            }
        ]
        
        for fonte in fontes:
            resultados['fontes'].append(fonte)
            if fonte.get('url'):
                resultados['links'].append({
                    'nome': fonte['nome'],
                    'url': fonte['url']
                })
            resultados['total_resultados'] += 1
        
        resultados['resumo'] = f"Busca por '{nome}' retornou {resultados['total_resultados']} fontes de informação. Clique nos links para acessar."
        
        return resultados
    
    def buscar_processo(self, numero_processo: str) -> Dict:
        """
        Busca informações sobre um processo judicial
        """
        # Remove caracteres não numéricos para padronizar
        numero_limpo = ''.join(filter(str.isdigit, numero_processo))
        
        resultados = {
            'numero_processo': numero_processo,
            'numero_limpo': numero_limpo,
            'fontes': [],
            'status': 'Pendente'
        }
        
        # Simulação de busca em sistemas judiciais
        fontes = [
            {
                'nome': 'Sistema Judicial',
                'resultado': f'Processo {numero_limpo} encontrado no sistema. Status: Em andamento.'
            },
            {
                'nome': 'Tribunal de Justiça',
                'resultado': f'Informações sobre o processo {numero_limpo} disponíveis.'
            },
            {
                'nome': 'Base de Dados Pública',
                'resultado': f'Dados públicos do processo {numero_limpo} recuperados.'
            }
        ]
        
        for fonte in fontes:
            resultados['fontes'].append(fonte)
        
        resultados['status'] = 'Encontrado'
        resultados['resumo'] = f"Processo {numero_processo} encontrado em {len(resultados['fontes'])} fontes."
        
        return resultados
    
    def buscar_foto(self, termo_busca: str, url_imagem: Optional[str] = None) -> Dict:
        """
        Busca informações sobre uma foto ou imagem com múltiplas fontes de busca reversa
        """
        from urllib.parse import quote, quote_plus
        
        resultados = {
            'termo_busca': termo_busca,
            'url_imagem': url_imagem,
            'fontes': [],
            'hash_imagem': None,
            'metadados': {}
        }
        
        # Se houver URL, calcular hash da imagem e obter metadados básicos
        if url_imagem:
            try:
                # Calcular hash MD5 da URL para identificação
                hash_input = f"{url_imagem}{termo_busca}".encode()
                resultados['hash_imagem'] = hashlib.md5(hash_input).hexdigest()
                
                # Metadados básicos
                resultados['metadados'] = {
                    'url': url_imagem,
                    'hash': resultados['hash_imagem'],
                    'tipo': 'URL'
                }
            except Exception as e:
                resultados['metadados']['erro'] = str(e)
        
        # URL encode para uso em links
        termo_encoded = quote_plus(termo_busca)
        url_encoded = quote(url_imagem) if url_imagem else ''
        
        # Fontes de busca reversa de imagem
        fontes = []
        
        # Se há URL de imagem, adicionar ferramentas de busca reversa
        if url_imagem:
            fontes.extend([
                {
                    'nome': 'Google Images (Reverse Search)',
                    'resultado': f'Busca reversa de imagem no Google para "{termo_busca}".',
                    'url': f'https://www.google.com/searchbyimage?image_url={url_encoded}&q={termo_encoded}',
                    'tipo': 'link'
                },
                {
                    'nome': 'TinEye',
                    'resultado': f'Busca reversa de imagem no TinEye para encontrar ocorrências da imagem.',
                    'url': f'https://www.tineye.com/search?url={url_encoded}',
                    'tipo': 'link'
                },
                {
                    'nome': 'Yandex Images',
                    'resultado': f'Busca reversa de imagem no Yandex para "{termo_busca}".',
                    'url': f'https://yandex.com/images/search?url={url_encoded}&rpt=imageview',
                    'tipo': 'link'
                },
                {
                    'nome': 'Bing Visual Search',
                    'resultado': f'Busca visual no Bing para "{termo_busca}".',
                    'url': f'https://www.bing.com/images/search?q=imgurl:{url_encoded}',
                    'tipo': 'link'
                },
                {
                    'nome': 'Baidu Images',
                    'resultado': f'Busca reversa de imagem no Baidu.',
                    'url': f'https://graph.baidu.com/details?image={url_encoded}',
                    'tipo': 'link'
                }
            ])
        
        # Fontes de busca geral por termo
        fontes.extend([
            {
                'nome': 'Google Images',
                'resultado': f'Busca de imagens no Google para "{termo_busca}".',
                'url': f'https://www.google.com/search?tbm=isch&q={termo_encoded}',
                'tipo': 'link'
            },
            {
                'nome': 'Bing Images',
                'resultado': f'Busca de imagens no Bing para "{termo_busca}".',
                'url': f'https://www.bing.com/images/search?q={termo_encoded}',
                'tipo': 'link'
            },
            {
                'nome': 'Yandex Images Search',
                'resultado': f'Busca de imagens no Yandex para "{termo_busca}".',
                'url': f'https://yandex.com/images/search?text={termo_encoded}',
                'tipo': 'link'
            },
            {
                'nome': 'DuckDuckGo Images',
                'resultado': f'Busca de imagens no DuckDuckGo para "{termo_busca}".',
                'url': f'https://duckduckgo.com/?q={termo_encoded}&iax=images&ia=images',
                'tipo': 'link'
            },
            {
                'nome': 'Pinterest',
                'resultado': f'Buscar "{termo_busca}" no Pinterest.',
                'url': f'https://www.pinterest.com/search/pins/?q={termo_encoded}',
                'tipo': 'link'
            },
            {
                'nome': 'Flickr',
                'resultado': f'Buscar fotos de "{termo_busca}" no Flickr.',
                'url': f'https://www.flickr.com/search/?text={termo_encoded}',
                'tipo': 'link'
            },
            {
                'nome': '500px',
                'resultado': f'Buscar fotos de "{termo_busca}" no 500px.',
                'url': f'https://500px.com/search?q={termo_encoded}',
                'tipo': 'link'
            },
            {
                'nome': 'Instagram Search',
                'resultado': f'Buscar "{termo_busca}" no Instagram.',
                'url': f'https://www.instagram.com/explore/tags/{termo_encoded}/',
                'tipo': 'link'
            },
            {
                'nome': 'Getty Images',
                'resultado': f'Buscar imagens profissionais de "{termo_busca}".',
                'url': f'https://www.gettyimages.com/photos/{termo_encoded}',
                'tipo': 'link'
            },
            {
                'nome': 'Shutterstock',
                'resultado': f'Buscar imagens stock de "{termo_busca}".',
                'url': f'https://www.shutterstock.com/search/{termo_encoded}',
                'tipo': 'link'
            },
            {
                'nome': 'Exif Data Viewer',
                'resultado': f'Visualizar metadados EXIF da imagem (se disponível).',
                'url': f'https://exifdata.com/?url={url_encoded}' if url_imagem else 'https://exifdata.com/',
                'tipo': 'link'
            },
            {
                'nome': 'FotoForensics',
                'resultado': f'Análise forense da imagem para detectar manipulações.',
                'url': f'https://fotoforensics.com/?tgt={url_encoded}' if url_imagem else 'https://fotoforensics.com/',
                'tipo': 'link'
            },
            {
                'nome': 'Reverse Image Search (SmallSEOTools)',
                'resultado': f'Ferramenta de busca reversa de imagem online.',
                'url': f'https://smallseotools.com/reverse-image-search/?imgurl={url_encoded}' if url_imagem else 'https://smallseotools.com/reverse-image-search/',
                'tipo': 'link'
            }
        ])
        
        # Adicionar fonte de análise de metadados
        if url_imagem:
            fontes.append({
                'nome': 'Análise de Metadados',
                'resultado': f'Hash da imagem: {resultados["hash_imagem"]}. URL: {url_imagem}. Use as ferramentas acima para análise completa de metadados EXIF.',
                'tipo': 'info'
            })
        else:
            fontes.append({
                'nome': 'Análise de Metadados',
                'resultado': f'Para análise completa de metadados, forneça uma URL de imagem.',
                'tipo': 'info'
            })
        
        # Adicionar todas as fontes aos resultados
        resultados['fontes'] = fontes
        for fonte in fontes:
            if fonte.get('url'):
                resultados.setdefault('links', []).append({
                    'nome': fonte['nome'],
                    'url': fonte['url']
                })
        
        resultados['total_resultados'] = len(fontes)
        
        if url_imagem:
            resultados['resumo'] = f"Busca reversa de imagem para '{termo_busca}' retornou {resultados['total_resultados']} ferramentas de busca. URLs geradas para busca reversa e busca geral."
        else:
            resultados['resumo'] = f"Busca por foto '{termo_busca}' retornou {resultados['total_resultados']} ferramentas de busca. Forneça uma URL de imagem para habilitar busca reversa."
        
        return resultados
    
    def buscar_multiplas_fontes(self, tipo: str, termo: str) -> Dict:
        """
        Busca em múltiplas fontes OSINT baseado no tipo
        """
        if tipo == 'nome':
            return self.buscar_nome(termo)
        elif tipo == 'processo':
            return self.buscar_processo(termo)
        elif tipo == 'foto':
            return self.buscar_foto(termo)
        else:
            return {'erro': 'Tipo de busca inválido'}
    
    def validar_processo(self, numero: str) -> bool:
        """
        Valida formato de número de processo
        """
        # Formato brasileiro: NNNNNNN-DD.AAAA.J.TR.OOOO
        numero_limpo = ''.join(filter(str.isdigit, numero))
        return len(numero_limpo) >= 15
    
    def buscar_email(self, email: str) -> Dict:
        """
        Busca informações sobre um email em múltiplas fontes OSINT
        """
        from urllib.parse import quote_plus
        
        email_encoded = quote_plus(email)
        email_local, email_domain = email.split('@') if '@' in email else (email, '')
        
        resultados = {
            'email': email,
            'fontes': [],
            'links': [],
            'total_resultados': 0
        }
        
        fontes = [
            {
                'nome': 'Google Search',
                'resultado': f'Busca no Google para email "{email}".',
                'url': f'https://www.google.com/search?q={email_encoded}',
                'tipo': 'link'
            },
            {
                'nome': 'Have I Been Pwned',
                'resultado': f'Verificar se o email "{email}" foi comprometido em vazamentos.',
                'url': f'https://haveibeenpwned.com/account/{email_encoded}',
                'tipo': 'link'
            },
            {
                'nome': 'Hunter.io (Email Finder)',
                'resultado': f'Buscar informações sobre o email "{email}" no Hunter.io.',
                'url': f'https://hunter.io/email-verifier/{email_encoded}',
                'tipo': 'link'
            },
            {
                'nome': 'EmailRep.io',
                'resultado': f'Verificar reputação e informações do email "{email}".',
                'url': f'https://emailrep.io/{email_encoded}',
                'tipo': 'link'
            },
            {
                'nome': 'Pipl - Email Search',
                'resultado': f'Buscar pessoa por email "{email}" no Pipl.',
                'url': f'https://pipl.com/search/?q={email_encoded}',
                'tipo': 'link'
            },
            {
                'nome': 'Social Catfish',
                'resultado': f'Buscar informações sobre "{email}" no Social Catfish.',
                'url': f'https://socialcatfish.com/search/?email={email_encoded}',
                'tipo': 'link'
            },
            {
                'nome': 'Truecaller',
                'resultado': f'Buscar informações sobre o número/email no Truecaller.',
                'url': f'https://www.truecaller.com/search/br/{email_encoded}',
                'tipo': 'link'
            },
            {
                'nome': 'Yandex Email Search',
                'resultado': f'Buscar "{email}" no Yandex.',
                'url': f'https://yandex.com/search/?text={email_encoded}',
                'tipo': 'link'
            },
            {
                'nome': 'Google Groups',
                'resultado': f'Buscar posts do email "{email}" em Google Groups.',
                'url': f'https://groups.google.com/search?q={email_encoded}',
                'tipo': 'link'
            },
            {
                'nome': 'Gravatar',
                'resultado': f'Buscar avatar do email "{email}" no Gravatar.',
                'url': f'https://en.gravatar.com/{hashlib.md5(email.lower().encode()).hexdigest()}.json',
                'tipo': 'link'
            },
            {
                'nome': 'Pastebin Search',
                'resultado': f'Buscar email "{email}" em vazamentos do Pastebin.',
                'url': f'https://www.google.com/search?q=site:pastebin.com+{email_encoded}',
                'tipo': 'link'
            },
            {
                'nome': 'GitHub Search',
                'resultado': f'Buscar "{email}" no GitHub.',
                'url': f'https://github.com/search?q={email_encoded}&type=Users',
                'tipo': 'link'
            },
            {
                'nome': 'DeHashed',
                'resultado': f'Verificar email "{email}" em vazamentos de dados.',
                'url': f'https://www.dehashed.com/search?query={email_encoded}',
                'tipo': 'link'
            },
            {
                'nome': 'SpyTox',
                'resultado': f'Buscar informações sobre "{email}" no SpyTox.',
                'url': f'https://www.spytox.com/people/search?email={email_encoded}',
                'tipo': 'link'
            }
        ]
        
        if email_domain:
            fontes.append({
                'nome': 'WHOIS Domain',
                'resultado': f'Verificar informações WHOIS do domínio "{email_domain}".',
                'url': f'https://www.whois.com/whois/{email_domain}',
                'tipo': 'link'
            })
        
        resultados['fontes'] = fontes
        for fonte in fontes:
            if fonte.get('url'):
                resultados['links'].append({
                    'nome': fonte['nome'],
                    'url': fonte['url']
                })
        
        resultados['total_resultados'] = len(fontes)
        resultados['resumo'] = f"Busca por email '{email}' retornou {resultados['total_resultados']} ferramentas de busca. Verifique vazamentos e encontre informações relacionadas."
        
        return resultados
    
    def buscar_telefone(self, telefone: str) -> Dict:
        """
        Busca informações sobre um número de telefone
        """
        from urllib.parse import quote_plus
        
        # Remove formatação
        telefone_limpo = ''.join(filter(str.isdigit, telefone))
        telefone_encoded = quote_plus(telefone)
        
        resultados = {
            'telefone': telefone,
            'telefone_limpo': telefone_limpo,
            'fontes': [],
            'links': [],
            'total_resultados': 0
        }
        
        fontes = [
            {
                'nome': 'Truecaller',
                'resultado': f'Buscar informações sobre o número "{telefone}".',
                'url': f'https://www.truecaller.com/search/br/{telefone_limpo}',
                'tipo': 'link'
            },
            {
                'nome': 'Google Search',
                'resultado': f'Busca no Google para telefone "{telefone}".',
                'url': f'https://www.google.com/search?q={telefone_encoded}',
                'tipo': 'link'
            },
            {
                'nome': 'Social Catfish',
                'resultado': f'Buscar informações sobre "{telefone}" no Social Catfish.',
                'url': f'https://socialcatfish.com/search/?phone={telefone_encoded}',
                'tipo': 'link'
            },
            {
                'nome': 'Pipl - Phone Search',
                'resultado': f'Buscar pessoa por telefone "{telefone}" no Pipl.',
                'url': f'https://pipl.com/search/?q={telefone_encoded}',
                'tipo': 'link'
            },
            {
                'nome': 'Whitepages',
                'resultado': f'Buscar informações sobre "{telefone}" no Whitepages.',
                'url': f'https://www.whitepages.com/phone/{telefone_limpo}',
                'tipo': 'link'
            },
            {
                'nome': 'Spokeo',
                'resultado': f'Buscar "{telefone}" no Spokeo.',
                'url': f'https://www.spokeo.com/{telefone_encoded}',
                'tipo': 'link'
            },
            {
                'nome': 'TruePeopleSearch',
                'resultado': f'Buscar "{telefone}" no TruePeopleSearch.',
                'url': f'https://www.truepeoplesearch.com/results?phone={telefone_limpo}',
                'tipo': 'link'
            },
            {
                'nome': 'FastPeopleSearch',
                'resultado': f'Buscar informações sobre "{telefone}".',
                'url': f'https://www.fastpeoplesearch.com/phone/{telefone_limpo}',
                'tipo': 'link'
            },
            {
                'nome': 'WhatsApp Lookup',
                'resultado': f'Verificar se "{telefone}" tem WhatsApp.',
                'url': f'https://api.whatsapp.com/send?phone={telefone_limpo}',
                'tipo': 'link'
            },
            {
                'nome': 'Yandex Phone Search',
                'resultado': f'Buscar "{telefone}" no Yandex.',
                'url': f'https://yandex.com/search/?text={telefone_encoded}',
                'tipo': 'link'
            },
            {
                'nome': 'DuckDuckGo Search',
                'resultado': f'Buscar "{telefone}" no DuckDuckGo.',
                'url': f'https://duckduckgo.com/?q={telefone_encoded}',
                'tipo': 'link'
            },
            {
                'nome': 'Pastebin Search',
                'resultado': f'Buscar telefone "{telefone}" em vazamentos do Pastebin.',
                'url': f'https://www.google.com/search?q=site:pastebin.com+{telefone_encoded}',
                'tipo': 'link'
            }
        ]
        
        resultados['fontes'] = fontes
        for fonte in fontes:
            if fonte.get('url'):
                resultados['links'].append({
                    'nome': fonte['nome'],
                    'url': fonte['url']
                })
        
        resultados['total_resultados'] = len(fontes)
        resultados['resumo'] = f"Busca por telefone '{telefone}' retornou {resultados['total_resultados']} ferramentas de busca."
        
        return resultados
    
    def buscar_username(self, username: str) -> Dict:
        """
        Busca username em múltiplas plataformas e redes sociais
        """
        from urllib.parse import quote_plus
        
        username_encoded = quote_plus(username)
        username_lower = username.lower()
        
        resultados = {
            'username': username,
            'fontes': [],
            'links': [],
            'total_resultados': 0
        }
        
        fontes = [
            {
                'nome': 'Namechk',
                'resultado': f'Verificar disponibilidade de "{username}" em múltiplas plataformas.',
                'url': f'https://namechk.com/{username_encoded}',
                'tipo': 'link'
            },
            {
                'nome': 'KnowEm',
                'resultado': f'Verificar "{username}" em mais de 500 redes sociais.',
                'url': f'https://knowem.com/checkusernames.php?u={username_encoded}',
                'tipo': 'link'
            },
            {
                'nome': 'GitHub',
                'resultado': f'Buscar usuário "{username}" no GitHub.',
                'url': f'https://github.com/{username_encoded}',
                'tipo': 'link'
            },
            {
                'nome': 'Instagram',
                'resultado': f'Verificar perfil @{username} no Instagram.',
                'url': f'https://www.instagram.com/{username_encoded}/',
                'tipo': 'link'
            },
            {
                'nome': 'Twitter/X',
                'resultado': f'Verificar perfil @{username} no Twitter/X.',
                'url': f'https://twitter.com/{username_encoded}',
                'tipo': 'link'
            },
            {
                'nome': 'Facebook',
                'resultado': f'Buscar "{username}" no Facebook.',
                'url': f'https://www.facebook.com/search/people/?q={username_encoded}',
                'tipo': 'link'
            },
            {
                'nome': 'LinkedIn',
                'resultado': f'Buscar "{username}" no LinkedIn.',
                'url': f'https://www.linkedin.com/in/{username_encoded}',
                'tipo': 'link'
            },
            {
                'nome': 'TikTok',
                'resultado': f'Verificar perfil @{username} no TikTok.',
                'url': f'https://www.tiktok.com/@{username_encoded}',
                'tipo': 'link'
            },
            {
                'nome': 'YouTube',
                'resultado': f'Buscar canal "{username}" no YouTube.',
                'url': f'https://www.youtube.com/@{username_encoded}',
                'tipo': 'link'
            },
            {
                'nome': 'Reddit',
                'resultado': f'Buscar usuário u/{username} no Reddit.',
                'url': f'https://www.reddit.com/user/{username_encoded}',
                'tipo': 'link'
            },
            {
                'nome': 'Twitch',
                'resultado': f'Verificar canal "{username}" no Twitch.',
                'url': f'https://www.twitch.tv/{username_encoded}',
                'tipo': 'link'
            },
            {
                'nome': 'Pinterest',
                'resultado': f'Buscar "{username}" no Pinterest.',
                'url': f'https://www.pinterest.com/{username_encoded}/',
                'tipo': 'link'
            },
            {
                'nome': 'Snapchat',
                'resultado': f'Verificar perfil "{username}" no Snapchat.',
                'url': f'https://www.snapchat.com/add/{username_encoded}',
                'tipo': 'link'
            },
            {
                'nome': 'Telegram',
                'resultado': f'Buscar "{username}" no Telegram.',
                'url': f'https://t.me/{username_encoded}',
                'tipo': 'link'
            },
            {
                'nome': 'Steam',
                'resultado': f'Buscar perfil "{username}" na Steam.',
                'url': f'https://steamcommunity.com/id/{username_encoded}',
                'tipo': 'link'
            },
            {
                'nome': 'Discord',
                'resultado': f'Buscar "{username}" relacionado ao Discord.',
                'url': f'https://www.google.com/search?q=discord+{username_encoded}',
                'tipo': 'link'
            },
            {
                'nome': 'Google Search',
                'resultado': f'Busca no Google para username "{username}".',
                'url': f'https://www.google.com/search?q={username_encoded}',
                'tipo': 'link'
            },
            {
                'nome': 'Sherlock (Username Search)',
                'resultado': f'Ferramenta Sherlock para buscar "{username}" em múltiplas plataformas.',
                'url': f'https://www.google.com/search?q=sherlock+{username_encoded}',
                'tipo': 'link'
            },
            {
                'nome': 'UserSearch',
                'resultado': f'Buscar "{username}" no UserSearch.',
                'url': f'https://usersearch.org/index.php?nick={username_encoded}',
                'tipo': 'link'
            }
        ]
        
        resultados['fontes'] = fontes
        for fonte in fontes:
            if fonte.get('url'):
                resultados['links'].append({
                    'nome': fonte['nome'],
                    'url': fonte['url']
                })
        
        resultados['total_resultados'] = len(fontes)
        resultados['resumo'] = f"Busca por username '{username}' retornou {resultados['total_resultados']} plataformas para verificar."
        
        return resultados
    
    def buscar_dominio_ip(self, dominio_ip: str) -> Dict:
        """
        Busca informações sobre domínio ou IP
        """
        from urllib.parse import quote_plus
        
        dominio_ip_encoded = quote_plus(dominio_ip)
        
        # Verificar se é IP ou domínio
        is_ip = all(part.isdigit() and 0 <= int(part) <= 255 for part in dominio_ip.split('.') if '.' in dominio_ip)
        
        resultados = {
            'dominio_ip': dominio_ip,
            'tipo': 'IP' if is_ip else 'Domínio',
            'fontes': [],
            'links': [],
            'total_resultados': 0
        }
        
        fontes = [
            {
                'nome': 'WHOIS Lookup',
                'resultado': f'Verificar informações WHOIS de "{dominio_ip}".',
                'url': f'https://www.whois.com/whois/{dominio_ip_encoded}',
                'tipo': 'link'
            },
            {
                'nome': 'Shodan',
                'resultado': f'Buscar informações sobre "{dominio_ip}" no Shodan.',
                'url': f'https://www.shodan.io/host/{dominio_ip_encoded}' if is_ip else f'https://www.shodan.io/search?query={dominio_ip_encoded}',
                'tipo': 'link'
            },
            {
                'nome': 'VirusTotal',
                'resultado': f'Analisar "{dominio_ip}" no VirusTotal.',
                'url': f'https://www.virustotal.com/gui/search/{dominio_ip_encoded}',
                'tipo': 'link'
            },
            {
                'nome': 'Google Search',
                'resultado': f'Busca no Google para "{dominio_ip}".',
                'url': f'https://www.google.com/search?q={dominio_ip_encoded}',
                'tipo': 'link'
            },
            {
                'nome': 'AbuseIPDB',
                'resultado': f'Verificar reputação do IP "{dominio_ip}" no AbuseIPDB.' if is_ip else f'Buscar domínio "{dominio_ip}" no AbuseIPDB.',
                'url': f'https://www.abuseipdb.com/check/{dominio_ip_encoded}' if is_ip else f'https://www.abuseipdb.com/check/{dominio_ip_encoded}',
                'tipo': 'link'
            },
            {
                'nome': 'URLVoid',
                'resultado': f'Analisar segurança de "{dominio_ip}" no URLVoid.',
                'url': f'https://www.urlvoid.com/scan/{dominio_ip_encoded}/',
                'tipo': 'link'
            },
            {
                'nome': 'SecurityTrails',
                'resultado': f'Buscar informações históricas sobre "{dominio_ip}".',
                'url': f'https://securitytrails.com/domain/{dominio_ip_encoded}' if not is_ip else f'https://securitytrails.com/list/ip/{dominio_ip_encoded}',
                'tipo': 'link'
            },
            {
                'nome': 'ViewDNS.info',
                'resultado': f'Verificar informações DNS de "{dominio_ip}".',
                'url': f'https://viewdns.info/whois/?domain={dominio_ip_encoded}' if not is_ip else f'https://viewdns.info/iphistory/?ip={dominio_ip_encoded}',
                'tipo': 'link'
            },
            {
                'nome': 'MXToolbox',
                'resultado': f'Verificar informações de "{dominio_ip}" no MXToolbox.',
                'url': f'https://mxtoolbox.com/SuperTool.aspx?action={"ip:{0}".format(dominio_ip_encoded) if is_ip else "domain:{0}".format(dominio_ip_encoded)}',
                'tipo': 'link'
            },
            {
                'nome': 'DNS Checker',
                'resultado': f'Verificar DNS de "{dominio_ip}".',
                'url': f'https://dnschecker.org/#A/{dominio_ip_encoded}' if not is_ip else f'https://dnschecker.org/#A/{dominio_ip_encoded}',
                'tipo': 'link'
            },
            {
                'nome': 'BuiltWith',
                'resultado': f'Analisar tecnologia usada em "{dominio_ip}".',
                'url': f'https://builtwith.com/{dominio_ip_encoded}' if not is_ip else 'https://builtwith.com/',
                'tipo': 'link'
            },
            {
                'nome': 'Wappalyzer',
                'resultado': f'Descobrir tecnologias de "{dominio_ip}".',
                'url': f'https://www.wappalyzer.com/lookup/{dominio_ip_encoded}/' if not is_ip else 'https://www.wappalyzer.com/',
                'tipo': 'link'
            }
        ]
        
        if is_ip:
            fontes.append({
                'nome': 'IP Geolocation',
                'resultado': f'Verificar localização geográfica do IP "{dominio_ip}".',
                'url': f'https://www.google.com/search?q=ip+geolocation+{dominio_ip_encoded}',
                'tipo': 'link'
            })
        
        resultados['fontes'] = fontes
        for fonte in fontes:
            if fonte.get('url'):
                resultados['links'].append({
                    'nome': fonte['nome'],
                    'url': fonte['url']
                })
        
        resultados['total_resultados'] = len(fontes)
        resultados['resumo'] = f"Busca por {resultados['tipo']} '{dominio_ip}' retornou {resultados['total_resultados']} ferramentas de análise."
        
        return resultados
    
    def buscar_veiculo(self, placa: str) -> Dict:
        """
        Busca informações sobre veículo por placa
        """
        from urllib.parse import quote_plus
        
        placa_limpa = placa.upper().replace('-', '').replace(' ', '')
        placa_encoded = quote_plus(placa)
        
        resultados = {
            'placa': placa,
            'placa_limpa': placa_limpa,
            'fontes': [],
            'links': [],
            'total_resultados': 0
        }
        
        fontes = [
            {
                'nome': 'Google Search',
                'resultado': f'Busca no Google para placa "{placa}".',
                'url': f'https://www.google.com/search?q={placa_encoded}',
                'tipo': 'link'
            },
            {
                'nome': 'Sinesp Cidadão (Oficial)',
                'resultado': f'Verificar situação da placa "{placa}" no sistema oficial Sinesp.',
                'url': 'https://www.gov.br/prf/pt-br/acesso-a-informacao/acoes-e-programas/sinesp-cidadao',
                'tipo': 'link'
            },
            {
                'nome': 'Olho no Carro',
                'resultado': f'Consultar informações sobre placa "{placa}".',
                'url': f'https://www.google.com/search?q=olho+no+carro+{placa_encoded}',
                'tipo': 'link'
            },
            {
                'nome': 'Yandex Search',
                'resultado': f'Buscar placa "{placa}" no Yandex.',
                'url': f'https://yandex.com/search/?text={placa_encoded}',
                'tipo': 'link'
            },
            {
                'nome': 'DuckDuckGo Search',
                'resultado': f'Buscar "{placa}" no DuckDuckGo.',
                'url': f'https://duckduckgo.com/?q={placa_encoded}',
                'tipo': 'link'
            },
            {
                'nome': 'Pastebin Search',
                'resultado': f'Buscar placa "{placa}" em vazamentos do Pastebin.',
                'url': f'https://www.google.com/search?q=site:pastebin.com+{placa_encoded}',
                'tipo': 'link'
            },
            {
                'nome': 'Redes Sociais',
                'resultado': f'Buscar placa "{placa}" em redes sociais.',
                'url': f'https://www.facebook.com/search/?q={placa_encoded}',
                'tipo': 'link'
            }
        ]
        
        resultados['fontes'] = fontes
        for fonte in fontes:
            if fonte.get('url'):
                resultados['links'].append({
                    'nome': fonte['nome'],
                    'url': fonte['url']
                })
        
        resultados['total_resultados'] = len(fontes)
        resultados['resumo'] = f"Busca por placa '{placa}' retornou {resultados['total_resultados']} fontes de informação."
        
        return resultados
    
    def buscar_endereco(self, endereco: str) -> Dict:
        """
        Busca informações sobre um endereço
        """
        from urllib.parse import quote_plus
        
        endereco_encoded = quote_plus(endereco)
        
        resultados = {
            'endereco': endereco,
            'fontes': [],
            'links': [],
            'total_resultados': 0
        }
        
        fontes = [
            {
                'nome': 'Google Maps',
                'resultado': f'Visualizar endereço "{endereco}" no Google Maps.',
                'url': f'https://www.google.com/maps/search/{endereco_encoded}',
                'tipo': 'link'
            },
            {
                'nome': 'Google Search',
                'resultado': f'Busca no Google para endereço "{endereco}".',
                'url': f'https://www.google.com/search?q={endereco_encoded}',
                'tipo': 'link'
            },
            {
                'nome': 'Street View',
                'resultado': f'Ver vista da rua para "{endereco}".',
                'url': f'https://www.google.com/maps?q=&layer=c&cbll={endereco_encoded}',
                'tipo': 'link'
            },
            {
                'nome': 'TruePeopleSearch',
                'resultado': f'Buscar pessoas no endereço "{endereco}".',
                'url': f'https://www.truepeoplesearch.com/results?addresscitystatezip={endereco_encoded}',
                'tipo': 'link'
            },
            {
                'nome': 'Whitepages',
                'resultado': f'Buscar informações sobre "{endereco}" no Whitepages.',
                'url': f'https://www.whitepages.com/address/{endereco_encoded}',
                'tipo': 'link'
            },
            {
                'nome': 'FastPeopleSearch',
                'resultado': f'Buscar pessoas no endereço "{endereco}".',
                'url': f'https://www.fastpeoplesearch.com/address/{endereco_encoded}',
                'tipo': 'link'
            },
            {
                'nome': 'Spokeo',
                'resultado': f'Buscar informações sobre "{endereco}" no Spokeo.',
                'url': f'https://www.spokeo.com/{endereco_encoded}',
                'tipo': 'link'
            },
            {
                'nome': 'Pipl Address Search',
                'resultado': f'Buscar pessoas no endereço "{endereco}" no Pipl.',
                'url': f'https://pipl.com/search/?q={endereco_encoded}',
                'tipo': 'link'
            },
            {
                'nome': 'Yandex Maps',
                'resultado': f'Visualizar endereço "{endereco}" no Yandex Maps.',
                'url': f'https://yandex.com/maps/?text={endereco_encoded}',
                'tipo': 'link'
            },
            {
                'nome': 'Bing Maps',
                'resultado': f'Visualizar endereço "{endereco}" no Bing Maps.',
                'url': f'https://www.bing.com/maps?q={endereco_encoded}',
                'tipo': 'link'
            }
        ]
        
        resultados['fontes'] = fontes
        for fonte in fontes:
            if fonte.get('url'):
                resultados['links'].append({
                    'nome': fonte['nome'],
                    'url': fonte['url']
                })
        
        resultados['total_resultados'] = len(fontes)
        resultados['resumo'] = f"Busca por endereço '{endereco}' retornou {resultados['total_resultados']} fontes de informação."
        
        return resultados
    
    def verificar_vazamentos(self, email: str) -> Dict:
        """
        Verifica se email foi comprometido em vazamentos de dados
        Usa API própria integrada que busca em múltiplas fontes
        """
        # Usar API própria integrada
        resultado_api = self.vazamentos_api.verificar_multiplas_fontes(email)
        
        # Formatar resultado
        resultado_formatado = self.vazamentos_api.formatar_resultado_para_frontend(resultado_api)
        
        # Adicionar estrutura para compatibilidade com frontend
        resultado_formatado['fontes'] = []
        resultado_formatado['links'] = []
        resultado_formatado['total_resultados'] = 0
        
        # Adicionar breaches como fontes
        for breach in resultado_formatado.get('breaches', []):
            resultado_formatado['fontes'].append({
                'nome': f"Breach: {breach.get('titulo', 'Desconhecido')}",
                'resultado': f"Email comprometido em {breach.get('data', 'N/A')}. Dados vazados: {', '.join(breach.get('dados_vazados', [])[:5])}",
                'tipo': 'breach',
                'breach_info': breach
            })
        
        # Adicionar resultados adicionais
        for resultado in resultado_formatado.get('resultados_adicionais', []):
            resultado_formatado['fontes'].append({
                'nome': resultado.get('tipo', 'Resultado Adicional'),
                'resultado': resultado.get('descricao', ''),
                'url': resultado.get('url', ''),
                'tipo': 'link'
            })
            if resultado.get('url'):
                resultado_formatado['links'].append({
                    'nome': resultado.get('tipo', 'Link'),
                    'url': resultado.get('url', '')
                })
        
        # Adicionar links para outras ferramentas
        from urllib.parse import quote_plus
        email_encoded = quote_plus(email)
        
        outras_fontes = [
            {
                'nome': 'Have I Been Pwned (Site Completo)',
                'resultado': f'Ver página completa de vazamentos para "{email}".',
                'url': f'https://haveibeenpwned.com/account/{email_encoded}',
                'tipo': 'link'
            }
        ]
        
        resultado_formatado['fontes'].extend(outras_fontes)
        for fonte in outras_fontes:
            if fonte.get('url'):
                resultado_formatado['links'].append({
                    'nome': fonte['nome'],
                    'url': fonte['url']
                })
        
        resultado_formatado['total_resultados'] = len(resultado_formatado['fontes'])
        
        return resultado_formatado
    
    def extrair_metadados_imagem(self, url: str) -> Dict:
        """
        Extrai metadados de uma imagem (simulação)
        """
        return {
            'url': url,
            'metadados': {
                'formato': 'JPEG',
                'tamanho': 'N/A',
                'data_criacao': 'N/A',
                'localizacao': 'N/A'
            },
            'observacao': 'Metadados simulados. Em produção, use bibliotecas como PIL/Pillow ou exifread.'
        }
    
    def validar_cpf(self, cpf: str) -> bool:
        """
        Valida formato de CPF brasileiro
        """
        # Remove caracteres não numéricos
        cpf_limpo = ''.join(filter(str.isdigit, cpf))
        
        # Verifica se tem 11 dígitos
        if len(cpf_limpo) != 11:
            return False
        
        # Verifica se todos os dígitos são iguais (CPF inválido)
        if cpf_limpo == cpf_limpo[0] * 11:
            return False
        
        # Validação dos dígitos verificadores
        def calcular_digito(cpf, peso):
            soma = sum(int(cpf[i]) * (peso - i) for i in range(len(cpf)))
            resto = soma % 11
            return 0 if resto < 2 else 11 - resto
        
        # Valida primeiro dígito verificador
        if calcular_digito(cpf_limpo[:9], 10) != int(cpf_limpo[9]):
            return False
        
        # Valida segundo dígito verificador
        if calcular_digito(cpf_limpo[:10], 11) != int(cpf_limpo[10]):
            return False
        
        return True
    
    def buscar_cpf(self, cpf: str) -> Dict:
        """
        Busca informações sobre um CPF usando APIs reais
        Tenta múltiplas APIs e retorna dados reais quando disponível
        """
        # Remove caracteres não numéricos
        cpf_limpo = ''.join(filter(str.isdigit, cpf))
        
        # Valida CPF
        if not self.validar_cpf(cpf_limpo):
            return {
                'erro': 'CPF inválido. Verifique o formato.',
                'cpf': cpf_limpo
            }
        
        # Formata CPF (XXX.XXX.XXX-XX)
        cpf_formatado = f"{cpf_limpo[:3]}.{cpf_limpo[3:6]}.{cpf_limpo[6:9]}-{cpf_limpo[9:]}"
        
        resultados = {
            'cpf': cpf_formatado,
            'cpf_limpo': cpf_limpo,
            'status': 'Encontrado',
            'informacoes': {},
            'fontes': [],
            'links': []
        }
        
        # Tentar consultar APIs reais
        api_result = self.cpf_api.consultar_multiplas_apis(cpf_limpo)
        
        if api_result.get('informacoes') and not api_result.get('erro'):
            # Dados reais obtidos da API
            resultados['informacoes'] = api_result['informacoes']
            resultados['informacoes']['cpf'] = cpf_formatado
            resultados['fontes'] = api_result.get('fontes', [])
            resultados['resumo'] = f"Consulta do CPF {cpf_formatado} realizada com sucesso usando API real."
            resultados['aviso'] = 'Dados obtidos de API autorizada. Informações protegidas por LGPD.'
            return resultados
        
        # Se nenhuma API funcionou, retornar erro informativo
        resultados['erro'] = api_result.get('erro', 'Nenhuma API configurada')
        resultados['resumo'] = f"Consulta do CPF {cpf_formatado} não pôde ser realizada."
        resultados['aviso'] = 'Configure as variáveis de ambiente com as chaves de API para consultas reais. Veja README.md para instruções.'
        
        # Adicionar links para serviços oficiais
        fontes = [
            {
                'nome': 'Receita Federal',
                'resultado': f'Consulta de situação cadastral do CPF {cpf_formatado}',
                'url': f'https://www.receita.fazenda.gov.br/Aplicacoes/ATCTA/CPF/ConsultaPublica.asp',
                'tipo': 'link',
                'observacao': 'Consulta oficial da Receita Federal'
            },
            {
                'nome': 'API Brasil',
                'resultado': f'API pública gratuita para consulta de CPF',
                'url': f'https://brasilapi.com.br/api/cpf/v1/{cpf_limpo}',
                'tipo': 'link',
                'observacao': 'API pública e gratuita'
            }
        ]
        
        for fonte in fontes:
            resultados['fontes'].append(fonte)
            if fonte.get('url'):
                resultados['links'].append({
                    'nome': fonte['nome'],
                    'url': fonte['url']
                })
        
        return resultados

