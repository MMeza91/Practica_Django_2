from django.urls import path
from .views import registro
from django.contrib.auth import views as authview

urlpatterns = [
    path("registro/",registro, name="registro"),
    path("login/", authview.LoginView.as_view(template_name="usuarios/login.html") , name="login"),
    path("logout/", authview.LogoutView.as_view() , name="logout")
]
