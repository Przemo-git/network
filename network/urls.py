from django.contrib.admin import views
from django.urls import path

from . import views

urlpatterns = [
    path('', views.index, name='index'),
    path('profile/<str:username>',views.profile, name='profile'),
    path('login', views.login_view, name='login'),
    path('logout', views.logout_view, name='logout'),
    path('register', views.register, name="register"),
    path('likes/<int:ID>', views.likes, name='likes'),path("edit/<int:post_id>", views.edit_page, name="edit"),
    path("edit/update/<int:post_id>/<str:content>", views.updated, name="update"),
    path("like/<int:ID>/<str:user>", views.likes, name="like"),
    path("profile/like/<int:ID>/<str:user>", views.likes, name="like"),
    path("following/<str:user>",views.following_page, name="following"),
    path("profile/follow/<str:user>/<str:currentuser>", views.follow_user, name="follow"),
    path("profile/unfollow/<str:user>/<str:currentuser>", views.unfollow_user, name="unfollow")
    ]