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


DomainModel.register(Reader)
