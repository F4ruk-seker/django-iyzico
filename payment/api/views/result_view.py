import json
import pprint
import iyzipay
from rest_framework.views import APIView
from rest_framework.response import Response
from config.settings.base import PAYMENT_OPTIONS
from payment.models import PaymentModel
from django.shortcuts import get_object_or_404


class ResultView(APIView):
    def post(self, request, *args, **kwargs):
        context = dict()

        if token := request.data.get('token', None):
            payment_model: PaymentModel = get_object_or_404(PaymentModel, token=token)
            print(payment_model)
            request = {
                'locale': payment_model.locale,
                'conversationId': payment_model.conversationId,
                'token': token
            }
            checkout_form_result = iyzipay.CheckoutForm().retrieve(request, PAYMENT_OPTIONS)
            print("************************")
            print(type(checkout_form_result))
            result = checkout_form_result.read().decode('utf-8')
            print(result)
            pyload = json.loads(result)

            pprint.pprint(pyload)
            print("************************")
            # print(sozlukToken[0])  # Form oluşturulduğunda
            print("************************")
            print("************************")
            sonuc = json.loads(result, object_pairs_hook=list)
            # print(sonuc[0][1])  # İşlem sonuç Durumu dönüyor
            # print(sonuc[5][1])   # Test ödeme tutarı
            print("************************")
            for i in sonuc:
                print(i)
            print("************************")
            print(token)
            print("************************")
            # paymentStatus
        return Response({}, status=200)

