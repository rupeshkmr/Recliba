from django.conf.urls import url
from .views import StudentList, RegisterDetail, ReturnBookUpdateRegister, IssueBookUpdateRegister, RegisterStudent,  BookAlreadyIssued, IssueBookFBV, ReturnBookFBV

'''ReturnBookView,IssueBookView,'''
urlpatterns = [
    url(r'^/$', StudentList.as_view(), name='list'),
    url(r'^/(?P<pk>\d+)/$', RegisterDetail.as_view(), name='detail'),
    url(r'^update-register/(?P<pk>\d+)/$', ReturnBookUpdateRegister.as_view(), name='update'),
    url(r'^issue-update-register/(?P<pk>\d+)/$', IssueBookUpdateRegister.as_view(), name='issue'),
    url(r'^register-student/$', RegisterStudent.as_view(), name='register-student'),
    url(r'^duplicacy/$', BookAlreadyIssued.as_view(), name='duplicacy'),
    url(r'^issue-book/$', IssueBookFBV, name='issue-book'),
    url(r'^return-book/$', ReturnBookFBV, name='return-book'),
]