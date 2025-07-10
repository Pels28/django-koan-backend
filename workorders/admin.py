from django.contrib import admin
from django.db.models import Case, When, Value, IntegerField
from .models import WorkOrder

class WorkOrderAdmin(admin.ModelAdmin):
    list_display = (
        'work_order_number', 
        'requester', 
        'location', 
        'priority', 
        'status',
        'review_status',  # Added review status
        'is_approved',
        'start_date', 
        'completion_date'
    )
    list_filter = (
        'priority', 
        'status', 
        'review_status',  # Added review status filter
        'is_approved',
        'start_date', 
        'completion_date'
    )
    search_fields = ('work_order_number', 'requester', 'location', 'description', 'assigned_technician')
    readonly_fields = ('created_at', 'updated_at', 'review_date', 'reviewed_by')  # Added readonly fields
    list_editable = ("priority", "status", "review_status", "is_approved")  # Added review_status
    date_hierarchy = 'date'
    
    # Custom ordering: High priority first, then Medium, then Low
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
        ).order_by('priority_order', '-start_date', '-created_at')
        return qs
    
    fieldsets = (
        ('Work Order Information', {
            'fields': (
                'work_order_number',
                ('date', 'status'),
                'priority',
                'is_approved'
            )
        }),
        ('Review Information', {  # New section for review fields
            'fields': (
                'review_status',
                'reviewed_by',
                'review_date',
                'review_notes'
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
    actions = [
        'mark_as_pending', 
        'mark_as_in_progress', 
        'mark_as_completed',
        'approve_work_orders',
        'unapprove_work_orders',
        'mark_as_pending_review',  # New action
        'mark_as_approved',  # New action
        'mark_as_rejected'  # New action
    ]
    
    def mark_as_pending(self, request, queryset):
        queryset.update(status='pending')
    mark_as_pending.short_description = "Mark as Pending"
    
    def mark_as_in_progress(self, request, queryset):
        queryset.update(status='in_progress')
    mark_as_in_progress.short_description = "Mark as In Progress"
    
    def mark_as_completed(self, request, queryset):
        queryset.update(status='completed')
    mark_as_completed.short_description = "Mark as Completed"
    
    def approve_work_orders(self, request, queryset):
        queryset.update(is_approved=True)
    approve_work_orders.short_description = "Approve selected"
    
    def unapprove_work_orders(self, request, queryset):
        queryset.update(is_approved=False)
    unapprove_work_orders.short_description = "Unapprove selected"
    
    # New actions for review status
    def mark_as_pending_review(self, request, queryset):
        queryset.update(review_status='pending_review')
    mark_as_pending_review.short_description = "Mark as Pending Review"
    
    def mark_as_approved(self, request, queryset):
        queryset.update(review_status='approved', is_approved=True)
    mark_as_approved.short_description = "Mark as Approved"
    
    def mark_as_rejected(self, request, queryset):
        queryset.update(review_status='rejected', is_approved=False)
    mark_as_rejected.short_description = "Mark as Rejected"

admin.site.register(WorkOrder, WorkOrderAdmin)