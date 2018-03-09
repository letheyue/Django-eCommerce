from django.shortcuts import render

import stripe
stripe.api_key = "sk_test_Vsa3Q1q8k6YRX2J600IWWzjl"


STRIPE_PUB_KEY = 'pk_test_zrQeiyEJDcWZZUouU084QErp'


def payment_method_view(request):
    if request.method == "POST":
        print(request.POST)
    return render(request, 'billing/payment-method.html', {"publish_key": STRIPE_PUB_KEY})
