from django.core.management.base import BaseCommand, CommandError
from ip_tracking.models import BlockedIP
from django.core.validators import validate_ipv46_address
from django.core.exceptions import ValidationError

class Command(BaseCommand):
    help = 'Blocks one or more IP addresses from accessing the site.'

    def add_arguments(self, parser):
        parser.add_argument(
            'ip_addresses', 
            nargs='+', 
            type=str,
            help='The IP address(es) to block.'
        )

    def handle(self, *args, **options):
        for ip_address in options['ip_addresses']:
            try:
                validate_ipv46_address(ip_address)

                obj, created = BlockedIP.objects.get_or_create(ip_address=ip_address)

                if created:
                    self.stdout.write(self.style.SUCCESS(f'Successfully blocked IP: {ip_address}'))
                else:
                    self.stdout.write(self.style.WARNING(f'IP: {ip_address} is already blocked.'))

            except ValidationError:
                raise CommandError(f"'{ip_address}' is not a valid IP address.")