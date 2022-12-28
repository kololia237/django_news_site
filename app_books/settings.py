from django.conf import settings

BOOKS_PER_PAGE = getattr(settings, 'BOOKS_PER_PAGE', 4)
REVIEWS_COMMENTS_PER_PAGE = getattr(settings, 'REVIEWS_COMMENTS_PER_PAGE', 3)
REVIEWS_PER_PAGE = getattr(settings, 'REVIEWS_PER_PAGE', 4)
