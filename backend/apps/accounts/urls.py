from django.urls import path
from . import views

app_name = 'accounts'

urlpatterns = [
    path('login/', views.login_view, name='login'),
    path('logout/', views.logout_view, name='logout'),
    path('dashboard/', views.dashboard_view, name='dashboard'),
    path('access-denied/', views.access_denied_view, name='access_denied'),
    path('super-admin-panel/', views.super_admin_panel, name='super_admin_panel'),
    path('admin-zone/', views.admin_zone, name='admin_zone'),
]
