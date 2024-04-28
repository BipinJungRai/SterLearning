from .forms import UserCreationWithEmailForm, GoogleUserChangeUsername, LoginForm
from django.views.generic import CreateView
from .models import ExtendedUser, FriendRequest
from django.urls import reverse_lazy
import os
from django.shortcuts import render, redirect
from google.oauth2 import id_token
from google.auth.transport import requests
from django.http import HttpResponse, HttpRequest
from django.utils.decorators import method_decorator
from django.views.decorators.csrf import csrf_exempt
from rest_framework.views import APIView
import uuid
from django.core.exceptions import ObjectDoesNotExist
from django.contrib.auth import login, authenticate, logout
from django.contrib.auth.decorators import login_required

# Create your views here.
def index(request):
    userList = ExtendedUser.objects.all()
    requestList = FriendRequest.objects.all()
    return render(request, 'index.html', {'users': userList, 'requestList': requestList})

def user_signup(request):
    if request.method == 'POST':
        form = UserCreationWithEmailForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('login')
    else:
        form = UserCreationWithEmailForm()
    return render(request, 'register.html', {'form': form})

#https://www.photondesigner.com/articles/google-sign-in
@method_decorator(csrf_exempt, name='dispatch')
class AuthGoogle(APIView):
    """
    Google calls this URL after the user has signed in with their Google account.
    """
    def post(self, request, *args, **kwargs):
        try:
            user_data = self.get_google_user_data(request)
        except ValueError:
            return HttpResponse("Invalid Google token", status=403)

        user_email = user_data["email"]
        try:
            user = ExtendedUser.objects.get(
                email=user_email
            )
        except ObjectDoesNotExist:
            user = ExtendedUser.objects.create(
                username=user_email,
                email=user_email,
                first_name=user_data["given_name"],
                )
            login(request, user)
            return redirect('change-username')

        if user is not None:
            login(request, user)
        # Add any other logic, such as setting a http only auth cookie as needed here.
        return redirect('index')

    @staticmethod
    def get_google_user_data(request: HttpRequest):
        token = request.POST['credential']
        return id_token.verify_oauth2_token(
            token, requests.Request(), os.environ['GOOGLE_OAUTH_CLIENT_ID']
        )

@login_required
def changeUsername(request):
    if request.method == "POST":
        form = GoogleUserChangeUsername(request.POST, instance=request.user)
        if form.is_valid():
            form.save()
            return redirect('index')
    else:
        form = GoogleUserChangeUsername(instance=request.user)
    return render(request, "change_username.html", {"form": form})

def user_login(request):
    if request.method == 'POST':
        form = LoginForm(request.POST)
        if form.is_valid():
            username = form.cleaned_data['username']
            password = form.cleaned_data['password']
            user = authenticate(request, username=username, password=password)
            if user:
                login(request, user)    
                return redirect('index')
    else:
        form = LoginForm()
    return render(request, 'login.html', {'form': form})

# logout page
def user_logout(request):
    logout(request)
    return redirect('login')

def user_settings(request):
    return render(request, 'settings.html')

def user_tools(request):
    return render(request, 'tools.html')

@login_required
def send_friend_request(request, userID):
    from_user = request.user
    to_user = ExtendedUser.objects.get(id=userID)
    friend_request, created = FriendRequest.objects.get_or_create(
        from_user=from_user, to_user=to_user
    )
    if created:
        return HttpResponse('friend request sent')
    else:
        return HttpResponse('request was already sent')

@login_required
def accept_friend_request(request, requestID):
    friend_request = FriendRequest.objects.get(id=requestID)
    if friend_request.to_user == request.user:
        friend_request.to_user.friends.add(friend_request.from_user)
        friend_request.from_user.friends.add(friend_request.to_user)
        friend_request.delete()
        return HttpResponse('request accepted')
    else:
        return HttpResponse('request not accepted')