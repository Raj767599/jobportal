# apps/seekers/urls.py
from django.urls import path
from .views import EmployerProfileView, DummyEmployerView

urlpatterns = [
    path('profile/', EmployerProfileView.as_view(), name='employer-profile'),
    path('test/', DummyEmployerView.as_view(), name='employer-test'),
]
