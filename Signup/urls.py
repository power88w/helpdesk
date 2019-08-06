from django.conf.urls import url
from . import views
from django.urls import path,include
urlpatterns = [
    path('', views.signup),
    url(r'^activate/(?P<uidb64>[0-9A-Za-z_\-]+)/(?P<token>[0-9A-Za-z]{1,13}-[0-9A-Za-z]{1,20})/$',
        views.activate, name='activate'),
]
