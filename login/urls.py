from django.urls import path
from .views import userloginview,userlogoutview



urlpatterns = [ 
    path("accounts/login/",userloginview),
    path("accounts/logout/",userlogoutview),
]


