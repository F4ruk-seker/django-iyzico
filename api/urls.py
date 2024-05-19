from django.urls import path, include


app_name: str = "api"

urlpatterns: list[path] = [
    path('', include('payment.api.urls'), name='payment')
]

