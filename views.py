"""
Training & Skills Module Views
"""
from django.utils.translation import gettext_lazy as _
from django.utils import timezone

from apps.accounts.decorators import login_required
from apps.core.htmx import htmx_view
from apps.modules_runtime.navigation import with_module_nav


@login_required
@with_module_nav('training', 'dashboard')
@htmx_view('training/pages/dashboard.html', 'training/partials/dashboard_content.html')
def dashboard(request):
    """Dashboard view."""
    hub_id = request.session.get('hub_id')
    return {}


@login_required
@with_module_nav('training', 'programs')
@htmx_view('training/pages/programs.html', 'training/partials/programs_content.html')
def programs(request):
    """Programs view."""
    hub_id = request.session.get('hub_id')
    return {}


@login_required
@with_module_nav('training', 'skills')
@htmx_view('training/pages/skills.html', 'training/partials/skills_content.html')
def skills(request):
    """Skills view."""
    hub_id = request.session.get('hub_id')
    return {}


@login_required
@with_module_nav('training', 'settings')
@htmx_view('training/pages/settings.html', 'training/partials/settings_content.html')
def settings(request):
    """Settings view."""
    hub_id = request.session.get('hub_id')
    return {}

