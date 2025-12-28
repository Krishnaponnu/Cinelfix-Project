from django.shortcuts import render,redirect

from django.views import View

from subscriptions.models import SubscriptionPlans,UserSubscriptions

from django.utils.decorators import method_decorator

from authentication.permissions import permitted_user_roles

import razorpay

from decouple import config

from payments.models import Transaction

from django.db import transaction

from django.utils import timezone

# Create your views here.

@method_decorator(permitted_user_roles(['User']),name='dispatch')
class RazorPayView(View):

    template = 'payments/razorpay.html'

    def get(self,request,*args,**kwargs):

        uuid = kwargs.get('uuid')

        user = request.user

        plan = SubscriptionPlans.objects.get(uuid=uuid)

        with transaction.atomic():

            user_subscription = UserSubscriptions.objects.create(profile=user,plan=plan)

            client = razorpay.Client(auth=(config('RZP_CLIENT_ID'), config('RZP_CLIENT_SECRET')))

            data = { "amount": plan.amount*100, "currency": "INR", "receipt": "order_rcptid_11" }

            payment = client.order.create(data=data)

            rzp_order_id = payment.get('id')

            transaction_obj = Transaction.objects.create(user_subscription=user_subscription,rzp_order_id=rzp_order_id,amount=plan.amount)

            data = {'RZP_CLIENT_ID':config('RZP_CLIENT_ID'),'amount':plan.amount,'order_id':rzp_order_id}

            return render(request,self.template,context=data)
        
class PaymentVerifyView(View):

    def post(self,request,*args,**kwargs):

        rzp_order_id = request.POST.get('razorpay_order_id')

        rzp_payment_id = request.POST.get('razorpay_payment_id')

        rzp_payment_signature = request.POST.get('razorpay_signature')

        transaction_obj = Transaction.objects.get(rzp_order_id=rzp_order_id)

        transaction_obj.rzp_payment_signature = rzp_payment_signature

        transaction_obj.save()

        client = razorpay.Client(auth=(config('RZP_CLIENT_ID'), config('RZP_CLIENT_SECRET')))

        paid=client.utility.verify_payment_signature({

                                                'razorpay_order_id': rzp_order_id,

                                                'razorpay_payment_id': rzp_payment_id,

                                                'razorpay_signature': rzp_payment_signature
                                                })
        
        if paid :

            transaction_obj.status = 'Success'

            transaction_obj.save()

            user_subscription = transaction_obj.user_subscription

            start_date = timezone.now()

            end_date = start_date+timezone.timedelta(days=30)

            #print(start_date,end_date)

            user_subscription.start_date = start_date

            user_subscription.end_date = end_date

            user_subscription.active = True

            user_subscription.save()

            return redirect('home')
        
        transaction_obj.status = 'Failed'

        transaction_obj.save()

        return redirect('razorpay',uuid=user_subscription.plan.uuid)