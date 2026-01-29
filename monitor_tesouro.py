import os
import requests
import smtplib
from email.mime.text import MIMEText

# --- CONFIGURAÇÕES DE SEGURANÇA ---
GMAIL_USER = 'edonizete7@gmail.com'
# O GitHub lerá a 'Secret' automaticamente. No PC, substitua pela sua senha de 16 dígitos se quiser testar.
GMAIL_PASS = os.getenv('GMAIL_PASS') or 'SUA_SENHA_DE_16_DIGITOS_AQUI'

# --- SUA CARTEIRA DE 10 TÍTULOS ---
minha_carteira = [
    {"nome": "IPCA+ 2029", "filtro": "Tesouro IPCA+ 2029", "alerta": 6.10},
    {"nome": "IPCA+ 2035 (Sem)", "filtro": "Tesouro IPCA+ com Juros Semestrais 2035", "alerta": 6.50},
    {"nome": "IPCA+ 2035 (Ap2)", "filtro": "Tesouro IPCA+ com Juros Semestrais 2035", "alerta": 6.50},
    {"nome": "Vazio 04", "filtro": "", "alerta": 0.0},
    {"nome": "Vazio 05", "filtro": "", "alerta": 0.0},
    {"nome": "Vazio 06", "filtro": "", "alerta": 0.0},
    {"nome": "Vazio 07", "filtro": "", "alerta": 0.0},
    {"nome": "Vazio 08", "filtro": "", "alerta": 0.0},
    {"nome": "Vazio 09", "filtro": "", "alerta": 0.0},
    {"nome": "Vazio 10", "filtro": "", "alerta": 0.0},
]

def buscar_taxas_api():
    url = "https://www.tesourodireto.com.br/json/br/com/b3/tesourodireto/service/api/treasurybondsinfo.json"
    try:
        response = requests.get(url, timeout=15)
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
    print("🔎 Verificando taxas no site do Tesouro...")
    taxas_hoje = buscar_taxas_api()
    if not taxas_hoje:
        return

    alertas = []
    for titulo in minha_carteira:
        if titulo['filtro'] in taxas_hoje:
            taxa_atual = taxas_hoje[titulo['filtro']]
            # Lógica: Se a taxa do site for menor ou igual ao seu alerta
            if taxa_atual <= titulo['alerta'] and titulo['alerta'] > 0:
                alertas.append(f"📌 {titulo['nome']}: Mercado {taxa_atual}% <= Alerta {titulo['alerta']}%")

    if alertas:
        enviar_email("⚠️ OPORTUNIDADE TESOURO DIRETO", "\n".join(alertas))
    else:
        print("😴 Nenhuma oportunidade detectada no momento.")

if __name__ == "__main__":
    executar_monitoramento()