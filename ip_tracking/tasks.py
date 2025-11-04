from celery import shared_task
from django.utils import timezone
from django.db.models import Count, Q
from datetime import timedelta
from .models import RequestLog, SuspiciousIP

@shared_task
def detect_suspicious_ips():
    print("Running hourly check for suspicious IPs...")

    one_hour_ago = timezone.now() - timedelta(hours=1)

    high_volume_ips = RequestLog.objects.filter(
        timestamp__gte=one_hour_ago
    ).values(
        'ip_address'
    ).annotate(
        request_count=Count('id')
    ).filter(
        request_count__gt=100
    )

    new_suspicious_ips = []
    for entry in high_volume_ips:
        reason = f"Exceeded 100 requests in one hour ({entry['request_count']} requests)"
        new_suspicious_ips.append(
            SuspiciousIP(ip_address=entry['ip_address'], reason=reason)
        )

    sensitive_paths = ['/admin', '/login']

    sensitive_access_logs = RequestLog.objects.filter(
        timestamp__gte=one_hour_ago
    ).filter(
        Q(path__startswith=sensitive_paths[0]) | 
        Q(path__startswith=sensitive_paths[1])
    ).distinct(
        'ip_address' 
    )

    for log in sensitive_access_logs:
        reason = f"Accessed sensitive path: {log.path}"
        new_suspicious_ips.append(
            SuspiciousIP(ip_address=log.ip_address, reason=reason)
        )

    if new_suspicious_ips:
        SuspiciousIP.objects.bulk_create(new_suspicious_ips, ignore_conflicts=True)
        print(f"Flagged {len(new_suspicious_ips)} new suspicious activities.")
    else:
        print("No new suspicious activities found.")

    return f"Completed scan. Flagged {len(new_suspicious_ips)} new activities."