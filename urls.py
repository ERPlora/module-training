from django.urls import path
from . import views

app_name = 'training'

urlpatterns = [
    # Dashboard
    path('', views.dashboard, name='dashboard'),

    # TrainingProgram
    path('training_programs/', views.training_programs_list, name='training_programs_list'),
    path('training_programs/add/', views.training_program_add, name='training_program_add'),
    path('training_programs/<uuid:pk>/edit/', views.training_program_edit, name='training_program_edit'),
    path('training_programs/<uuid:pk>/delete/', views.training_program_delete, name='training_program_delete'),
    path('training_programs/<uuid:pk>/toggle/', views.training_program_toggle_status, name='training_program_toggle_status'),
    path('training_programs/bulk/', views.training_programs_bulk_action, name='training_programs_bulk_action'),

    # Skill
    path('skills/', views.skills_list, name='skills_list'),
    path('skills/add/', views.skill_add, name='skill_add'),
    path('skills/<uuid:pk>/edit/', views.skill_edit, name='skill_edit'),
    path('skills/<uuid:pk>/delete/', views.skill_delete, name='skill_delete'),
    path('skills/<uuid:pk>/toggle/', views.skill_toggle_status, name='skill_toggle_status'),
    path('skills/bulk/', views.skills_bulk_action, name='skills_bulk_action'),

    # EmployeeTraining
    path('employee_trainings/', views.employee_trainings_list, name='employee_trainings_list'),
    path('employee_trainings/add/', views.employee_training_add, name='employee_training_add'),
    path('employee_trainings/<uuid:pk>/edit/', views.employee_training_edit, name='employee_training_edit'),
    path('employee_trainings/<uuid:pk>/delete/', views.employee_training_delete, name='employee_training_delete'),
    path('employee_trainings/bulk/', views.employee_trainings_bulk_action, name='employee_trainings_bulk_action'),

    # Settings
    path('settings/', views.settings_view, name='settings'),
]
