"""Tests for training models."""
import pytest
from django.utils import timezone

from training.models import TrainingProgram, Skill, EmployeeTraining


@pytest.mark.django_db
class TestTrainingProgram:
    """TrainingProgram model tests."""

    def test_create(self, training_program):
        """Test TrainingProgram creation."""
        assert training_program.pk is not None
        assert training_program.is_deleted is False

    def test_str(self, training_program):
        """Test string representation."""
        assert str(training_program) is not None
        assert len(str(training_program)) > 0

    def test_soft_delete(self, training_program):
        """Test soft delete."""
        pk = training_program.pk
        training_program.is_deleted = True
        training_program.deleted_at = timezone.now()
        training_program.save()
        assert not TrainingProgram.objects.filter(pk=pk).exists()
        assert TrainingProgram.all_objects.filter(pk=pk).exists()

    def test_queryset_excludes_deleted(self, hub_id, training_program):
        """Test default queryset excludes deleted."""
        training_program.is_deleted = True
        training_program.deleted_at = timezone.now()
        training_program.save()
        assert TrainingProgram.objects.filter(hub_id=hub_id).count() == 0

    def test_toggle_active(self, training_program):
        """Test toggling is_active."""
        original = training_program.is_active
        training_program.is_active = not original
        training_program.save()
        training_program.refresh_from_db()
        assert training_program.is_active != original


@pytest.mark.django_db
class TestSkill:
    """Skill model tests."""

    def test_create(self, skill):
        """Test Skill creation."""
        assert skill.pk is not None
        assert skill.is_deleted is False

    def test_str(self, skill):
        """Test string representation."""
        assert str(skill) is not None
        assert len(str(skill)) > 0

    def test_soft_delete(self, skill):
        """Test soft delete."""
        pk = skill.pk
        skill.is_deleted = True
        skill.deleted_at = timezone.now()
        skill.save()
        assert not Skill.objects.filter(pk=pk).exists()
        assert Skill.all_objects.filter(pk=pk).exists()

    def test_queryset_excludes_deleted(self, hub_id, skill):
        """Test default queryset excludes deleted."""
        skill.is_deleted = True
        skill.deleted_at = timezone.now()
        skill.save()
        assert Skill.objects.filter(hub_id=hub_id).count() == 0

    def test_toggle_active(self, skill):
        """Test toggling is_active."""
        original = skill.is_active
        skill.is_active = not original
        skill.save()
        skill.refresh_from_db()
        assert skill.is_active != original


@pytest.mark.django_db
class TestEmployeeTraining:
    """EmployeeTraining model tests."""

    def test_create(self, employee_training):
        """Test EmployeeTraining creation."""
        assert employee_training.pk is not None
        assert employee_training.is_deleted is False

    def test_soft_delete(self, employee_training):
        """Test soft delete."""
        pk = employee_training.pk
        employee_training.is_deleted = True
        employee_training.deleted_at = timezone.now()
        employee_training.save()
        assert not EmployeeTraining.objects.filter(pk=pk).exists()
        assert EmployeeTraining.all_objects.filter(pk=pk).exists()

    def test_queryset_excludes_deleted(self, hub_id, employee_training):
        """Test default queryset excludes deleted."""
        employee_training.is_deleted = True
        employee_training.deleted_at = timezone.now()
        employee_training.save()
        assert EmployeeTraining.objects.filter(hub_id=hub_id).count() == 0


