from django.urls import path
from .views import (Blog_Post_Detail_Page,
                   Edit_Comment,
                   Blog_Post_List_Page,
                   #Blog_Post_Delete_Page,
                   #Blog_Post_Edit_Page,
                   Create_Comment,
                   Blog_Like,
                   Donate)
urlpatterns = [
        path("",Blog_Post_List_Page),
        path("donate/",Donate),
        path("<str:post_id>/",Blog_Post_Detail_Page),
        path("<str:post_id>/like/",Blog_Like),
        path("<str:post_id>/add/",Create_Comment),
        path("comment/<str:comment_id>/",Edit_Comment),
        #path("<str:blog_id>/delete/",Blog_Post_Delete_Page),
        #path("<str:blog_id>/edit/",Blog_Post_Edit_Page),
]
