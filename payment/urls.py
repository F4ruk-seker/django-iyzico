from django.urls import path, include
from payment.views import PaymentPage, CheckoutView, PaymentStatusView


app_name: str = 'payment'


urlpatterns: list[path] = [
    path('payment', PaymentPage.as_view()),
    path('checkout', CheckoutView.as_view()),
    path('status', PaymentStatusView.as_view(), name='status'),
]


