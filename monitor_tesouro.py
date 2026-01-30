import os
import requests
import smtplib
from email.mime.text import MIMEText

# --- CONFIGURAÇÕES ---
GMAIL_USER = 'edonizete7@gmail.com'
GMAIL_PASS = os.getenv('GMAIL_PASS')

# Lista completa com seus 14 títulos
minha_carteira = [
    {"nome": "IPCA+ 2026", "filtro": "Tesouro IPCA+ 2026", "alerta": 4.50},
    {"nome": "IPCA+ 2029", "filtro": "Tesouro IPCA+ 2029", "alerta": 6.00},
    {"nome": "IPCA+ 2035 (Semestral 1)", "filtro": "Tesouro IPCA+ com Juros Semestrais 2035", "alerta": 7.40},
    {"nome": "IPCA+ 2035 (Semestral 2)", "filtro": "Tesouro IPCA+ com Juros Semestrais 2035", "alerta": 7.60},
    {"nome": "IPCA+ 2035 (Semestral 3)", "filtro": "Tesouro IPCA+ com Juros Semestrais 2035", "alerta": 6.30},
    {"nome": "IPCA+ 2040 (Semestral 1)", "filtro": "Tesouro IPCA+ com Juros Semestrais 2040", "alerta": 6.00},
    {"nome": "IPCA+ 2040 (Semestral 2)", "filtro": "Tesouro IPCA+ com Juros Semestrais 2040", "alerta": 6.30},
    {"nome": "IPCA+ 2040 (Semestral 3)", "filtro": "Tesouro IPCA+ com Juros Semestrais 2040", "alerta": 7.30},
    {"nome": "IPCA+ 2055 (Semestral 1)", "filtro": "Tesouro IPCA+ com Juros Semestrais 2055", "alerta": 6.10},
    {"nome": "IPCA+ 2055 (Semestral 2)", "filtro": "Tesouro IPCA+ com Juros Semestrais 2055", "alerta": 7.20},
    {"nome": "PREFIXADO 2031", "filtro": "Tesouro Prefixado com Juros Semestrais 2031", "alerta": 12.10},
    {"nome": "SELIC 2029", "filtro": "Tesouro Selic 2029", "alerta": 0.10},
    {"nome": "SELIC 2031", "filtro": "Tesouro Selic 2031", "alerta": 0.15},
    {"nome": "IPCA+ 2035 (Aporte Extra)", "filtro": "Tesouro IPCA+ com Juros Semestrais 2035", "alerta": 6.00}
]

def buscar_taxas_api():
    # Link oficial da B3 que alimenta o Tesouro
    url = "https://www.tesourodireto.com.br/json/br/com/b3/tesourodireto/service/api/treasurybondsinfo.json"
    
    # Headers reforçados para evitar bloqueios (simula um navegador real)
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/122.0.0.0 Safari/537.36',
        'Accept': 'application/json, text/plain, */*',
        'Referer': 'https://www.tesourodireto.com.br/titulos/precos-e-taxas.asp',
        'Origin': 'https://www.tesourodireto.com.br'
    }
    
    try:
        response = requests.get(url, headers=headers, timeout=30)
        
        # Se o site responder algo diferente de OK (200)
        if response.status_code != 200:
            print(f"⚠️ O site do Tesouro retornou erro HTTP {response.status_code}")
            return None
            
        dados = response.json()
        lista = dados['response']['TrsuryBondIndxList']
        
        # Cria um dicionário: { "Nome do Titulo": Taxa }
        return {t['TrsuryBond']['nm']: t['TrsuryBond']['anulInvstmtRate'] for t in lista}
        
    except requests.exceptions.JSONDecodeError:
        print("❌ Erro: O site retornou uma página vazia ou inválida (Mercado pode estar suspenso).")
        return None
    except Exception as e:
        print(f"⚠️ Erro inesperado: {e}")
        return None

def executar():
    print("🔍 Iniciando busca de taxas na B3...")
    taxas = buscar_taxas_api()
    
    if not taxas:
        print("❌ Operação cancelada por falta de dados da API.")
        return

    alertas_encontrados = []
    for t in minha_carteira:
        taxa_mercado = taxas.get(t['filtro'])
        
        if taxa_mercado is not None:
            # Verifica se a taxa de mercado é MENOR ou IGUAL ao seu alerta
            if taxa_mercado <= t['alerta'] and t['alerta'] > 0:
                alertas_encontrados.append(f"📌 {t['nome']}: Mercado {taxa_mercado}% <= Alerta {t['alerta']}%")
        else:
            print(f"❓ Filtro não encontrado: {t['filtro']}")

    if alertas_encontrados:
        corpo_email = "Oportunidades encontradas:\n\n" + "\n".join(alertas_encontrados)
        msg = MIMEText(corpo_email)
        msg['Subject'] = "⚠️ OPORTUNIDADE: Alerta de Taxas Tesouro"
        msg['From'], msg['To'] = GMAIL_USER, GMAIL_USER
        try:
            with smtplib.SMTP_SSL('smtp.gmail.com', 465) as s:
                s.login(GMAIL_USER, GMAIL_PASS)
                s.send_message(msg)
            print("✅ Alerta enviado com sucesso por e-mail!")
        except Exception as e:
            print(f"❌ Erro ao enviar e-mail: {e}")
    else:
        print(f"😴 Monitoradas {len(minha_carteira)} taxas. Nenhuma oportunidade de lucro no momento.")

if __name__ == "__main__":
    executar()
