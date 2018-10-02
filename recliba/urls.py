from django.conf import settings
from django.conf.urls.static import static
from django.conf.urls import url, include
from django.contrib import admin
from .views import home_page,about_page,contact_page
from accounts.views import login_page,RegisterView,logout_page,ActivateAccount
from django.views.generic import TemplateView


urlpatterns = [
    url(r'^login/$',login_page, name='login'),
    url(r'^logout/$',logout_page,name='logout'),
    url(r'^register/$',RegisterView.as_view(),name='register'),
    url(r'^activate-account/(?P<pk>\d+)/$', ActivateAccount.as_view(), name='activate-account'),
    # url(r'^$',home_page, name='home'),
    url(r'^about/$', about_page, name='about'),
    url(r'^contact/$', contact_page,name='contact'),
    url(r'^admin/', admin.site.urls),
    url(r'^bootstrap/', TemplateView.as_view(template_name='bootstrap/example.html')),
    url(r'^', include("books.urls", namespace="books")),
    url(r'^student-register/',include("register.urls", namespace="student-register")),
    # url(r'^cart/', include("carts.urls", namespace="cart")),
    url(r'^search/', include("search.urls", namespace="search")),
    url(r'^profile/', include("profile.urls", namespace="profile")),

]

if settings.DEBUG:
    urlpatterns = urlpatterns + static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
    urlpatterns = urlpatterns + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)







#url(r'^products/$', ProductListView.as_view()),
    #url(r'^products-fbv/$', product_list_view),
    #url(r'^products/(?P<pk>\d+)/$',ProductDetailView.as_view()),
    #url(r'^products/(?P<slug>[\w-]+)/$', ProductDetailSlugView.as_view()),
    #url(r'^products-fbv/(?P<pk>\d+)/$',product_detail_view),
    #url(r'^featured/$', ProductFeaturedListView.as_view()),
    #url(r'^featured/(?P<pk>\d+)/$', ProductFeaturedDetailView.as_view()),
