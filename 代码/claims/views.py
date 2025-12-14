import io
import zipfile
import openpyxl
from docx import Document
from django.http import HttpResponse
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.utils import timezone
from .models import Reimbursement, Invoice
from .forms import ReimbursementForm, ReimbursementItemFormSet, InvoiceUploadForm

@login_required
def dashboard(request):
    """
    仪表盘视图
    根据用户角色显示不同的内容：
    - 负责人：显示本部门所有待审核的报销单
    - 普通用户：显示自己提交的所有报销单
    """
    context = {}
    if request.user.is_lead:
        # 负责人查看本部门的所有报销单
        # 优先使用organization字段（如果已设置），否则使用department字段
        dept_filter = request.user.organization or request.user.department
        # 排除草稿状态的报销单，只显示已提交的
        claims = Reimbursement.objects.filter(
            department=dept_filter
        ).exclude(status=Reimbursement.Status.DRAFT).order_by('-created_at')
        context['claims'] = claims
    else:
        # 普通用户只查看自己提交的报销单，按创建时间倒序
        my_claims = Reimbursement.objects.filter(applicant=request.user).order_by('-created_at')
        context['my_claims'] = my_claims
        
    return render(request, 'dashboard.html', context)

@login_required
def create_reimbursement(request):
    """
    创建报销单视图
    处理报销单的创建，包括基本信息、物品明细和发票上传
    支持暂存功能（保存为草稿）和直接提交
    """
    if request.method == 'POST':
        form = ReimbursementForm(request.POST)
        formset = ReimbursementItemFormSet(request.POST)
        invoice_form = InvoiceUploadForm(request.POST, request.FILES)
        
        if form.is_valid() and formset.is_valid():
            # 先保存基本信息，但不提交到数据库
            reimbursement = form.save(commit=False)
            reimbursement.applicant = request.user
            reimbursement.department = request.user.department or "未分配"
            
            # 根据提交按钮判断是暂存还是正式提交
            if 'save_draft' in request.POST:
                # 暂存：状态设为草稿，用户可以稍后继续编辑
                reimbursement.status = Reimbursement.Status.DRAFT
                reimbursement.save()
                formset.instance = reimbursement
                formset.save()
                
                # 处理上传的发票文件，支持多文件上传
                files = request.FILES.getlist('files')
                for f in files:
                    Invoice.objects.create(reimbursement=reimbursement, file=f)
                
                # 重新计算总金额
                reimbursement.calculate_total()
                messages.info(request, '报销单已暂存，您可以稍后继续编辑')
            else:
                # 正式提交：状态设为待处理，等待负责人审核
                reimbursement.status = Reimbursement.Status.SUBMITTED
                reimbursement.save()
                
                formset.instance = reimbursement
                formset.save()
                
                # 处理上传的发票文件
                files = request.FILES.getlist('files')
                for f in files:
                    Invoice.objects.create(reimbursement=reimbursement, file=f)
                
                # 重新计算总金额
                reimbursement.calculate_total()
                messages.success(request, '报销单提交成功！')
            
            return redirect('dashboard')
    else:
        # GET请求：显示空表单
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
    """
    编辑报销单视图
    只允许编辑草稿状态或已驳回状态的报销单
    已提交或已打包的报销单不允许编辑
    """
    reimbursement = get_object_or_404(Reimbursement, pk=pk)
    
    # 权限检查：只能编辑自己的报销单
    if reimbursement.applicant != request.user:
        messages.error(request, "您没有权限编辑此报销单")
        return redirect('dashboard')
    
    # 状态检查：只有草稿或已驳回状态的报销单可以编辑
    if reimbursement.status not in [Reimbursement.Status.DRAFT, Reimbursement.Status.REJECTED]:
        messages.error(request, "只有草稿或已驳回状态的报销单可以编辑")
        return redirect('reimbursement_detail', pk=pk)
    
    if request.method == 'POST':
        form = ReimbursementForm(request.POST, instance=reimbursement)
        formset = ReimbursementItemFormSet(request.POST, instance=reimbursement)
        invoice_form = InvoiceUploadForm(request.POST, request.FILES)
        
        if form.is_valid() and formset.is_valid():
            reimbursement = form.save(commit=False)
            
            # 根据提交按钮判断是暂存还是重新提交
            if 'save_draft' in request.POST:
                reimbursement.status = Reimbursement.Status.DRAFT
                reimbursement.save()
                formset.save()
                
                # 处理新上传的发票文件
                files = request.FILES.getlist('files')
                for f in files:
                    Invoice.objects.create(reimbursement=reimbursement, file=f)
                
                reimbursement.calculate_total()
                messages.info(request, '报销单已暂存')
            else:
                # 重新提交：状态改为待处理，等待审核
                reimbursement.status = Reimbursement.Status.SUBMITTED
                reimbursement.save()
                
                formset.save()
                
                # 处理新上传的发票文件
                files = request.FILES.getlist('files')
                for f in files:
                    Invoice.objects.create(reimbursement=reimbursement, file=f)
                
                reimbursement.calculate_total()
                messages.success(request, '报销单已重新提交！')
            
            return redirect('dashboard')
    else:
        # GET请求：显示编辑表单，预填充现有数据
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
    """
    报销单详情视图
    显示报销单的完整信息，包括物品明细和发票
    普通用户只能查看自己的报销单，负责人可以查看本部门的报销单
    """
    reimbursement = get_object_or_404(Reimbursement, pk=pk)
    
    # 权限检查：普通用户只能查看自己的，负责人可以查看本部门的
    if not request.user.is_lead and reimbursement.applicant != request.user:
        messages.error(request, "您没有权限查看此报销单")
        return redirect('dashboard')

    return render(request, 'claims/reimbursement_detail.html', {
        'reimbursement': reimbursement
    })

@login_required
def review_reimbursement(request, pk):
    """
    审核报销单视图
    只有负责人可以执行审核操作
    支持通过（标记为已打包）和驳回两种操作
    """
    # 权限检查：只有负责人可以审核
    if not request.user.is_lead:
        return redirect('dashboard')
        
    reimbursement = get_object_or_404(Reimbursement, pk=pk)
    
    if request.method == 'POST':
        action = request.POST.get('action')
        note = request.POST.get('note', '')
        
        # 保存审核备注
        reimbursement.reviewer_note = note
        
        # 根据操作类型更新状态
        if action == 'approve':
            # 审核通过：标记为已打包
            reimbursement.status = Reimbursement.Status.PACKED
            messages.success(request, '已标记为已打包')
        elif action == 'reject':
            # 审核驳回：标记为已驳回，申请人可以修改后重新提交
            reimbursement.status = Reimbursement.Status.REJECTED
            messages.warning(request, '已驳回该申请')
            
        reimbursement.save()
        return redirect('dashboard')
        
    return redirect('reimbursement_detail', pk=pk)

@login_required
def export_claims(request):
    """
    导出报销单视图
    负责人可以将本部门的报销单导出为ZIP文件
    ZIP文件包含：Excel汇总表、Word活动说明、所有发票文件
    """
    # 权限检查：只有负责人可以导出
    if not request.user.is_lead:
        messages.error(request, "无权限执行此操作")
        return redirect('dashboard')

    # 获取本部门的所有报销单，排除草稿和已驳回的
    dept_filter = request.user.organization or request.user.department
    claims = Reimbursement.objects.filter(
        department=dept_filter
    ).exclude(status=Reimbursement.Status.DRAFT).exclude(status=Reimbursement.Status.REJECTED)

    if not claims.exists():
        messages.warning(request, "没有可导出的报销单")
        return redirect('dashboard')

    # 在内存中创建ZIP文件，避免临时文件
    buffer = io.BytesIO()
    with zipfile.ZipFile(buffer, 'w', zipfile.ZIP_DEFLATED) as zip_file:
        
        # 1. 生成Excel汇总表
        wb = openpyxl.Workbook()
        ws = wb.active
        ws.title = "报销汇总"
        # 设置表头
        ws.append(['申请人', '学号', '部门', '主题', '内容', '总金额', '提交时间', '状态'])
        
        # 2. 生成Word活动说明文档
        doc = Document()
        doc.add_heading('报销活动情况说明汇总', 0)
        
        for claim in claims:
            # 将数据添加到Excel表格
            ws.append([
                claim.applicant.username,
                claim.applicant.student_id,
                claim.department,
                claim.theme,
                claim.description,
                claim.total_amount,
                claim.created_at.strftime('%Y-%m-%d %H:%M'),
                claim.get_status_display()
            ])
            
            # 将活动说明添加到Word文档
            doc.add_heading(f"{claim.theme} - {claim.applicant.username}", level=1)
            doc.add_paragraph(f"部门: {claim.department}")
            doc.add_paragraph(f"时间: {claim.created_at.strftime('%Y-%m-%d')}")
            doc.add_paragraph("情况说明:")
            doc.add_paragraph(claim.description or "无")
            doc.add_paragraph("-" * 20)

            # 3. 将发票文件添加到ZIP
            # 按报销单ID和主题创建文件夹，便于分类
            folder_name = f"{claim.id}_{claim.theme}_{claim.applicant.username}"
            # 清理文件夹名称，只保留字母数字和常用符号
            folder_name = "".join([c for c in folder_name if c.isalnum() or c in (' ', '_', '-')]).strip()
            
            for invoice in claim.invoices.all():
                try:
                    # 读取发票文件并添加到ZIP
                    file_path = invoice.file.path
                    # 在ZIP中的路径：文件夹名/文件名
                    arcname = f"{folder_name}/{invoice.file.name.split('/')[-1]}"
                    zip_file.write(file_path, arcname=arcname)
                except Exception as e:
                    # 如果文件读取失败，记录错误但不中断导出
                    print(f"Error packing file {invoice.file}: {e}")

        # 将Excel文件保存到ZIP
        excel_buffer = io.BytesIO()
        wb.save(excel_buffer)
        zip_file.writestr("报销汇总表.xlsx", excel_buffer.getvalue())

        # 将Word文档保存到ZIP
        doc_buffer = io.BytesIO()
        doc.save(doc_buffer)
        zip_file.writestr("活动情况说明汇总.docx", doc_buffer.getvalue())

    # 将内存中的ZIP文件作为HTTP响应返回
    buffer.seek(0)
    response = HttpResponse(buffer, content_type='application/zip')
    # 生成带时间戳的文件名，避免文件名冲突
    filename = f"Reimbursement_Export_{timezone.now().strftime('%Y%m%d%H%M')}.zip"
    response['Content-Disposition'] = f'attachment; filename="{filename}"'
    return response
