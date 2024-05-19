import json
from config.settings.base import PAYMENT_OPTIONS
from django.shortcuts import render
from requests import api
import pprint
import iyzipay
from django.views.generic import TemplateView
from django.contrib import messages


class PaymentPage(TemplateView):
    template_name = 'payment.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
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
            'ip': '85.34.78.112',
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

        basket_items = [
            {
                'id': 'BI101',
                'name': 'Binocular',
                'category1': 'Collectibles',
                'category2': 'Accessories',
                'itemType': 'PHYSICAL',
                'price': '0.3'
            },
            {
                'id': 'BI102',
                'name': 'Game code',
                'category1': 'Game',
                'category2': 'Online Game Items',
                'itemType': 'VIRTUAL',
                'price': '0.5'
            },
            {
                'id': 'BI103',
                'name': 'Usb',
                'category1': 'Electronics',
                'category2': 'Usb / Cable',
                'itemType': 'PHYSICAL',
                'price': '0.2'
            }
        ]

        request = {
            'locale': 'tr',
            'conversationId': '123456789',
            'price': '1',
            'paidPrice': '1.2',
            'currency': 'TRY',
            'basketId': 'B67832',
            'paymentGroup': 'PRODUCT',
            "callbackUrl": "http://localhost:8000/api/result",
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
        print(type(json_content))
        print(json_content["checkoutFormContent"])
        print("************************")
        print(json_content["token"])
        print("************************")
        context['form'] = json_content["checkoutFormContent"]
        return context


class CheckoutView(TemplateView):
    template_name = 'checkout.html'


class PaymentStatusView(TemplateView):
    template_name = 'status.html'

    def get(self, request, *args, **kwargs):
        status = request.GET.get('status', None)
        match status:
            case 'success':
                messages.add_message(request, messages.SUCCESS, "payment successful.".title())
            case 'fail':
                messages.add_message(request, messages.ERROR, "payment could not be received".capitalize())
            case _:
                messages.add_message(request, messages.ERROR, "unknown error while receiving payment".capitalize())
        return super().get(request, *args, **kwargs)


