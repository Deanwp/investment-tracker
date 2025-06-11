from datetime import timedelta
from django.utils.timezone import now
from .models import UserInvestment

class InvestmentService:

    def calculate_portfolio_performance(self, user):
        investments = UserInvestment.objects.filter(user=user, is_active=True)
        total_invested = sum(inv.amount_invested for inv in investments)
        total_current = sum(inv.current_value for inv in investments)
        if total_invested == 0:
            return 0
        return (total_current - total_invested) / total_invested * 100

    def get_investment_insights(self, user):
        investments = UserInvestment.objects.filter(user=user, is_active=True)
        if not investments:
            return {
                "average_holding_period_days": 0,
                "preferred_investment_size": 0
            }
        total_days = sum((now() - inv.purchase_date).days for inv in investments)
        average_holding_period = total_days / investments.count()

        average_investment = sum(inv.amount_invested for inv in investments) / investments.count()

        return {
            "average_holding_period_days": average_holding_period,
            "preferred_investment_size": average_investment
        }
