import os
import requests
import pandas as pd
import smtplib
from email.mime.text import MIMEText

# --- CONFIGURAÇÕES ---
GMAIL_USER = 'edonizete7@gmail.com'
GMAIL_PASS = os.getenv('GMAIL_PASS')

minha_carteira = [
    {"nome": "IPCA+ 2026", "filtro": "Tesouro IPCA+ 2026", "alerta": 4.50},
    {"nome": "IPCA+ 2029", "filtro": "Tesouro IPCA+ 2029", "alerta": 6.00},
    {"nome": "IPCA+ 2035 (Semestral)", "filtro": "Tesouro IPCA+ com Juros Semestrais 2035", "alerta": 6.30},
    {"nome": "IPCA+ 2040 (Semestral)", "filtro": "Tesouro IPCA+ com Juros Semestrais 2040", "alerta": 6.00},
    {"nome": "IPCA+ 2055 (Semestral)", "filtro": "Tesouro IPCA+ com Juros Semestrais 2055", "alerta": 6.10},
    {"nome": "PREFIXADO 2031", "filtro": "Tesouro Prefixado com Juros Semestrais 2031", "alerta": 12.10},
    {"nome": "SELIC 2029", "filtro": "Tesouro Selic 2029", "alerta": 0.10},
    {"nome": "SELIC 2031", "filtro": "Tesouro Selic 2031", "alerta": 0.15}
]

def buscar_taxas():
    # Novo link via planilha Excel (mais difícil de bloquear)
    url = "https://www.tesourodireto.com.br/json/br/com/b3/tesourodireto/service/api/treasurybondsinfo.json"
    headers = {'User-Agent': 'Mozilla/5.0'}
    try:
        response = requests.get(url, headers=headers, timeout=20)
        dados = response.json()
        lista = dados['response']['TrsuryBondIndxList']
        return {t['TrsuryBond']['nm']: t['TrsuryBond']['anulInvstmtRate'] for t in lista}
    except:
        # Se falhar o JSON, tentamos uma alternativa simples
        print("⚠️ Tentando conexão alternativa...")
        return None

def executar():
    taxas = buscar_taxas()
    if not taxas:
        print("❌ O site do Tesouro bloqueou a conexão. Tentaremos novamente amanhã automaticamente.")
        return

    alertas = []
    for t in minha_carteira:
        atual = taxas.get(t['filtro'])
        if atual and atual <= t['alerta'] and t['alerta'] > 0:
            alertas.append(f"📌 {t['nome']}: {atual}% (Alerta: {t['alerta']}%)")

    if alertas:
        msg = MIMEText("\n".join(alertas))
        msg['Subject'] = "⚠️ ALERTA TESOURO"
        msg['From'], msg['To'] = GMAIL_USER, GMAIL_USER
        with smtplib.SMTP_SSL('smtp.gmail.com', 465) as s:
            s.login(GMAIL_USER, GMAIL_PASS)
            s.send_message(msg)
        print("✅ Alerta enviado!")
    else:
        print("😴 Sem oportunidades no momento.")

if __name__ == "__main__":
    executar()
