from django.urls import path
from .views import RegisterUserView, DummyUserView

urlpatterns = [
    path('register/', RegisterUserView.as_view(), name='register'),
    path('test/', DummyUserView.as_view(), name='user-test'),
]
