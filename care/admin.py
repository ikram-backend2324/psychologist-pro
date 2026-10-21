from django.contrib import admin
from django.utils.translation import gettext_lazy as _

from .models import Connection


@admin.register(Connection)
class ConnectionAdmin(admin.ModelAdmin):
    """Platform admins see who works with whom; message contents stay private."""

    list_display = ("client", "psychologist", "status", "message_count", "created_at", "updated_at")
    list_filter = ("status",)
    search_fields = ("client__username", "psychologist__username")
    readonly_fields = ("client", "psychologist", "concern", "created_at", "updated_at")
    fields = ("client", "psychologist", "status", "concern", "created_at", "updated_at")

    @admin.display(description=_("Messages"))
    def message_count(self, obj):
        return obj.messages.count()

    def has_add_permission(self, request):
        return False

    def _platform_admin(self, request):
        return request.user.is_superuser or getattr(request.user, "role", None) == "admin"

    def has_module_permission(self, request):
        return self._platform_admin(request)

    def has_view_permission(self, request, obj=None):
        return self._platform_admin(request)

    def has_change_permission(self, request, obj=None):
        return self._platform_admin(request)
