from django.core.management.base import BaseCommand
from django.utils import timezone
from apps.models import User


class Command(BaseCommand):
    help = "Deactivate users whose subscription expired"
    def handle(self, *args, **kwargs):
        now = timezone.now()
        expired_users = User.objects.filter(
            subscription_end__lte=now,
            is_active=True
        )

        if not expired_users.exists():
            self.stdout.write(self.style.WARNING("No expired users found"))
            return

        self.stdout.write(self.style.NOTICE("Expired users:"))
        for user in expired_users:
            self.stdout.write(f" - {user.email} (expired at {user.subscription_end})")

        count = expired_users.update(is_active=False)
        self.stdout.write(self.style.SUCCESS(f"{count} users deactivated at {now}"))
