from django.urls import path
from irr_app.views import (HomePageView, UserLoginView,
                           NewIRView, IRRegisterView,
                           UserLogoutView)

app_name = 'irr_app'

urlpatterns = [
    path('', HomePageView.as_view(), name='home-page'),
    path('login', UserLoginView.as_view(), name='user-login'),
    path('logout', UserLogoutView.as_view(), name='user-logout'),
    path('new', NewIRView.as_view(), name='new-ir'),
    path('register', IRRegisterView.as_view(), name='register'),
]