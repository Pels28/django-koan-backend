from django.urls import path
from .views import WorkOrderListCreateView, WorkOrderRetrieveUpdateDestroyView

urlpatterns = [
    path('work-orders/', WorkOrderListCreateView.as_view(), name='workorder-list-create'),
    path('work-orders/<int:pk>/', WorkOrderRetrieveUpdateDestroyView.as_view(), name='workorder-detail'),
]