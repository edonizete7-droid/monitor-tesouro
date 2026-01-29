import os
import requests
import smtplib
from email.mime.text import MIMEText

# --- CONFIGURAÇÕES DE SEGURANÇA ---
GMAIL_USER = 'edonizete7@gmail.com'
GMAIL_PASS = os.getenv('GMAIL_PASS') or 'SUA_SENHA_DE_16_DIGITOS_AQUI'

# --- SUA CARTEIRA DE 14 TÍTULOS ATUALIZADA ---
# Dica: O 'alerta' deve ser MENOR que a taxa que você comprou para indicar lucro na venda.
minha_carteira = [
    {"nome": "IPCA+ 2026", "filtro": "Tesouro IPCA+ 2026", "alerta": 4.50},
    {"nome": "IPCA+ 2029", "filtro": "Tesouro IPCA+ 2029", "alerta": 6.00},
    {"nome": "IPCA+ 2035 (Semestral 1)", "filtro": "Tesouro IPCA+ com Juros Semestrais 2035", "alerta": 6.30},
    {"nome": "IPCA+ 2035 (Semestral 2)", "filtro": "Tesouro IPCA+ com Juros Semestrais 2035", "alerta": 6.00},
    {"nome": "IPCA+ 2035 (Semestral 3)", "filtro": "Tesouro IPCA+ com Juros Semestrais 2035", "alerta": 7.20},
    {"nome": "IPCA+ 2040 (Semestral 1)", "filtro": "Tesouro IPCA+ com Juros Semestrais 2040", "alerta": 6.00},
    {"nome": "IPCA+ 2040 (Semestral 2)", "filtro": "Tesouro IPCA+ com Juros Semestrais 2040", "alerta": 6.30},
    {"nome": "IPCA+ 2040 (Semestral 3)", "filtro": "Tesouro IPCA+ com Juros Semestrais 2040", "alerta": 7.30},
    {"nome": "IPCA+ 2055 (Semestral 1)", "filtro": "Tesouro IPCA+ com Juros Semestrais 2055", "alerta": 6.10},
    {"nome": "IPCA+ 2055 (Semestral 2)", "filtro": "Tesouro IPCA+ com Juros Semestrais 2055", "alerta": 7.20},
    {"nome": "PREFIXADO 2031", "filtro": "Tesouro Prefixado com Juros Semestrais 2031", "alerta": 12.10},
    {"nome": "SELIC 2029", "filtro": "Tesouro Selic 2029", "alerta": 0.10},
    {"nome": "SELIC 2031", "filtro": "Tesouro Selic 2031", "alerta": 0.15}
]

def buscar_taxas_api()
    url = "https://www.tesourodireto.com.br/json/br/com/b3/tesourodireto/service/api/treasurybondsinfo.json"
    # Adicionamos este 'headers' para evitar o erro que apareceu no seu log
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/115.0.0.0 Safari/537.36'
    }
    try:
        response = requests.get(url, headers=headers, timeout=15)
        dados = response.json()
        lista = dados['response']['TrsuryBondIndxList']
        return {t['TrsuryBond']['nm']: t['TrsuryBond']['anulInvstmtRate'] for t in lista}
    except Exception as e:
        print(f"Erro ao acessar API: {e}")
        return None
def enviar_email(assunto, mensagem):
    msg = MIMEText(mensagem)
    msg['Subject'] = assunto
    msg['From'] = GMAIL_USER
    msg['To'] = GMAIL_USER
    try:
        with smtplib.SMTP_SSL('smtp.gmail.com', 465) as server:
            server.login(GMAIL_USER, GMAIL_PASS)
            server.send_message(msg)
            print("✅ E-mail enviado com sucesso!")
    except Exception as e:
        print(f"❌ Erro no envio: {e}")

def executar_monitoramento():
    print("🔎 Verificando 14 títulos no Tesouro...")
    taxas_hoje = buscar_taxas_api()
    if not taxas_hoje:
        return

    alertas = []
    for titulo in minha_carteira:
        if titulo['filtro'] in taxas_hoje:
            taxa_atual = taxas_hoje[titulo['filtro']]
            if taxa_atual <= titulo['alerta'] and titulo['alerta'] > 0:
                alertas.append(f"📌 {titulo['nome']}: Mercado {taxa_atual}% <= Alerta {titulo['alerta']}%")

    if alertas:
        enviar_email("⚠️ OPORTUNIDADE TESOURO DIRETO", "\n".join(alertas))
    else:
        print("😴 Nenhuma das 14 taxas atingiu o limite de alerta.")

if __name__ == "__main__":
    executar_monitoramento()

