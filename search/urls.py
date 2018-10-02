from django.conf.urls import url
from books.views import BookListView
from .views import SearchBookView

urlpatterns = [
    url(r'^/$', SearchBookView.as_view(), name='query'),

]

