from django.shortcuts import render
from books.models import Book
from django.views.generic import ListView
class SearchBookView(ListView):
    template_name = "search/view.html"

    def get_context_data(self, *args, **kwargs):
        context = super(SearchBookView, self).get_context_data(*args, **kwargs)
        context['query'] = self.request.GET.get('q')
        return context


    def get_queryset(self, *args, **kwargs):
        request = self.request
        method_dict=request.GET
        query = method_dict.get('q',None) # method_dict['q']
        #print(query)
        if query is not None:
            return Book.objects.search(query)
        return Book.objects.featured()
    '''
    __icontains = field contains this
    __ieaxct = field is exactly this
    '''