from django.core.management import BaseCommand, call_command
from library.models import User, Book
from library.util import get_book_cover_url

class Command(BaseCommand):
    help = "[DEV COMMAND] Fill databasse with initial data and set passwords for users."

    def add_arguments(self, parser):
        parser.add_argument('file', type=str, help='Path to the json file containing the initial data. (default: initial_data.json)', default='initial_data.json', nargs='?')

    def handle(self, *args, **options):
        call_command('loaddata', options['file'])
        self.stdout.write("Setting passwords for users...")
        for user in User.objects.all():
            user.set_password(user.password)
            user.save()
        self.stdout.write("Setting cover for books...")
        for book in Book.objects.all():
            book.cover = get_book_cover_url(book.title, book.author)
            book.save()
        self.stdout.write("Done.")