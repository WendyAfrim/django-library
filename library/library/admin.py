from django.contrib import admin
from .models import Library
from .models import Session
from .models import Borrowing

admin.site.register(Library)
admin.site.register(Session)
admin.site.register(Borrowing)