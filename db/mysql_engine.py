from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
import os
from dotenv import load_dotenv
from urllib.parse import quote

load_dotenv()

GLPI_DB_SERVER = (os.getenv('GLPI_DB_SERVER'))
GLPI_DB_USER = (os.getenv('GLPI_DB_USER'))
GLPI_DB_PASSWORD = quote(os.getenv('GLPI_DB_PASSWORD'))
GLPI_DB_NAME = (os.getenv('GLPI_DB_NAME'))

engine = create_engine(f'mysql+mysqlconnector://{GLPI_DB_USER}:{GLPI_DB_PASSWORD}@{GLPI_DB_SERVER}/{GLPI_DB_NAME}')

Session = sessionmaker(bind=engine)