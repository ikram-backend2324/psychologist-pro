"""Create the Psychologists group with studio permissions, and the platform admin from env vars."""
import os

from django.contrib.auth.models import Group, Permission
from django.core.management.base import BaseCommand

from accounts.admin import PSYCHOLOGIST_GROUP
from accounts.models import User

PSYCHOLOGIST_PERMISSIONS = {
    "topic": ("add", "change", "delete", "view"),
    "step": ("add", "change", "delete", "view"),
    "quizquestion": ("add", "change", "delete", "view"),
    "category": ("view",),
    "enrollment": ("view",),
    "quizresult": ("view",),
    "reflection": ("view",),
}


class Command(BaseCommand):
    help = "Ensure roles/permissions exist and create the superuser from DJANGO_SUPERUSER_* env vars."

    def handle(self, *args, **options):
        group, _ = Group.objects.get_or_create(name=PSYCHOLOGIST_GROUP)
        perms = [
            Permission.objects.get(content_type__app_label="learning", codename=f"{action}_{model}")
            for model, actions in PSYCHOLOGIST_PERMISSIONS.items()
            for action in actions
        ]
        group.permissions.set(perms)
        verified = User.objects.filter(role=User.Role.PSYCHOLOGIST, is_verified=True)
        verified.update(is_staff=True)
        for user in verified:
            user.groups.add(group)
        self.stdout.write(self.style.SUCCESS(f"Group '{PSYCHOLOGIST_GROUP}' has {len(perms)} permissions."))

        username = os.environ.get("DJANGO_SUPERUSER_USERNAME")
        password = os.environ.get("DJANGO_SUPERUSER_PASSWORD")
        if not (username and password):
            self.stdout.write("DJANGO_SUPERUSER_USERNAME/PASSWORD not set; skipping admin creation.")
            return
        admin, created = User.objects.get_or_create(
            username=username,
            defaults={"email": os.environ.get("DJANGO_SUPERUSER_EMAIL", ""), "role": User.Role.ADMIN},
        )
        if created:
            admin.set_password(password)
        admin.is_staff = admin.is_superuser = True
        admin.role = User.Role.ADMIN
        admin.save()
        self.stdout.write(self.style.SUCCESS(f"Admin '{username}' {'created' if created else 'ensured'}."))
