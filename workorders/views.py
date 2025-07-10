# workorders/views.py
from django.utils import timezone
from django.shortcuts import render
from rest_framework import generics, permissions
from .models import WorkOrder
from .serializers import WorkOrderSerializer
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework.pagination import PageNumberPagination
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from django.contrib.auth import get_user_model

# Create your views here.

class CustomPagination(PageNumberPagination):
    page_size_query_param = 'page_size'
    max_page_size = 100

class WorkOrderListCreateView(generics.ListCreateAPIView):
    serializer_class = WorkOrderSerializer
    permission_classes = [permissions.IsAuthenticated]
    filter_backends = [DjangoFilterBackend]
    filterset_fields = ['priority', 'status', 'review_status']  # Add review_status here
    pagination_class = CustomPagination

    def get_queryset(self):
        queryset = WorkOrder.objects.all().order_by('-created_at')
        
        # Add review_status filter if provided
        review_status = self.request.query_params.get('review_status', None)
        if review_status:
            queryset = queryset.filter(review_status=review_status)
            
        if not self.request.user.is_manager:
            queryset = queryset.filter(user=self.request.user)
            
        return queryset

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)

class WorkOrderRetrieveUpdateDestroyView(generics.RetrieveUpdateDestroyAPIView):
    serializer_class = WorkOrderSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        if self.request.user.is_manager:
            return WorkOrder.objects.all()
        return WorkOrder.objects.filter(user=self.request.user)

class WorkOrderReviewView(APIView):
    permission_classes = [permissions.IsAuthenticated]

    def post(self, request, pk):
        try:
            work_order = WorkOrder.objects.get(pk=pk)
        except WorkOrder.DoesNotExist:
            return Response(status=status.HTTP_404_NOT_FOUND)
        
        user = request.user
        # Only managers can review
        if not user.is_manager:
            return Response(
                {"error": "Only managers can review work orders"},
                status=status.HTTP_403_FORBIDDEN
            )
        
        # Get review action and notes from request
        action_type = request.data.get('action')
        notes = request.data.get('notes', '')
        
        if action_type not in ['approve', 'reject']:
            return Response(
                {"error": "Invalid action. Use 'approve' or 'reject'"},
                status=status.HTTP_400_BAD_REQUEST
            )
        
        # Update work order based on action
        if action_type == 'approve':
            work_order.review_status = 'approved'
            work_order.is_approved = True
        else:
            work_order.review_status = 'rejected'
            work_order.is_approved = False
        
        work_order.reviewed_by = user
        work_order.review_date = timezone.now()
        work_order.review_notes = notes
        work_order.save()
        
        serializer = WorkOrderSerializer(work_order)
        return Response(serializer.data)