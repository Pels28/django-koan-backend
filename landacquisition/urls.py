from django.urls import path
from .views import LandAcquisitionListCreateView, LandAcquisitionRetrieveUpdateDestroyView, LandAcquisitionReviewView

urlpatterns = [
    path('land-acquisitions/', LandAcquisitionListCreateView.as_view(), name='landacquisition-list-create'),
    path('land-acquisitions/<int:pk>/', LandAcquisitionRetrieveUpdateDestroyView.as_view(), name='landacquisition-detail'),
    path('land-acquisitions/<int:pk>/review/', 
         LandAcquisitionReviewView.as_view(), 
         name='land-acquisition-review'),
]