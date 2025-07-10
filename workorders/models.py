from django.db import models
import uuid

# Create your models here.

from django.db import models
from django.conf import settings
from django.utils import timezone
from api.models import User

class WorkOrder(models.Model):
    PRIORITY_CHOICES = [
        ('low', 'Low'),
        ('medium', 'Medium'),
        ('high', 'High'),
    ]
    
    STATUS_CHOICES = [
        ('pending', 'Pending'),
        ('in_progress', 'In Progress'),
        ('completed', 'Completed'),
    ]
    DEPARTMENT_CHOICES = [
        ('exploration', 'Exploration'),
        ('drilling', 'Drilling Operations'),
        ('production', 'Production Operations'),
        ('reservoir', 'Reservoir Engineering'),
        ('hse', 'Health, Safety & Environment (HSE)'),
        ('maintenance', 'Maintenance & Reliability'),
        ('project', 'Project Management'),
        ('process', 'Process Engineering'),
        ('subsurface', 'Subsurface Engineering'),
        ('facilities', 'Facilities Engineering'),
        ('logistics', 'Logistics & Supply Chain'),
        ('qa_qc', 'Quality Assurance/Quality Control'),
        ('ic', 'Instrumentation & Control'),
        ('pipeline', 'Pipeline Operations'),
        ('refining', 'Refining Operations'),
        ('tech_support', 'Technical Support'),
        ('field_ops', 'Field Operations'),
        ('geosciences', 'Geosciences'),
        ('well_services', 'Well Services'),
        ('commissioning', 'Commissioning & Start-up'),
    ]
    
    REVIEW_STATUS_CHOICES = [
        ('pending_review', 'Pending Review'),
        ('approved', 'Approved'),
        ('rejected', 'Rejected'),
    ]


    user = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name='work_orders'
    )
    date = models.DateField(default=timezone.now)
    work_order_number = models.CharField(max_length=50, unique=True)
    requester = models.CharField(max_length=100, choices=DEPARTMENT_CHOICES)
    contact_number = models.CharField(max_length=20)
    assigned_technician = models.CharField(max_length=100)
    location = models.CharField(max_length=200)
    description = models.TextField()
    start_date = models.DateField()
    completion_date = models.DateField()
    priority = models.CharField(max_length=10, choices=PRIORITY_CHOICES, default='medium')
    parts_and_materials = models.TextField()
    special_instructions = models.TextField(blank=True)
    approval_signature = models.CharField(max_length=100, blank=True)
    approver_name_and_title = models.CharField(max_length=100, blank=True)
    date_of_approval = models.DateField(null=True, blank=True)
    review_status = models.CharField(
        max_length=20, 
        choices=REVIEW_STATUS_CHOICES, 
        default='pending_review'
    )
    reviewed_by = models.ForeignKey(
        User,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name='reviewed_work_orders'
    )
    review_date = models.DateTimeField(null=True, blank=True)
    review_notes = models.TextField(blank=True, null=True)

    is_approved = models.BooleanField(
        default=False,
        verbose_name="Approval Status",
        help_text="Indicates if the work order has been approved"
    )
    status = models.CharField(  # Add this field
        max_length=20, 
        choices=STATUS_CHOICES, 
        default='pending'
    )
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"{self.work_order_number} - {self.description[:50]}"

    class Meta:
        ordering = ['-created_at']
        
    def save(self, *args, **kwargs):
    # For new instances
        if not self.id:
        # First save with a dummy value to get an ID
            self.work_order_number = "TEMP"  # Temporary value to satisfy DB constraints
            super().save(*args, **kwargs)
        
        # Generate formatted work order number
            self.work_order_number = f"W0-{str(self.id).zfill(3)}"
        
        # Save only the work_order_number field
            super().save(update_fields=['work_order_number'])
        else:
            super().save(*args, **kwargs)
        

        

