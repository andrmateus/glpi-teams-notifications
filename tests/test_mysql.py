import unittest
import os
from dotenv import load_dotenv
from unittest.mock import patch, MagicMock
from db.mysql_engine import engine, Session
from sqlalchemy.orm import Session as SqlAlchemySession

class TestMysql(unittest.TestCase):
    def setUp(self):
        load_dotenv()

    def test_engine(self):
        # Assert that the engine object is not None
        self.assertIsNotNone(engine)
        

    def test_enviroment_variables(self):
        # Assert that the enviroment variables are not None
        self.assertIsNotNone(os.getenv('GLPI_DB_SERVER'))
        self.assertIsNotNone(os.getenv('GLPI_DB_USER'))
        self.assertIsNotNone(os.getenv('GLPI_DB_PASSWORD'))
        self.assertIsNotNone(os.getenv('GLPI_DB_NAME'))

    def test_session(self):
        # Assert that the session object is not None
        self.assertIsNotNone(Session())