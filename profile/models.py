from django.db import models
from accounts.models import User
from register.models import StudentRegister
DESG_CHOICES = (
    ("Faculty", "Faculty"),
    ("Librarian", "Librarian"),
    ("Student", "Student"),

)
class UserProfile(models.Model):
    user      = models.ForeignKey(User, on_delete=models.CASCADE)
    name      = models.CharField(max_length=255, blank=True)
    req_desg  = models.CharField(max_length=30,choices=DESG_CHOICES,blank=True,null=True)
    updated = models.BooleanField(default=False)

    def __str__(self):
        return self.user.email
User.profile = property(lambda u: UserProfile.objects.get_or_create(user=u)[0])

class StudentProfile(models.Model):
    user_profile = models.ForeignKey(UserProfile,on_delete=models.CASCADE,null=True, blank=True)
    student = models.ForeignKey(StudentRegister, on_delete=models.CASCADE, null=True, blank=True)
    roll_no = models.IntegerField(null=True, blank=True, unique=True)

    def __str__(self):
        return str(self.roll_no)

class FacultyProfile(models.Model):
    user_profile = models.ForeignKey(UserProfile, on_delete=models.CASCADE,null=True, blank=True)
    aadhaar  = models.IntegerField(unique=True,blank=True,null=True)
    mobile_no= models.IntegerField(unique=True,null=True,blank=True)

    def __str__(self):
        return str(self.aadhaar)

class LibrarianProfile(models.Model):
    user_profile = models.ForeignKey(UserProfile, on_delete=models.CASCADE,null=True, blank=True)
    aadhaar = models.IntegerField(unique=True,blank=True,null=True )
    mobile_no = models.IntegerField(unique=True, null=True, blank=True)

    def __str__(self):
        return str(self.aadhaar)
