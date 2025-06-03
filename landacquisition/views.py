from rest_framework import generics, permissions
from .models import LandAcquisition
from .serializers import LandAcquisitionSerializer
from rest_framework.pagination import PageNumberPagination
from rest_framework import filters

class StandardResultsSetPagination(PageNumberPagination):
    page_size = 10
    page_size_query_param = 'page_size'
    max_page_size = 100

class LandAcquisitionListCreateView(generics.ListCreateAPIView):
    serializer_class = LandAcquisitionSerializer
    permission_classes = [permissions.IsAuthenticated]
    pagination_class = StandardResultsSetPagination
    
    def get_queryset(self):
        return LandAcquisition.objects.filter(user=self.request.user).order_by('-created_at')
    
    def perform_create(self, serializer):
        serializer.save(user=self.request.user)
        
    filter_backends = [filters.SearchFilter]
    search_fields = [
        'propertyType',
        'locationRegion',
        'locationDistrict',
        'locationRoad',
        'stationCurrentOMC',
        'landSize'
    ]

class LandAcquisitionRetrieveUpdateDestroyView(generics.RetrieveUpdateDestroyAPIView):
    serializer_class = LandAcquisitionSerializer
    permission_classes = [permissions.IsAuthenticated]
    
    def get_queryset(self):
        return LandAcquisition.objects.filter(user=self.request.user)