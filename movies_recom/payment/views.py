from django.shortcuts import render
from django.views import View
from django.views.decorators.csrf import csrf_exempt
from django.http import  HttpResponseRedirect
from django.urls import reverse
from .checksum import generate_checksum, verify_checksum
from login_regis.models import UserInfo, Payment
from datetime import datetime



MERCHANT_KEY = 'kbzk1DSbJiV_O3p5'
amount = 2

# Create your views here.
class PaymentView(View):

    def __init__(self):
        super().__init__()
        self.params = {
            'MID':'WorldP64425807474247',
            # 'ORDER_ID':'dddgfgfeeed',
            'TXN_AMOUNT': str(amount),
            # 'CUST_ID':'acfff@paytm.com',
            'INDUSTRY_TYPE_ID':'Retail',
            'WEBSITE':'worldpressplg',
            'CHANNEL_ID':'WEB',
            # "CALLBACK_URL": request.build_absolute_uri(reverse('handlerequest')),
        }
        self.user : UserInfo

    def get(self, request, message=''):
        self.user = UserInfo.objects.filter(id=request.session.get('id')).first()
        if self.user:
            self.params['ORDER_ID'] = str(self.user.id)
            self.params['CUST_ID'] = self.user.email
        return render(request, 'payment.html', {'params':self.params, 'message':message})
    
    def post(self, request, message=''):
        self.user = UserInfo.objects.filter(id=request.session.get('id')).first()
        if self.user:
            self.params['ORDER_ID'] = str(self.user.id)
            self.params['CUST_ID'] = self.user.email
            self.params["CALLBACK_URL"] = request.build_absolute_uri(reverse('handlerequest'))
            self.params['CHECKSUMHASH'] = generate_checksum(self.params, MERCHANT_KEY)
        return render(request, 'paytm.html', {'params':self.params})
    
@csrf_exempt
def handlerequest(request):
    form = request.POST
    response_dict = {}
    for i in form.keys():
        response_dict[i] = form[i]
        if i == 'CHECKSUMHASH':
            checksum = form[i]
    try:
        if verify_checksum(response_dict, MERCHANT_KEY, checksum):
            user = UserInfo.objects.get(id=int(response_dict['ORDERID']))
            user_payment = Payment.objects.filter(user=user).first()
            if user_payment:
                user_payment.amount = amount
                user_payment.timestamp = datetime.now(user_payment.timestamp.tzinfo)
                user_payment.save()
            else:
                Payment.objects.create(user=user, amount=amount).save()
            return HttpResponseRedirect(reverse('home')) 
    except:
        return HttpResponseRedirect(reverse('payment_page', args=('Payment Failed',)))
