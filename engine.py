import time

from sqlalchemy.orm import sessionmaker, joinedload

from sqlalchemy.orm import with_polymorphic

from checks.check_executor import CheckExecutor
from checks.service_checks import CheckRound, Service
from checks.services.check_dns import DnsService
from checks.services.check_mysql import MysqlService
from checks.services.check_ssh import SshService
from checks.services.check_web import WebService
from configuration.persistence import engine
from teams.team import Team


class Engine:

    def __init__(self, db_engine):
        self.Session = sessionmaker(bind=db_engine)

        self.session = self.Session(autoflush=False)
        self.teams = []

        self.load_teams()

        self.rounds = 1
        self.session.commit()

    def load_teams(self):
        service_poly = with_polymorphic(Service, [DnsService, MysqlService, SshService, WebService], aliased=True)
        self.teams = self.session.query(Team). \
            options(
            joinedload(Team.services.of_type(service_poly))
        ).all()

    def check_round(self):

        check_round = CheckRound()
        self.session.add(check_round)
        self.session.commit()

        check_threads = []

        for team in self.teams:
            for service in team.services:

                service_credentials = service.credentials
                credential_index = 0
                if service.credentials:
                    credential_index = self.rounds % len(service_credentials)

                for check in service.checks:
                    credentials = None
                    if service.requires_credentials(check) and service_credentials:
                        credentials = service_credentials[credential_index]
                        credential_index += 1
                        credential_index %= len(service_credentials)

                    check_thread = CheckExecutor(service, check, credentials)
                    check_thread.start()
                    check_threads.append(check_thread)

        for thread in check_threads:
            thread.join()
            check_round.checks.append(thread.result)

        check_round.end()

        print('All checks in round %d finished' % self.rounds)
        self.session.commit()
        self.rounds += 1
        print('Session committed')

    def start(self):
        while True:
            self.load_teams()
            self.check_round()
            time.sleep(30)

scoring_engine = Engine(engine)
scoring_engine.start()