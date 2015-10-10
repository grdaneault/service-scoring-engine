from configuration.persistence import Base
import teams
import checks
import checks.services
import scoring


def create_tables(engine):
    Base.metadata.create_all(engine)
