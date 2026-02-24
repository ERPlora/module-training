from django import forms
from django.utils.translation import gettext_lazy as _

from .models import TrainingProgram, Skill, EmployeeTraining

class TrainingProgramForm(forms.ModelForm):
    class Meta:
        model = TrainingProgram
        fields = ['name', 'description', 'duration_hours', 'is_mandatory', 'is_active']
        widgets = {
            'name': forms.TextInput(attrs={'class': 'input input-sm w-full'}),
            'description': forms.Textarea(attrs={'class': 'textarea textarea-sm w-full', 'rows': 3}),
            'duration_hours': forms.TextInput(attrs={'class': 'input input-sm w-full', 'type': 'number'}),
            'is_mandatory': forms.CheckboxInput(attrs={'class': 'toggle'}),
            'is_active': forms.CheckboxInput(attrs={'class': 'toggle'}),
        }

class SkillForm(forms.ModelForm):
    class Meta:
        model = Skill
        fields = ['name', 'category', 'is_active']
        widgets = {
            'name': forms.TextInput(attrs={'class': 'input input-sm w-full'}),
            'category': forms.TextInput(attrs={'class': 'input input-sm w-full'}),
            'is_active': forms.CheckboxInput(attrs={'class': 'toggle'}),
        }

class EmployeeTrainingForm(forms.ModelForm):
    class Meta:
        model = EmployeeTraining
        fields = ['employee_id', 'employee_name', 'program', 'status', 'start_date', 'completion_date', 'score']
        widgets = {
            'employee_id': forms.TextInput(attrs={'class': 'input input-sm w-full'}),
            'employee_name': forms.TextInput(attrs={'class': 'input input-sm w-full'}),
            'program': forms.Select(attrs={'class': 'select select-sm w-full'}),
            'status': forms.TextInput(attrs={'class': 'input input-sm w-full'}),
            'start_date': forms.TextInput(attrs={'class': 'input input-sm w-full', 'type': 'date'}),
            'completion_date': forms.TextInput(attrs={'class': 'input input-sm w-full', 'type': 'date'}),
            'score': forms.TextInput(attrs={'class': 'input input-sm w-full', 'type': 'number'}),
        }

