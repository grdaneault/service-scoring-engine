import abc

class ServiceCheck:

    __slots__ = ('host')

    def __init__(self, host):
        self.host = host

    @abc.abstractstaticmethod
    def get_checks(self, team):
        return []

    @abc.abstractmethod
    def execute(self):
        return CheckResult()


class CheckResult:
    __slots__ = ('success', 'reason')

    def __init__(self, success=True, reason=''):
        self.success = success
        self.reason = reason


