class BookListRequestObject(object):
    @classmethod
    def from_dict(cls, adict):
        return BookListRequestObject()

    def __nonzero__(self):
        return True
