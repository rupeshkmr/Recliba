from django.conf.urls import url
from .views import BookListView, BookDetailSlugView, RegisterBooks

urlpatterns = [
    url(r'^$', BookListView.as_view(), name='list'),
    url(r'^(?P<slug>[\w-]+)/$', BookDetailSlugView.as_view(), name='detail'),
    url(r'^register-books$', RegisterBooks.as_view(), name='register-books'),

]

