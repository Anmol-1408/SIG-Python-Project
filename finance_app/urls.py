from django.urls import path
from . import views
from .views import generate_financial_reports

urlpatterns = [
    path('', views.finance_dashboard, name='finance_dashboard'),
    path('add/', views.add_record, name='add_record'),
    path('update/<int:record_id>/', views.update_record, name='update_record'),
    path('delete/<int:record_id>/', views.delete_record, name='delete_record'),
    path('reports/', generate_financial_reports, name='financial_reports'),
]
