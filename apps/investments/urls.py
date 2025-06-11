from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import UserInvestmentViewSet, InvestmentSummaryView

router = DefaultRouter()
router.register(r'investments', UserInvestmentViewSet, basename='userinvestment')

urlpatterns = [
    path('investments/summary/', InvestmentSummaryView.as_view(), name='investment-summary'),
    path('', include(router.urls)),
]