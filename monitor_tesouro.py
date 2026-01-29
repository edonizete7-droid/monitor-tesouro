import os
import requests
import smtplib
from email.mime.text import MIMEText

# --- CONFIGURAÇÕES ---
GMAIL_USER = 'edonizete7@gmail.com'
GMAIL_PASS = os.getenv('GMAIL_PASS')

# Lista completa com seus 14 títulos (organizados por filtros oficiais da B3)
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
    url = "https://www.tesourodireto.com.br/json/br/com/b3/tesourodireto/service/api/treasurybondsinfo.json"
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/115.0.0.0 Safari/537.36'
    }
    try:
        response = requests.get(url, headers=headers, timeout=20)
        dados = response.json()
        lista = dados['response']['TrsuryBondIndxList']
        return {t['TrsuryBond']['nm']: t['TrsuryBond']['anulInvstmtRate'] for t in lista}
    except Exception as e:
        print(f"⚠️ Erro de conexão (Mercado pode estar fechado): {e}")
        return None

def executar():
    # Agora o nome da função (buscar_taxas_api) combina perfeitamente
    taxas = buscar_taxas_api() 
    
    if not taxas:
        print("❌ Não foi possível ler as taxas. O site do Tesouro pode estar em manutenção.")
        return

    alertas_encontrados = []
    for t in minha_carteira:
        taxa_mercado = taxas.get(t['filtro'])
        if taxa_mercado and taxa_mercado <= t['alerta'] and t['alerta'] > 0:
            alertas_encontrados.append(f"📌 {t['nome']}: Mercado {taxa_mercado}% <= Alerta {t['alerta']}%")

    if alertas_encontrados:
        corpo_email = "\n".join(alertas_encontrados)
        msg = MIMEText(corpo_email)
        msg['Subject'] = "⚠️ OPORTUNIDADE: Alerta de Taxas Tesouro"
        msg['From'], msg['To'] = GMAIL_USER, GMAIL_USER
        try:
            with smtplib.SMTP_SSL('smtp.gmail.com', 465) as s:
                s.login(GMAIL_USER, GMAIL_PASS)
                s.send_message(msg)
            print("✅ E-mail de alerta enviado com sucesso!")
        except Exception as e:
            print(f"❌ Erro ao enviar e-mail: {e}")
    else:
        print(f"😴 Monitoradas {len(minha_carteira)} taxas. Nenhuma oportunidade no momento.")

if __name__ == "__main__":
    executar()
