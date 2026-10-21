from django.contrib import admin
from django.urls import include, path

admin.site.site_header = "Ruhiyat Studio"
admin.site.site_title = "Ruhiyat Studio"
admin.site.index_title = "Boshqaruv paneli"

urlpatterns = [
    path("admin/", admin.site.urls),
    path("i18n/", include("django.conf.urls.i18n")),
    path("accounts/", include("accounts.urls")),
    path("topics/", include("learning.urls")),
    path("", include("care.urls")),
    path("", include("core.urls")),
]
