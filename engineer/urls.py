from django.urls import path
from .views import EngineerRegisterView

app_name = 'engineer'

urlpattern = [
    path('register/<str:token>', EngineerRegisterView.as_view(), name='engineer-register')
]
