from django.urls import path
from netbuddyapp import views
from .views import home

app_name = 'netbuddyapp'

urlpatterns = [
    path('', home, name='home'),
]