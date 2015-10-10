from sqlalchemy import Column, Integer, Boolean, String, DateTime, Text, ForeignKey, Table
from sqlalchemy.orm import relationship

from configuration.persistence import Base


class Inject(Base):
    __tablename__ = 'inject'

    id = Column(Integer, primary_key=True)
    title = Column(String(255), nullable=False)
    body = Column(Text, nullable=False)
    value = Column(Integer, nullable=False)
    enabled = Column(Boolean, nullable=False, default=True)
    max_solves = Column(Integer, nullable=True, default=1)

    solves = relationship('InjectSolve', backref='inject')


team_inject_relation = Table('inject_team_availability', Base.metadata,
                             Column('team_id', Integer, ForeignKey('team.id')),
                             Column('inject_id', Integer, ForeignKey('inject.id'))
                             )


class InjectSolve(Base):
    __tablename__ = 'inject_solve'

    id = Column(Integer, primary_key=True)
    team_id = Column(Integer, ForeignKey('team.id'), nullable=False)
    inject_id = Column(Integer, ForeignKey('inject.id'), nullable=False)
    approved = Column(Boolean, nullable=False, default=False)
    approver_id = Column(Integer, ForeignKey('user.id'), nullable=True)
    approving_user = relationship("User")
    date_requested = Column(DateTime, nullable=False)
    date_approved = Column(DateTime, nullable=True)
    value_approved = Column(Integer, nullable=False)
