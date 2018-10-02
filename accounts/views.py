from django.contrib.auth import authenticate , login , get_user_model , logout
from django.http import HttpResponse
from django.contrib.auth.decorators import user_passes_test
from .models import User
from profile.models import UserProfile,StudentProfile,FacultyProfile
from django.shortcuts import render,redirect
from django.utils.decorators import method_decorator

from .forms import RegisterForm,LoginForm
from django.urls import reverse_lazy,reverse
from django.views.generic.edit import CreateView,UpdateView
def login_page(request):
    if request.user.is_authenticated():
        return redirect("/")
    form=LoginForm(request.POST or None)
    context = {"form": form}
    if form.is_valid():
        username=form.cleaned_data.get("username")
        password=form.cleaned_data.get("password")
        user=authenticate(request,username=username,password=password)
        if user is not None:
                try:
                    profile = UserProfile.objects.get(user=user)
                    login(request,user)
                    context['form']=LoginForm()
                    return redirect(reverse_lazy("profile:profile-page"))# 'books:list'))
                except:
                    return HttpResponse("Please Register Yourself first<a href="">Go Back</a>")

                context['form']=LoginForm()
                context['error']="Please enter correct username or password"

    return render(request,"auth/login.html",context)

class ActivateAccount(UpdateView):
    @method_decorator(user_passes_test(lambda u: u.is_librarian))
    def dispatch(self, *args, **kwargs):
         return super().dispatch(*args, **kwargs)
    model = User
    template_name = 'accounts/activate-account.html'
    fields = ['desg']
    def form_valid(self, form):
        obj = form.save(commit=False)
        obj.acc_on = True
        profile = UserProfile.objects.get(user=obj)
        profile.save()
        if (obj.is_student):
             StudentProfile.objects.create(user_profile=profile)
        if (obj.is_faculty):
            FacultyProfile.objects.create(user_profile=profile)
        obj.save()
        return redirect(reverse_lazy("profile:confirm-profile"))
    # success_url = reverse_lazy("profile:confirm-profile")


def logout_page(request,*args,**kwargs):
     if request.user.is_authenticated():
        logout(request,*args,**kwargs)
        return redirect("/login/")
     else:
        return redirect("/login/")
class RegisterView(CreateView):
    form_class = RegisterForm
    template_name = 'auth/register.html'
    def form_valid(self, form):
        obj = form.save(commit=True)
        profile = UserProfile.objects.create(user=obj)
        login(self.request,obj)
        # obj.save()
        return redirect(reverse('profile:update-user-profile',kwargs={'pk':profile.id}))
    success_url = '/login/'
# User=get_user_model()
# def register_page(request):
#     if request.user.is_authenticated():
#         return redirect("/")
#     form = RegisterForm(request.POST or None)
#     context={"form":form}
#     if form.is_valid():
#         email=form.cleaned_data.get("email")
#         password=form.cleaned_data.get("password")
#         new_user=User.objects.create_user(email,password)
#         if new_user is not None:
#             login(request,new_user)
#             context['form']=RegisterForm()
#             return redirect(reverse_lazy("profile:user-profile"))
#     return render(request,"auth/register.html",context)
