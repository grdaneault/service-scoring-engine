from sqlalchemy import Column, Integer, Boolean, String, DateTime, Text, ForeignKey, Table
from sqlalchemy.orm import relationship

from configuration.persistence import Base


class Inject(Base):

    UNLIMITED_SOLVES = -1

    __tablename__ = 'inject'

    id = Column(Integer, primary_key=True)
    title = Column(String(255), nullable=False)
    body = Column(Text, nullable=False)
    value = Column(Integer, nullable=False)
    opened = Column(Boolean, nullable=True, default=None)
    closed = Column(Boolean, nullable=True, default=None)
    max_solves = Column(Integer, nullable=True, default=1)

    solves = relationship('InjectSolve', backref='inject')

    def is_open(self):
        return self.closed is None

    def is_visible(self):
        return self.opened is not None

    def is_unlimited(self):
        return self.max_solves == self.UNLIMITED_SOLVES


team_inject_relation = Table('inject_team_availability', Base.metadata,
                             Column('team_id', Integer, ForeignKey('team.id')),
                             Column('inject_id', Integer, ForeignKey('inject.id'))
                             )


class InjectSolve(Base):
    __tablename__ = 'inject_solve'

    id = Column(Integer, primary_key=True)
    team_id = Column(Integer, ForeignKey('team.id'), nullable=False)
    inject_id = Column(Integer, ForeignKey('inject.id'), nullable=False)
    approved = Column(Boolean, nullable=True, default=None)
    approver_id = Column(Integer, ForeignKey('user.id'), nullable=True)
    approving_user = relationship("User")
    date_requested = Column(DateTime, nullable=False)
    date_approved = Column(DateTime, nullable=True)
    value_approved = Column(Integer, nullable=True)
