from django.contrib.auth.models import AbstractUser
from django.db import models
from django.utils.translation import gettext_lazy as _

AVATAR_GRADIENTS = ["violet", "ocean", "sunset", "mint", "rose", "amber"]

AGE_GROUPS = [
    ("children", _("Children (6–12)")),
    ("teens", _("Teenagers (13–17)")),
    ("adults", _("Adults (18–59)")),
    ("seniors", _("Seniors (60+)")),
]
AGE_GROUP_ICONS = {"children": "🧒", "teens": "🧑‍🎓", "adults": "🧑", "seniors": "🧓"}
SPOKEN_LANGUAGES = [("uz", "O‘zbekcha"), ("kaa", "Qaraqalpaqsha"), ("ru", "Русский"), ("en", "English")]


class User(AbstractUser):
    class Role(models.TextChoices):
        CLIENT = "client", _("Client")
        PSYCHOLOGIST = "psychologist", _("Psychologist")
        ADMIN = "admin", _("Administrator")

    role = models.CharField(_("role"), max_length=20, choices=Role.choices, default=Role.CLIENT)
    email = models.EmailField(_("email address"), blank=True)
    # Psychologist profile; ignored for clients.
    specialization = models.CharField(_("specialization"), max_length=150, blank=True)
    bio = models.TextField(_("about"), blank=True)
    experience_years = models.PositiveSmallIntegerField(_("years of experience"), default=0)
    is_verified = models.BooleanField(
        _("verified psychologist"),
        default=False,
        help_text=_("Verified psychologists can publish topics in the studio."),
    )
    # Comma-separated codes from AGE_GROUPS / SPOKEN_LANGUAGES.
    age_groups = models.CharField(_("works with ages"), max_length=60, blank=True)
    spoken_languages = models.CharField(_("consultation languages"), max_length=40, blank=True)
    accepts_clients = models.BooleanField(_("accepts new clients"), default=True)
    # Client profile: used to recommend suitable psychologists.
    age_group = models.CharField(_("age group"), max_length=20, choices=AGE_GROUPS, blank=True)

    class Meta(AbstractUser.Meta):
        verbose_name = _("user")
        verbose_name_plural = _("Users")

    @property
    def is_client(self):
        return self.role == self.Role.CLIENT

    @property
    def is_psychologist(self):
        return self.role == self.Role.PSYCHOLOGIST

    @property
    def display_name(self):
        return self.get_full_name() or self.username

    @property
    def initials(self):
        parts = [p for p in (self.first_name, self.last_name) if p]
        if parts:
            return "".join(p[0] for p in parts).upper()
        return self.username[:2].upper()

    @property
    def age_group_list(self):
        labels = dict(AGE_GROUPS)
        return [
            {"code": c, "label": labels[c], "icon": AGE_GROUP_ICONS[c]}
            for c in self.age_groups.split(",")
            if c in labels
        ]

    @property
    def language_list(self):
        names = dict(SPOKEN_LANGUAGES)
        return [names[c] for c in self.spoken_languages.split(",") if c in names]

    @property
    def avatar_gradient(self):
        return AVATAR_GRADIENTS[(self.pk or 0) % len(AVATAR_GRADIENTS)]
