from django.contrib import admin

from .models import TrainingProgram, Skill, EmployeeTraining

@admin.register(TrainingProgram)
class TrainingProgramAdmin(admin.ModelAdmin):
    list_display = ['name', 'duration_hours', 'is_mandatory', 'is_active', 'created_at']
    search_fields = ['name', 'description']
    readonly_fields = ['created_at', 'updated_at']

@admin.register(Skill)
class SkillAdmin(admin.ModelAdmin):
    list_display = ['name', 'category', 'is_active', 'created_at']
    search_fields = ['name', 'category']
    readonly_fields = ['created_at', 'updated_at']

@admin.register(EmployeeTraining)
class EmployeeTrainingAdmin(admin.ModelAdmin):
    list_display = ['employee_id', 'employee_name', 'program', 'status', 'start_date', 'created_at']
    search_fields = ['employee_name', 'status']
    readonly_fields = ['created_at', 'updated_at']

