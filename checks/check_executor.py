import threading
from checks.service_checks import CheckResult


class CheckExecutor(threading.Thread):

    __slots__ = ('result_lock', 'round', 'service', 'check', 'credentials')

    def __init__(self, result_lock, round, service, check, credentials):
        threading.Thread.__init__(self)
        self.result_lock = result_lock
        self.round = round
        self.service = service
        self.check = check
        self.credentials = credentials

    def run(self):
        try:
            result = self.service.try_check(self.check, self.credentials)
        except Exception as e:
            result = CheckResult(False, 'Unhandled exception during check: ' + str(e))
            result.check = self.check

        pass_str = "PASS" if result.success else "FAIL"
        print('%s - check %s (%s)' % (pass_str, str(self.check), result.reason))
        self.result_lock.acquire()
        self.round.checks.append(result)
        self.result_lock.release()
