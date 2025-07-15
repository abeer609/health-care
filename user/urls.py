from django.urls import path

from user import views

urlpatterns = [
    path("login/", views.signin, name="login"),
    path("register", views.register, name="register"),
]
