import logging

import requests
import json
import os
from dotenv import load_dotenv

load_dotenv()

webhook_url = os.getenv('WEBHOOK_URL')
glpi_ticket_url = f'{os.getenv("GLPI_URL_HOST")}/front/ticket.form.php?id='


def send_notifications_by_webhook(ticket, office, time_to_resolve, it_support, expired=False):
    title = 'CHAMADO ESTOURADO' if expired else 'CHAMADO EXPIRANDO'
    title_color = 'Attention' if expired else 'Default'

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
                            "type": "Container",
                            "style": f"{title_color}",
                            "items": [
                                {
                                    "type": "TextBlock",
                                    "text": f"{title}",
                                    "wrap": True,
                                    "size": "Large",
                                    "weight": "Bolder",
                                    "fontType": "Monospace",
                                    "color": f"{title_color}",
                                    "spacing": "None",
                                    "maxLines": 1
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
                                                    "text": f"**{ticket}**",
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
                                                    "text": f"**{office}**",
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
                                                    "text": "Data Expiracao:",
                                                    "wrap": True
                                                },
                                                {
                                                    "type": "TextBlock",
                                                    "text": f"**{time_to_resolve}**",
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
                                                    "text": "Tecnico Atribuido:",
                                                    "wrap": True
                                                },
                                                {
                                                    "type": "TextBlock",
                                                    "text": f"**{it_support}**",
                                                    "wrap": True
                                                }
                                            ]
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
                                    "url": f"{glpi_ticket_url}{ticket}"
                                }
                            ],
                            "horizontalAlignment": "Center"
                        }
                    ],
                    "verticalContentAlignment": "Center",
                    "minHeight": "7px",
                }
            }
        ]
    }
    # Converte a carga útil para uma string JSON
    payload_json = json.dumps(payload)

    logging.info('Sending webhook')
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
    logging.info('Webhook sent')
    return
