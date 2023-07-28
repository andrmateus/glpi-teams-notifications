from sqlalchemy import create_engine
import pandas as pd
import os
from dotenv import load_dotenv
from urllib.parse import quote

def consulta_banco(query):
    load_dotenv()

    user = os.getenv('GLPI_DB_USER')
    password = quote(os.getenv('GLPI_DB_PASSWORD'))
    host = os.getenv('GLPI_DB_SERVER')
    database = os.getenv('GLPI_DB_NAME')

    engine = create_engine(f'mysql+mysqlconnector://{user}:{password}@{host}/{database}')

    consulta = pd.read_sql(query, engine)

    return consulta

def request_tickets():
    with open('sql\\ticket.sql', 'r') as file:
        query = file.read()
    tickets = consulta_banco(query)
    return tickets

def aprovacao_excedido():
    with open('sql\\chamados prazo para aprovacao excedido.sql', 'r') as file:
        query = file.read()
    tickets = consulta_banco(query)
    return tickets

def get_phones():
    with open('sql\\phones.sql', 'r') as file:
        query = file.read()
    phones = consulta_banco(query)
    return phones

def get_expired_tickets():
    with open('sql\\expired_tickets.sql', 'r') as file:
        query = file.read()
    tickets = consulta_banco(query)
    return tickets
    
def get_expiring_tickets():
    with open('sql\\tickets_less_two_hour.sql', 'r') as file:
        query = file.read()
    tickets = consulta_banco(query)
    return tickets