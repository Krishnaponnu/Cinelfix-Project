from django.db import models

# Create your models here.

from movies.models import BaseClass

class StatusChoices(models.TextChoices):

    SUCCESS = 'Success','Success'

    FAILED = 'Failed','Failed'

    PENDING = 'Pending','Pending'

class Transaction(BaseClass):

    user_subscription = models.ForeignKey('subscriptions.UserSubscriptions',on_delete=models.CASCADE)

    rzp_order_id = models.SlugField()

    status = models.CharField(max_length=25,choices=StatusChoices.choices,default=StatusChoices.PENDING)

    amount = models.FloatField()

    rzp_payment_id = models.SlugField(null=True,blank=True)

    rzp_payment_signature = models.TextField(null=True,blank=True)

    def __str__(self):

        return f'{self.user_subscription.profile.username} {self.user_subscription.plan.name} {self.user_subscription.created_at}'
    
    class Meta :

        verbose_name = 'Transactions'

        verbose_name_plural = 'transactions'