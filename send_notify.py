import requests
import json
import pandas as pd
import time
import os
from dotenv import load_dotenv
from db_glpi import get_expired_tickets

load_dotenv()

# Defina o URL do webhook que você obteve do seu serviço (por exemplo, Microsoft Teams ou Slack)
webhook_url = os.getenv('WEBHOOK_URL')

glpi_ticket_url = os.getenv('GLPI_TICKET_URL')

# Define o caminho do arquivo de log para notificações de SLA expirado
sla_expired_log_file_path = 'sla_expired_notifications.log'

# Verifique se o arquivo de log existe e crie-o se não existir
if not os.path.exists(sla_expired_log_file_path):
    with open(sla_expired_log_file_path, 'w') as f:
        f.write('id,fila_atendimento,data_notificacao\n')

# Define a função para enviar notificações de SLA expirado
def send_sla_expired_notifications():
    # Leia as notificações existentes do arquivo de log
    notified_tickets = set()
    with open(sla_expired_log_file_path, 'r') as f:
        next(f)  # Pula a primeira linha (cabeçalho)
        for line in f:
            ticket_id, fila_atendimento, data_notificacao = line.strip().split(',')
            notified_tickets.add(int(ticket_id))

    # Obtenha a lista de chamados com SLA expirado
    expired_tickets = get_expired_tickets()

    # Filtra os chamados que já foram notificados
    new_tickets = expired_tickets[~expired_tickets['id'].isin(notified_tickets)]

    # Envia uma notificação para cada novo chamado e salva no arquivo de log
    with open(sla_expired_log_file_path, 'a') as f:
        for _, ticket in new_tickets.iterrows():

            # Define a carga útil da mensagem para o seu webhook
            payload = {
                "type": "message",
                "attachments": [
                    {
                        "contentType": "application/vnd.microsoft.card.adaptive",
                        "content": {
                            "type": "AdaptiveCard",
                            "$schema": "http://adaptivecards.io/schemas/adaptive-card.json",
                            "version": "1.4",
                            "body": [
                                {
                                    "type": "TextBlock",
                                    "text": "CHAMADO ESTOURADO",
                                    "wrap": True,
                                    "size": "Large",
                                    "weight": "Bolder",
                                    "fontType": "Monospace"
                                },
                                {
                                    "type": "ColumnSet",
                                    "columns": [
                                        {
                                            "type": "Column",
                                            "width": "stretch",
                                            "items": [
                                                {
                                                    "type": "TextBlock",
                                                    "text": "Chamado:",
                                                    "wrap": True
                                                },
                                                {
                                                    "type": "TextBlock",
                                                    "text": f"**{ticket['id']}**",
                                                    "wrap": True
                                                }
                                            ]
                                        },
                                        {
                                            "type": "Column",
                                            "width": "stretch",
                                            "items": [
                                                {
                                                    "type": "TextBlock",
                                                    "text": "Fila de atendimento:",
                                                    "wrap": True
                                                },
                                                {
                                                    "type": "TextBlock",
                                                    "text": f"**{ticket['fila_atendimento']}**",
                                                    "wrap": True
                                                }
                                            ]
                                        }
                                    ]
                                },
                                {
                                    "type": "ActionSet",
                                    "actions": [
                                        {
                                            "type": "Action.OpenUrl",
                                            "title": "LINK CHAMADO GLPI",
                                            "url": f"{glpi_ticket_url}{ticket['id']}"
                                        }
                                    ],
                                    "horizontalAlignment": "Center"
                                }
                            ]
                        }
                    }
                ]
            }

            # Converte a carga útil para uma string JSON
            payload_json = json.dumps(payload)

            # Envia o webhook
            response = requests.post(
                webhook_url, 
                data=payload_json,
                headers={'Content-Type': 'application/json'}
            )

            # Verifica se o webhook foi enviado com sucesso
            if response.status_code != 200:
                raise ValueError(
                    'Request to webhook returned an error %s, the response is:\n%s'
                    % (response.status_code, response.text)
                )

            # Salva a notificação no arquivo de log
            f.write(f"{ticket['id']},{ticket['fila_atendimento']},{time.strftime('%Y-%m-%d %H:%M:%S')}\n")

# Define a função principal para chamar a tarefa de enviar notificações de SLA expirado
def main():
    send_sla_expired_notifications()

if __name__ == '__main__':
    main()