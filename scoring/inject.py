from sqlalchemy import Column, Integer, Boolean, String, DateTime, Text, ForeignKey
from sqlalchemy.orm import relationship

from configuration.persistence import Base


class Inject(Base):
    __tablename__ = 'inject'

    id = Column(Integer, primary_key=True)
    title = Column(String(255))
    body = Column(Text)
    start = Column(DateTime)
    end = Column(DateTime)
    value = Column(Integer)

class InjectSolve(Base):
    id = Column(Integer, primary_key=True)
    team = relationship('Team')
    inject = relationship('Inject')
    approved = Column(Boolean)
    approving_user = relationship("User")
    date_requested = Column(DateTime)
    date_approved = Column(DateTime)
