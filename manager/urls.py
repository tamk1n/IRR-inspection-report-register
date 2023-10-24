from django.urls import path
from manager.views import (RegisterEmployeeView)
from django.conf import settings
from django.conf.urls.static import static

app_name = 'manager'

urlpatterns = [
    path('register-employee',RegisterEmployeeView.as_view(), name='register-employee'),
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)