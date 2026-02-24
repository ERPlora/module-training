"""
Training & Skills Module Views
"""
from django.core.paginator import Paginator
from django.db.models import Q, Count
from django.shortcuts import get_object_or_404, render as django_render
from django.utils import timezone
from django.utils.translation import gettext_lazy as _
from django.views.decorators.http import require_POST

from apps.accounts.decorators import login_required
from apps.core.htmx import htmx_view
from apps.core.services import export_to_csv, export_to_excel
from apps.modules_runtime.navigation import with_module_nav

from .models import TrainingProgram, Skill, EmployeeTraining

PER_PAGE_CHOICES = [10, 25, 50, 100]


# ======================================================================
# Dashboard
# ======================================================================

@login_required
@with_module_nav('training', 'dashboard')
@htmx_view('training/pages/index.html', 'training/partials/dashboard_content.html')
def dashboard(request):
    hub_id = request.session.get('hub_id')
    return {
        'total_training_programs': TrainingProgram.objects.filter(hub_id=hub_id, is_deleted=False).count(),
        'total_skills': Skill.objects.filter(hub_id=hub_id, is_deleted=False).count(),
        'total_employee_trainings': EmployeeTraining.objects.filter(hub_id=hub_id, is_deleted=False).count(),
    }


# ======================================================================
# TrainingProgram
# ======================================================================

TRAINING_PROGRAM_SORT_FIELDS = {
    'name': 'name',
    'is_mandatory': 'is_mandatory',
    'is_active': 'is_active',
    'duration_hours': 'duration_hours',
    'description': 'description',
    'created_at': 'created_at',
}

def _build_training_programs_context(hub_id, per_page=10):
    qs = TrainingProgram.objects.filter(hub_id=hub_id, is_deleted=False).order_by('name')
    paginator = Paginator(qs, per_page)
    page_obj = paginator.get_page(1)
    return {
        'training_programs': page_obj,
        'page_obj': page_obj,
        'search_query': '',
        'sort_field': 'name',
        'sort_dir': 'asc',
        'current_view': 'table',
        'per_page': per_page,
    }

def _render_training_programs_list(request, hub_id, per_page=10):
    ctx = _build_training_programs_context(hub_id, per_page)
    return django_render(request, 'training/partials/training_programs_list.html', ctx)

@login_required
@with_module_nav('training', 'programs')
@htmx_view('training/pages/training_programs.html', 'training/partials/training_programs_content.html')
def training_programs_list(request):
    hub_id = request.session.get('hub_id')
    search_query = request.GET.get('q', '').strip()
    sort_field = request.GET.get('sort', 'name')
    sort_dir = request.GET.get('dir', 'asc')
    page_number = request.GET.get('page', 1)
    current_view = request.GET.get('view', 'table')
    per_page = int(request.GET.get('per_page', 10))
    if per_page not in PER_PAGE_CHOICES:
        per_page = 10

    qs = TrainingProgram.objects.filter(hub_id=hub_id, is_deleted=False)

    if search_query:
        qs = qs.filter(Q(name__icontains=search_query) | Q(description__icontains=search_query))

    order_by = TRAINING_PROGRAM_SORT_FIELDS.get(sort_field, 'name')
    if sort_dir == 'desc':
        order_by = f'-{order_by}'
    qs = qs.order_by(order_by)

    export_format = request.GET.get('export')
    if export_format in ('csv', 'excel'):
        fields = ['name', 'is_mandatory', 'is_active', 'duration_hours', 'description']
        headers = ['Name', 'Is Mandatory', 'Is Active', 'Duration Hours', 'Description']
        if export_format == 'csv':
            return export_to_csv(qs, fields=fields, headers=headers, filename='training_programs.csv')
        return export_to_excel(qs, fields=fields, headers=headers, filename='training_programs.xlsx')

    paginator = Paginator(qs, per_page)
    page_obj = paginator.get_page(page_number)

    if request.htmx and request.htmx.target == 'datatable-body':
        return django_render(request, 'training/partials/training_programs_list.html', {
            'training_programs': page_obj, 'page_obj': page_obj,
            'search_query': search_query, 'sort_field': sort_field,
            'sort_dir': sort_dir, 'current_view': current_view, 'per_page': per_page,
        })

    return {
        'training_programs': page_obj, 'page_obj': page_obj,
        'search_query': search_query, 'sort_field': sort_field,
        'sort_dir': sort_dir, 'current_view': current_view, 'per_page': per_page,
    }

@login_required
def training_program_add(request):
    hub_id = request.session.get('hub_id')
    if request.method == 'POST':
        name = request.POST.get('name', '').strip()
        description = request.POST.get('description', '').strip()
        duration_hours = int(request.POST.get('duration_hours', 0) or 0)
        is_mandatory = request.POST.get('is_mandatory') == 'on'
        is_active = request.POST.get('is_active') == 'on'
        obj = TrainingProgram(hub_id=hub_id)
        obj.name = name
        obj.description = description
        obj.duration_hours = duration_hours
        obj.is_mandatory = is_mandatory
        obj.is_active = is_active
        obj.save()
        return _render_training_programs_list(request, hub_id)
    return django_render(request, 'training/partials/panel_training_program_add.html', {})

@login_required
def training_program_edit(request, pk):
    hub_id = request.session.get('hub_id')
    obj = get_object_or_404(TrainingProgram, pk=pk, hub_id=hub_id, is_deleted=False)
    if request.method == 'POST':
        obj.name = request.POST.get('name', '').strip()
        obj.description = request.POST.get('description', '').strip()
        obj.duration_hours = int(request.POST.get('duration_hours', 0) or 0)
        obj.is_mandatory = request.POST.get('is_mandatory') == 'on'
        obj.is_active = request.POST.get('is_active') == 'on'
        obj.save()
        return _render_training_programs_list(request, hub_id)
    return django_render(request, 'training/partials/panel_training_program_edit.html', {'obj': obj})

@login_required
@require_POST
def training_program_delete(request, pk):
    hub_id = request.session.get('hub_id')
    obj = get_object_or_404(TrainingProgram, pk=pk, hub_id=hub_id, is_deleted=False)
    obj.is_deleted = True
    obj.deleted_at = timezone.now()
    obj.save(update_fields=['is_deleted', 'deleted_at', 'updated_at'])
    return _render_training_programs_list(request, hub_id)

@login_required
@require_POST
def training_program_toggle_status(request, pk):
    hub_id = request.session.get('hub_id')
    obj = get_object_or_404(TrainingProgram, pk=pk, hub_id=hub_id, is_deleted=False)
    obj.is_active = not obj.is_active
    obj.save(update_fields=['is_active', 'updated_at'])
    return _render_training_programs_list(request, hub_id)

@login_required
@require_POST
def training_programs_bulk_action(request):
    hub_id = request.session.get('hub_id')
    ids = [i.strip() for i in request.POST.get('ids', '').split(',') if i.strip()]
    action = request.POST.get('action', '')
    qs = TrainingProgram.objects.filter(hub_id=hub_id, is_deleted=False, id__in=ids)
    if action == 'activate':
        qs.update(is_active=True)
    elif action == 'deactivate':
        qs.update(is_active=False)
    elif action == 'delete':
        qs.update(is_deleted=True, deleted_at=timezone.now())
    return _render_training_programs_list(request, hub_id)


# ======================================================================
# Skill
# ======================================================================

SKILL_SORT_FIELDS = {
    'name': 'name',
    'is_active': 'is_active',
    'category': 'category',
    'created_at': 'created_at',
}

def _build_skills_context(hub_id, per_page=10):
    qs = Skill.objects.filter(hub_id=hub_id, is_deleted=False).order_by('name')
    paginator = Paginator(qs, per_page)
    page_obj = paginator.get_page(1)
    return {
        'skills': page_obj,
        'page_obj': page_obj,
        'search_query': '',
        'sort_field': 'name',
        'sort_dir': 'asc',
        'current_view': 'table',
        'per_page': per_page,
    }

def _render_skills_list(request, hub_id, per_page=10):
    ctx = _build_skills_context(hub_id, per_page)
    return django_render(request, 'training/partials/skills_list.html', ctx)

@login_required
@with_module_nav('training', 'skills')
@htmx_view('training/pages/skills.html', 'training/partials/skills_content.html')
def skills_list(request):
    hub_id = request.session.get('hub_id')
    search_query = request.GET.get('q', '').strip()
    sort_field = request.GET.get('sort', 'name')
    sort_dir = request.GET.get('dir', 'asc')
    page_number = request.GET.get('page', 1)
    current_view = request.GET.get('view', 'table')
    per_page = int(request.GET.get('per_page', 10))
    if per_page not in PER_PAGE_CHOICES:
        per_page = 10

    qs = Skill.objects.filter(hub_id=hub_id, is_deleted=False)

    if search_query:
        qs = qs.filter(Q(name__icontains=search_query) | Q(category__icontains=search_query))

    order_by = SKILL_SORT_FIELDS.get(sort_field, 'name')
    if sort_dir == 'desc':
        order_by = f'-{order_by}'
    qs = qs.order_by(order_by)

    export_format = request.GET.get('export')
    if export_format in ('csv', 'excel'):
        fields = ['name', 'is_active', 'category']
        headers = ['Name', 'Is Active', 'Category']
        if export_format == 'csv':
            return export_to_csv(qs, fields=fields, headers=headers, filename='skills.csv')
        return export_to_excel(qs, fields=fields, headers=headers, filename='skills.xlsx')

    paginator = Paginator(qs, per_page)
    page_obj = paginator.get_page(page_number)

    if request.htmx and request.htmx.target == 'datatable-body':
        return django_render(request, 'training/partials/skills_list.html', {
            'skills': page_obj, 'page_obj': page_obj,
            'search_query': search_query, 'sort_field': sort_field,
            'sort_dir': sort_dir, 'current_view': current_view, 'per_page': per_page,
        })

    return {
        'skills': page_obj, 'page_obj': page_obj,
        'search_query': search_query, 'sort_field': sort_field,
        'sort_dir': sort_dir, 'current_view': current_view, 'per_page': per_page,
    }

@login_required
def skill_add(request):
    hub_id = request.session.get('hub_id')
    if request.method == 'POST':
        name = request.POST.get('name', '').strip()
        category = request.POST.get('category', '').strip()
        is_active = request.POST.get('is_active') == 'on'
        obj = Skill(hub_id=hub_id)
        obj.name = name
        obj.category = category
        obj.is_active = is_active
        obj.save()
        return _render_skills_list(request, hub_id)
    return django_render(request, 'training/partials/panel_skill_add.html', {})

@login_required
def skill_edit(request, pk):
    hub_id = request.session.get('hub_id')
    obj = get_object_or_404(Skill, pk=pk, hub_id=hub_id, is_deleted=False)
    if request.method == 'POST':
        obj.name = request.POST.get('name', '').strip()
        obj.category = request.POST.get('category', '').strip()
        obj.is_active = request.POST.get('is_active') == 'on'
        obj.save()
        return _render_skills_list(request, hub_id)
    return django_render(request, 'training/partials/panel_skill_edit.html', {'obj': obj})

@login_required
@require_POST
def skill_delete(request, pk):
    hub_id = request.session.get('hub_id')
    obj = get_object_or_404(Skill, pk=pk, hub_id=hub_id, is_deleted=False)
    obj.is_deleted = True
    obj.deleted_at = timezone.now()
    obj.save(update_fields=['is_deleted', 'deleted_at', 'updated_at'])
    return _render_skills_list(request, hub_id)

@login_required
@require_POST
def skill_toggle_status(request, pk):
    hub_id = request.session.get('hub_id')
    obj = get_object_or_404(Skill, pk=pk, hub_id=hub_id, is_deleted=False)
    obj.is_active = not obj.is_active
    obj.save(update_fields=['is_active', 'updated_at'])
    return _render_skills_list(request, hub_id)

@login_required
@require_POST
def skills_bulk_action(request):
    hub_id = request.session.get('hub_id')
    ids = [i.strip() for i in request.POST.get('ids', '').split(',') if i.strip()]
    action = request.POST.get('action', '')
    qs = Skill.objects.filter(hub_id=hub_id, is_deleted=False, id__in=ids)
    if action == 'activate':
        qs.update(is_active=True)
    elif action == 'deactivate':
        qs.update(is_active=False)
    elif action == 'delete':
        qs.update(is_deleted=True, deleted_at=timezone.now())
    return _render_skills_list(request, hub_id)


# ======================================================================
# EmployeeTraining
# ======================================================================

EMPLOYEE_TRAINING_SORT_FIELDS = {
    'program': 'program',
    'status': 'status',
    'score': 'score',
    'employee_id': 'employee_id',
    'employee_name': 'employee_name',
    'start_date': 'start_date',
    'created_at': 'created_at',
}

def _build_employee_trainings_context(hub_id, per_page=10):
    qs = EmployeeTraining.objects.filter(hub_id=hub_id, is_deleted=False).order_by('program')
    paginator = Paginator(qs, per_page)
    page_obj = paginator.get_page(1)
    return {
        'employee_trainings': page_obj,
        'page_obj': page_obj,
        'search_query': '',
        'sort_field': 'program',
        'sort_dir': 'asc',
        'current_view': 'table',
        'per_page': per_page,
    }

def _render_employee_trainings_list(request, hub_id, per_page=10):
    ctx = _build_employee_trainings_context(hub_id, per_page)
    return django_render(request, 'training/partials/employee_trainings_list.html', ctx)

@login_required
@with_module_nav('training', 'programs')
@htmx_view('training/pages/employee_trainings.html', 'training/partials/employee_trainings_content.html')
def employee_trainings_list(request):
    hub_id = request.session.get('hub_id')
    search_query = request.GET.get('q', '').strip()
    sort_field = request.GET.get('sort', 'program')
    sort_dir = request.GET.get('dir', 'asc')
    page_number = request.GET.get('page', 1)
    current_view = request.GET.get('view', 'table')
    per_page = int(request.GET.get('per_page', 10))
    if per_page not in PER_PAGE_CHOICES:
        per_page = 10

    qs = EmployeeTraining.objects.filter(hub_id=hub_id, is_deleted=False)

    if search_query:
        qs = qs.filter(Q(employee_name__icontains=search_query) | Q(status__icontains=search_query))

    order_by = EMPLOYEE_TRAINING_SORT_FIELDS.get(sort_field, 'program')
    if sort_dir == 'desc':
        order_by = f'-{order_by}'
    qs = qs.order_by(order_by)

    export_format = request.GET.get('export')
    if export_format in ('csv', 'excel'):
        fields = ['program', 'status', 'score', 'employee_id', 'employee_name', 'start_date']
        headers = ['TrainingProgram', 'Status', 'Score', 'Employee Id', 'Employee Name', 'Start Date']
        if export_format == 'csv':
            return export_to_csv(qs, fields=fields, headers=headers, filename='employee_trainings.csv')
        return export_to_excel(qs, fields=fields, headers=headers, filename='employee_trainings.xlsx')

    paginator = Paginator(qs, per_page)
    page_obj = paginator.get_page(page_number)

    if request.htmx and request.htmx.target == 'datatable-body':
        return django_render(request, 'training/partials/employee_trainings_list.html', {
            'employee_trainings': page_obj, 'page_obj': page_obj,
            'search_query': search_query, 'sort_field': sort_field,
            'sort_dir': sort_dir, 'current_view': current_view, 'per_page': per_page,
        })

    return {
        'employee_trainings': page_obj, 'page_obj': page_obj,
        'search_query': search_query, 'sort_field': sort_field,
        'sort_dir': sort_dir, 'current_view': current_view, 'per_page': per_page,
    }

@login_required
def employee_training_add(request):
    hub_id = request.session.get('hub_id')
    if request.method == 'POST':
        employee_id = request.POST.get('employee_id', '').strip()
        employee_name = request.POST.get('employee_name', '').strip()
        status = request.POST.get('status', '').strip()
        start_date = request.POST.get('start_date') or None
        completion_date = request.POST.get('completion_date') or None
        score = request.POST.get('score', '0') or '0'
        obj = EmployeeTraining(hub_id=hub_id)
        obj.employee_id = employee_id
        obj.employee_name = employee_name
        obj.status = status
        obj.start_date = start_date
        obj.completion_date = completion_date
        obj.score = score
        obj.save()
        return _render_employee_trainings_list(request, hub_id)
    return django_render(request, 'training/partials/panel_employee_training_add.html', {})

@login_required
def employee_training_edit(request, pk):
    hub_id = request.session.get('hub_id')
    obj = get_object_or_404(EmployeeTraining, pk=pk, hub_id=hub_id, is_deleted=False)
    if request.method == 'POST':
        obj.employee_id = request.POST.get('employee_id', '').strip()
        obj.employee_name = request.POST.get('employee_name', '').strip()
        obj.status = request.POST.get('status', '').strip()
        obj.start_date = request.POST.get('start_date') or None
        obj.completion_date = request.POST.get('completion_date') or None
        obj.score = request.POST.get('score', '0') or '0'
        obj.save()
        return _render_employee_trainings_list(request, hub_id)
    return django_render(request, 'training/partials/panel_employee_training_edit.html', {'obj': obj})

@login_required
@require_POST
def employee_training_delete(request, pk):
    hub_id = request.session.get('hub_id')
    obj = get_object_or_404(EmployeeTraining, pk=pk, hub_id=hub_id, is_deleted=False)
    obj.is_deleted = True
    obj.deleted_at = timezone.now()
    obj.save(update_fields=['is_deleted', 'deleted_at', 'updated_at'])
    return _render_employee_trainings_list(request, hub_id)

@login_required
@require_POST
def employee_trainings_bulk_action(request):
    hub_id = request.session.get('hub_id')
    ids = [i.strip() for i in request.POST.get('ids', '').split(',') if i.strip()]
    action = request.POST.get('action', '')
    qs = EmployeeTraining.objects.filter(hub_id=hub_id, is_deleted=False, id__in=ids)
    if action == 'delete':
        qs.update(is_deleted=True, deleted_at=timezone.now())
    return _render_employee_trainings_list(request, hub_id)


@login_required
@with_module_nav('training', 'settings')
@htmx_view('training/pages/settings.html', 'training/partials/settings_content.html')
def settings_view(request):
    return {}

