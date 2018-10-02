from django.conf.urls import url
from .views import user_profile, UpdateUserProfile, ProfilePage, error, ConfirmProfile,UpdateStudentProfile,UpdateFacultyProfile


urlpatterns = [
    url(r'^user-profile/$', user_profile, name='user-profile'),
    url(r'^update-user-profile/(?P<pk>\d+)/$', UpdateUserProfile.as_view(), name='update-user-profile'),
    url(r'^update-student-profile/(?P<pk>\d+)/$', UpdateStudentProfile.as_view(), name='update-student-profile'),
    url(r'^update-faculty-profile/(?P<pk>\d+)/$', UpdateFacultyProfile.as_view(), name='update-faculty-profile'),
    url(r'^profile-page/$', ProfilePage.as_view(), name='profile-page'),
    url(r'^error/$', error, name='error'),
    url(r'^confirm-profile/$', ConfirmProfile.as_view(), name='confirm-profile'),

]

