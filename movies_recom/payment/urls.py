from django.urls import path
from .views import PaymentView, handlerequest

urlpatterns = [
	path('<str:message>', PaymentView.as_view(), name='payment_page'),
    path('handlerequest/', handlerequest, name='handlerequest'),
]
