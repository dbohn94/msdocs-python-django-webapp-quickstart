from django.urls import path
from . import views

urlpatterns = [
    path('', views.index, name='index'),
    path('hello', views.hello, name='hello'),
    #path('spy_chart', views.spy_chart, name='spy_chart'),
    path('templates/hello_azure/', views.spy_chart, name='spy_chart.html'),
]