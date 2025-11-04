from django.db import models

class RequestLog(models.Model):
    """
    Model to store details of an incoming request.
    """
    
    ip_address = models.GenericIPAddressField()
    
    timestamp = models.DateTimeField(auto_now_add=True)
    
    path = models.CharField(max_length=2048)

    country = models.CharField(max_length=100, null=True, blank=True)
    city = models.CharField(max_length=100, null=True, blank=True)


    def __str__(self):
        return f"{self.ip_address} at {self.timestamp} on {self.path}"
    
class BlockedIP(models.Model):
    """
    Model to store IP addresses that are blocked from accessing the site.
    """
    ip_address = models.GenericIPAddressField(unique=True)
    
    timestamp = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.ip_address} (blocked on {self.timestamp.date()})"

class SuspiciousIP(models.Model):
    """
    Model to log IPs flagged for suspicious activity.
    """
    ip_address = models.GenericIPAddressField()
    reason = models.TextField(help_text="Reason for suspicion (e.g., rate limit, path)")
    
    timestamp = models.DateTimeField(auto_now_add=True)

    class Meta:
        unique_together = ['ip_address', 'reason']

    def __str__(self):
        return f"{self.ip_address} - {self.reason}"        