from rest_framework import serializers
from .models import UserInvestment, TransactionLog
from django.utils import timezone
import uuid
from .services import InvestmentService


class UserInvestmentSerializer(serializers.ModelSerializer):
    profit_loss = serializers.SerializerMethodField()
    profit_loss_percentage = serializers.SerializerMethodField()

    class Meta:
        model = UserInvestment
        fields = [
            'id', 'asset_name', 'amount_invested', 'current_value',
            'profit_loss', 'profit_loss_percentage', 'purchase_date',
            'is_active'
        ]

    def get_profit_loss(self, obj): 
        return obj.current_value - obj.amount_invested

    def get_profit_loss_percentage(self, obj):
        if obj.amount_invested == 0:
            return 0
        pl = self.get_profit_loss(obj)
        return (pl / obj.amount_invested) * 100

    def validate_amount_invested(self, value):
        if value < 1000:
            raise serializers.ValidationError("Minimum investment amount is $1000", 400)
        return value
