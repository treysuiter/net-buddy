from django.urls import include, path
from netbuddyapp import views
from .views import *

app_name = 'netbuddyapp'

urlpatterns = [
    path('', home, name='home'),
    path('accounts/', include('django.contrib.auth.urls')),
    path('logout/', logout_user, name='logout'),
    path('routerconfiglist/', router_config_list, name='routerconfiglist')
]