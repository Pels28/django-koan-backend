from django.shortcuts import render
from rest_framework import generics, permissions
from .models import WorkOrder
from .serializers import WorkOrderSerializer
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework.pagination import PageNumberPagination

# Create your views here.

class CustomPagination(PageNumberPagination):
    page_size_query_param = 'page_size'
    max_page_size = 100

class WorkOrderListCreateView(generics.ListCreateAPIView):
    serializer_class = WorkOrderSerializer
    permission_classes = [permissions.IsAuthenticated]
    filter_backends = [DjangoFilterBackend]
    filterset_fields = ['priority', 'status']
    pagination_class = CustomPagination

    def get_queryset(self):
        return WorkOrder.objects.filter(user=self.request.user).order_by('-created_at')

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)

class WorkOrderRetrieveUpdateDestroyView(generics.RetrieveUpdateDestroyAPIView):
    serializer_class = WorkOrderSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        return WorkOrder.objects.filter(user=self.request.user)
