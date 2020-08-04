import datetime
import uuid

from django.test import TestCase
from django.utils import timezone

from ..forms import RenewBookForm
from ..models import Author, BookInstance, Book, Genre

class RenewBookFormTest(TestCase):

    book_instance_id = uuid.uuid4()

    @classmethod
    def setUpTestData(cls):
        # Set up non-modified objects used by all test methods
        Author.objects.create(first_name='Big', last_name='Bob')
        author = Author.objects.get(id=1)
        Genre.objects.create(name='TestGenre')
        genre = Genre.objects.get(id=1)
        Book.objects.create(title='abc', author=author, 
            summary='abcabcabac', isbn='9783598215995')
        
        book = Book.objects.get(id=1)
        book.genre.add(genre)

        BookInstance.objects.create(id=cls.book_instance_id, book=book, imprint='hogjeoiajge',
            due_back=(datetime.date.today() + datetime.timedelta(weeks=2)),
            status='o')
        
        print('database set up')

    def setUp(self):
        self.book_instance = BookInstance.objects.get(id=self.book_instance_id)

    def test_renew_form_date_field_label(self):
        proposed_renewal_date = self.book_instance.due_back + datetime.timedelta(weeks=3)
        form = RenewBookForm(initial={'renewal_date': proposed_renewal_date}, 
            book_instance=self.book_instance)
        #print('test 1')
        #print(form.fields['renewal_date'].label)
        self.assertTrue(form.fields['renewal_date'].label == None or form.fields['renewal_date'].label == 'renewal date')

    def test_renew_form_date_field_help_text(self):
        proposed_renewal_date = self.book_instance.due_back + datetime.timedelta(weeks=3)
        form = RenewBookForm(initial={'renewal_date': proposed_renewal_date}, 
            book_instance=self.book_instance)
        #print('test 2')
        #print(form.fields['renewal_date'].help_text)
        self.assertEqual(form.fields['renewal_date'].help_text, 'Enter a date between now and 4 weeks (default 3).')

    def test_renew_form_date_in_past(self):
        date = datetime.date.today() - datetime.timedelta(days=1)
        form = RenewBookForm(data={'renewal_date': date}, 
            book_instance=self.book_instance)
        self.assertFalse(form.is_valid())

    def test_renew_form_date_too_far_in_future(self):
        date = self.book_instance.due_back + datetime.timedelta(weeks=4) + datetime.timedelta(days=1)
        form = RenewBookForm(data={'renewal_date': date},
            book_instance=self.book_instance)
        self.assertFalse(form.is_valid())

    def test_renew_form_date_today(self):
        date = datetime.date.today()
        form = RenewBookForm(data={'renewal_date': date}, 
            book_instance=self.book_instance)
        self.assertFalse(form.is_valid())
        
    def test_renew_form_date_max(self):
        date = self.book_instance.due_back + datetime.timedelta(weeks=4)
        form = RenewBookForm(data={'renewal_date': date}, 
            book_instance=self.book_instance)
        self.assertTrue(form.is_valid())