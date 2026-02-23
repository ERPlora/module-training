    from django.utils.translation import gettext_lazy as _

    MODULE_ID = 'training'
    MODULE_NAME = _('Training & Skills')
    MODULE_VERSION = '1.0.0'
    MODULE_ICON = 'school-outline'
    MODULE_DESCRIPTION = _('Employee training programs and skill tracking')
    MODULE_AUTHOR = 'ERPlora'
    MODULE_CATEGORY = 'hr'

    MENU = {
        'label': _('Training & Skills'),
        'icon': 'school-outline',
        'order': 44,
    }

    NAVIGATION = [
        {'label': _('Dashboard'), 'icon': 'speedometer-outline', 'id': 'dashboard'},
{'label': _('Programs'), 'icon': 'school-outline', 'id': 'programs'},
{'label': _('Skills'), 'icon': 'ribbon-outline', 'id': 'skills'},
{'label': _('Settings'), 'icon': 'settings-outline', 'id': 'settings'},
    ]

    DEPENDENCIES = []

    PERMISSIONS = [
        'training.view_trainingprogram',
'training.add_trainingprogram',
'training.change_trainingprogram',
'training.delete_trainingprogram',
'training.view_skill',
'training.manage_settings',
    ]
