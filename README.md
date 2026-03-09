# Training & Skills

## Overview

| Property | Value |
|----------|-------|
| **Module ID** | `training` |
| **Version** | `1.0.0` |
| **Icon** | `school-outline` |
| **Dependencies** | None |

## Models

### `TrainingProgram`

TrainingProgram(id, hub_id, created_at, updated_at, created_by, updated_by, is_deleted, deleted_at, name, description, duration_hours, is_mandatory, is_active)

| Field | Type | Details |
|-------|------|---------|
| `name` | CharField | max_length=255 |
| `description` | TextField | optional |
| `duration_hours` | PositiveIntegerField |  |
| `is_mandatory` | BooleanField |  |
| `is_active` | BooleanField |  |

### `Skill`

Skill(id, hub_id, created_at, updated_at, created_by, updated_by, is_deleted, deleted_at, name, category, is_active)

| Field | Type | Details |
|-------|------|---------|
| `name` | CharField | max_length=100 |
| `category` | CharField | max_length=100, optional |
| `is_active` | BooleanField |  |

### `EmployeeTraining`

EmployeeTraining(id, hub_id, created_at, updated_at, created_by, updated_by, is_deleted, deleted_at, employee_id, employee_name, program, status, start_date, completion_date, score)

| Field | Type | Details |
|-------|------|---------|
| `employee_id` | UUIDField | max_length=32 |
| `employee_name` | CharField | max_length=255 |
| `program` | ForeignKey | → `training.TrainingProgram`, on_delete=CASCADE |
| `status` | CharField | max_length=20 |
| `start_date` | DateField | optional |
| `completion_date` | DateField | optional |
| `score` | DecimalField | optional |

## Cross-Module Relationships

| From | Field | To | on_delete | Nullable |
|------|-------|----|-----------|----------|
| `EmployeeTraining` | `program` | `training.TrainingProgram` | CASCADE | No |

## URL Endpoints

Base path: `/m/training/`

| Path | Name | Method |
|------|------|--------|
| `(root)` | `dashboard` | GET |
| `programs/` | `programs` | GET |
| `training_programs/` | `training_programs_list` | GET |
| `training_programs/add/` | `training_program_add` | GET/POST |
| `training_programs/<uuid:pk>/edit/` | `training_program_edit` | GET |
| `training_programs/<uuid:pk>/delete/` | `training_program_delete` | GET/POST |
| `training_programs/<uuid:pk>/toggle/` | `training_program_toggle_status` | GET |
| `training_programs/bulk/` | `training_programs_bulk_action` | GET/POST |
| `skills/` | `skills_list` | GET |
| `skills/add/` | `skill_add` | GET/POST |
| `skills/<uuid:pk>/edit/` | `skill_edit` | GET |
| `skills/<uuid:pk>/delete/` | `skill_delete` | GET/POST |
| `skills/<uuid:pk>/toggle/` | `skill_toggle_status` | GET |
| `skills/bulk/` | `skills_bulk_action` | GET/POST |
| `employee_trainings/` | `employee_trainings_list` | GET |
| `employee_trainings/add/` | `employee_training_add` | GET/POST |
| `employee_trainings/<uuid:pk>/edit/` | `employee_training_edit` | GET |
| `employee_trainings/<uuid:pk>/delete/` | `employee_training_delete` | GET/POST |
| `employee_trainings/bulk/` | `employee_trainings_bulk_action` | GET/POST |
| `settings/` | `settings` | GET |

## Permissions

| Permission | Description |
|------------|-------------|
| `training.view_trainingprogram` | View Trainingprogram |
| `training.add_trainingprogram` | Add Trainingprogram |
| `training.change_trainingprogram` | Change Trainingprogram |
| `training.delete_trainingprogram` | Delete Trainingprogram |
| `training.view_skill` | View Skill |
| `training.manage_settings` | Manage Settings |

**Role assignments:**

- **admin**: All permissions
- **manager**: `add_trainingprogram`, `change_trainingprogram`, `view_skill`, `view_trainingprogram`
- **employee**: `add_trainingprogram`, `view_skill`, `view_trainingprogram`

## Navigation

| View | Icon | ID | Fullpage |
|------|------|----|----------|
| Dashboard | `speedometer-outline` | `dashboard` | No |
| Programs | `school-outline` | `programs` | No |
| Skills | `ribbon-outline` | `skills` | No |
| Settings | `settings-outline` | `settings` | No |

## AI Tools

Tools available for the AI assistant:

### `list_training_programs`

List training programs.

| Parameter | Type | Required | Description |
|-----------|------|----------|-------------|
| `is_active` | boolean | No |  |
| `is_mandatory` | boolean | No |  |

### `create_training_program`

Create a training program.

| Parameter | Type | Required | Description |
|-----------|------|----------|-------------|
| `name` | string | Yes |  |
| `description` | string | No |  |
| `duration_hours` | integer | No |  |
| `is_mandatory` | boolean | No |  |

### `enroll_employee_in_training`

Enroll an employee in a training program.

| Parameter | Type | Required | Description |
|-----------|------|----------|-------------|
| `employee_id` | string | Yes |  |
| `employee_name` | string | Yes |  |
| `program_id` | string | Yes |  |
| `start_date` | string | No |  |

## File Structure

```
README.md
__init__.py
admin.py
ai_tools.py
apps.py
forms.py
locale/
  en/
    LC_MESSAGES/
      django.po
  es/
    LC_MESSAGES/
      django.po
migrations/
  0001_initial.py
  __init__.py
models.py
module.py
static/
  icons/
    icon.svg
  training/
    css/
    js/
templates/
  training/
    pages/
      dashboard.html
      employee_training_add.html
      employee_training_edit.html
      employee_trainings.html
      index.html
      programs.html
      settings.html
      skill_add.html
      skill_edit.html
      skills.html
      training_program_add.html
      training_program_edit.html
      training_programs.html
    partials/
      dashboard_content.html
      employee_training_add_content.html
      employee_training_edit_content.html
      employee_trainings_content.html
      employee_trainings_list.html
      panel_employee_training_add.html
      panel_employee_training_edit.html
      panel_skill_add.html
      panel_skill_edit.html
      panel_training_program_add.html
      panel_training_program_edit.html
      programs_content.html
      settings_content.html
      skill_add_content.html
      skill_edit_content.html
      skills_content.html
      skills_list.html
      training_program_add_content.html
      training_program_edit_content.html
      training_programs_content.html
      training_programs_list.html
tests/
  __init__.py
  conftest.py
  test_models.py
  test_views.py
urls.py
views.py
```
