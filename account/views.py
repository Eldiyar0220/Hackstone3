from django.contrib.auth import get_user_model
from django.shortcuts import render, get_object_or_404

# Create your views here.
from rest_framework import status, generics, permissions
from rest_framework.authtoken.models import Token
from rest_framework.authtoken.views import ObtainAuthToken
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView


from .serializers import *
#TODO: register view
class RegisterView(APIView):
    def post(self,request):
        data = request.data
        serializer = RegisterSerializer(data=data)
        if serializer.is_valid(raise_exception=True):
            serializer.save()
            return Response('Successfully sighed up!', status=status.HTTP_201_CREATED)
#TODO: activate view

class ActivateView(APIView):
    def get(self, request, activation_code):
        User = get_user_model()
        user = get_object_or_404(User, activation_code=activation_code)
        # user.is_active = True
        user.activation_code = ''
        user.save()
        return Response("Your account successfully activate!", status=status.HTTP_200_OK)


#TODO: login view
class LoginView(ObtainAuthToken):
    serializer_class = LoginSerializer

#TODO: logout view

class LogoutView(APIView):
    permission_classes = [IsAuthenticated,]

    def post(self, request):
        user = request.user
        Token.objects.filter(user=user).delete()
        return Response('Successfully logged out', status=status.HTTP_200_OK)

#reset password
class ResetPasswordView(APIView):
    def post(self, request):
        serializer = ForgotPasswordSerializer(data=request.data)
        if serializer.is_valid(raise_exception=True):
            serializer.send_reset_email()
            return Response('вам отправлен код для смены пароля', status=status.HTTP_200_OK)

class ResetPasswordComplete(APIView):
    def post(self, request):
        serializer = CreateNewPasswordSerializer(data=request.data)
        if serializer.is_valid(raise_exception=True):
            serializer.create_pass()
            return Response('вы успешно сменили пароль........!123', status=status.HTTP_200_OK)


# 1111
class ChangePasswordView(APIView):
    #чтоб пользователь был залогиненным
    permission_classes = [IsAuthenticated]
    def post(self,request):
        serializer = ChangePasswordSerializer(data=request.data, context={'request': request})
        if serializer.is_valid(raise_exception=True):
            serializer.set_new_password()
            return Response('проль успешно обнавлен..!', status=status.HTTP_200_OK)


#profile

