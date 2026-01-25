from django.contrib import admin
from .models import Branch, Client, Visit, UserProfile

@admin.register(Branch)
class BranchAdmin(admin.ModelAdmin):
    list_display = ('name', 'location')

@admin.register(Client)
class ClientAdmin(admin.ModelAdmin):
    list_display = ('name', 'phone', 'client_type', 'created_at')
    search_fields = ('name', 'phone')

@admin.register(Visit)
class VisitAdmin(admin.ModelAdmin):
    list_display = ('agent', 'client', 'visit_type', 'status', 'visit_date')
    list_filter = ('status', 'visit_type', 'visit_date')

@admin.register(UserProfile)
class UserProfileAdmin(admin.ModelAdmin):
    list_display = ('user', 'role', 'branch')