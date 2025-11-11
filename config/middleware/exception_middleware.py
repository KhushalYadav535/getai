import logging

from django.conf import settings
from django.shortcuts import render

logger = logging.getLogger(__name__)


class ExceptionMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        response = self.get_response(request)
        if not settings.DEBUG:
            if response.status_code == 500:
                return render(request, "error_templates/500.html")
            if response.status_code == 404:
                return render(request, "error_templates/404.html")
            if response.status_code == 403:
                return render(request, "error_templates/403.html")
        return response

    def process_exception(self, request, exception):
        logger.exception("An exception occurred", extra={'request': request})
        return None
