from django.urls import path
from . import views

# 报销应用的URL路由配置
# 所有路径都以/claims/为前缀（在主urls.py中定义）
urlpatterns = [
    path('create/', views.create_reimbursement, name='create_reimbursement'),  # 创建报销单
    path('edit/<int:pk>/', views.edit_reimbursement, name='edit_reimbursement'),  # 编辑报销单（草稿或已驳回）
    path('detail/<int:pk>/', views.reimbursement_detail, name='reimbursement_detail'),  # 查看报销单详情
    path('review/<int:pk>/', views.review_reimbursement, name='review_reimbursement'),  # 审核报销单（仅负责人）
    path('export/', views.export_claims, name='export_claims'),  # 导出报销单（Excel+Word+发票打包）
]
