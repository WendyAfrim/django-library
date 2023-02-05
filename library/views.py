import base64
import datetime
from django.urls import reverse
import humanize
from django.shortcuts import render
from django.shortcuts import redirect
from django.utils import timezone
from django.utils.html import format_html
from django.contrib.auth.decorators import user_passes_test
from .util import get_book_cover_url, upload_image_to_imgbb
from .models import ReadingGroup, User, Book, Library, Borrowing
import django_filters
import django_tables2 as tables


class ReminderBookTable(tables.Table):
    class Meta:
        model = Borrowing
        attrs = {"class": "table"}
        template_name = "django_tables2/semantic.html"
        fields = ["book__title", "book__author", "due_at"]
        row_attrs = {
            "class": "is-clickable",
            "data-href": lambda record: reverse("book", kwargs={"book_id": record.book.id}),
        }

    book__title = tables.Column(verbose_name="Title")
    due_at = tables.Column(verbose_name="Due in")
    created_at = tables.Column(verbose_name="Borrowed at")

    def render_book__title(self, value, record):
        return format_html(f'<a href="{reverse("book", kwargs={"book_id": record.book.id})}">{value}</a>')

    def render_created_at(self, value):
        return format_html(f'<span class="tag is-info" title="{value.strftime("%d/%m/%Y %H:%M")}">{humanize.naturaltime(value, when=timezone.now())}</span>')

    def render_due_at(self, value):
        if value > timezone.now():
            return format_html(f'<span class="tag is-success" title="{value.strftime("%d/%m/%Y %H:%M")}">{(value - timezone.now()).days} days</span>')
        else:
            return format_html(f'<span class="tag is-danger" title="{value.strftime("%d/%m/%Y %H:%M")}">Overdue by {(timezone.now() - value).days} days</span>')

def index(request):
    trending_books = Book.objects.all().order_by("?")[:3]
    reminder_book_table = ReminderBookTable(Borrowing.objects.filter(user=request.user.id))
    reading_group_table = ReadingGroupTable(ReadingGroup.objects.all(), user=request.user)
    return render(request, "library/index.html", {
        "trending_books": trending_books,
        "reminder_book_table": reminder_book_table,
        "reading_group_table": reading_group_table,
    })

def search(request):
    if request.GET.get("library"):
        try:
            library_id = int(request.GET.get("library"))
        except ValueError:
            library_id = None
        try:
            library = Library.objects.get(id=library_id)
        except Library.DoesNotExist:
            library = None
    else:
        library = None
    query = request.GET.get("title") if request.GET.get("title") else ""
    books = Book.objects.all()
    if query:
        books = books.filter(title__icontains=query)
    if library:
        books = books.filter(libraries__id=library.id)
    context = {
        "query": query,
        "library": library,
        "books": books,
    }
    return render(request, "library/search.html", context)

def libraries(request):
    libraries = Library.objects.all()
    return render(request, "library/libraries.html", {"libraries": libraries})

def library(request, library_id):
    try:
        library = Library.objects.get(id=library_id)
    except Library.DoesNotExist:
        return redirect("libraries")
    books = Book.objects.filter(libraries__id=library_id)
    return render(request, "library/library.html", {"library": library, "books": books})

@user_passes_test(lambda u: u.is_superuser or User.is_bookseller(u))
def update_book(request, book_id):
    book = Book.objects.get(id=book_id)
    users = User.objects.all()
    libraries = Library.objects.all()
    if request.method == "POST":
        book.title = request.POST.get("title")
        book.author = request.POST.get("author")
        if request.FILES.get("cover"):
            b64 = base64.b64encode(request.FILES.get("cover").read())
            imgbb_url = upload_image_to_imgbb(b64) or book.cover
            book.cover = imgbb_url
        book.editor = request.POST.get("editor")
        book.collection = request.POST.get("collection")
        book.gender = request.POST.get("gender")
        libraries = request.POST.getlist("libraries")
        book.libraries.clear()
        libraries = Library.objects.filter(id__in=libraries)
        book.libraries.set(libraries)

        book.save()
        return redirect("book", book_id=book.id)
    return render(request, "library/book_update.html", {"book": book, "libraries": libraries, "users": users})

@user_passes_test(lambda u: u.is_superuser or User.is_bookseller(u))
def add_book(request):
    libraries = Library.objects.all()
    if request.method == "POST":
        book = Book()
        book.title = request.POST.get("title")
        book.author = request.POST.get("author")
        if request.FILES.get("cover"):
            b64 = base64.b64encode(request.FILES.get("cover").read())
            imgbb_url = upload_image_to_imgbb(b64) or book.cover
            book.cover = imgbb_url
        else:
            book.cover = get_book_cover_url(request.POST.get("title"), request.POST.get("author"))
        book.editor = request.POST.get("editor")
        book.collection = request.POST.get("collection")
        book.gender = request.POST.get("gender")
        libraries = request.POST.getlist("libraries")
        for library_id in libraries:
            library = Library.objects.get(id=library_id)
            book.libraries.add(library)
        book.save()
        return redirect("book", book_id=book.id)
    return render(request, "library/book_add.html", {"libraries": libraries})

@user_passes_test(lambda u: u.is_superuser or User.is_bookseller(u))
def delete_book(request, book_id):
    book = Book.objects.get(id=book_id)
    book.delete()
    return redirect("books")

def books(request):
    books = Book.objects.all()
    return render(request, "library/books.html", {"books": books})

def book(request, book_id):
    book = Book.objects.get(id=book_id)
    return render(request, "library/book.html", {"book": [book]})

def borrow_book(request, book_id):
    book = Book.objects.get(id=book_id)
    if book.borrowing:
        raise Exception("Book already borrowed")
    borrowing = Borrowing()
    borrowing.user = request.user
    borrowing.due_at = datetime.datetime.now() + datetime.timedelta(days=30)
    book.borrowing = borrowing
    borrowing.save()
    book.save()
    return redirect("book", book_id=book.id)

@user_passes_test(lambda u: u.is_superuser or User.is_bookseller(u))
def return_book(request, book_id):
    book = Book.objects.get(id=book_id)
    if not book.borrowing:
        raise Exception("Book not borrowed")
    book.borrowing.delete()
    book.borrowing = None
    book.save()
    return redirect("dashboard")

@user_passes_test(lambda u: u.is_superuser or User.is_bookseller(u))
def delete_reading_group(request, reading_group_id):
    reading_group = ReadingGroup.objects.get(id=reading_group_id)
    reading_group.delete()
    return redirect("dashboard")

@user_passes_test(lambda u: u.is_superuser or User.is_bookseller(u))
def add_reading_group(request):
    users = User.objects.all()
    if request.method == "POST":
        reading_group = ReadingGroup()
        reading_group.name = request.POST.get("name")
        reading_group.capacity = int(request.POST.get("capacity"))
        reading_group.description = request.POST.get("description")
        users = request.POST.getlist("users")
        if len(users) > reading_group.capacity:
            raise Exception("Too many users")
        reading_group.save()
        for user_id in users:
            user = User.objects.get(id=user_id)
            reading_group.users.add(user)
        reading_group.save()
        return redirect("dashboard")
    return render(request, "library/reading_group_add.html", {"users": users})

def reading_groups(request):
    reading_groups = ReadingGroup.objects.all()
    return render(request, "library/reading_groups.html", {"reading_groups": reading_groups})

def reading_group(request, reading_group_id):
    reading_group = ReadingGroup.objects.get(id=reading_group_id)
    return render(request, "library/reading_group.html", {"reading_groups": [reading_group]})

def join_reading_group(request, reading_group_id):
    reading_group = ReadingGroup.objects.get(id=reading_group_id)
    if request.user in reading_group.users.all():
        raise Exception("User already in reading group")
    if len(reading_group.users.all()) >= reading_group.capacity:
        raise Exception("Reading group is full")
    reading_group.users.add(request.user)
    reading_group.save()
    return redirect("reading_group", reading_group_id=reading_group.id)

def leave_reading_group(request, reading_group_id):
    reading_group = ReadingGroup.objects.get(id=reading_group_id)
    if request.user not in reading_group.users.all():
        raise Exception("User not in reading group")
    reading_group.users.remove(request.user)
    reading_group.save()
    return redirect("reading_group", reading_group_id=reading_group.id)

class BorrowedBookFilter(django_filters.FilterSet):
    overdue_only = django_filters.BooleanFilter(field_name="borrowing__due_at", method='filter_overdue')

    class Meta:
        model = Book
        fields = []

    def filter_overdue(self, queryset, name, value):
        if value:
            return queryset.filter(borrowing__due_at__lt=timezone.now())
        return queryset

class BorrowedBookTable(tables.Table):
    class Meta:
        model = Book
        attrs = {"class": "table", "id": "borrowed-book-table"}
        template_name = "django_tables2/semantic.html"
        fields = ("title", "author")
        row_attrs = {
            "class": "is-clickable",
            "data-href": lambda record: reverse("book", kwargs={"book_id": record.id}),
        }

    borrowing__user = tables.Column(verbose_name="Borrowed by")
    borrowing__created_at = tables.Column(verbose_name="Borrowed at")
    borrowing__due_at = tables.Column(verbose_name="Due at")
    actions = tables.TemplateColumn(template_name="table/book_actions.html", verbose_name="Actions")

    def render_borrowing__user(self, value):
        return f"{value.first_name} {value.last_name}" if (value.first_name or value.last_name) else value.username

    def render_borrowing__created_at(self, value):
        return format_html(f'<span class="tag is-info" title="{value.strftime("%d/%m/%Y %H:%M")}">{humanize.naturaltime(value, when=timezone.now())}</span>')

    def render_borrowing__due_at(self, value):
        if value > timezone.now():
            return format_html(f'<span class="tag is-success">Due in {(value - timezone.now()).days} days</span>')
        else:
            return format_html(f'<span class="tag is-danger">Overdue by {(timezone.now() - value).days} days</span>')

class DuedBooksUserTable(tables.Table):
    class Meta:
        model = Borrowing
        attrs = {"class": "table", "id": "dued-books-user-table"}
        template_name = "django_tables2/semantic.html"
        fields = ("book__title",)

    book__title = tables.Column(verbose_name="Book title")
    due_at = tables.Column(verbose_name="Overdue by")
    user = tables.Column(verbose_name="Borrowed by")
    created_at = tables.Column(verbose_name="Borrowed at")
    actions = tables.TemplateColumn(template_name="table/user_actions.html", verbose_name="Actions")

    def render_due_at(self, value):
        return format_html(f'<span class="tag is-danger" title="{value.strftime("%d/%m/%Y %H:%M")}">{(timezone.now() - value).days} days</span>')

    def render_created_at(self, value):
        return format_html(f'<span class="tag is-info" title="{value.strftime("%d/%m/%Y %H:%M")}">{humanize.naturaltime(value, when=timezone.now())}</span>')

    def render_user(self, value):
        return f"{value.first_name} {value.last_name}" if (value.first_name or value.last_name) else value.username

class ReadingGroupTable(tables.Table):
    def __init__(self, *args, **kwargs):
        self.user = kwargs.pop('user', None)
        super().__init__(*args, **kwargs)

    class Meta:
        model = ReadingGroup
        attrs = {"class": "table", "id": "reading-groups-table"}
        template_name = "django_tables2/semantic.html"
        fields = ("name", "description", "capacity", "actions")
        row_attrs = {
            "class": "is-clickable",
            "data-href": lambda record: reverse("reading_group", kwargs={"reading_group_id": record.id}),
        }

    actions = tables.Column(empty_values=())
    def render_actions(self, value, record):
        html = ""
        if self.user.reading_groups.filter(pk=record.pk).exists():
            html = format_html(f'<a class="button is-small is-danger mr-1" href="{reverse("reading_group_leave", kwargs={"reading_group_id": record.id})}">Leave</a>')
        else:
            html = format_html(f'<a class="button is-small is-primary mr-1" href="{reverse("reading_group_join", kwargs={"reading_group_id": record.id})}">Join</a>')
        if self.user.is_superuser or User.is_bookseller(self.user):
            # html += format_html(f'<a class="button is-small is-info mr-1" href="{reverse("reading_group_update", kwargs={"reading_group_id": record.id})}">Update</a>')
            html += format_html(f'<a class="button is-small is-danger" href="{reverse("reading_group_delete", kwargs={"reading_group_id": record.id})}">Delete</a>')
        return format_html(html)

@user_passes_test(lambda u: u.is_superuser or User.is_bookseller(u))
def dashboard(request):
    queryset = Book.objects.filter(borrowing__isnull=False)
    filterset = BorrowedBookFilter(request.GET, queryset=queryset)
    borrowed_book_table = BorrowedBookTable(filterset.qs)
    borrowed_book_table.paginate(page=request.GET.get("page", 1), per_page=10)
    dued_books_user_table = DuedBooksUserTable(Borrowing.objects.filter(due_at__lt=timezone.now()))
    dued_books_user_table.paginate(page=request.GET.get("page", 1), per_page=10)
    reading_group_table = ReadingGroupTable(ReadingGroup.objects.all(), user=request.user)
    reading_group_table.paginate(page=request.GET.get("page", 1), per_page=10)
    return render(request, "library/dashboard.html", {
        "borrowed_book_table": borrowed_book_table,
        "dued_books_user_table": dued_books_user_table,
        "reading_group_table": reading_group_table,
    })