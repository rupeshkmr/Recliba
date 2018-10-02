from django.shortcuts import render
from .models import UserProfile,FacultyProfile,StudentProfile,LibrarianProfile
from django.contrib.auth.models import User
from django.http import Http404
from django.contrib.auth.decorators import login_required
from .forms import UserProfileForm
from django.urls import reverse_lazy,reverse
from django.template.context_processors import csrf
from django.http import HttpResponseRedirect,HttpResponse
from django.views.generic.edit import CreateView,UpdateView,DeleteView,FormView
from register.models import StudentRegister, BookRegister
from django.shortcuts import redirect
from django.utils.decorators import method_decorator
from django.contrib.auth.decorators import user_passes_test
from django.views.generic import ListView, DetailView
from .models import UserProfile,FacultyProfile,LibrarianProfile,StudentProfile
from django.contrib.auth import authenticate , login , get_user_model , logout
User = get_user_model()

class ConfirmProfile(ListView):
    @method_decorator(user_passes_test(lambda u:  u.is_librarian))
    def dispatch(self, *args, **kwargs):
        return super().dispatch(*args, **kwargs)

    template_name = 'user-profile/confirm_profile.html'
    def get_queryset(self):
        queryset = UserProfile.objects.all()
        return queryset
    def get_queryset2(self):
        return User.objects.filter(acc_on=False)
    def get_context_data(self, **kwargs):
        context = super(ConfirmProfile, self).get_context_data(**kwargs)
        context['user_list'] = self.get_queryset2()
        # And so on for more models
        return context

@login_required
def user_profile(request):
    if request.method == 'POST':
        form = UserProfileForm(request.POST, instance=request.user.profile)
        if form.is_valid():
            form.save()
            return HttpResponseRedirect('/')
    else:
        user = request.user
        profile = user.profile
        form = UserProfileForm(instance=profile)

    args = {}
    args.update(csrf(request))
    args['form'] = form
    return  redirect(reverse('profile:update-user-profile',kwargs={'pk':profile.id}))
class UpdateStudentProfile(UpdateView):
    @method_decorator(user_passes_test(lambda u: u.is_authenticated))
    def dispatch(self, *args, **kwargs):
         return super().dispatch(*args, **kwargs)
    model = StudentProfile
    fields = ['roll_no']
    template_name = 'user-profile/update-student-profile.html'
    def form_valid(self,form):
        obj = form.save(commit=False)
        try:
            obj.student = StudentRegister.objects.get(roll_no=obj.roll_no)
            obj.save()
        except:
            raise Http404('Sorry that roll number is not Registered!Contact Library')
        form.save(commit=True)
        return HttpResponseRedirect(reverse_lazy('profile:profile-page'))
    success_url = 'profile:profile-page'
class UpdateFacultyProfile(UpdateView):
    @method_decorator(user_passes_test(lambda u: u.is_authenticated))
    def dispatch(self, *args, **kwargs):
         return super().dispatch(*args, **kwargs)
    model = FacultyProfile
    fields = ['aadhaar','mobile_no']
    template_name = 'user-profile/update-faculty-profile.html'
    success_url = reverse_lazy('profile:profile-page')

class UpdateUserProfile(UpdateView):
    @method_decorator(user_passes_test(lambda u: u.is_authenticated))
    def dispatch(self, *args, **kwargs):
        return super().dispatch(*args, **kwargs)

    template_name = 'user-profile/update-profile.html'
    model = UserProfile
    fields = ['name','req_desg']
    #
    # def form_valid(self, form):
    #     obj = form.save(commit=False)
    #     try:
    #         obj.student = StudentRegister.objects.get(roll_no__iexact=obj.roll_no)
    #         obj.save()
    #         obj.name = obj.student.name
    #         obj.save()
    #         return HttpResponseRedirect('/')
    #     except:
    #         # user = self.request.user
    #         user = User.objects.get(email=self.request.user.email)
    #         logout(self.request)
    #         user.delete()
    #         obj.delete()
    #         return redirect(reverse("profile:error"))
    success_url = reverse_lazy('profile:profile-page')

def error(request):
    return render(request,'user-profile/error.html',{})
User = get_user_model()
class ProfilePage(ListView):
    @method_decorator(user_passes_test(lambda u: u.is_authenticated))# and u.is_staff==False))
    def dispatch(self, *args, **kwargs):
        return super().dispatch(*args, **kwargs)

    template_name = 'user-profile/profile-page.html'
    def get_queryset(self):
        query = None
        if(self.request.user.is_student):
            profile = UserProfile.objects.filter(user=self.request.user)
            query = StudentProfile.objects.filter(user_profile=profile)

        if(self.request.user.is_faculty):
             profile = UserProfile.objects.filter(user=self.request.user)
             query = FacultyProfile.objects.filter(user_profile=profile)
        if (self.request.user.is_librarian):
            profile = UserProfile.objects.filter(user=self.request.user)
            query = LibrarianProfile.objects.filter(user_profile=profile)
        return query
    def get_queryset2(self):
        query = None
        if(self.request.user.is_student):
            profile = UserProfile.objects.filter(user=self.request.user)
            try:
                student = StudentProfile.objects.get(user_profile=profile).student
                query = BookRegister.objects.filter(student=student)
            except:
                query=None
        if(self.request.user.is_faculty):
             profile = UserProfile.objects.filter(user=self.request.user)
             query = FacultyProfile.objects.filter(user_profile=profile)
        if (self.request.user.is_librarian):
            profile = UserProfile.objects.filter(user=self.request.user)
            query = LibrarianProfile.objects.filter(user_profile=profile)
        return query

    def get_context_data(self, **kwargs):
        context = super(ProfilePage, self).get_context_data(**kwargs)
        context['book_list'] = self.get_queryset2()
        # And so on for more models
        return context
