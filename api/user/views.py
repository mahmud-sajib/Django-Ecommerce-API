from rest_framework import viewsets
from rest_framework.permissions import AllowAny
from .serializers import UserSerializer
from .models import CustomUser
from django.http import JsonResponse
from django.contrib.auth import get_user_model
from django.views.decorators.csrf import csrf_exempt
from django.contrib.auth import login, logout

import random
import re

# Create your views here.

# Generate session view
def generate_session_token(length=10):
    char_list = [chr(i) for i in range(97, 123)]
    int_list = [str(i) for i in range(10)]
    
    # Create a unique token
    return ''.join(random.SystemRandom().choice(char_list + int_list) for _ in range(length))

# Login view
@csrf_exempt # Allow CSRF
def signin(request):
    if not request.method == 'POST':
        return JsonResponse({'error':"You are not eligible for login"})

    username = request.POST['email']
    password = request.POST['password']

    if not re.match("^[\w\.\+\-]+\@[\w]+\.[a-z]{2,3}$", username):
        return JsonResponse({'error':"Enter a valid Email"})

    if len(password) < 6:
        return JsonResponse({'error':"Password must be 6 character long"})

    UserModel = get_user_model()

    try:
        user = UserModel.objects.get(email=username)

        if user.check_password(password):
            usr_dict = UserModel.objects.filter(email=username).values().first()
            usr_dict.pop('password') # Extract Password so it doesn't travel to frontend

            # If session_token is not 0 it's already running (user is logged in)
            if user.session_token != '0':
                # If user is not logged in we set session_token to 0
                user.session_token = '0'
                # Save session
                user.save()
                return JsonResponse({'error':"Previous session exists"})

            # Generate session token
            token = generate_session_token()
            user.session_token = token
            # Save session
            user.save()
            # Log user in
            login (request, user)
            # Return session token along with user attributes
            return JsonResponse({'token': token, 'user': usr_dict})
        else:
            return JsonResponse({'token': 'Invalid password'})

    except UserModel.DoesNotExist:
        return JsonResponse({'error': 'Invalid Email'})

# Logout view
def signout(request, id):

    UserModel = get_user_model()

    try:
        user = UserModel.objects.get(pk=id)
        user.session_token = "0"
        user.save()
        logout(request)
    
    except UserModel.DoesNotExist:
        return JsonResponse({'error': 'Invalid User ID'})

    return JsonResponse({'success': 'Logout successful'})

# User Permission View
class UserViewSet(viewsets.ModelViewSet):
    permission_classes_by_action = {'create' : [AllowAny]}
    queryset = CustomUser.objects.all().order_by('id')
    serializer_class = UserSerializer

    def get_permissions(self):
        try:
            # Return permission_classes depending on `action` 
            return [permission() for permission in self.permission_classes_by_action[self.action]]

        except KeyError:
            # If action is not set return default permission_classes
            return [permission() for permission in self.permission_classes]
        







