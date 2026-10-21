from whitenoise.storage import CompressedManifestStaticFilesStorage


class StaticStorage(CompressedManifestStaticFilesStorage):
    """Jazzmin builds some static paths (e.g. 'vendor/bootswatch') that are folders, not files.

    A strict manifest raises a 500 for those; non-strict falls back to the plain URL.
    """

    manifest_strict = False
