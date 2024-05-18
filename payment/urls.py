from django.urls import path, include
from payment.views import PaymentPage, CheckoutView


urlpatterns: list[path] = [
    path('payment', PaymentPage.as_view()),
    path('checkout', CheckoutView.as_view()),
]

