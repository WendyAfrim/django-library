from django.contrib.auth.admin import UserAdmin
from django.contrib import admin
from .models import ReadingGroups, User, Library, Book, Session, Borrowing

# Register your models here.
# admin.site.register(User, UserAdmin)

@admin.register(User)
class UserAdmin(UserAdmin):
    list_display = ('username', 'email', 'first_name', 'last_name', 'is_staff', 'is_active', 'reading_groups')
    list_filter = ('username', 'email', 'first_name', 'last_name', 'is_staff', 'is_active', 'reading_groups')
    fieldsets = (
        (None, {'fields': ('username', 'email', 'password', 'reading_groups')}),
        ('Personal info', {'fields': ('first_name', 'last_name')}),
        ('Permissions', {'fields': ('is_active', 'is_staff', 'is_superuser', 'groups', 'user_permissions')}),
        ('Important dates', {'fields': ('last_login', 'date_joined')}),
    )
    add_fieldsets = (
        (None, {
            'classes': ('wide',),
            'fields': ('username', 'password1', 'password2', 'reading_groups'),
        }),
        ('Personal info', {'fields': ('first_name', 'last_name', 'email', 'reading_groups')}),
        ('Permissions', {'fields': ('is_active', 'is_staff', 'is_superuser', 'groups', 'user_permissions')}),
    )
    @admin.display(description='Parent')
    def get_parent_name(self, obj):
        return obj.parent.name

admin.site.register(ReadingGroups)
admin.site.register(Library)
admin.site.register(Book)
admin.site.register(Session)
admin.site.register(Borrowing)
