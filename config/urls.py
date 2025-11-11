from django.conf import settings
from django.conf.urls.static import static
from django.contrib import admin
from django.urls import path, include

from scrap_data.views import (
    scrape_data,
    DataListView,
    ProfilePictureView,
    bookmark_view,
    add_bookmark,
    ResearchListView,
    submit_tool,
    ScrapeGoogleNewsView,
    NewsListView,
    StoryMakerView, TribeView
)
from users.views import (
    custom_login,
    register_view,
    logout_view,
    verify_email,
    send_verification_email,
    email_verify,
    forgot_password,
    reset_password
)

urlpatterns = [
    path('admin/', admin.site.urls),
    path('accounts/', include('allauth.urls')),
    path('', DataListView.as_view(), name='data_list'),
    path('add-bookmark/<int:item_id>/', add_bookmark, name='add_bookmark'),
    path('bookmark/', bookmark_view, name='bookmark_view'),
    path('research/', ResearchListView.as_view(), name='research'),
    path('news/', NewsListView.as_view(), name='news'),
    path('submit/', submit_tool, name='submit'),
    path('scrape/', scrape_data, name='scrape_data'),
    path('tribe/', TribeView.as_view(), name='tribe'),
    path('story-maker/', StoryMakerView.as_view(), name='story-maker'),
    path('image', ProfilePictureView.as_view(), name="profile-picture"),
    path('scrape-google-news/', ScrapeGoogleNewsView.as_view(), name='scrape_google_news'),

    path('send-verification-email/', send_verification_email, name='send_verification_email'),
    path('login/', custom_login, name='login'),
    path('register/', register_view, name='register'),
    path('logout/', logout_view, name='logout'),
    path('verify-email/<str:verification_token>/', verify_email, name='verify_email'),
    path('email-verify', email_verify, name='email_verify'),
    path('forgot-password/', forgot_password, name='forgot_password'),
    path('reset-password/<int:user_id>/<str:token>/', reset_password, name='reset_password'),
    path("api/v1/", include(("app_modules.core.urls", "app_modules.core"), namespace="core")),

]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
    urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
