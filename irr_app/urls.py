from django.urls import path
from irr_app.views import HomePageView, UserLoginView

urlpatterns = [
    path('', HomePageView.as_view(), name='home-page'),
    path('login', UserLoginView.as_view(), name='user-login'),
]