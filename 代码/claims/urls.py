from django.urls import path
from . import views

urlpatterns = [
    path('create/', views.create_reimbursement, name='create_reimbursement'),
    path('edit/<int:pk>/', views.edit_reimbursement, name='edit_reimbursement'),
    path('detail/<int:pk>/', views.reimbursement_detail, name='reimbursement_detail'),
    path('review/<int:pk>/', views.review_reimbursement, name='review_reimbursement'),
    path('export/', views.export_claims, name='export_claims'),
    
    # API端点
    path('api/themes/', views.get_activity_themes, name='get_activity_themes'),
    path('api/invoice/<int:invoice_id>/delete/', views.delete_invoice, name='delete_invoice'),
]
