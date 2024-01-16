from django.urls import path
from . import views


urlpatterns = [
    path('', views.index, name='index'),
    path('posts/', views.posts, name='posts'),
    path('posts/<slug:slug>/', views.post_detail, name='post_detail_url'),
    path('category/<slug:slug>/', views.category_detail, name='category_detail_url'),
    path('login/', views.login_site, name = 'login_url'),
    path('logout/', views.logout_site, name = 'logout_url'),
    path('register/', views.register, name = 'register'),
]