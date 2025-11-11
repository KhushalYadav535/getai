from django.urls import path
from rest_framework.routers import DefaultRouter

from . import views

llm_router = DefaultRouter()
llm_urlpatterns = [
    path('llm/start-chat/', views.StartChatAPIView.as_view(), name='start-chat'),
    path('llm/text-generation/', views.TextGenerationAPIView.as_view(), name='text-generation'),
    path('llm/chaining/', views.ChainingAPIView.as_view(), name='text-chaining'),
    path('llm/agent-text-generation/', views.AgentTextGenerationAPIView.as_view(), name='agent-text-generation'),
    # path('llm/clear-cache/', views.ClearCacheAPIView.as_view(), name='clear-cache'),
]
