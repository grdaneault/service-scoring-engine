import mysql.connector
from mysql.connector import connect, errorcode
from sqlalchemy import Column, Integer, String, ForeignKey
from sqlalchemy.orm import relationship
from checks import CheckResult, ServiceCheck
from checks.services import Service


class MysqlService(Service):

    def friendly_name(self):
        return 'MySQL Server'

    __mapper_args__ = {'polymorphic_identity': 'mysql'}
    checks = relationship('MysqlCheck', backref='service')

    def __init__(self, host, port=3306):
        Service.__init__(self, host, port)

    def requires_credentials(self, check):
        return True

    def run_check(self, check, credentials=None):
        """
        Runs a check against the mysql service

        :type check: MysqlCheck
        :param check:  Parameters for the check
        :param credentials:  Credentials for the check
        :return: CheckResult
        """
        try:
            if not credentials or not credentials.user or not credentials.password:
                return self.missing_credentials()
            connection = connect(user=credentials.user,
                                 password=credentials.password,
                                 host=self.host,
                                 database=check.database,
                                 connection_timeout=Service.TIMEOUT)

            cursor = connection.cursor()

            query = ('select COUNT(*) from %s' % check.table)

            cursor.execute(query)
            (num_rows,) = cursor.fetchone()

            connection.close()
            if num_rows > 0:
                return CheckResult(True, 'Table %s has data' % check.table)
            else:
                return CheckResult(False, 'Table %s is empty' % check.table)

        except mysql.connector.Error as err:
            if err.errno == errorcode.ER_ACCESS_DENIED_ERROR:
                return self.invalid_credentials(credentials)
            elif err.errno == errorcode.ER_BAD_DB_ERROR:
                return CheckResult(False, 'Database %s does not exist' % check.database)
            elif err.errno == errorcode.CR_CONN_HOST_ERROR:
                return self.connection_error()
            else:
                return CheckResult(False, 'Mysql error: %s' % err.msg)


class MysqlCheck(ServiceCheck):
    __tablename__ = 'check_detail_mysql'
    __mapper_args__ = {'polymorphic_identity': 'mysql'}

    mysql_check_id = Column('id', Integer, ForeignKey('service_check.id'), primary_key=True)

    database = Column(String(255), nullable=False)
    table = Column(String(255), nullable=False)

    def __init__(self, database, table, value=10):
        ServiceCheck.__init__(self, value=value)
        self.database = database
        self.table = table

    def __str__(self):
        return '<MysqlCheck of %s/%s.%s>' % (self.service.host, self.database, self.table)
