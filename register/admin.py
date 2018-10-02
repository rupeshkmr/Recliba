from django.contrib import admin
from .models import StudentRegister, BookRegister

admin.site.register(StudentRegister)
admin.site.register(BookRegister)