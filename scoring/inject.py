import datetime
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
    date_opened = Column(DateTime, nullable=True, default=None)
    date_closed = Column(DateTime, nullable=True, default=None)
    max_solves = Column(Integer, nullable=True, default=1)

    solves = relationship('InjectSolve', backref='inject')

    def can_submit(self):
        return self.is_visible() and (self.date_closed is None or self.date_closed > datetime.datetime.now())

    def open(self):
        self.date_opened = datetime.datetime.now()
        self.date_closed = None

    def close(self):
        self.date_closed = datetime.datetime.now()

    def is_visible(self):
        return self.date_opened is not None and self.date_opened < datetime.datetime.now()

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
    reviewing_user_id = Column(Integer, ForeignKey('user.id'), nullable=True)
    reviewing_user = relationship("User")
    date_requested = Column(DateTime, nullable=False)
    date_reviewed = Column(DateTime, nullable=True)
    value_approved = Column(Integer, nullable=True)

    def is_reviewed(self):
        return self.date_reviewed is not None

    def reject(self, reviewer):
        self.approved = False
        self.value_approved = 0
        self.date_reviewed = datetime.datetime.now()
        self.reviewing_user = reviewer

    def approve(self, reviewer, value):
        self.approved = True
        self.value_approved = value
        self.date_reviewed = datetime.datetime.now()
        self.reviewing_user = reviewer
