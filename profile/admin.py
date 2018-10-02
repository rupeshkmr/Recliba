from django.contrib import admin
from .models import UserProfile,StudentProfile,FacultyProfile,LibrarianProfile

admin.site.register(UserProfile)
admin.site.register(StudentProfile)
admin.site.register(FacultyProfile)
admin.site.register(LibrarianProfile)