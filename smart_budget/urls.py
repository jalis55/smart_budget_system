from django.contrib import admin
from django.urls import path
from main_app import views

urlpatterns = [
    path('',views.home,name='home'),
    path('admin/', admin.site.urls),
    path('sign-up/',views.sign_up,name='signup'),
    path('login/', views.user_login, name='login'),
    path('logout/', views.user_logout, name='logout'),
    path('user-dashboard/',views.user_dashboard,name='user_dashboard'),
    path('manage-budget/<int:id>',views.manage_budget,name="manage_budget"),
    path('view-budget-details/<int:id>',views.view_budget_details,name="view_budget_details"),
    path('delete-budget/<int:id>',views.delete_budget,name="delete_budget")


]
