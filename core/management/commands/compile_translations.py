"""Compile locale/*/LC_MESSAGES/django.po to .mo without GNU gettext (works on Windows)."""
from pathlib import Path

import polib
from django.conf import settings
from django.core.management.base import BaseCommand


class Command(BaseCommand):
    help = "Compile .po translation files to .mo using polib (no gettext tools needed)."

    def handle(self, *args, **options):
        count = 0
        for locale_dir in settings.LOCALE_PATHS:
            for po_path in Path(locale_dir).glob("*/LC_MESSAGES/*.po"):
                po = polib.pofile(str(po_path))
                po.save_as_mofile(str(po_path.with_suffix(".mo")))
                count += 1
                self.stdout.write(f"compiled {po_path} ({po.percent_translated()}% translated)")
        self.stdout.write(self.style.SUCCESS(f"{count} catalog(s) compiled."))
