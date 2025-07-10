from django.contrib import admin
from .models import LandAcquisition
from django.utils import timezone

class LandAcquisitionAdmin(admin.ModelAdmin):
    list_display = (
        'id', 
        'user', 
        'propertyType', 
        'locationRegion', 
        'decision', 
        'review_status', 
        'reviewed_by', 
        'review_date', 
        'created_at'
    )
    
    list_filter = (
        'propertyType', 
        'stationType', 
        'decision', 
        'review_status', 
        'created_at'
    )
    
    search_fields = (
        'user__username', 
        'locationRegion', 
        'locationDistrict', 
        'locationRoad',
        'review_notes'
    )
    
    readonly_fields = ('created_at', 'updated_at', 'review_date')
    
    # Add autocomplete for user fields
    autocomplete_fields = ['user', 'reviewed_by']
    
    # Add date hierarchy for review date
    date_hierarchy = 'review_date'
    
    fieldsets = (
        ('User Information', {
            'fields': ('user',)
        }),
        ('Review Information', {
            'fields': (
                'review_status',
                'reviewed_by',
                'review_date',
                'review_notes'
            )
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
    
    # Custom method to display reviewed_by username
    def reviewed_by_username(self, obj):
        return obj.reviewed_by.username if obj.reviewed_by else None
    reviewed_by_username.short_description = 'Reviewed By'
    
    # Add action to update review status
    actions = ['mark_as_approved', 'mark_as_rejected']
    
    def mark_as_approved(self, request, queryset):
        updated = queryset.update(
            review_status='approved',
            reviewed_by=request.user,
            review_date=timezone.now()
        )
        self.message_user(request, f"{updated} acquisition(s) marked as approved.")
    
    def mark_as_rejected(self, request, queryset):
        updated = queryset.update(
            review_status='rejected',
            reviewed_by=request.user,
            review_date=timezone.now()
        )
        self.message_user(request, f"{updated} acquisition(s) marked as rejected.")

admin.site.register(LandAcquisition, LandAcquisitionAdmin)