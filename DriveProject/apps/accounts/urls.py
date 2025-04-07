# Import views from the accounts app

from django.urls import path

from .views import RegisterView

urlpatterns = [
    path('register/', RegisterView.as_view(), name='register'),
]
