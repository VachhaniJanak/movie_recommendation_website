from django.urls import path

from .views import RegisterView, LoginView, PasswordResetView, EmailVerificationView

urlpatterns = [
	path('', LoginView.as_view(), name='login'),
	path('login', LoginView.as_view(), name='login'),
	path('registration', RegisterView.as_view(), name='registration'),
	path('verify-email', EmailVerificationView.as_view(), name='verify-email'),
	path('forgot-password', PasswordResetView.as_view(), name='forgot-password'),
]
