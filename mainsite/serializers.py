from rest_framework import serializers
from .models import Order

class DeadlineSerializer(serializers.ModelSerializer):

	class Meta:
		model = Order
		fields = ['deadline']


class AmountSerializer(serializers.ModelSerializer):

	class Meta:
		model = Order
		fields = ['amount', 'bargain_amount']