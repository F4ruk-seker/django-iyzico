from django.urls import path, include


urlpatterns: list[path] = [
    path('', include('payment.api.urls'))
]

