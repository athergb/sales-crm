from django.contrib import admin
from .models import Branch, Client, Visit, UserProfile, Agency

@admin.register(Agency)
class AgencyAdmin(admin.ModelAdmin):
    list_display = ('name',)

@admin.register(Branch)
class BranchAdmin(admin.ModelAdmin):
    list_display = ('name', 'location')

@admin.register(Client)
class ClientAdmin(admin.ModelAdmin):
    list_display = ('name', 'phone', 'client_type', 'created_at')
    search_fields = ('name', 'phone')

@admin.register(Visit)
class VisitAdmin(admin.ModelAdmin):
    list_display = ('agent', 'agency', 'visit_date', 'type_of_business', 'contact_person')
    list_filter = ('type_of_business', 'visit_date')

@admin.register(UserProfile)
class UserProfileAdmin(admin.ModelAdmin):
    list_display = ('user', 'role', 'branch')