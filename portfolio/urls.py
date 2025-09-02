from .views import *
from django.urls import path

urlpatterns = [
    path('', home, name='home'),
    path('portfolio/<int:pk>/', portfolio_details, name='portfolio_details'),
]