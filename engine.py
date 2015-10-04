import threading
from sqlalchemy.orm import sessionmaker, subqueryload_all, joinedload
from checks.check_executor import CheckExecutor
from checks.service_checks import CheckRound, Service, ServiceCheck
from checks.services.check_dns import DnsService, DnsCheck
from checks.services.check_mysql import MysqlService, MysqlCheck
from checks.services.check_ssh import SshService, SshCheck
from checks.services.check_web import WebService, WebCheck
from configuration.persistence import engine
from teams.team import Team
from sqlalchemy.orm import with_polymorphic

class Engine:

    def __init__(self, db_engine):
        Session = sessionmaker(bind=db_engine)

        self.session = Session()

        service_poly = with_polymorphic(Service, [DnsService, MysqlService, SshService, WebService], aliased=True)
        check_poly = with_polymorphic(ServiceCheck, [DnsCheck, MysqlCheck, SshCheck, WebCheck], aliased=True)

        self.teams = self.session.query(Team). \
            options(
                joinedload(Team.services.of_type(service_poly))
            ).all()

    def check_round(self):
        check_round = CheckRound()
        self.session.add(check_round)
        self.session.flush()

        lock = threading.Lock()

        check_threads = []

        for team in self.teams:
            for service in team.services:
                if service.credentials:
                    service_credentials = service.credentials
                    credential_index = check_round.id % len(service_credentials)

                for check in service.checks:
                    credentials = None
                    if service.requires_credentials(check) and service_credentials:
                        credentials = service_credentials[credential_index]
                        credential_index += 1
                        credential_index %= len(service_credentials)

                    check_thread = CheckExecutor(lock, check_round, service, check, credentials)
                    check_thread.start()
                    check_threads.append(check_thread)

        for thread in check_threads:
            thread.join()

        print('All checks finished')
        self.session.flush()

scoring_engine = Engine(engine)
scoring_engine.check_round()
