from django.forms import ModelForm

from Django.books.models import Book
from Django.shared.custom_fields import StrictCharField


class NewBookForm(ModelForm):
    class Meta:
        model = Book
        fields = ["title", "author", "year", "language"]

    title = StrictCharField()
    author = StrictCharField()
    language = StrictCharField()
