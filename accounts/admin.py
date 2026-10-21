from django.contrib import admin, messages
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
from django.contrib.auth.models import Group
from django.utils.translation import gettext_lazy as _

from .models import User

PSYCHOLOGIST_GROUP = "Psychologists"


@admin.register(User)
class UserAdmin(BaseUserAdmin):
    list_display = ("username", "display_name", "role", "specialization", "is_verified", "is_staff", "date_joined")
    list_filter = ("role", "is_verified", "is_staff", "is_active")
    search_fields = ("username", "first_name", "last_name", "email", "specialization")
    actions = ["verify_psychologists", "revoke_verification"]
    fieldsets = BaseUserAdmin.fieldsets + (
        (_("Ruhiyat profile"), {"fields": ("role", "is_verified", "specialization", "experience_years", "bio")}),
    )

    @admin.display(description=_("Name"))
    def display_name(self, obj):
        return obj.display_name

    @admin.action(description=_("Verify selected psychologists (studio access)"))
    def verify_psychologists(self, request, queryset):
        group = Group.objects.filter(name=PSYCHOLOGIST_GROUP).first()
        count = 0
        for user in queryset.filter(role=User.Role.PSYCHOLOGIST):
            user.is_verified = True
            user.is_staff = True
            user.save(update_fields=["is_verified", "is_staff"])
            if group:
                user.groups.add(group)
            count += 1
        self.message_user(request, _("%(count)d psychologist(s) verified.") % {"count": count}, messages.SUCCESS)

    @admin.action(description=_("Revoke verification"))
    def revoke_verification(self, request, queryset):
        count = queryset.filter(role=User.Role.PSYCHOLOGIST, is_superuser=False).update(is_verified=False, is_staff=False)
        self.message_user(request, _("%(count)d psychologist(s) revoked.") % {"count": count}, messages.WARNING)
