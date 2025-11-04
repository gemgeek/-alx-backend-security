from django.http import HttpResponse
from django_ratelimit.decorators import ratelimit

@ratelimit(key='ip', rate=None)
def sensitive_login_view(request):
    """
    A sample sensitive view (like a login page)
    that is rate-limited.
    """

    return HttpResponse("This is the sensitive login page. You are not rate-limited.")