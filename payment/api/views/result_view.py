import json
import pprint
import iyzipay
from django.http import HttpResponseRedirect
from rest_framework.views import APIView
from django.shortcuts import reverse, resolve_url
from django.views.generic import RedirectView
from rest_framework.response import Response
from config.settings.base import PAYMENT_OPTIONS
from payment.models import PaymentModel
from django.shortcuts import get_object_or_404

# RedirectView


class ResultView(APIView):
    def post(self, request, *args, **kwargs):
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
            '''
            paymentStatus : could be SUCCESS, FAILURE, INIT_THREEDS, CALLBACK_THREEDS, BKM_POS_SELECTED, CALLBACK_PECCO
            '''
            pprint.pprint(pyload)

            if payment_status := pyload.get('paymentStatus', None):
                result_path = reverse('payment:status')
                match payment_status:
                    case 'SUCCESS':
                        return HttpResponseRedirect(f'{result_path}?status=success')
                    case _:
                        return HttpResponseRedirect(f'{result_path}?status=fail')

