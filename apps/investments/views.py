from rest_framework import viewsets, status
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.pagination import PageNumberPagination
from django.db.models import Sum, Max, Min, F, ExpressionWrapper, DecimalField
from django.utils.timezone import now
from .models import UserInvestment, TransactionLog
from .serializers import UserInvestmentSerializer
from .services import InvestmentService
import uuid

class StandardResultsSetPagination(PageNumberPagination):
    page_size = 10

class UserInvestmentViewSet(viewsets.ModelViewSet):
    serializer_class = UserInvestmentSerializer
    permission_classes = [IsAuthenticated]
    pagination_class = StandardResultsSetPagination

    def get_queryset(self):
        return UserInvestment.objects.filter(user=self.request.user).order_by('-purchase_date')

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        # Create investment
        investment = serializer.save(user=request.user)
        # Create transaction log for PURCHASE
        TransactionLog.objects.create(
            user=request.user,
            transaction_type=TransactionLog.PURCHASE,
            amount=investment.amount_invested,
            reference_id=str(uuid.uuid4())
        )
        serialized_investment = self.get_serializer(investment)
        return Response(serialized_investment.data, status=status.HTTP_201_CREATED)

from rest_framework.views import APIView

class InvestmentSummaryView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        user = request.user
        investments = UserInvestment.objects.filter(user=user, is_active=True)

        total_invested = investments.aggregate(total=Sum('amount_invested'))['total'] or 0
        current_value = investments.aggregate(total=Sum('current_value'))['total'] or 0
        total_profit_loss = current_value - total_invested
        active_count = investments.count()

        # Best performing
        best_investment = None
        worst_investment = None
        if active_count > 0:
            # Calculate profit percentages for each investment
            def profit_percent(inv):
                if inv.amount_invested > 0:
                    return ((inv.current_value - inv.amount_invested) / inv.amount_invested) * 100
                return 0
            best_investment = max(investments, key=profit_percent)
            worst_investment = min(investments, key=profit_percent)

        data = {
            "total_invested": total_invested,
            "current_portfolio_value": current_value,
            "total_profit_loss": total_profit_loss,
            "number_of_active_investments": active_count,
            "best_performing_investment": UserInvestmentSerializer(best_investment).data if best_investment else None,
            "worst_performing_investment": UserInvestmentSerializer(worst_investment).data if worst_investment else None,
        }
        return Response(data)
