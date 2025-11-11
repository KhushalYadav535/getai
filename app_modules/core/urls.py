from django.urls import path, include
from rest_framework.routers import DefaultRouter

from app_modules.llm.urls import llm_urlpatterns

router = DefaultRouter()

urlpatterns = [path('', include(router.urls))] + llm_urlpatterns
