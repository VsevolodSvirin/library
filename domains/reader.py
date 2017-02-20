from shared.domain_model import DomainModel


class Reader(object):
    def __init__(self, code, full_name, reg_date):
        self.code = code
        self.full_name = full_name
        self.reg_date = reg_date

    @classmethod
    def from_dict(cls, adict):
        reader = Reader(
            code=adict['code'],
            full_name=adict['full_name'],
            reg_date=adict['reg_date']
        )

        return reader


DomainModel.register(Reader)
