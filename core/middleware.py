from django.http import JsonResponse


class HealthCheckMiddleware:
    """Answer /healthz before host validation: platform probes may use an internal Host header."""

    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        if request.path == "/healthz":
            return JsonResponse({"status": "ok"})
        return self.get_response(request)
