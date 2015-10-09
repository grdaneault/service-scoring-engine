import random
import time

from sqlalchemy.orm import sessionmaker, joinedload

from sqlalchemy.orm import with_polymorphic
from checks import CheckRound, TeamCheckRound, ServiceCheckRound

from checks.check_executor import CheckExecutor
from checks.services import Service
from checks.services.check_dns import DnsService
from checks.services.check_mysql import MysqlService
from checks.services.check_ssh import SshService
from checks.services.check_web import WebService
from checks.services.check_ftp import FtpService
from checks.services.check_ping import PingService
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
        service_poly = with_polymorphic(Service, [DnsService, MysqlService, SshService, WebService, FtpService, PingService], aliased=True)
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
            team_round = TeamCheckRound(team=team, check_round=check_round)

            for service in team.services:
                service_round_threads = []
                service_round = ServiceCheckRound(team_round=team_round, service=service)
                check_threads.append((service_round, service_round_threads))

                for check in service.checks:
                    credentials = [None]
                    if service.requires_credentials(check) and check.credentials:
                        credentials = check.credentials

                    for credential in credentials:
                        check_thread = CheckExecutor(service, check, credential)
                        check_thread.start()
                        service_round_threads.append(check_thread)

        for service_round in check_threads:
            for thread in service_round[1]:
                thread.join()
                service_round[0].results.append(thread.result)

        check_round.finish()

        print('All checks in round %d finished' % self.rounds)
        self.session.commit()
        self.rounds += 1
        print('Session committed')

    def start(self):
        while True:
            self.load_teams()
            self.check_round()
            time.sleep(random.randint(30, 90))

scoring_engine = Engine(engine)
scoring_engine.start()
