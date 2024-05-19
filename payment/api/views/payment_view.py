import json

from django.shortcuts import render
from requests import api
import pprint
import iyzipay
from django.shortcuts import reverse
from rest_framework.views import APIView
from rest_framework.response import Response
from config.settings.base import PAYMENT_OPTIONS
from payment.api.serializers import ProductSerializer
from products.models import BasketModel
from payment.models import PaymentModel


def get_client_ip(request):
    x_forwarded_for = request.META.get('HTTP_X_FORWARDED_FOR')
    return x_forwarded_for.split(',')[0] if x_forwarded_for else request.META.get('REMOTE_ADDR')


class Payment(APIView):
    def get(self, request, *args, **kwargs):
        # request_host = request.get_host()
        # path = reverse('api:payment:result')
        # callback_url = f'{request_host}{path}'
        callback_url = f'{request.scheme}://{request.get_host()}{reverse('api:payment:result')}'
        payment_model: PaymentModel = PaymentModel.objects.create()
        basket_model: BasketModel = BasketModel.objects.first()
        print(basket_model.get_products())
        basket_items = ProductSerializer(basket_model.get_products(), many=True).data
        pprint.pprint(basket_items[0])
        print(basket_model.get_total_price())
        buyer = {
            'id': 'BY789',
            'name': 'John',
            'surname': 'Doe',
            'gsmNumber': '+905350000000',
            'email': 'email@email.com',
            'identityNumber': '74300864791',
            'lastLoginDate': '2015-10-05 12:43:35',
            'registrationDate': '2013-04-21 15:12:09',
            'registrationAddress': 'Nidakule Göztepe, Merdivenköy Mah. Bora Sok. No:1',
            'ip': get_client_ip(request),
            'city': 'Istanbul',
            'country': 'Turkey',
            'zipCode': '34732'
        }

        address = {
            'contactName': 'Jane Doe',
            'city': 'Istanbul',
            'country': 'Turkey',
            'address': 'Nidakule Göztepe, Merdivenköy Mah. Bora Sok. No:1',
            'zipCode': '34732'
        }

        request = {
            'locale': 'tr',
            'conversationId': payment_model.conversationId,
            'price': basket_model.get_total_price(),
            'paidPrice': basket_model.get_total_price(),
            'currency': 'TRY',
            'basketId': 'B67832',
            'paymentGroup': 'PRODUCT',
            "callbackUrl": callback_url,
            "enabledInstallments": ['2', '3', '6', '9'],
            'buyer': buyer,
            'shippingAddress': address,
            'billingAddress': address,
            'basketItems': basket_items,
            # 'debitCardAllowed': True
        }

        checkout_form_initialize = iyzipay.CheckoutFormInitialize().create(request, PAYMENT_OPTIONS)

        # print(checkout_form_initialize.read().decode('utf-8'))
        page = checkout_form_initialize
        header = {'Content-Type': 'application/json'}
        content = checkout_form_initialize.read().decode('utf-8')
        json_content = json.loads(content)
        print(json_content)
        pprint.pprint(json_content)
        payment_model.token = json_content["token"]
        payment_model.save()
        print(type(json_content))
        print(json_content["checkoutFormContent"])
        print("************************")
        print(json_content["token"])
        print("************************")
        form = json_content["checkoutFormContent"]
        # form.replace('<script>', '')
        # form.replace('</script>', '')
        return Response({'message': 'ok :)', 'context': json_content["checkoutFormContent"]}, status=201)


