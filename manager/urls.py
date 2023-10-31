from django.urls import path
from manager.views import (AddEngineerView, EngineerRegisterView)
from django.conf import settings
from django.conf.urls.static import static

app_name = 'manager'

urlpatterns = [
    path('register-engineer',AddEngineerView.as_view(), name='add-engineer'),
    path('register-engineer/<str:token>', EngineerRegisterView.as_view(), name='register-engineer')
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)