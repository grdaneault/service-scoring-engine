import datetime
from sqlalchemy import Column, Integer, ForeignKey, String, Boolean, Text, Table, DateTime
from sqlalchemy.orm import relationship

from configuration.persistence import Base

__author__ = 'gregd'


class ServiceCheck(Base):
    __tablename__ = 'service_check'

    id = Column(Integer, primary_key=True)
    service_id = Column(Integer, ForeignKey('service.id'), nullable=False)

    check_type = Column('type', String(50), nullable=False)
    value = Column(Integer, nullable=False, default=5)

    is_enabled = Column(Boolean, nullable=False, default=True)

    results = relationship('CheckResult', backref='check', lazy='noload')
    __mapper_args__ = {'polymorphic_on': check_type}

    def __init__(self, **kwargs):
        credentials = kwargs.pop('credentials', [])
        if credentials is None:
            credentials = []

        Base.__init__(self, **kwargs)

        for credential in credentials:
            self.credentials.append(credential)

    def friendly_name(self):
        return str(self)


class CheckResult(Base):
    __tablename__ = 'check_result'

    id = Column(Integer, primary_key=True)
    check_id = Column(Integer, ForeignKey('service_check.id'), nullable=False)
    service_check_round_id = Column(Integer, ForeignKey('service_check_round.id'), nullable=False)

    success = Column(Boolean, nullable=False, default=False)
    message = Column(Text, nullable=False, default='')

    def __init__(self, success=True, message=''):
        self.success = success
        self.message = message

    def __eq__(self, other):
        return isinstance(other, CheckResult) \
               and self.success == other.success \
               and self.message == other.message

    def __str__(self):
        return 'Check<%s, %s>' % (self.success, self.message)

credentials_check_relation = Table('check_credential_association', Base.metadata,
                                   Column('check_id', Integer, ForeignKey('service_check.id')),
                                   Column('credential_id', Integer, ForeignKey('check_credentials.id'))
                                   )

class CheckCredentials(Base):
    __tablename__ = 'check_credentials'

    id = Column(Integer, primary_key=True)
    team_id = Column(Integer, ForeignKey('team.id'))
    user = Column(String(255), nullable=False)
    password = Column(String(255), nullable=False)
    last_changed = Column(DateTime, nullable=True)
    old_password = Column(String(255), nullable=True)

    checks = relationship('ServiceCheck', secondary=credentials_check_relation, backref='credentials')

    def __init__(self, user, password):
        self.user = user
        self.password = password
        self.last_changed = datetime.datetime.now()
        self.old_password = ''

    def change_password(self, new_password):
        self.old_password = self.password
        self.password = new_password
        self.last_changed = datetime.datetime.now()
