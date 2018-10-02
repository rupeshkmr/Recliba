from django.shortcuts import render
from .models import StudentRegister, BookRegister , booksissued_post_save_receiver
from django.views.generic import ListView, DetailView
from django.http import Http404
from django.views.generic.edit import CreateView,UpdateView,DeleteView,FormView
from django.urls import reverse_lazy,reverse
from django.http import HttpResponseRedirect, HttpResponse
from datetime import date, timedelta
from books.models import Book
from django.shortcuts import redirect
from django.db.models import Q
from django.db.models.signals import pre_save, post_save, m2m_changed
from django.contrib.auth.decorators import user_passes_test
from django.utils.decorators import method_decorator
from django.contrib.auth.decorators import login_required
from .forms import RegisterUpdateForm, IssueForm, ReturnForm
from profile.models import UserProfile
today = date.today()
class StudentList(ListView):
    @method_decorator(user_passes_test(lambda u: u.is_librarian))#u.is_superuser))
    def dispatch(self, *args, **kwargs):
        return super().dispatch(*args, **kwargs)

    template_name = 'register/list.html'
    def get_queryset(self, *args, **kwargs):
        request = self.request
        method_dict = request.GET
        query = method_dict.get('q', None)  # method_dict['q']
        if query is not None:
            lookups = Q(name__icontains=query) | Q(roll_no__icontains=query) | Q(batch__icontains=query)
            return StudentRegister.objects.filter(lookups)
        return StudentRegister.objects.all()


def length(x):
    s = 0
    while(x >0):
        s=s+1
        x=x/10
    return s

class RegisterDetail(DetailView):
    @method_decorator(user_passes_test(lambda u:  u.is_librarian))
    def dispatch(self, *args, **kwargs):
        return super().dispatch(*args, **kwargs)

    template_name = 'register/detail.html'
    def get_object(self, *args, **kwargs):
        request = self.request
        id = self.kwargs.get('pk')
        try:
            instance = []
            instance.append(BookRegister.objects.get(student=StudentRegister.objects.filter(id=id)))
        except BookRegister.DoesNotExist:
            instance = []
            instance.append(StudentRegister.objects.get(id=id))
        except BookRegister.MultipleObjectsReturned:
            qs = BookRegister.objects.filter(student=StudentRegister.objects.filter(id=id)).all()
            instance = []
            for i in qs:
                instance.append(i)
        except:
            raise Http404("Uhmm")
        return instance

# class IssueBookUpdateRegister(CreateView):
#         template_name = 'register/issue.html'
#         model = BookRegister
#         fields = ['student','book_no']
#
#         def form_valid(self, form):
#             obj = form.save(commit=False)
#             obj.new = False
#             obj.status = False
#             obj.save()
#             x = obj.book_no
#             x = int(x / 100)
#             obj.book = Book.objects.get(isbn__iexact=x)
#             obj.due_date = obj.issue_date + timedelta(days=15)
#             obj.save()
#             booksissued_post_save_receiver(instance=obj, sender=BookRegister)
#             #post_save.connect(booksissued_post_save_receiver, sender=BookRegister)
#             return HttpResponseRedirect(reverse_lazy('student-register:list'))
#
#
#         success_url = reverse_lazy('student-register:list')

class IssueBookUpdateRegister(UpdateView):
        '''Class Based View for issuing book'''
        @method_decorator(user_passes_test(lambda u:  u.is_librarian))
        def dispatch(self, *args, **kwargs):
            return super().dispatch(*args, **kwargs)

        template_name = 'register/issue.html'
        model = BookRegister
        fields = ['book_no','due_date']

        def form_valid(self, form):
            obj = form.save(commit=False)
            obj.new = False
            obj.status = False
            obj.save()
            x = obj.book_no
            try:
                objb = BookRegister.objects.filter(book_no__iexact=x, status=False)
                y = 0
                for i in objb:
                    y += 1
                if(y==1):
                    x = int(x / 100)
                    obj.book = Book.objects.get(isbn__iexact=x)
                    if obj.book.less_quantity:
                        print(obj.book.copies,obj.book.less_quantity)
                        return HttpResponse("<h1>Sorry! Only a few amount of the book is available in the library<a href="">Go back</a></h1>")
                    if obj.due_date is None:
                        obj.due_date = obj.issue_date + timedelta(days=15)
                    obj.save()
                    booksissued_post_save_receiver(instance=obj, sender=BookRegister)
                    # post_save.connect(booksissued_post_save_receiver, sender=BookRegister)
                    return HttpResponseRedirect(reverse_lazy('student-register:issue-book'))
                else:
                    return HttpResponseRedirect(reverse_lazy('student-register:duplicacy'))
            except:
                return HttpResponse("<h2>Sorry The book is not avialable</h2>")

class RegisterStudent(CreateView):
    @method_decorator(user_passes_test(lambda u: u.is_librarian))
    def dispatch(self, *args, **kwargs):
        return super().dispatch(*args, **kwargs)

    template_name = 'register/student_form.html'
    model = StudentRegister
    fields = ['name', 'roll_no', 'batch', 'year']
    success_url = reverse_lazy('student-register:list')


class ReturnBookUpdateRegister(UpdateView):
        @method_decorator(user_passes_test(lambda u:  u.is_librarian))
        def dispatch(self, *args, **kwargs):
            return super().dispatch(*args, **kwargs)

        template_name = 'register/register_update_form.html'
        model = BookRegister
        fields=['fine']

        def form_valid(self, form):
            obj = form.save(commit=False)
            obj.status = True
            obj.return_date=today
            obj.save()
            booksissued_post_save_receiver(instance=obj, sender=BookRegister)
            obj.save()
            return HttpResponseRedirect(reverse_lazy('student-register:return-book'))
        success_url=reverse_lazy('student-register:return-book')

# class ReturnBookView(ListView):
#     @method_decorator(user_passes_test(lambda u: u.is_superuser))
#     def dispatch(self, *args, **kwargs):
#         return super().dispatch(*args, **kwargs)
#
#     template_name = "register/returnview.html"
#
#     def get_queryset(self, *args, **kwargs):
#         request = self.request
#         method_dict=request.GET
#         query = method_dict.get('q',None) # method_dict['q']
#         if query is not None:
#             return BookRegister.objects.filter(book_no__iexact=query, status=False)
#         return

# class IssueBookView(ListView):
#     @method_decorator(user_passes_test(lambda u: u.is_superuser))
#     def dispatch(self, *args, **kwargs):
#         return super().dispatch(*args, **kwargs)
#
#     template_name = "register/issueview.html"
#     def get_queryset(self, *args, **kwargs):
#         blank_obj = BookRegister.objects.filter(book=None)
#         blank_obj.delete()
#         request = self.request
#         method_dict=request.GET
#         query = method_dict.get('q',None) # method_dict['q']
#         if query is not None:
#             if(StudentRegister.objects.filter(roll_no__iexact=query)):
#                 obj = StudentRegister.objects.get(roll_no__iexact=query)
#                 obj1 = StudentRegister.objects.get(roll_no__iexact=query)
#                 obj2 = BookRegister.objects.filter(student=obj1, new=False)
#                 objs = StudentRegister.objects.get(roll_no__iexact=query)
#                 y = objs.books_issued
#                 if(y<10):
#                     BookRegister.objects.create(student=obj)
#                     return BookRegister.objects.filter(student=obj1, new=True)
#                 if(y>=10):
#                     return y
#         return False

class BookAlreadyIssued(ListView):
    @method_decorator(user_passes_test(lambda u:  u.is_librarian))
    def dispatch(self, *args, **kwargs):
        return super().dispatch(*args, **kwargs)

    template_name = 'register/duplicacy.html'
    queryset = BookRegister.objects.filter(book=None, status=False, new=False)
@login_required
def IssueBookFBV(request):
    form = IssueForm(request.POST or None)
    context = {'form': form}
    user = UserProfile.objects.get(user=request.user)
    if(request.user.is_librarian):
        try:
            blank_obj = BookRegister.objects.filter(book=None)
            blank_obj.delete()
        except:
            pass
        if form.is_valid():
            roll_no = form.cleaned_data.get("roll")
            try:
                student = StudentRegister.objects.get(roll_no=roll_no)
                y = student.books_issued
                if (y < 10):
                    BookRegister.objects.create(student=student)
                    obj = BookRegister.objects.get(student=student, new=True)
                    return redirect(reverse('student-register:issue',kwargs={'pk':obj.id}))
                else:
                    context = {'form':form,
                               'error':"Sorry You have exceeded the limit of 10 issues"}
            except:# StudentRegister matching query does not exist:
              context = {'form':form,'register':'Please Register First'}

        return render(request,"register/issuefbv.html",context)
    else:
        context = {'error':"Sorry you can't see this page"}
        raise Http404("Page does not exists")

@login_required
def ReturnBookFBV(request):
    form = ReturnForm(request.POST or None)
    context = {'form': form}
    user = UserProfile.objects.get(user=request.user)
    if(request.user.is_librarian):
        blank_obj = BookRegister.objects.filter(book=None)
        blank_obj.delete()
        if form.is_valid():
            book_no = form.cleaned_data.get("book")
            try:
                book = BookRegister.objects.get(book_no__iexact=book_no, status=False)
                d0 = book.due_date
                d1 = today
                delta = d1 - d0
                if(delta.days>0):
                    book.fine = delta.days * 10
                    book.save()
                return redirect(reverse('student-register:update', kwargs={'pk': book.id}))
            except:
                context = {'form':form,'register':'Sorry the book is not issued'}

        return render(request,"register/returnfbv.html",context)
    else:
        context = {'error':"Sorry you can't see this page"}
        raise Http404("Page does not exists")
