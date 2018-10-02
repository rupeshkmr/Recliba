from django.http import Http404
from django.views.generic import ListView , DetailView
from .models import Book
from django.views.generic import CreateView
from django.urls import reverse_lazy,reverse
from django.http import HttpResponseRedirect
from django.utils.decorators import method_decorator
from django.contrib.auth.decorators import user_passes_test
from profile.models import UserProfile
from django.shortcuts import render , get_object_or_404
#from carts.models  import Cart

# class ProductFeaturedListView(ListView):
#     template_name = "products/list.html"

#     def get_queryset(self, *args, **kwargs):
#         request = self.request
#         return Product.objects.all().featured()

# class ProductFeaturedDetailView(DetailView):
#     template_name = "products/featured-detail.html"
#     queryset = Product.objects.all().featured()
#     #def get_queryset(self, *args, **kwargs):
#      #   request = self.request
#       #  return Product.objects.featured()


class RegisterBooks(CreateView):
    @method_decorator(user_passes_test(lambda u:  u.is_librarian))
    def dispatch(self, *args, **kwargs):
        return super().dispatch(*args, **kwargs)

    template_name = 'books/book_form.html'
    model = Book
    fields = ['title', 'author','isbn',  'total_copies','description','price','image']

    def form_valid(self, form):
        obj = form.save(commit=False)
        try:
            if((Book.objects.get(title=obj.title) != None) and (Book.objects.get(author=obj.author) != None)):
                return
        except:
            pass
        obj.copies = obj.total_copies
        obj.save()
        return HttpResponseRedirect(reverse_lazy('books:list'))

    success_url = reverse_lazy('books:list')

class BookListView(ListView):
    template_name = "books/list.html"
    def get_queryset(self, *args, **kwargs):
        request = self.request
        return Book.objects.all()

# get_context_data(abc, 123, adsfads, another=abc, abc=123)


class BookDetailSlugView(DetailView):
    queryset = Book.objects.all()
    template_name="books/detail.html"

    def get_object(self, *args, **kwargs):
        request = self.request
        slug = self.kwargs.get('slug')
        try:
            instance = Book.objects.get(slug=slug, active=True)
        except Book.DoesNotExist:
            raise Http404("Not Found")
        except Book.MultipleObjectsReturned:
            qs = Book.objects.filter(slug=slug, active=True)
            instance = qs.first()
        except:
            raise Http404("Uhmm")

        return instance


# class ProductDetailView(DetailView):
#     #queryset = Product.objects.all()
#     template_name="products/detail.html"
#     def get_object(self, *args, **kwargs):
#         request = self.request
#         pk = self.kwargs.get('pk')
#         instance = Product.objects.get_by_id(pk)
#         if instance is None:
#             raise Http404("Product doesn,t exist")
#         return instance

    #def get_queryset(self, *args, **kwargs):
     #   request = self.request
      #  pk = self.kwargs.get('pk')
       # return Product.objects.filter(pk=pk)

# def product_detail_view(request, pk=None,  *args, **kwargs ):
#     #instance = Product.objects.get(pk=pk)
#     #instance = get_object_or_404(Product, pk=pk)
#     #try:
#      #   instance = Product.objects.get(id=pk)
#     #except Product.DoesNotExist:
#       #  print("No product found")
#        # raise Http404("Product doesn,t exist")
#     #except:
#         #print("huh")
#     instance = Product.objects.get_by_id(pk)
#     if instance is None:
#         raise Http404("Product doesn,t exist")
#     # print(instance)
#     # qs = Product.objects.filter(id=pk)
#     #if qs.exists() and qs.count() == 1: # len(qs)
#      #   instance = qs.first()
#     #else:
#      #   raise Http404("Product does not exists")
#     context = {'object' : instance }
#     return render(request, "products/detail.html" , context)
