from django.shortcuts import render,redirect
from django.contrib.auth import authenticate,logout
from django.contrib.auth import login as auth_login
# Create your views here.




def userloginview(request):
    if request.POST:
        username = request.POST.get('username')
        password = request.POST.get('password')
        user = authenticate(username=username,password=password)
        error = ""
        if user:
            auth_login(request,user)
            return redirect("/")
        else:
            error = "Username or password incorrect"
        return render(request,"registration/login.html",{'username':username,"error":error})
    template_name = "registration/login.html"
    return render(request, template_name)


def userlogoutview(request):
    if request.user.is_authenticated:
        logout(request)
        return redirect("/")

