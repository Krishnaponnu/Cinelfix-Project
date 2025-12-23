from django.shortcuts import render


from django.views import View
# Create your views here.

class SubscriptionsView(View):

    template = 'subscriptions/subscription-list.html'

    def get(self,request,*args,**kwargs):

        return render(request,self.template)