from django.urls import path
from irr_app.views import (HomePageView, UserLoginView,
                           NewIRView, IRRegisterView,
                           UserLogoutView, SingleDeleteIR,
                           UpdateIRView)
from django.conf import settings
from django.conf.urls.static import static
app_name = 'irr_app'

urlpatterns = [
    path('', HomePageView.as_view(), name='home-page'),
    path('login/', UserLoginView.as_view(), name='user-login'),
    path('logout/', UserLogoutView.as_view(), name='user-logout'),
    path('new/', NewIRView.as_view(), name='new-ir'),
    path('irr/', IRRegisterView.as_view(), name='irr'),
    path('delete/<int:pk>', SingleDeleteIR.as_view(), name='single-delete-ir'),
    path('update/<int:pk>', UpdateIRView.as_view(), name='update-ir'),
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
    urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)