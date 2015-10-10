import abc


class Machine:

    @abc.abstractmethod
    def get_services(self, team, ip=None, hostname=None):
        return []

    @abc.abstractmethod
    def get_flags(self, team):
        return []

    @abc.abstractmethod
    def get_injects(self, team):
        return []
