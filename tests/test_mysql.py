import unittest

from checks.services.check_mysql import MysqlService, MysqlCheck
from checks.service_checks import CheckCredentials
from tests.service_test import ServiceTest


class MysqlTestCase(ServiceTest):
    def test_mysql(self):
        service = MysqlService('192.168.243.131')
        cred = CheckCredentials('root', 'greg')

        result = service.try_check(MysqlCheck('secret', 'secret_keys'), cred)

        self.assertEqual(True, result.success)
        self.assertEqual('Table secret_keys has data', result.message)

    def test_mysql_bad_credentials(self):
        service = MysqlService('192.168.243.131')
        cred = CheckCredentials('root', 'bad_pass')

        result = service.try_check(MysqlCheck('secret', 'secret_keys'), cred)
        self.assertEqual(service.invalid_credentials(cred), result)

    def test_mysql_empty_table(self):
        service = MysqlService('192.168.243.131')
        cred = CheckCredentials('root', 'greg')

        result = service.try_check(MysqlCheck('secret', 'red_team_was_here'), cred)
        self.assertEqual(False, result.success)
        self.assertEqual('Table red_team_was_here is empty', result.message)

    def test_mysql_no_database(self):
        service = MysqlService('192.168.243.131')
        cred = CheckCredentials('root', 'greg')

        result = service.try_check(MysqlCheck('gone_db', 'secret_keys'), cred)
        self.assertEqual(False, result.success)
        self.assertEqual('Database gone_db does not exist', result.message)

    def test_mysql_no_connection(self):
        service = MysqlService('192.168.243.123')
        cred = CheckCredentials('root', 'greg')

        result = service.try_check(MysqlCheck('secret', 'secret_keys'), cred)
        self.assertEqual(service.connection_error(), result)

if __name__ == '__main__':
    unittest.main()
