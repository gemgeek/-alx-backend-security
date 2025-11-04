from .models import RequestLog, BlockedIP
from django_ipware.ip import get_client_ip
from django.http import HttpResponseForbidden

class IPLoggingMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        ip, is_routable = get_client_ip(request)
        
        if not ip:
            return self.get_response(request)

        if BlockedIP.objects.filter(ip_address=ip).exists():
            return HttpResponseForbidden("Your IP address has been blocked.")

        RequestLog.objects.create(
            ip_address=ip,
            path=request.path
        )

        response = self.get_response(request)
        return response