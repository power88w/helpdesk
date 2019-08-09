from django.shortcuts import render
from django.http import HttpResponse
from services.models import BlogPost as bbp



def home_page(request):
    bc = bbp.objects.all().count()
    if bc>3:
        blogs = bbp.objects.order_by('votes')[bc-3::-1]
    else:
        blogs = bbp.objects.order_by('votes')[::-1]
    context = {'rows_services':blogs,}
    return render(request,"helpdesk.html",context)