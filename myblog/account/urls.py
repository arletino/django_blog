from django.urls import path
from . import views
from django.contrib.auth import views as auth_views


urlpatterns = [
    # базовый url входа
    # path(
    #     'login/',
    #     views.user_login,
    #     name='login'
    # ),
    # url из встроенной auth views
    path(
        'login/',
        auth_views.LoginView.as_view(), 
        name='login'
    ),
    path(
        'logout/', 
        auth_views.LogoutView.as_view(),
        name='logout'
    ),
    path(
        '', 
        views.dashboard, 
        name='dashboard'
    ),
]