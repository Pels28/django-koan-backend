from django.db import models

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

    user = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name='work_orders'
    )
    date = models.DateField(default=timezone.now)
    work_order_number = models.CharField(max_length=50, unique=True)
    requester = models.CharField(max_length=100)
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
