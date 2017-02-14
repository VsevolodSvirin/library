class BookListRequestObject(object):
    @classmethod
    def from_dict(cls, adict):
        return BookListRequestObject()

    def __nonzero__(self):
        return True


class ReaderListRequestObject(object):
    @classmethod
    def from_dict(cls, adict):
        return ReaderListRequestObject()

    def __nonzero__(self):
        return True