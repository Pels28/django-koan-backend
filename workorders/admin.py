from django.contrib import admin
from django.db.models import Case, When, Value, IntegerField
from .models import WorkOrder

class WorkOrderAdmin(admin.ModelAdmin):
    list_display = ('work_order_number', 'requester', 'location', 'priority', 'status', 'start_date', 'completion_date')
    list_filter = ('priority', 'status', 'start_date', 'completion_date')
    search_fields = ('work_order_number', 'requester', 'location', 'description', 'assigned_technician')
    readonly_fields = ('created_at', 'updated_at')
    list_editable = ("priority", "status",)
    date_hierarchy = 'date'
    
    # Custom ordering: High priority first, then Medium, then Low
    # Within each priority, newest start_date first
    def get_queryset(self, request):
        qs = super().get_queryset(request)
        qs = qs.annotate(
            priority_order=Case(
                When(priority='high', then=Value(0)),
                When(priority='medium', then=Value(1)),
                When(priority='low', then=Value(2)),
                default=Value(3),
                output_field=IntegerField(),
            )
        ).order_by('priority_order', '-start_date', '-created_at')  # Added created_at as final sort
        return qs
    
    fieldsets = (
        ('Work Order Information', {
            'fields': (
                'work_order_number',
                ('date', 'status'),
                'priority'
            )
        }),
        ('Requester Information', {
            'fields': (
                'requester',
                'contact_number',
                'user'
            )
        }),
        ('Assignment Details', {
            'fields': (
                'assigned_technician',
                'location',
            )
        }),
        ('Work Details', {
            'fields': (
                'description',
                ('start_date', 'completion_date'),
                'parts_and_materials',
                'special_instructions'
            )
        }),
        ('Approval Information', {
            'classes': ('collapse',),
            'fields': (
                'approval_signature',
                'approver_name_and_title',
                'date_of_approval'
            )
        }),
        ('Timestamps', {
            'classes': ('collapse',),
            'fields': (
                ('created_at', 'updated_at'),
            )
        }),
    )
    
    # Add a status filter to the action dropdown
    actions = ['mark_as_pending', 'mark_as_in_progress', 'mark_as_completed']
    
    def mark_as_pending(self, request, queryset):
        queryset.update(status='pending')
    mark_as_pending.short_description = "Mark selected work orders as Pending"
    
    def mark_as_in_progress(self, request, queryset):
        queryset.update(status='in_progress')
    mark_as_in_progress.short_description = "Mark selected work orders as In Progress"
    
    def mark_as_completed(self, request, queryset):
        queryset.update(status='completed')
    mark_as_completed.short_description = "Mark selected work orders as Completed"

admin.site.register(WorkOrder, WorkOrderAdmin)