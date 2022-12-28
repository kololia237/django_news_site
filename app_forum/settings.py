from django.conf import settings

FORUM_PER_PAGE = getattr(settings, 'FORUM_TOPICS_PER_PAGE', 10)
FORUM_COMMENTS_PER_PAGE = getattr(settings, 'FORUM_COMMENTS_PER_PAGE', 3)
FORUM_FILTER_PROFANE_WORDS = getattr(settings, 'FORUM_FILTER_PROFANE_WORDS', True)
