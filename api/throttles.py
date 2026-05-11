from rest_framework.throttling import ScopedRateThrottle


class CommentRateThrottle(ScopedRateThrottle):
    """
    Limit comment creation to prevent spam.
    Rate is defined in settings.py: 'comments': '5/minute'
    
    This throttle is only applied on the 'create' action
    of the CommentViewSet (see views.py → get_throttles).
    """
    scope = 'comments'
