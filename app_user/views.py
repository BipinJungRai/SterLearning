from .forms import UserCreationWithEmailForm, GoogleUserChangeUsername, LoginForm
from django.views.generic import CreateView
from .models import ExtendedUser, Avatar, Decoration
from django.urls import reverse_lazy
import os
from django.shortcuts import render, redirect, get_object_or_404
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
from django.contrib import messages

# Create your views here.
def index(request):
    if request.user.is_authenticated:
        return redirect('pathways-home')
    else:
        return redirect('login')

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

def shop(request):
    if request.user.is_authenticated:
        if request.method == 'POST':
            user = request.user
            requestType = request.POST.get('type')
            requestId = request.POST.get('id')

            if requestType == 'buy_avatar':
                avatar = get_object_or_404(Avatar, id = requestId)

                if user.points() >= avatar.cost:
                    user.spentPoints += avatar.cost
                    user.inventoryAvatar.add(avatar)
                    user.save()

                    messages.add_message(request, messages.SUCCESS, 'You have successfully ' +
                                          'purchased ' + avatar.name + ' for ' + str(avatar.cost) + 
                                          ' points!')
                else:
                    messages.add_message(request, messages.ERROR, 'You do not have enough' +
                                           ' points for this item! Complete more quizzes to ' +
                                           'earn more points.')
            elif requestType == 'buy_decoration':
                decoration = get_object_or_404(Decoration, id = requestId)
                
                if user.points() >= decoration.cost:
                    user.spentPoints += decoration.cost
                    user.inventoryDecoration.add(decoration)
                    user.save()

                    messages.add_message(request, messages.SUCCESS, 'You have successfully ' +
                                          'purchased ' + decoration.name + ' for ' + str(decoration.cost) + 
                                          ' points!')
                else:
                    messages.add_message(request, messages.ERROR, 'You do not have enough' +
                                           ' points for this item! Complete more quizzes to ' +
                                           'earn more points.')
            elif requestType == 'equip_avatar':
                avatar = get_object_or_404(Avatar, id = requestId)

                if user.inventoryAvatar.all().filter(id = requestId).count() == 1:
                    user.avatar = avatar
                    user.save()

                    messages.add_message(request, messages.SUCCESS, 'You have successfully ' +
                                          'equipped ' + avatar.name)
                else:
                    messages.add_message(request, messages.ERROR, 'You are unable to equip this.')
            elif requestType == 'equip_decoration':
                decoration = get_object_or_404(Decoration, id = requestId)

                if user.inventoryDecoration.all().filter(id = requestId).count() == 1:
                    user.decoration = decoration
                    user.save()

                    messages.add_message(request, messages.SUCCESS, 'You have successfully ' +
                                          'equipped ' + decoration.name)
                else:
                    messages.add_message(request, messages.ERROR, 'You are unable to equip this.')

        context = {}
        context['points'] = request.user.points
        context['equipped_avatar'] = request.user.avatar
        context['equipped_decoration'] = request.user.decoration
        context['owned_avatars'] = request.user.inventoryAvatar.all()
        context['owned_decorations'] = request.user.inventoryDecoration.all()
        context['avatars'] = Avatar.objects.exclude(id__in = context['owned_avatars'])
        context['decorations'] = Decoration.objects.exclude(id__in = context['owned_decorations'])

        return render(request, 'shop.html', context)
    else:
        messages.add_message(request, messages.ERROR, 'You need to be logged in')
        return redirect('login')
