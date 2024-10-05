from django.urls import path
from rest_framework_simplejwt.views import TokenRefreshView
from password_manager.views.auth.login import LoginView
from password_manager.views.auth.register import RegisterView

urlpatterns = [
    path('register/', RegisterView.as_view(), name='register'),
    path('login/', LoginView.as_view(), name='login'),
    path('token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
]
