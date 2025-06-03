from django.urls import path
from .views import LandAcquisitionListCreateView, LandAcquisitionRetrieveUpdateDestroyView

urlpatterns = [
    path('land-acquisitions/', LandAcquisitionListCreateView.as_view(), name='landacquisition-list-create'),
    path('land-acquisitions/<int:pk>/', LandAcquisitionRetrieveUpdateDestroyView.as_view(), name='landacquisition-detail'),
]