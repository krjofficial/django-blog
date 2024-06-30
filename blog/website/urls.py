from django.urls import path
from . import views

urlpatterns = [
    path('', views.home, name='home'),
    # path('login/', views.login_user, name='login'),
    path('logout', views.logout_user, name='logout'),
    path('register', views.register_user, name='register'),
    path('blog/<int:pk>', views.user_blog, name='blog'),
    # <int:pk> is like params in nodejs 
    path('delete_blog/<int:pk>', views.delete_blog, name='delete_blog'),
    path('add_blog' , views.add_blog, name='add_blog'),
    path('update_blog/<int:pk>', views.update_blog, name='update_blog'),
    path('author/<int:pk>', views.view_profile, name='author'),
    path('edit_profile/<int:pk>', views.edit_profile, name='edit_profile')
]
