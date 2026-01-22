from django.contrib import admin
from django.urls import path
from django.contrib.auth import views as auth_views  
from core.views import dashboard, add_visit, add_client, export_visits_to_excel  

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', dashboard, name='dashboard'),
    path('add-visit/', add_visit, name='add_visit'),
    path('add-client/', add_client, name='add_client'),
    path('export/', export_visits_to_excel, name='export_excel'),
    path('login/', auth_views.LoginView.as_view(template_name='core/login.html'), name='login'),
    path('logout/', auth_views.LogoutView.as_view(), name='logout'),
]