from django.urls import path
from . import views

urlpatterns = [
    path('', views.spy_chart, name='spy_chart.html')
    
]
