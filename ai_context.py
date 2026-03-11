"""
AI context for the Training module.
Loaded into the assistant system prompt when this module's tools are active.
"""

CONTEXT = """
## Module Knowledge: Training

### Models

**TrainingProgram**
- name (str), description (text), duration_hours (int)
- is_mandatory (bool), is_active (bool)

**Skill**
- name (str), category (str, optional grouping label), is_active (bool)
- Standalone skill catalog; not directly linked to programs

**EmployeeTraining**
- employee_id (UUID, indexed) — references the employee's UUID
- employee_name (str, cached)
- program (FK → TrainingProgram)
- status (str, default 'enrolled') — typical values: enrolled | in_progress | completed | failed | cancelled
- start_date (optional), completion_date (optional)
- score (Decimal, optional) — e.g. 85.00 for 85%

### Key flows

1. **Create training catalog**: Create TrainingProgram records; mark mandatory ones with is_mandatory=True
2. **Enroll employee**: Create EmployeeTraining with employee_id, program, status=enrolled, start_date
3. **Start training**: Update status → in_progress
4. **Complete training**: Update status → completed, set completion_date, set score if assessed
5. **Failed training**: Update status → failed, optionally re-enroll

### Notes

- employee_id is a UUID matching the staff member's pk (no FK enforced at DB level)
- Skills are a separate catalog — they are not linked to TrainingProgram in the model; manage separately
- There is no automatic status transition — all status changes are manual
- To check if mandatory training is complete: query EmployeeTraining for employee + is_mandatory programs + status=completed
"""
