from django.urls import path
from .views import *

urlpatterns = [
    path("", index, name="index"),
    path("signup", user_signup, name="signup-user"),
    path("auth-receiver", AuthGoogle.as_view(), name='auth-receiver'),
    path("change-username", changeUsername, name="change-username"),
    path("login", user_login, name="login"),
    path("logout", user_logout, name="logout"),
    path("settings", user_settings, name="settings"),
    path("tools", user_tools, name="tools"),
    path("add_friend/<int:userID>/", add_friend, name="add-friend"),
    path("remove_friend/<int:userID>/", remove_friend, name="remove-friend"),
]