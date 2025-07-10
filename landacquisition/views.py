from rest_framework import generics, permissions, status
from .models import LandAcquisition
from .serializers import LandAcquisitionSerializer
from rest_framework.pagination import PageNumberPagination
from rest_framework import filters
from django.utils import timezone
from rest_framework.response import Response
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework.views import APIView


class StandardResultsSetPagination(PageNumberPagination):
    page_size = 10
    page_size_query_param = 'page_size'
    max_page_size = 100

class LandAcquisitionListCreateView(generics.ListCreateAPIView):
    serializer_class = LandAcquisitionSerializer
    permission_classes = [permissions.IsAuthenticated]
    pagination_class = StandardResultsSetPagination
    filter_backends = [filters.SearchFilter, DjangoFilterBackend]
    filterset_fields = ['review_status', 'propertyType']  # Add review_status filter
    search_fields = [
        'propertyType',
        'locationRegion',
        'locationDistrict',
        'locationRoad',
        'stationCurrentOMC',
        'landSize'
 
    ]
    
    def get_queryset(self):
        queryset = LandAcquisition.objects.all().order_by('-created_at')
        
        # Add review_status filter if provided
        review_status = self.request.query_params.get('filter') or self.request.query_params.get('review_status')
        if review_status:
            queryset = queryset.filter(review_status=review_status)
            
        # Managers see all records, regular users see only their own
        if not self.request.user.is_manager:
            queryset = queryset.filter(user=self.request.user)
            
        return queryset
    
    def perform_create(self, serializer):
        serializer.save(user=self.request.user)
class LandAcquisitionRetrieveUpdateDestroyView(generics.RetrieveUpdateDestroyAPIView):
    serializer_class = LandAcquisitionSerializer
    permission_classes = [permissions.IsAuthenticated]
    
    def get_queryset(self):
        # Managers can access any record, users only their own
        if self.request.user.is_manager:
            return LandAcquisition.objects.all()
        return LandAcquisition.objects.filter(user=self.request.user)
    
class LandAcquisitionReviewView(APIView):
    permission_classes = [permissions.IsAuthenticated]

    def post(self, request, pk):
        try:
            land_acquisition = LandAcquisition.objects.get(pk=pk)
        except LandAcquisition.DoesNotExist:
            return Response(status=status.HTTP_404_NOT_FOUND)
        
        user = request.user
        # Only managers can review
        if not user.is_manager:
            return Response(
                {"error": "Only managers can review land acquisitions"},
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
        
        # Update land acquisition based on action
        if action_type == 'approve':
            land_acquisition.review_status = 'approved'
        else:
            land_acquisition.review_status = 'rejected'
        
        land_acquisition.reviewed_by = user
        land_acquisition.review_date = timezone.now()
        land_acquisition.review_notes = notes
        land_acquisition.save()
        
        serializer = LandAcquisitionSerializer(land_acquisition)
        return Response(serializer.data)