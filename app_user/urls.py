from django.urls import path
from .views import index, AuthGoogle, changeUsername, user_signup, user_login, user_logout

urlpatterns = [
    path("", index, name="index"),
    path("signup", user_signup, name="signup-user"),
    path("auth-receiver", AuthGoogle.as_view(), name='auth-receiver'),
    path("change-username", changeUsername, name="change_username"),
    path("login", user_login, name="login"),
    path("logout", user_logout, name="logout")
]