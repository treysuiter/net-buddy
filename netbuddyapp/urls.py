from django.urls import path
from netbuddyapp import views
from .views import *

app_name = 'netbuddyapp'

urlpatterns = [
    path('', home, name='home'),
    path('routerconfiglist/', router_config_list, name='router_config_list')
]