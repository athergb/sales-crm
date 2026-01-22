from django.db import models
from django.contrib.auth.models import User

# 1. Branch Model
class Branch(models.Model):
    name = models.CharField(max_length=100)
    location = models.CharField(max_length=100, blank=True)

    def __str__(self):
        return self.name

# 2. User Profile Model (The ID Card)
class UserProfile(models.Model):
    ROLE_CHOICES = [
        ('ADMIN', 'System Administrator'),
        ('SALES_MGR', 'Sales Manager'),
        ('BRANCH_MGR', 'Branch Manager'),
        ('AGENT', 'Sales Agent'),
    ]

    user = models.OneToOneField(User, on_delete=models.CASCADE)
    role = models.CharField(max_length=20, choices=ROLE_CHOICES, default='AGENT')
    branch = models.ForeignKey(Branch, on_delete=models.SET_NULL, null=True, blank=True)
    
    def __str__(self):
        return f"{self.user.username} ({self.get_role_display()})"

# 3. Client Model
class Client(models.Model):
    CLIENT_TYPE_CHOICES = [
        ('EXISTING', 'Existing Client'),
        ('NEW', 'New Client'),
    ]

    name = models.CharField(max_length=200)
    phone = models.CharField(max_length=20)
    address = models.TextField(blank=True)
    visiting_card = models.ImageField(upload_to='visiting_cards/', blank=True, null=True)
    client_type = models.CharField(max_length=10, choices=CLIENT_TYPE_CHOICES, default='NEW')
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.name

# 4. Visit Model
class Visit(models.Model):
    VISIT_TYPE_CHOICES = [
        ('PHYSICAL', 'Physical Visit'),
        ('TELEPHONIC', 'Telephonic Call'),
    ]

    STATUS_CHOICES = [
        ('SUCCESS', 'Successful'),
        ('PENDING', 'Follow-up Required'),
        ('UNSUCCESSFUL', 'Unsuccessful'),
    ]

    agent = models.ForeignKey(User, on_delete=models.CASCADE, related_name='visits')
    client = models.ForeignKey(Client, on_delete=models.CASCADE, related_name='visits')
    visit_type = models.CharField(max_length=20, choices=VISIT_TYPE_CHOICES)
    visit_date = models.DateTimeField(auto_now_add=True)
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='PENDING')
    summary = models.TextField()

    def __str__(self):
        return f"{self.agent.username} - {self.client.name} ({self.visit_date.strftime('%Y-%m-%d')})"