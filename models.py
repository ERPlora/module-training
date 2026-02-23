from django.db import models
from django.utils.translation import gettext_lazy as _

from apps.core.models.base import HubBaseModel

class TrainingProgram(HubBaseModel):
    name = models.CharField(max_length=255, verbose_name=_('Name'))
    description = models.TextField(blank=True, verbose_name=_('Description'))
    duration_hours = models.PositiveIntegerField(default=0, verbose_name=_('Duration Hours'))
    is_mandatory = models.BooleanField(default=False, verbose_name=_('Is Mandatory'))
    is_active = models.BooleanField(default=True, verbose_name=_('Is Active'))

    class Meta(HubBaseModel.Meta):
        db_table = 'training_trainingprogram'

    def __str__(self):
        return self.name


class Skill(HubBaseModel):
    name = models.CharField(max_length=100, verbose_name=_('Name'))
    category = models.CharField(max_length=100, blank=True, verbose_name=_('Category'))
    is_active = models.BooleanField(default=True, verbose_name=_('Is Active'))

    class Meta(HubBaseModel.Meta):
        db_table = 'training_skill'

    def __str__(self):
        return self.name


class EmployeeTraining(HubBaseModel):
    employee_id = models.UUIDField(db_index=True, verbose_name=_('Employee Id'))
    employee_name = models.CharField(max_length=255, verbose_name=_('Employee Name'))
    program = models.ForeignKey('TrainingProgram', on_delete=models.CASCADE)
    status = models.CharField(max_length=20, default='enrolled', verbose_name=_('Status'))
    start_date = models.DateField(null=True, blank=True, verbose_name=_('Start Date'))
    completion_date = models.DateField(null=True, blank=True, verbose_name=_('Completion Date'))
    score = models.DecimalField(max_digits=5, decimal_places=2, null=True, blank=True, verbose_name=_('Score'))

    class Meta(HubBaseModel.Meta):
        db_table = 'training_employeetraining'

    def __str__(self):
        return str(self.id)

