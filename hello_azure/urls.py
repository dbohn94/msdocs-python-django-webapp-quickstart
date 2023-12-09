from django.urls import path
from . import views
from .views import run_algorithm

urlpatterns = [
    path('', views.index, name='index'),
    path('hello', views.hello, name='hello'),
    path('run_algorithm/', run_algorithm, name='run_algorithm')
]