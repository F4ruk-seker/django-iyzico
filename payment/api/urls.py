from django.urls import path, include
from payment.api.views import Payment, ResultView


app_name: str = 'payment'

urlpatterns: list[path] = [
    path('payment', Payment.as_view(), name='pay'),
    path('result', ResultView.as_view(), name='result'),
]

