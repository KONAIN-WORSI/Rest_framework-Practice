from django.urls import path
from accounts import views

urlpatterns = [
    path('register/', views.RegisterView.as_view()),
    path('verify-otp/', views.verify_otp.as_view())
]