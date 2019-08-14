
from django.contrib import admin
from django.urls import path, include
from .views import home_page,charts
from django.conf import settings
from services.views import Blog_Post_Create_Page
from hardware import views
from django.conf.urls.static import static

urlpatterns = [
    path("",home_page),
    path("services-new/", Blog_Post_Create_Page),
    path('services/', include('services.urls')),
    path('admin/', admin.site.urls),
    path('login/', include('login.urls')),
    path('signup/', include('Signup.urls')),
    path('hardware/', include('hardware.urls')),
    path("hardware-new/",views.Blog_Post_Create_Page),
    path('cart/',include('cart.urls')),
    path('charts/',charts),
]

if settings.DEBUG:
    urlpatterns += static(settings.STATIC_URL, document_root=settings.STATICFILES_DIRS)
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)