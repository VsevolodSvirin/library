from django.http import QueryDict
from django.test import RequestFactory
from django.test import TestCase
from django.urls import reverse


class RequestStandartizerTestCase(TestCase):
    def setUp(self):
        self.factory = RequestFactory()

    class RequestStandartizerTestCase(TestCase):
        def setUp(self):
            self.factory = RequestFactory()

        def test_with_post_data(self):
            initial_data = {
                'title': '1984',
                'author': 'George Orwell',
                'year': 1984,
                'language': 'English',
            }
            request = self.factory.post(reverse('books_list'), initial_data)
            qdict = QueryDict(mutable=True)
            qdict.update(initial_data)
            self.assertEqual(request.POST.dict(), qdict.dict())

    def test_with_body_data(self):
        pass
