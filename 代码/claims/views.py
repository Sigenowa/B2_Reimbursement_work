from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from .models import Reimbursement, Invoice
from .forms import ReimbursementForm, ReimbursementItemFormSet, InvoiceUploadForm

@login_required
def dashboard(request):
    """仪表盘视图，根据用户角色显示不同的内容：负责人显示本部门报销单，普通用户显示自己的报销单"""
    context = {}
    if request.user.is_lead:
        # 修复bug：之前只用了organization，现在优先使用organization，如果没有则使用department
        dept_filter = request.user.organization or request.user.department
        claims = Reimbursement.objects.filter(
            department=dept_filter
        ).exclude(status=Reimbursement.Status.DRAFT).order_by('-created_at')
        context['claims'] = claims
    else:
        my_claims = Reimbursement.objects.filter(applicant=request.user).order_by('-created_at')
        context['my_claims'] = my_claims
        
    return render(request, 'dashboard.html', context)

@login_required
def create_reimbursement(request):
    """创建报销单视图，处理报销单的创建，包括基本信息、物品明细和发票上传，支持暂存和直接提交"""
    if request.method == 'POST':
        form = ReimbursementForm(request.POST)
        formset = ReimbursementItemFormSet(request.POST)
        invoice_form = InvoiceUploadForm(request.POST, request.FILES)
        
        if form.is_valid() and formset.is_valid():
            reimbursement = form.save(commit=False)
            reimbursement.applicant = request.user
            reimbursement.department = request.user.department or "未分配"
            
            if 'save_draft' in request.POST:
                reimbursement.status = Reimbursement.Status.DRAFT
                reimbursement.save()
                formset.instance = reimbursement
                formset.save()
                
                # 处理文件上传
                files = request.FILES.getlist('files')
                for f in files:
                    Invoice.objects.create(reimbursement=reimbursement, file=f)
                
                reimbursement.calculate_total()
                messages.info(request, '报销单已暂存，您可以稍后继续编辑')
            else:
                reimbursement.status = Reimbursement.Status.SUBMITTED
                reimbursement.save()
                formset.instance = reimbursement
                formset.save()
                
                # 处理文件上传
                files = request.FILES.getlist('files')
                for f in files:
                    Invoice.objects.create(reimbursement=reimbursement, file=f)
                
                reimbursement.calculate_total()
                messages.success(request, '报销单提交成功！')
            
            return redirect('dashboard')
    else:
        form = ReimbursementForm()
        formset = ReimbursementItemFormSet()
        invoice_form = InvoiceUploadForm()
    
    return render(request, 'claims/reimbursement_form.html', {
        'form': form,
        'formset': formset,
        'invoice_form': invoice_form,
        'is_new': True
    })

@login_required
def edit_reimbursement(request, pk):
    """编辑报销单视图，只允许编辑草稿状态或已驳回状态的报销单"""
    reimbursement = get_object_or_404(Reimbursement, pk=pk)
    
    if reimbursement.applicant != request.user:
        messages.error(request, "您没有权限编辑此报销单")
        return redirect('dashboard')
    
    # 修复bug：之前只允许DRAFT状态，现在也允许REJECTED状态
    if reimbursement.status not in [Reimbursement.Status.DRAFT, Reimbursement.Status.REJECTED]:
        messages.error(request, "只有草稿或已驳回状态的报销单可以编辑")
        return redirect('reimbursement_detail', pk=pk)
    
    if request.method == 'POST':
        form = ReimbursementForm(request.POST, instance=reimbursement)
        formset = ReimbursementItemFormSet(request.POST, instance=reimbursement)
        invoice_form = InvoiceUploadForm(request.POST, request.FILES)
        
        if form.is_valid() and formset.is_valid():
            reimbursement = form.save(commit=False)
            
            if 'save_draft' in request.POST:
                reimbursement.status = Reimbursement.Status.DRAFT
                reimbursement.save()
                formset.save()
                
                files = request.FILES.getlist('files')
                for f in files:
                    Invoice.objects.create(reimbursement=reimbursement, file=f)
                
                reimbursement.calculate_total()
                messages.info(request, '报销单已暂存')
            else:
                reimbursement.status = Reimbursement.Status.SUBMITTED
                reimbursement.save()
                formset.save()
                
                files = request.FILES.getlist('files')
                for f in files:
                    Invoice.objects.create(reimbursement=reimbursement, file=f)
                
                reimbursement.calculate_total()
                messages.success(request, '报销单已重新提交')
            
            return redirect('dashboard')
    else:
        form = ReimbursementForm(instance=reimbursement)
        formset = ReimbursementItemFormSet(instance=reimbursement)
        invoice_form = InvoiceUploadForm()
    
    return render(request, 'claims/reimbursement_form.html', {
        'form': form,
        'formset': formset,
        'invoice_form': invoice_form,
        'reimbursement': reimbursement,
        'is_new': False
    })

@login_required
def reimbursement_detail(request, pk):
    """报销单详情视图，显示报销单的完整信息，包括物品明细和发票"""
    reimbursement = get_object_or_404(Reimbursement, pk=pk)
    
    # 修复bug：权限检查逻辑，允许申请人或同部门的负责人查看
    if reimbursement.applicant != request.user:
        if not request.user.is_lead or reimbursement.department != (request.user.organization or request.user.department):
            messages.error(request, "您没有权限查看此报销单")
            return redirect('dashboard')
    
    return render(request, 'claims/reimbursement_detail.html', {
        'reimbursement': reimbursement
    })
