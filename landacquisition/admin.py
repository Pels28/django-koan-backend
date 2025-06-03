from django.contrib import admin
from .models import LandAcquisition

class LandAcquisitionAdmin(admin.ModelAdmin):
    list_display = ('id', 'user', 'propertyType', 'locationRegion', 'decision', 'created_at')
    list_filter = ('propertyType', 'stationType', 'decision', 'created_at')
    search_fields = ('user__username', 'locationRegion', 'locationDistrict', 'locationRoad')
    readonly_fields = ('created_at', 'updated_at')
    fieldsets = (
        ('User Information', {
            'fields': ('user',)
        }),
        ('Property Information', {
            'fields': (
                'propertyType',
                ('locationRegion', 'locationDistrict'),
                'locationRoad'
            )
        }),
        ('Land Details', {
            'classes': ('collapse',),
            'fields': (
                'landSize',
                'landValue',
            )
        }),
        ('Station Details', {
            'classes': ('collapse',),
            'fields': (
                'stationType',
                'stationCurrentOMC',
                'stationDebtWithOMC',
                ('stationTankCapacityDiesel', 'stationTankCapacitySuper'),
            )
        }),
        ('Project & Lease Info', {
            'fields': (
                'projectedVolume',
                ('leaseYears', 'leaseRemaining'),
                'loadingLocation',
                'distance'
            )
        }),
        ('Decision Making', {
            'fields': (
                'decision',
                'reason'
            )
        }),
        ('Personnel Information', {
            'classes': ('collapse',),
            'fields': (
                'originator',
                'distributionManager',
                'position'
            )
        }),
        ('Civil Works', {
            'classes': ('collapse',),
            'fields': (
                'civilWorksEstimatedCost',
                ('civilWorksForecourtRequired', 'civilWorksForecourtComment'),
                ('civilWorksBuildingRequired', 'civilWorksBuildingComment'),
                ('civilWorksCanopyRequired', 'civilWorksCanopyComment'),
                ('civilWorksTankFarmRequired', 'civilWorksTankFarmComment'),
                ('civilWorksElectricalsRequired', 'civilWorksElectricalsComment'),
                ('civilWorksInterceptorStatus', 'civilWorksInterceptorFunctional'),
                ('civilWorksVentsStatus', 'civilWorksVentsFunctional'),
                'civilWorksOtherWorks'
            )
        }),
        ('Cost & Logistics', {
            'fields': (
                'logistics',
                'totalEstimatedCost'
            )
        }),
        ('Timestamps', {
            'classes': ('collapse',),
            'fields': (
                ('created_at', 'updated_at'),
            )
        }),
    )

admin.site.register(LandAcquisition, LandAcquisitionAdmin)