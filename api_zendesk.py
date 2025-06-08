### Bibliotecas utilizadas
"""

import requests
import pandas as pd
from requests.auth import HTTPBasicAuth

"""### Credencias da API do zendesk"""

ZENDESK_SUBDOMAIN = "Seu Domínio Zendesk"
ZENDESK_EMAIL = "teste@zendek.com"
ZENDESK_API_TOKEN = "Seu token de API"
BASE_URL = f"https://{ZENDESK_SUBDOMAIN}.zendesk.com/api/v2"

"""### Função que extrais os dados de Tickets (.CSV)"""

def listar_tickets():
    url = f"{BASE_URL}/tickets.json"
    auth = HTTPBasicAuth(f"{ZENDESK_EMAIL}/token", ZENDESK_API_TOKEN)

    tickets_data = []

    while url:
        response = requests.get(url, auth=auth)

        if response.status_code == 200:
            data = response.json()
            tickets = data.get("tickets", [])

            for ticket in tickets:
                tickets_data.append({
                    "ID do Ticket": ticket.get("id"),
                    "Assunto": ticket.get("subject"),
                    "Descrição": ticket.get("description"),
                    "Status": ticket.get("status"),
                    "Prioridade": ticket.get("priority"),
                    "Criado em": ticket.get("created_at"),
                    "Atualizado em": ticket.get("updated_at"),
                    "Solicitante ID": ticket.get("requester_id"),
                    "Responsável ID": ticket.get("assignee_id")
                })

            url = data.get("next_page")  # Paginação automática
        else:
            print(f"Erro ao consultar tickets: {response.status_code}")
            print(response.text)
            break

    df = pd.DataFrame(tickets_data)
    df.to_csv("tickets_zendesk.csv", index=False)
    print("Arquivo CSV 'tickets_zendesk.csv' criado com sucesso!")

"""###Realizando a transformação e padronização dos dados"""

df = pd.read_csv('/content/tickets_zendesk.csv')

df.head()

df['Criado em'] = pd.to_datetime(df['Criado em'])
df['Atualizado em'] = pd.to_datetime(df['Atualizado em'])

df.head()

"""###Salvando os dados tratados"""

df.to_csv('tickets_zendesk_new.csv')