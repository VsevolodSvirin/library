import uuid

from domains.book import Book


def test_book_model_init():
    code = uuid.uuid4()
    book = Book(code=code, title='1984', author='George Orwell', year=1984,
                language='English', is_available=True, reader=None)
    assert book.code == code
    assert book.title == '1984'
    assert book.author == 'George Orwell'
    assert book.year == 1984
    assert book.language == 'English'
    assert book.is_available is True
    assert book.reader is None


def test_book_model_from_dict():
    code = uuid.uuid4()
    book = Book.from_dict(
        {
            'code': code,
            'title': '1984',
            'author': 'George Orwell',
            'year': 1984,
            'language': 'English',
            'is_available': True,
            'reader': None
        }
    )
    assert book.code == code
    assert book.title == '1984'
    assert book.author == 'George Orwell'
    assert book.year == 1984
    assert book.language == 'English'
    assert book.is_available is True
    assert book.reader is None
