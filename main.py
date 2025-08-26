import gspread, smtplib, os, logging
import pandas as pd
from datetime import datetime
from google.oauth2.service_account import Credentials
from email.message import EmailMessage
from dotenv import load_dotenv

load_dotenv()

logging.basicConfig(
    filename='/home/gammu/Netline/alerta_baterias/alerta_baterias.log',
    filemode='a',
    level=logging.INFO,
    format='[%(asctime)s] %(levelname)s - %(message)s',
    datefmt='%d/%m/%Y %H:%M:%S'
)

arquivo_credenciais = '/home/gammu/Netline/alerta_baterias/ordinal-verbena-470213-q6-0f8c3fe16d05.json'

escopos = [
  'https://spreadsheets.google.com/feeds',
  'https://www.googleapis.com/auth/drive',
]

credenciais = Credentials.from_service_account_file(filename=arquivo_credenciais, scopes=escopos)
cliente = gspread.authorize(credenciais)

chave = os.getenv('KEY_SHEETS')

# 6 é a posição da planilha
planilha = cliente.open_by_key(chave).get_worksheet(6)

def captura_dados_da_planilha(planilha):
  dados = planilha.get_all_records()
  df = pd.DataFrame(dados)

  return df

def formata_data_validade(df):
  df['Data Validade'] = pd.to_datetime(df['Data Validade'], dayfirst=True, errors='coerce')

  return df

def calcula_dias_restantes(df):
  data_atual = pd.to_datetime(datetime.now().date())

  if 'Data Validade' not in df.columns:
    raise Exception('A coluna "Data Validade" não foi encontrada na planilha.')

  df['Dias Restantes'] = (df['Data Validade'] - data_atual).dt.days

  return df

def envia_email(local, dias_restantes):
  mensagem = EmailMessage()
  mensagem['Subject'] = 'ALERTA | BATERIAS COM VALIDADE PRÓXMA'
  mensagem['From'] = os.getenv('SMTP_USERNAME')
  mensagem['To'] = os.getenv('RECEIVE_EMAIL')
  
  mensagem.set_content(f"""
  🚨 ATENÇÃO!

  As baterias do local: {local} estão prestes a vencer.

  ⏳ Faltam apenas {dias_restantes} dias para o vencimento.

  Por favor, providencie a substituição o quanto antes para evitar falhas no sistema.
  """)

  with smtplib.SMTP_SSL('smtp.gmail.com', 465) as smtp:
    smtp.login(os.getenv('SMTP_USERNAME'), os.getenv('SMTP_PASSWORD'))
    smtp.send_message(mensagem)

def verifica_se_envia_email(df):
  for _, row in df.iterrows():
    dias = row['Dias Restantes']

    if pd.isna(dias):
        continue

    dias = int(dias)
    local = row['Local instalado']

    if dias in [30, 15, 2, 0]:
      envia_email(local, dias)
      logging.info(f"🚀 Alerta enviado - local: {local} (faltam {dias} dias)")


if __name__ == '__main__':
  logging.info("Script iniciado")

  try:
    df = captura_dados_da_planilha(planilha)
    df = formata_data_validade(df)
    df = calcula_dias_restantes(df)
    verifica_se_envia_email(df)
  except Exception as e:
    logging.error(f"Erro ao executar o script: {e}")

  logging.info("Fim do script")