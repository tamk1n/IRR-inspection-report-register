from django.urls import path
from irr_app.views import HomePageView

urlpatterns = [
    path('', HomePageView.as_view(), name='home-page'),
]