from django.shortcuts import render


from django.views import View

from .models import SubscriptionPlans
# Create your views here.

class SubscriptionsView(View):

    template = 'subscriptions/subscription-list.html'

    def get(self,request,*args,**kwargs):

        plans = SubscriptionPlans.objects.all()

        data = {'plans':plans}

        return render(request,self.template,context=data)