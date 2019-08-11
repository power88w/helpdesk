from django.urls import path
from .views import (Cart_Fill,Item_Up,Item_Down,Item_Delete,Checkout,Complete,payment)

urlpatterns = [
    path("",Cart_Fill),
    path("<str:post_id>/add_vote/",Item_Up),
    path("<str:post_id>/sub_vote/",Item_Down),
    path("<str:post_id>/remove/",Item_Delete),
    path("checkout/",Checkout),
    path("payment/",payment),
    path("complete/",Complete),
]
