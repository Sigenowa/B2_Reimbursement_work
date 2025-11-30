from django.urls import path
from . import views

# 报销应用的URL路由配置，所有路径都以/claims/为前缀（在主urls.py中定义）
urlpatterns = [
    path('create/', views.create_reimbursement, name='create_reimbursement'),
    path('edit/<int:pk>/', views.edit_reimbursement, name='edit_reimbursement'),
    path('detail/<int:pk>/', views.reimbursement_detail, name='reimbursement_detail'),
]
