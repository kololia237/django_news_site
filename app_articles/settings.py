from django.conf import settings

MAIN_TASKS_PER_PAGE = getattr(settings, 'MAIN_TASKS_PER_PAGE', 10)
MAIN_TASKS_FOR_PROFILE_PER_PAGE = getattr(settings, 'MAIN_TASKS_FOR_PROFILE_PER_PAGE', 3)
