"""Tests for training views."""
import pytest
from django.urls import reverse


@pytest.mark.django_db
class TestDashboard:
    """Dashboard view tests."""

    def test_dashboard_loads(self, auth_client):
        """Test dashboard page loads."""
        url = reverse('training:dashboard')
        response = auth_client.get(url)
        assert response.status_code == 200

    def test_dashboard_htmx(self, auth_client):
        """Test dashboard HTMX partial."""
        url = reverse('training:dashboard')
        response = auth_client.get(url, HTTP_HX_REQUEST='true')
        assert response.status_code == 200

    def test_dashboard_requires_auth(self, client):
        """Test dashboard requires authentication."""
        url = reverse('training:dashboard')
        response = client.get(url)
        assert response.status_code == 302


@pytest.mark.django_db
class TestTrainingProgramViews:
    """TrainingProgram view tests."""

    def test_list_loads(self, auth_client):
        """Test list view loads."""
        url = reverse('training:training_programs_list')
        response = auth_client.get(url)
        assert response.status_code == 200

    def test_list_htmx(self, auth_client):
        """Test list HTMX partial."""
        url = reverse('training:training_programs_list')
        response = auth_client.get(url, HTTP_HX_REQUEST='true')
        assert response.status_code == 200

    def test_list_search(self, auth_client):
        """Test list search."""
        url = reverse('training:training_programs_list')
        response = auth_client.get(url, {'q': 'test'})
        assert response.status_code == 200

    def test_list_sort(self, auth_client):
        """Test list sorting."""
        url = reverse('training:training_programs_list')
        response = auth_client.get(url, {'sort': 'created_at', 'dir': 'desc'})
        assert response.status_code == 200

    def test_export_csv(self, auth_client):
        """Test CSV export."""
        url = reverse('training:training_programs_list')
        response = auth_client.get(url, {'export': 'csv'})
        assert response.status_code == 200
        assert 'text/csv' in response['Content-Type']

    def test_export_excel(self, auth_client):
        """Test Excel export."""
        url = reverse('training:training_programs_list')
        response = auth_client.get(url, {'export': 'excel'})
        assert response.status_code == 200

    def test_add_form_loads(self, auth_client):
        """Test add form loads."""
        url = reverse('training:training_program_add')
        response = auth_client.get(url)
        assert response.status_code == 200

    def test_add_post(self, auth_client):
        """Test creating via POST."""
        url = reverse('training:training_program_add')
        data = {
            'name': 'New Name',
            'description': 'Test description',
            'duration_hours': '5',
            'is_mandatory': 'on',
            'is_active': 'on',
        }
        response = auth_client.post(url, data)
        assert response.status_code == 200

    def test_edit_form_loads(self, auth_client, training_program):
        """Test edit form loads."""
        url = reverse('training:training_program_edit', args=[training_program.pk])
        response = auth_client.get(url)
        assert response.status_code == 200

    def test_edit_post(self, auth_client, training_program):
        """Test editing via POST."""
        url = reverse('training:training_program_edit', args=[training_program.pk])
        data = {
            'name': 'Updated Name',
            'description': 'Test description',
            'duration_hours': '5',
            'is_mandatory': '',
            'is_active': '',
        }
        response = auth_client.post(url, data)
        assert response.status_code == 200

    def test_delete(self, auth_client, training_program):
        """Test soft delete via POST."""
        url = reverse('training:training_program_delete', args=[training_program.pk])
        response = auth_client.post(url)
        assert response.status_code == 200
        training_program.refresh_from_db()
        assert training_program.is_deleted is True

    def test_toggle_status(self, auth_client, training_program):
        """Test toggle active status."""
        url = reverse('training:training_program_toggle_status', args=[training_program.pk])
        original = training_program.is_active
        response = auth_client.post(url)
        assert response.status_code == 200
        training_program.refresh_from_db()
        assert training_program.is_active != original

    def test_bulk_delete(self, auth_client, training_program):
        """Test bulk delete."""
        url = reverse('training:training_programs_bulk_action')
        response = auth_client.post(url, {'ids': str(training_program.pk), 'action': 'delete'})
        assert response.status_code == 200
        training_program.refresh_from_db()
        assert training_program.is_deleted is True

    def test_list_requires_auth(self, client):
        """Test list requires authentication."""
        url = reverse('training:training_programs_list')
        response = client.get(url)
        assert response.status_code == 302


@pytest.mark.django_db
class TestSkillViews:
    """Skill view tests."""

    def test_list_loads(self, auth_client):
        """Test list view loads."""
        url = reverse('training:skills_list')
        response = auth_client.get(url)
        assert response.status_code == 200

    def test_list_htmx(self, auth_client):
        """Test list HTMX partial."""
        url = reverse('training:skills_list')
        response = auth_client.get(url, HTTP_HX_REQUEST='true')
        assert response.status_code == 200

    def test_list_search(self, auth_client):
        """Test list search."""
        url = reverse('training:skills_list')
        response = auth_client.get(url, {'q': 'test'})
        assert response.status_code == 200

    def test_list_sort(self, auth_client):
        """Test list sorting."""
        url = reverse('training:skills_list')
        response = auth_client.get(url, {'sort': 'created_at', 'dir': 'desc'})
        assert response.status_code == 200

    def test_export_csv(self, auth_client):
        """Test CSV export."""
        url = reverse('training:skills_list')
        response = auth_client.get(url, {'export': 'csv'})
        assert response.status_code == 200
        assert 'text/csv' in response['Content-Type']

    def test_export_excel(self, auth_client):
        """Test Excel export."""
        url = reverse('training:skills_list')
        response = auth_client.get(url, {'export': 'excel'})
        assert response.status_code == 200

    def test_add_form_loads(self, auth_client):
        """Test add form loads."""
        url = reverse('training:skill_add')
        response = auth_client.get(url)
        assert response.status_code == 200

    def test_add_post(self, auth_client):
        """Test creating via POST."""
        url = reverse('training:skill_add')
        data = {
            'name': 'New Name',
            'category': 'New Category',
            'is_active': 'on',
        }
        response = auth_client.post(url, data)
        assert response.status_code == 200

    def test_edit_form_loads(self, auth_client, skill):
        """Test edit form loads."""
        url = reverse('training:skill_edit', args=[skill.pk])
        response = auth_client.get(url)
        assert response.status_code == 200

    def test_edit_post(self, auth_client, skill):
        """Test editing via POST."""
        url = reverse('training:skill_edit', args=[skill.pk])
        data = {
            'name': 'Updated Name',
            'category': 'Updated Category',
            'is_active': '',
        }
        response = auth_client.post(url, data)
        assert response.status_code == 200

    def test_delete(self, auth_client, skill):
        """Test soft delete via POST."""
        url = reverse('training:skill_delete', args=[skill.pk])
        response = auth_client.post(url)
        assert response.status_code == 200
        skill.refresh_from_db()
        assert skill.is_deleted is True

    def test_toggle_status(self, auth_client, skill):
        """Test toggle active status."""
        url = reverse('training:skill_toggle_status', args=[skill.pk])
        original = skill.is_active
        response = auth_client.post(url)
        assert response.status_code == 200
        skill.refresh_from_db()
        assert skill.is_active != original

    def test_bulk_delete(self, auth_client, skill):
        """Test bulk delete."""
        url = reverse('training:skills_bulk_action')
        response = auth_client.post(url, {'ids': str(skill.pk), 'action': 'delete'})
        assert response.status_code == 200
        skill.refresh_from_db()
        assert skill.is_deleted is True

    def test_list_requires_auth(self, client):
        """Test list requires authentication."""
        url = reverse('training:skills_list')
        response = client.get(url)
        assert response.status_code == 302


@pytest.mark.django_db
class TestEmployeeTrainingViews:
    """EmployeeTraining view tests."""

    def test_list_loads(self, auth_client):
        """Test list view loads."""
        url = reverse('training:employee_trainings_list')
        response = auth_client.get(url)
        assert response.status_code == 200

    def test_list_htmx(self, auth_client):
        """Test list HTMX partial."""
        url = reverse('training:employee_trainings_list')
        response = auth_client.get(url, HTTP_HX_REQUEST='true')
        assert response.status_code == 200

    def test_list_search(self, auth_client):
        """Test list search."""
        url = reverse('training:employee_trainings_list')
        response = auth_client.get(url, {'q': 'test'})
        assert response.status_code == 200

    def test_list_sort(self, auth_client):
        """Test list sorting."""
        url = reverse('training:employee_trainings_list')
        response = auth_client.get(url, {'sort': 'created_at', 'dir': 'desc'})
        assert response.status_code == 200

    def test_export_csv(self, auth_client):
        """Test CSV export."""
        url = reverse('training:employee_trainings_list')
        response = auth_client.get(url, {'export': 'csv'})
        assert response.status_code == 200
        assert 'text/csv' in response['Content-Type']

    def test_export_excel(self, auth_client):
        """Test Excel export."""
        url = reverse('training:employee_trainings_list')
        response = auth_client.get(url, {'export': 'excel'})
        assert response.status_code == 200

    def test_add_form_loads(self, auth_client):
        """Test add form loads."""
        url = reverse('training:employee_training_add')
        response = auth_client.get(url)
        assert response.status_code == 200

    def test_add_post(self, auth_client):
        """Test creating via POST."""
        url = reverse('training:employee_training_add')
        data = {
            'employee_id': 'test',
            'employee_name': 'New Employee Name',
            'status': 'New Status',
            'start_date': '2025-01-15',
        }
        response = auth_client.post(url, data)
        assert response.status_code == 200

    def test_edit_form_loads(self, auth_client, employee_training):
        """Test edit form loads."""
        url = reverse('training:employee_training_edit', args=[employee_training.pk])
        response = auth_client.get(url)
        assert response.status_code == 200

    def test_edit_post(self, auth_client, employee_training):
        """Test editing via POST."""
        url = reverse('training:employee_training_edit', args=[employee_training.pk])
        data = {
            'employee_id': 'test',
            'employee_name': 'Updated Employee Name',
            'status': 'Updated Status',
            'start_date': '2025-01-15',
        }
        response = auth_client.post(url, data)
        assert response.status_code == 200

    def test_delete(self, auth_client, employee_training):
        """Test soft delete via POST."""
        url = reverse('training:employee_training_delete', args=[employee_training.pk])
        response = auth_client.post(url)
        assert response.status_code == 200
        employee_training.refresh_from_db()
        assert employee_training.is_deleted is True

    def test_bulk_delete(self, auth_client, employee_training):
        """Test bulk delete."""
        url = reverse('training:employee_trainings_bulk_action')
        response = auth_client.post(url, {'ids': str(employee_training.pk), 'action': 'delete'})
        assert response.status_code == 200
        employee_training.refresh_from_db()
        assert employee_training.is_deleted is True

    def test_list_requires_auth(self, client):
        """Test list requires authentication."""
        url = reverse('training:employee_trainings_list')
        response = client.get(url)
        assert response.status_code == 302


@pytest.mark.django_db
class TestSettings:
    """Settings view tests."""

    def test_settings_loads(self, auth_client):
        """Test settings page loads."""
        url = reverse('training:settings')
        response = auth_client.get(url)
        assert response.status_code == 200

    def test_settings_requires_auth(self, client):
        """Test settings requires authentication."""
        url = reverse('training:settings')
        response = client.get(url)
        assert response.status_code == 302

