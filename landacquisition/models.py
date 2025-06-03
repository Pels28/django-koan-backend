from django.db import models
from api.models import User
from django.utils import timezone

class LandAcquisition(models.Model):
    PROPERTY_TYPE_CHOICES = [
        ('land', 'Land'),
        ('station', 'Station'),
    ]
    
    STATION_TYPE_CHOICES = [
        ('fuel', 'Fuel'),
        ('lpg', 'LPG'),
        ('crm', 'CRM'),
        ('premix', 'Premix'),
    ]
    
    DECISION_CHOICES = [
        ('accept', 'Accept'),
        ('reject', 'Reject'),
    ]
    
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    
    # Section A
    propertyType = models.CharField(max_length=20, choices=PROPERTY_TYPE_CHOICES)
    locationRegion = models.CharField(max_length=100)
    locationDistrict = models.CharField(max_length=100)
    locationRoad = models.CharField(max_length=100)
    
    # Land-specific fields
    landSize = models.CharField(max_length=100, blank=True, null=True)
    landValue = models.CharField(max_length=100, blank=True, null=True)
    
    # Station-specific fields
    stationType = models.CharField(max_length=20, choices=STATION_TYPE_CHOICES, blank=True, null=True)
    stationCurrentOMC = models.CharField(max_length=100, blank=True, null=True)
    stationDebtWithOMC = models.CharField(max_length=100, blank=True, null=True)
    stationTankCapacityDiesel = models.CharField(max_length=100, blank=True, null=True)
    stationTankCapacitySuper = models.CharField(max_length=100, blank=True, null=True)
    
    projectedVolume = models.CharField(max_length=100)
    leaseYears = models.CharField(max_length=100)
    leaseRemaining = models.CharField(max_length=100)
    loadingLocation = models.CharField(max_length=100)
    distance = models.CharField(max_length=100)
    decision = models.CharField(max_length=20, choices=DECISION_CHOICES)
    reason = models.TextField()
    
    originator = models.CharField(max_length=100, blank=True, null=True)
    distributionManager = models.CharField(max_length=100, null=True, blank=True)
    position = models.CharField(max_length=100, null=True, blank=True)
    
    # Section B
    civilWorksEstimatedCost = models.CharField(max_length=100)
    civilWorksForecourtRequired = models.CharField(max_length=100, blank=True, null=True)
    civilWorksForecourtComment = models.CharField(max_length=255, blank=True, null=True)
    civilWorksBuildingRequired = models.CharField(max_length=100, blank=True, null=True)
    civilWorksBuildingComment = models.CharField(max_length=255, blank=True, null=True)
    civilWorksCanopyRequired = models.CharField(max_length=100, blank=True, null=True)
    civilWorksCanopyComment = models.CharField(max_length=255, blank=True, null=True)
    civilWorksTankFarmRequired = models.CharField(max_length=100, blank=True, null=True)
    civilWorksTankFarmComment = models.CharField(max_length=255, blank=True, null=True)
    civilWorksElectricalsRequired = models.CharField(max_length=100, blank=True, null=True)
    civilWorksElectricalsComment = models.CharField(max_length=255, blank=True, null=True)
    civilWorksInterceptorStatus = models.CharField(max_length=100, blank=True, null=True)
    civilWorksInterceptorFunctional = models.CharField(max_length=100, blank=True, null=True)
    civilWorksVentsStatus = models.CharField(max_length=100, blank=True, null=True)
    civilWorksVentsFunctional = models.CharField(max_length=100, blank=True, null=True)
    civilWorksOtherWorks = models.TextField(blank=True, null=True)
    
    logistics = models.JSONField(default=list)  # List of strings
    totalEstimatedCost = models.CharField(max_length=100)
    
    created_at = models.DateTimeField(default=timezone.now)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"Land Acquisition {self.id} - {self.propertyType}"