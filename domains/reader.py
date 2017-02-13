from shared.domain_model import DomainModel


class Reader(object):
    def __init__(self, code, full_name, reg_date):
        self.code = code
        self.full_name = full_name
        self.reg_date = reg_date


DomainModel.register(Reader)
