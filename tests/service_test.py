import unittest
from sqlalchemy.engine import create_engine
from sqlalchemy.orm.session import Session

# Import all persistence classes so that the proper tables get built for testing
# noinspection PyUnresolvedReferences
from checks.services import CheckCredentials
# noinspection PyUnresolvedReferences
from checks.services.check_dns import DnsService, DnsCheck
# noinspection PyUnresolvedReferences
from checks.services.check_ftp import FtpService, FtpCheck
# noinspection PyUnresolvedReferences
from checks.services.check_ping import PingService, PingCheck
# noinspection PyUnresolvedReferences
from checks.services.check_mysql import MysqlService, MysqlCheck
# noinspection PyUnresolvedReferences
from checks.services.check_ssh import SshService, SshCheck
# noinspection PyUnresolvedReferences
from checks.services.check_web import WebService, WebCheck
# noinspection PyUnresolvedReferences
from teams.team import Team

from configuration.persistence import Base, engine


def setup_module():
    global transaction, connection, engine

    # Connect to the database and create the schema within a transaction
    engine = create_engine('mysql+mysqlconnector://greg:greg@192.168.243.100/scoring_engine_test')
    connection = engine.connect()
    transaction = connection.begin()
    Base.metadata.create_all(connection)


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
