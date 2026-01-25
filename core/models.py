from django.db import models
from django.contrib.auth.models import User

# 1. New Agency Model (For the List Selection)
class Agency(models.Model):
    name = models.CharField(max_length=200, unique=True)
    
    def __str__(self):
        return self.name

# 2. Branch Model
class Branch(models.Model):
    name = models.CharField(max_length=100)
    location = models.CharField(max_length=100, blank=True)

    def __str__(self):
        return self.name

# 3. User Profile Model
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

# 4. Updated Visit Model
class Visit(models.Model):
    BUSINESS_TYPE_CHOICES = [
        ('B2B', 'B2B'),
        ('B2C', 'B2C'),
        ('Umrah', 'Umrah'),
        ('Ziyarat', 'Ziyarat'),
    ]

    # Old fields removed (client, visit_type, status)
    # New fields added
    agent = models.ForeignKey(User, on_delete=models.CASCADE, related_name='visits')
    agency = models.ForeignKey(Agency, on_delete=models.CASCADE, related_name='visits', null=True, blank=True)
    
    visit_date = models.DateTimeField()
    
    contact_person = models.CharField(max_length=200, blank=True)
    mobile_number = models.CharField(max_length=20, blank=True)
    email_address = models.EmailField(blank=True)
    type_of_business = models.CharField(max_length=20, choices=BUSINESS_TYPE_CHOICES, blank=True)
    remarks = models.TextField(blank=True)

    def __str__(self):
        return f"{self.agent.username} - {self.visit_date.strftime('%Y-%m-%d')}"

# 5. Client Model (Keep old one just in case, though not used now)
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