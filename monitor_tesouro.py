import os
import requests
import smtplib
from email.mime.text import MIMEText

# --- CONFIGURAÇÕES ---
GMAIL_USER = 'edonizete7@gmail.com'
GMAIL_PASS = os.getenv('GMAIL_PASS')

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
    # LINK ATUALIZADO: Este é o endereço que o site oficial usa agora
    url = "https://www.tesourodireto.com.br/json/br/com/b3/tesourodireto/service/api/treasurybondsinfo.json"
    
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/121.0.0.0 Safari/537.36',
        'Accept': 'application/json, text/plain, */*',
        'Referer': 'https://www.tesourodireto.com.br/titulos/precos-e-taxas.asp',
        'Host': 'www.tesourodireto.com.br'
    }
    
    try:
        response = requests.get(url, headers=headers, timeout=30)
        
        if response.status_code != 200:
            print(f"⚠️ O site retornou erro {response.status_code}")
            return None
            
        dados = response.json()
        
        # Acessando os dados na estrutura correta do JSON da B3
        if 'response' in dados and 'TrsuryBondIndxList' in dados['response']:
            lista = dados['response']['TrsuryBondIndxList']
            return {t['TrsuryBond']['nm']: t['TrsuryBond']['anulInvstmtRate'] for t in lista}
        else:
            print("❌ Estrutura do JSON mudou.")
            return None
            
    except Exception as e:
        print(f"❌ Erro na extração: {e}")
        return None

def executar():
    print("🔍 Iniciando busca de taxas na B3...")
    taxas = buscar_taxas_api()
    
    if not taxas:
        print("❌ Operação abortada. Site do Tesouro indisponível no momento.")
        return

    alertas_encontrados = []
    for t in minha_carteira:
        taxa_mercado = taxas.get(t['filtro'])
        if taxa_mercado is not None and taxa_mercado <= t['alerta'] and t['alerta'] > 0:
            alertas_encontrados.append(f"📌 {t['nome']}: Mercado {taxa_mercado}% <= Alerta {t['alerta']}%")

    if alertas_encontrados:
        corpo_email = "OPORTUNIDADES:\n\n" + "\n".join(alertas_encontrados)
        msg = MIMEText(corpo_email)
        msg['Subject'] = "⚠️ ALERTA TESOURO"
        msg['From'], msg['To'] = GMAIL_USER, GMAIL_USER
        try:
            with smtplib.SMTP_SSL('smtp.gmail.com', 465) as s:
                s.login(GMAIL_USER, GMAIL_PASS)
                s.send_message(msg)
            print("✅ Alerta enviado!")
        except:
            print("❌ Erro no envio do e-mail.")
    else:
        print(f"😴 Monitoradas {len(minha_carteira)} taxas. Sem oportunidades.")

if __name__ == "__main__":
    executar()
