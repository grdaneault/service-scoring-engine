import unittest
from sqlalchemy.engine import create_engine
from sqlalchemy.orm.session import Session

# Import all persistence classes so that the proper tables get built for testing
from configuration.models import create_tables

def setup_module():
    global transaction, connection, engine

    # Connect to the database and create the schema within a transaction
    engine = create_engine('mysql+mysqlconnector://greg:greg@192.168.243.100/scoring_engine_test')
    connection = engine.connect()
    transaction = connection.begin()
    create_tables(connection)


def teardown_module():
    # Roll back the top level transaction and disconnect from the database
    transaction.rollback()
    connection.close()
    engine.dispose()


class ServiceTest(unittest.TestCase):
    def setup(self):
        self.__transaction = connection.begin_nested()
        self.session = Session(connection)

    def teardown(self):
        self.session.close()
        self.__transaction.rollback()
