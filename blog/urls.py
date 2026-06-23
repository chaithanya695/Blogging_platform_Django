# creating urls.py file manually in blog(as it doesn't exists in app folders)
from django.urls import path
from.views import post_list,post_detail,create_post,edit_post
from .views import delete_post,my_posts,add_comment,like_post,dashboard

# URL Namespacing.
app_name = 'blog'

urlpatterns = [
    path("",post_list,name="post_list"),
    path("post/<int:post_id>/",post_detail,name="post_detail"),

    # CRUD
    path('create/',create_post,name='create_post'),
    path('edit/<int:post_id>/', edit_post, name='edit_post'),
    path('delete/<int:post_id>/', delete_post, name='delete_post'),
    path("my-posts/", my_posts, name="my_posts"),

    # Interations
    path('comment/<int:post_id>/', add_comment, name='add_comment'),
    path('like/<int:post_id>/',like_post,name='like_post'),
    path('dashboard/',dashboard,name='dashboard'),


]
