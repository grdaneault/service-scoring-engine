from configuration.persistence import Base
import teams
import checks
import checks.services


def create_tables(engine):
    Base.metadata.create_all(engine)
