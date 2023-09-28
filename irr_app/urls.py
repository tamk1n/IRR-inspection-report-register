from django.urls import path
from irr_app.views import (HomePageView, UserLoginView,
                           NewIRView,)

app_name = 'irr_app'

urlpatterns = [
    path('', HomePageView.as_view(), name='home-page'),
    path('login', UserLoginView.as_view(), name='user-login'),
    path('new', NewIRView.as_view(), name='new-ir'),
]