import threading
from checks.service_checks import CheckResult


class CheckExecutor(threading.Thread):

    __slots__ = ('result', 'service', 'check', 'credentials')

    def __init__(self, service, check, credentials):
        threading.Thread.__init__(self)
        self.service = service
        self.check = check
        self.credentials = credentials
        self.result = CheckResult(False, 'Check not executed')

    def run(self):
        try:
            result = self.service.try_check(self.check, self.credentials)
        except Exception as e:
            result = CheckResult(False, 'Unhandled exception during check: ' + str(e))

        result.check = self.check

        pass_str = "PASS" if result.success else "FAIL"
        print('%s - check %s (%s)' % (pass_str, str(self.check), result.message))
        self.result = result
