from django.contrib import admin
from django.urls import path

from company.views import *
from user.views import LoginAPI

urlpatterns = [
    path('admin/', admin.site.urls),
    path('rest/login/', LoginAPI.as_view(), name='login'),

    path('rest/company/create/', CompanyCreateAPIView.as_view(), name='company_create'),
    path('rest/company/<int:company_id>/', CompanyDetailAPIView.as_view(), name='company-detail'),
    path('rest/company/list-all', CompanyListAPIView.as_view(), name='company-list_by_user'),
    path('rest/company/<int:company_id>/delete/', CompanyDeleteAPIView.as_view(), name='company-delete'),
    path('rest/company/<int:company_id>/update/', CompanyUpdateView.as_view(), name='company-update'),

]
