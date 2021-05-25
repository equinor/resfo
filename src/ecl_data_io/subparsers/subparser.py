from abc import ABCMeta, abstractmethod, abstractproperty


class SubParser:
    @abstractproperty
    def keyword(self):
        pass

    def parse(self, super_parser, lines):
        pass
