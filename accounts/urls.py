from django.urls import path
from .views import *


app_name = 'accounts'

urlpatterns = [
    path('login', login_user, name="login"),
    path('signup', signup, name="signup"),
    path('email-confirmation/<str:token>', signup, name="email-confirmation"),
]
