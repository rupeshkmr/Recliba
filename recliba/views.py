from django.http import HttpResponse
from django.shortcuts import render,redirect
from .forms import ContactForm
from django.urls import reverse_lazy,reverse


def home_page(request):
    # print(request.session.get("first_name","Unknown")) # getter
    context={
        "title":"Hello World",
        "content":"Welcome to homepage",
        #"premium_content":"YEAHHHH"
    }#render:Renders html pages requires 3 parameters request,template,context(dictionary)
    if request.user.is_authenticated():
        context["premium_content"]="YEAHHH"

    if request.user.is_superuser:
        context["superuser"]="Welcome Sir"
    return render(request, "home_page.html",context)
def about_page(request):
    context = {
        "title": "Hello World",
        "content": "Welcome to Aboutpage"
    }
    return render(request, "home_page.html",context)
def contact_page(request):
    contact_form=ContactForm(request.POST or None)#checks tha there is only post request
    context = {
        "title": "Contact",
        "content": "Welcome to Contact Page",
        "form": contact_form
    }
    #if contact_form.is_valid():
        #print(contact_form.cleaned_data)
    '''if request.method == 'POST':#checks whether the request is post or not
        #print(request.POST)
        print(request.POST.get('fullname'))#get fullname atribute from the request
        print(request.POST.get('email'))
        print(request.POST.get('content'))'''
    return render(request, "contact/view.html",context)


def home_page_old(request):
    html_="""<!doctype html>
<html lang="en">
  <head>
    <!-- Required meta tags -->
    <meta charset="utf-8">
    <meta name="viewport" content="width=device-width, initial-scale=1, shrink-to-fit=no">

    <!-- Bootstrap CSS -->
    <link rel="stylesheet" href="https://stackpath.bootstrapcdn.com/bootstrap/4.1.1/css/bootstrap.min.css" integrity="sha384-WskhaSGFgHYWDcbwN70/dfYBj47jz9qbsMId/iRN3ewGhXQFZCSftd1LZCfmhktB" crossorigin="anonymous">
    
    <title>Hello, world!</title>
  <body><div class='text-center'>
    <h1>Hello, world!</h1></div>
  </head>

    <!-- Optional JavaScript -->
    <!-- jQuery first, then Popper.js, then Bootstrap JS -->
    <script src="https://code.jquery.com/jquery-3.3.1.slim.min.js" integrity="sha384-q8i/X+965DzO0rT7abK41JStQIAqVgRVzpbzo5smXKp4YfRvH+8abtTE1Pi6jizo" crossorigin="anonymous"></script>
    <script src="https://cdnjs.cloudflare.com/ajax/libs/popper.js/1.14.3/umd/popper.min.js" integrity="sha384-ZMP7rVo3mIykV+2+9J3UJ46jBk0WLaUAdn689aCwoqbBJiSnjAK/l8WvCWPIPm49" crossorigin="anonymous"></script>
    <script src="https://stackpath.bootstrapcdn.com/bootstrap/4.1.1/js/bootstrap.min.js" integrity="sha384-smHYKdLADwkXOn1EmN1qk/HfnUcbVRZyYmZ4qpPea6sjB/pTJ0euyQp0Mk8ck+5T" crossorigin="anonymous"></script>
  </body>
</html>"""
    return HttpResponse(html_)
