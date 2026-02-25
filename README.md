# Training & Skills Module

Employee training programs and skill tracking.

## Features

- Define training programs with description, duration in hours, and mandatory flag
- Maintain a skill catalog organized by category
- Track employee training enrollments with start dates, completion dates, and scores
- Monitor training status (enrolled, in progress, completed, etc.)
- Mark programs as mandatory for compliance tracking
- Dashboard with training progress and skill coverage metrics

## Installation

This module is installed automatically via the ERPlora Marketplace.

## Configuration

Access settings via: **Menu > Training & Skills > Settings**

## Usage

Access via: **Menu > Training & Skills**

### Views

| View | URL | Description |
|------|-----|-------------|
| Dashboard | `/m/training/dashboard/` | Training progress and skill overview |
| Programs | `/m/training/programs/` | Create and manage training programs |
| Skills | `/m/training/skills/` | Maintain skill catalog and categories |
| Settings | `/m/training/settings/` | Module configuration |

## Models

| Model | Description |
|-------|-------------|
| `TrainingProgram` | Training program with name, description, duration in hours, mandatory flag, and active status |
| `Skill` | Skill definition with name, category, and active status |
| `EmployeeTraining` | Employee training enrollment linking an employee to a program with status, start/completion dates, and score |

## Permissions

| Permission | Description |
|------------|-------------|
| `training.view_trainingprogram` | View training programs |
| `training.add_trainingprogram` | Create new training programs |
| `training.change_trainingprogram` | Edit existing training programs |
| `training.delete_trainingprogram` | Delete training programs |
| `training.view_skill` | View skills catalog |
| `training.manage_settings` | Manage module settings |

## License

MIT

## Author

ERPlora Team - support@erplora.com
