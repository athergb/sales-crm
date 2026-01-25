from django.contrib import admin
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
from django.contrib.auth.forms import UserChangeForm
from .models import Branch, Client, Visit, UserProfile, Agency

# 1. Enhanced User Admin with Password Reset in Inline
class UserAdmin(BaseUserAdmin):
    # Show basic fields in the list
    list_display = ('username', 'email', 'is_active')
    
    # Add Password Reset directly to the edit form
    add_form_template = "admin/change_password_form.html"
    change_password_template = "admin/change_password_form.html"
    
    # Inline settings
    def get_inline_instances(self, request, obj):
        # Return the UserProfile inline as normal
        return super().get_inline_instances(request, obj)

# 2. Agency Admin
@admin.register(Agency)
class AgencyAdmin(admin.ModelAdmin):
    list_display = ('name',)

# 3. Branch Admin
@admin.register(Branch)
class BranchAdmin(admin.ModelAdmin):
    list_display = ('name', 'location')

# 4. Client Admin
@admin.register(Client)
class ClientAdmin(admin.ModelAdmin):
    list_display = ('name', 'phone', 'client_type', 'created_at')
    search_fields = ('name', 'phone')

# 5. Visit Admin
@admin.register(Visit)
class VisitAdmin(admin.ModelAdmin):
    list_display = ('agent', 'agency', 'visit_date', 'type_of_business', 'contact_person')
    list_filter = ('type_of_business', 'visit_date')

# 6. UserProfile Admin
@admin.register(UserProfile)
class UserProfileAdmin(admin.ModelAdmin):
    list_display = ('user', 'role', 'branch')

# 7. Register User with our enhanced admin
# We unregister default User and register our custom one
admin.site.unregister(User)
admin.site.register(User, UserAdmin)