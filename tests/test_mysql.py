from checks.services.check_mysql import MysqlService
from checks.service_checks import CheckCredentials

__author__ = 'gregd'

import unittest


class MysqlTestCase(unittest.TestCase):
    def test_mysql(self):
        check = MysqlService('192.168.243.131', 'secret', 'secret_keys')
        cred = CheckCredentials('root', 'greg')

        result = check.execute(cred)

        self.assertEqual(True, result.success)
        self.assertEqual('Table secret_keys has data', result.reason)

    def test_mysql_bad_credentials(self):
        check = MysqlService('192.168.243.131', 'secret', 'secret_keys')
        cred = CheckCredentials('root', 'badpass')

        result = check.execute(cred)
        self.assertEqual(check.invalid_credentials(cred), result)

    def test_mysql_empty_table(self):
        check = MysqlService('192.168.243.131', 'secret', 'red_team_was_here')
        cred = CheckCredentials('root', 'greg')

        result = check.execute(cred)
        self.assertEqual(False, result.success)
        self.assertEqual('Table red_team_was_here is empty', result.reason)

    def test_mysql_no_database(self):
        check = MysqlService('192.168.243.131', 'gone_db', 'secret_keys')
        cred = CheckCredentials('root', 'greg')

        result = check.execute(cred)
        self.assertEqual(False, result.success)
        self.assertEqual('Database gone_db does not exist', result.reason)

    def test_mysql_no_connection(self):
        check = MysqlService('192.168.243.131', 'secret', 'secret_keys')
        cred = CheckCredentials('root', 'greg')

        result = check.execute(cred)
        self.assertEqual(check.connection_error(), result)

if __name__ == '__main__':
    unittest.main()
