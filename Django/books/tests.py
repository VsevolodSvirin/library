import uuid

from django.test import TestCase
from Django.books.forms import NewBookForm


class BookFormTestCase(TestCase):
    def test_form_accept_valid_data(self):
        code = uuid.uuid4()
        form_data = {
            "code": code,
            "title": "1984",
            "author": "George Orwell",
            "year": 1984,
            "language": "English",
            "is_available": True,
            "reader": None
        }
        form = NewBookForm(data=form_data)
        self.assertTrue(form.is_valid())

    def test_form_repulse_invalid_data(self):
        code = uuid.uuid4()
        form_data1 = {
            "code": code,
            "title": "1984",
            "author": "George Orwell",
            "year": "ololo",
            "language": "English",
            "is_available": True,
            "reader": None
        }
        form = NewBookForm(data=form_data1)
        self.assertFalse(form.is_valid())

        form_data2 = {
            "code": code,
            "title": (1,),
            "author": True,
            "year": 1984,
            "language": 1984,
            "is_available": True,
            "reader": None
        }
        form = NewBookForm(data=form_data2)
        self.assertFalse(form.is_valid())
