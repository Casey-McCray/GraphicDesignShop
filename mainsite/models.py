from django.db import models
from django.contrib.auth.models import User
from django.urls import reverse
from django.conf import settings
from django.db.models.signals import post_save
from django.dispatch import receiver
from django.core.mail import send_mail

class Order(models.Model):
	user = models.ForeignKey(User, on_delete=None)
	title = models.CharField(max_length=50)
	description = models.TextField()
	img = models.ImageField(blank=True, null=True)
	amount = models.IntegerField()
	deadline = models.DateTimeField()
	creation_date = models.DateTimeField(auto_now_add=True)
	
	bargain_amount = models.IntegerField(blank=True, null=True)
	bargain_deadline = models.DateTimeField(blank=True, null=True)
	bargain_amount_email = models.BooleanField(default=False)
	bargain_deadline_email = models.BooleanField(default=False)

	confirmed = models.BooleanField(default=False)
	paid = models.BooleanField(default=False)
	completed = models.BooleanField(default=False)
	# message = models.TextField()


	def __str__(self):
		return self.title


	def get_absolute_url(self):
		return reverse('orders')


@receiver(post_save, sender=Order)
def update_bargain_price(sender, instance, **kwargs):
	if instance.bargain_amount and instance.bargain_amount_email:
		title = 'A Bargain Amount Has Been Set For Your Order'
		message = 'Please check your account for the updated price.'
		send_mail(title, message, settings.EMAIL_HOST_USER, [instance.user.email], fail_silently=False)
		instance.bargain_amount_email = False
	elif instance.bargain_deadline and instance.bargain_deadline_email: #this shouldn't be an elif.
		title = 'A Bargain Deadline Has Been Set For Your Order.'
		message = 'Please check your account for the Updated Deadline.'
		send_mail(title, message, settings.EMAIL_HOST_USER, [instance.user.email], fail_silently=False)
		instance.bargain_deadline_email = False