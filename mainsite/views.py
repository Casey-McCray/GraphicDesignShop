from django.shortcuts import render, redirect
from django.core.mail import send_mail
from django.conf import settings
from django.contrib.auth.forms import UserCreationForm
from django.contrib import messages
from .models import Order
from .forms import UserRegistrationForm
from django.contrib.auth.decorators import login_required
from django.views.generic import CreateView
from django.contrib.auth.mixins import LoginRequiredMixin
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from .serializers import DeadlineSerializer, AmountSerializer
from django.views.decorators.csrf import ensure_csrf_cookie
import json
import razorpay

def home(request):
	return render(request, 'mainsite/index.html')

def work(request):
	return render(request, 'mainsite/work.html')

def register(request):
	if request.method == 'POST':
		form = UserRegistrationForm(request.POST)
		if form.is_valid():
			username = form.cleaned_data.get('username')
			email = form.cleaned_data.get('email')
			form.save()
			title = 'You are one step closer to working with me.'
			message = 'Thank you for creating an account. Please verify it by clicking the link provided below'
			send_mail(title, message, settings.EMAIL_HOST_USER, [email], fail_silently=False)
			messages.success(request, f'Account Created for { username }')
			return redirect('login')
	else:
		form = UserRegistrationForm()
	return render(request, 'mainsite/register.html', {'form': form})



@ensure_csrf_cookie
def purchase(request):
	order_id = request.__dict__['_post']['id']
	payment_id = dict(request.__dict__['_post'])['razorpay_payment_id'][0]
	payment_amount = int(request.__dict__['_post']['amount'])
	
	order = Order.objects.filter(user=request.user, id=order_id, confirmed=True, completed=False)[0]
	resp = settings.CLIENT.payment.capture(payment_id, payment_amount)
	if resp['status'] == 'captured':
		print(order.paid)
		order.save()
		return render(request, 'mainsite/purchase.html')


class NewOrder(LoginRequiredMixin, CreateView):
	model = Order
	fields = ['title', 'description', 'img', 'amount', 'deadline']
	template_name = 'mainsite/new_order.html' 
	success_url = '/order/new/success/'

	def form_valid(self, form):
		form.instance.user = self.request.user
		form.instance.amount *= 100 #Converting Rupees into Paisa for Razorpay
		if form.is_valid():
			#Get form data
			order_title = form.cleaned_data.get('title')
			order_amount = int(form.cleaned_data.get('amount'))*100
			amount_currency = 'INR'
			receipt_id = form.cleaned_data.get('id')

			#Creating Order
			DATA = {
				'amount': order_amount,
				'currency': amount_currency,
				'receipt': receipt_id,
				'payment_capture': 1 # if capture should be done automatically or else 0
				#notes(optional)  : optional notes for order
			}
			settings.CLIENT.order.create(data=DATA)

			#Send Email
			# title = 'Your Order Has Been Placed!'
			# message = 'Thank your for placing your order for "{}". Please wait while I review and confirm the order.'.format(order_title)
			# messages.success(self.request, f'Your Order has been Placed!')
			# send_mail(title, message, settings.EMAIL_HOST_USER, [self.request.user.email], fail_silently=False)
			form.save()
		return super().form_valid(form)

@login_required
def orders(request):
	pending_orders = Order.objects.filter(user=request.user, confirmed=False)
	active_orders = Order.objects.filter(user=request.user, confirmed=True, completed=False)
	completed_orders = Order.objects.filter(user=request.user, confirmed=True, completed=True)
	return render(request, 'mainsite/orders.html', {'active_orders': active_orders, 
													'pending_orders': pending_orders, 
													'completed_orders': completed_orders})

def order_success(request):
	return render(request, 'mainsite/order_success.html')


class amount_update(LoginRequiredMixin, APIView):

	def get(self, request, pk):
		order = Order.objects.get(pk=pk)
		serializer = AmountSerializer(order, many=False)
		if order.bargain_amount:
			order.amount = order.bargain_amount
			order.bargain_amount = None
			order.save()
		return Response(serializer.data)


class deadline_update(LoginRequiredMixin, APIView):

	def get(self, request, pk):
		order = Order.objects.get(pk=pk)
		serializer = DeadlineSerializer(order, many=False)
		if order.bargain_deadline:
			order.deadline = order.bargain_deadline
			order.bargain_deadline = None
			order.save()
		return Response(serializer.data)


class get_amount(LoginRequiredMixin, APIView):

	def get(self, request, pk):
		order = Order.objects.get(pk=pk)
		serializer = AmountSerializer(order, many=False)
		return Response(serializer.data)