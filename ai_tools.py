"""AI tools for the Training module."""
from assistant.tools import AssistantTool, register_tool


@register_tool
class ListTrainingPrograms(AssistantTool):
    name = "list_training_programs"
    description = "List training programs."
    module_id = "training"
    required_permission = "training.view_trainingprogram"
    parameters = {
        "type": "object",
        "properties": {"is_active": {"type": "boolean"}, "is_mandatory": {"type": "boolean"}},
        "required": [],
        "additionalProperties": False,
    }

    def execute(self, args, request):
        from training.models import TrainingProgram
        qs = TrainingProgram.objects.all()
        if 'is_active' in args:
            qs = qs.filter(is_active=args['is_active'])
        if 'is_mandatory' in args:
            qs = qs.filter(is_mandatory=args['is_mandatory'])
        return {"programs": [{"id": str(p.id), "name": p.name, "duration_hours": p.duration_hours, "is_mandatory": p.is_mandatory, "is_active": p.is_active} for p in qs]}


@register_tool
class CreateTrainingProgram(AssistantTool):
    name = "create_training_program"
    description = "Create a training program."
    module_id = "training"
    required_permission = "training.add_trainingprogram"
    requires_confirmation = True
    parameters = {
        "type": "object",
        "properties": {
            "name": {"type": "string"}, "description": {"type": "string"},
            "duration_hours": {"type": "integer"}, "is_mandatory": {"type": "boolean"},
        },
        "required": ["name"],
        "additionalProperties": False,
    }

    def execute(self, args, request):
        from training.models import TrainingProgram
        p = TrainingProgram.objects.create(name=args['name'], description=args.get('description', ''), duration_hours=args.get('duration_hours', 0), is_mandatory=args.get('is_mandatory', False))
        return {"id": str(p.id), "name": p.name, "created": True}


@register_tool
class EnrollEmployeeInTraining(AssistantTool):
    name = "enroll_employee_in_training"
    description = "Enroll an employee in a training program."
    module_id = "training"
    required_permission = "training.add_employeetraining"
    requires_confirmation = True
    parameters = {
        "type": "object",
        "properties": {
            "employee_id": {"type": "string"}, "employee_name": {"type": "string"},
            "program_id": {"type": "string"}, "start_date": {"type": "string"},
        },
        "required": ["employee_id", "employee_name", "program_id"],
        "additionalProperties": False,
    }

    def execute(self, args, request):
        from training.models import EmployeeTraining
        t = EmployeeTraining.objects.create(employee_id=args['employee_id'], employee_name=args['employee_name'], program_id=args['program_id'], start_date=args.get('start_date'))
        return {"id": str(t.id), "created": True}


@register_tool
class GetTrainingProgram(AssistantTool):
    name = "get_training_program"
    description = "Get details of a specific training program by ID."
    module_id = "training"
    required_permission = "training.view_trainingprogram"
    parameters = {
        "type": "object",
        "properties": {"program_id": {"type": "string"}},
        "required": ["program_id"],
        "additionalProperties": False,
    }

    def execute(self, args, request):
        from training.models import TrainingProgram
        try:
            p = TrainingProgram.objects.get(id=args['program_id'])
        except TrainingProgram.DoesNotExist:
            return {"error": "Training program not found"}
        return {"id": str(p.id), "name": p.name, "description": p.description, "duration_hours": p.duration_hours, "is_mandatory": p.is_mandatory, "is_active": p.is_active}


@register_tool
class UpdateTrainingProgram(AssistantTool):
    name = "update_training_program"
    description = "Update a training program's details."
    module_id = "training"
    required_permission = "training.change_trainingprogram"
    requires_confirmation = True
    parameters = {
        "type": "object",
        "properties": {
            "program_id": {"type": "string"},
            "name": {"type": "string"}, "description": {"type": "string"},
            "duration_hours": {"type": "integer"}, "is_mandatory": {"type": "boolean"},
            "is_active": {"type": "boolean"},
        },
        "required": ["program_id"],
        "additionalProperties": False,
    }

    def execute(self, args, request):
        from training.models import TrainingProgram
        try:
            p = TrainingProgram.objects.get(id=args['program_id'])
        except TrainingProgram.DoesNotExist:
            return {"error": "Training program not found"}
        for field in ('name', 'description', 'duration_hours', 'is_mandatory', 'is_active'):
            if field in args:
                setattr(p, field, args[field])
        p.save()
        return {"id": str(p.id), "name": p.name, "updated": True}


@register_tool
class DeleteTrainingProgram(AssistantTool):
    name = "delete_training_program"
    description = "Delete a training program by ID."
    module_id = "training"
    required_permission = "training.delete_trainingprogram"
    requires_confirmation = True
    parameters = {
        "type": "object",
        "properties": {"program_id": {"type": "string"}},
        "required": ["program_id"],
        "additionalProperties": False,
    }

    def execute(self, args, request):
        from training.models import TrainingProgram
        try:
            p = TrainingProgram.objects.get(id=args['program_id'])
        except TrainingProgram.DoesNotExist:
            return {"error": "Training program not found"}
        p.delete()
        return {"deleted": True}


@register_tool
class ListTrainingEnrollments(AssistantTool):
    name = "list_training_enrollments"
    description = "List employee training enrollments with optional filters."
    module_id = "training"
    required_permission = "training.view_employeetraining"
    parameters = {
        "type": "object",
        "properties": {
            "program_id": {"type": "string"}, "employee_id": {"type": "string"},
            "status": {"type": "string", "description": "enrolled, in_progress, completed, failed"},
        },
        "required": [],
        "additionalProperties": False,
    }

    def execute(self, args, request):
        from training.models import EmployeeTraining
        qs = EmployeeTraining.objects.select_related('program').all()
        if args.get('program_id'):
            qs = qs.filter(program_id=args['program_id'])
        if args.get('employee_id'):
            qs = qs.filter(employee_id=args['employee_id'])
        if args.get('status'):
            qs = qs.filter(status=args['status'])
        return {"enrollments": [{"id": str(e.id), "employee_name": e.employee_name, "program": e.program.name, "status": e.status, "start_date": str(e.start_date) if e.start_date else None, "completion_date": str(e.completion_date) if e.completion_date else None, "score": str(e.score) if e.score else None} for e in qs]}
