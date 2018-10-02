from django.db import models
from books.models import Book
from django.db.models.signals import pre_save, post_save, m2m_changed, pre_init,post_init
from datetime import date

today=date.today()
BATCH_CHOICES = (
    ("CSE", "Computer Science & Engineering"),
    ("CIVIL", "Civil Engineering"),
    ("ELECTRICAL", "Electrical Engineering"),
    ("ELECTRONICS", "Electronics Engineering"),
)
class RegisterQuerySet(models.query.QuerySet):
    def Returned(self):
        return self.filter(returned=True)

    def active(self):
        return self.filter(active=True)

class RegisterManager(models.Manager):
    def get_queryset(self):
        return self.all()

    def all(self):
        return self.get_queryset().active()

    def returned(self): #Product.objects.featured()
        return self.get_queryset().returned()

    def get_by_id(self, id):
        qs = self.get_queryset().filter(id=id) # Product.objects == self.get_queryset()
        if qs.count() == 1:
            return qs.first()
        return None

    # def search(self, query):
    #     return self.get_queryset().active().search(query)


class StudentRegister(models.Model):
    name                  = models.CharField(max_length=120)
    roll_no               = models.IntegerField(unique=True)
    batch                 = models.CharField(max_length=120,choices=BATCH_CHOICES)
    year                  = models.IntegerField()
    books_issued          = models.IntegerField(default=0)
    books_issued_tilldate = models.IntegerField(default=0)

    objects       = RegisterManager

    def __str__(self):
        return "{}{}".format(self.name,self.roll_no)



    def __meta__(self):
        ordering='roll_no'

class BookRegister(models.Model):
    student      = models.ForeignKey(StudentRegister, on_delete=models.CASCADE)
    book         = models.ForeignKey(Book, on_delete=models.CASCADE, null=True, blank=True)
    book_no      = models.IntegerField(default=0)
    issue_date   = models.DateField(auto_now_add=True)
    return_date  = models.DateField(auto_now_add=False, blank=True,null=True)
    due_date     = models.DateField(blank=True,null=True)
    fine         = models.IntegerField(default=0)
    status       = models.BooleanField(default=True)
    new          = models.BooleanField(default=True)
    objects      = RegisterManager
    def __str__(self):
        return "{}{}".format(self.student,self.book)

    @property
    def is_past_due(self):
        return self.due_date<=today and self.return_date is None

    def __meta__(self):
        ordering='student'


def booksissued_post_save_receiver(sender, instance, *args, **kwargs):
    if(instance.status==False):
        qs = instance.student
        qs1 = BookRegister.objects.filter(student=qs.id)
        # print(BookRegister.objects.filter(student=qs.id))
        y = 0
        x = 0
        for i in qs1:
            y += 1
            if (i.status == False):
                x += 1
        qs.books_issued_tilldate = y
        qs.books_issued = x
        qs.save()
        #qs = instance.book
        qs = instance.book
        qs1 = BookRegister.objects.filter(book=qs.id,status=False)
        #print(qs1)
        # print(BookRegister.objects.filter(student=qs.id))
        y = 0
        for i in qs1:
            y += 1
        qs.copies = qs.total_copies - y
        qs.save()
    else:
        qs = instance.student
        qs1 = BookRegister.objects.filter(student=qs.id)
        # print(BookRegister.objects.filter(student=qs.id))
        y = 0
        x = 0
        for i in qs1:
            y += 1
            if (i.status == False):
                x += 1
        qs.books_issued_tilldate = y
        qs.books_issued = x
        qs.save()
        qs = instance.book
        qs1 = BookRegister.objects.filter(book=qs.id, status=False)
        #print(qs1)
        # print(BookRegister.objects.filter(student=qs.id))
        y = 0
        for i in qs1:
            y += 1
        qs.copies = qs.total_copies - y
        qs.save()

# post_save.connect(booksissued_post_save_receiver, sender=BookRegister)
#m2m_changed.connect(booksissued_pre_save_receiver, sender=BookRegister)
