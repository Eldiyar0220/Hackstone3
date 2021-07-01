from django.urls import path
from . import views
from .views import *

urlpatterns = [
    path('register/', RegisterView.as_view()),
    path('activate/<str:activation_code>/', ActivateView.as_view()),
    path('login/', LoginView.as_view()),
    path('logout/', LogoutView.as_view()),
    #reset
    #cod
    path('reset_password/', views.ResetPasswordView.as_view()),
    path('reset_password_completes/', views.ResetPasswordComplete.as_view()),
    #reset_password
    path('reset_password_complete/', views.ChangePasswordView.as_view()),


]