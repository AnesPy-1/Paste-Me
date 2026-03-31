from datetime import timedelta

from django.core.management.base import BaseCommand
from django.utils import timezone

from core.models import PasteItem


class Command(BaseCommand):
    help = "Delete paste items older than 24 hours and remove their files from media storage."

    def handle(self, *args, **options):
        cutoff = timezone.now() - timedelta(hours=24)
        expired_qs = PasteItem.objects.filter(created_at__lt=cutoff)

        total = expired_qs.count()
        removed_files = 0

        for item in expired_qs.iterator():
            if item.file:
                removed_files += 1
            item.delete()

        self.stdout.write(
            self.style.SUCCESS(
                f"Deleted {total} paste(s); removed {removed_files} file(s) older than 24 hours."
            )
        )
