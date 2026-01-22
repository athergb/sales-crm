from django.contrib import admin
from django.contrib.auth.models import User
from .models import Branch, Client, Visit, UserProfile

# Link Profile to User in Admin
class UserProfileInline(admin.StackedInline):
    model = UserProfile
    can_delete = False

class UserAdmin(admin.ModelAdmin):
    inlines = (UserProfileInline,)

# Unregister default User and register ours
admin.site.unregister(User)
admin.site.register(User, UserAdmin)

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