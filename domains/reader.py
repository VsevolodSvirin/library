from shared.domain_model import DomainModel


class Reader(object):
    __slots__ = ('code', 'full_name', 'reg_date', )

    def __init__(self, **kwargs):
        self.code = kwargs['code']
        self.full_name = kwargs['full_name']
        self.reg_date = kwargs['reg_date']

    @classmethod
    def from_dict(cls, adict):
        reader = Reader(
            code=adict['code'],
            full_name=adict['full_name'],
            reg_date=adict['reg_date']
        )

        return reader

    def __eq__(self, other):
        return self.code == other.code and self.full_name == other.full_name and self.reg_date == other.reg_date

DomainModel.register(Reader)
