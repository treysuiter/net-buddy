from django.urls import include, path
from netbuddyapp import views
from .views import *

app_name = 'netbuddyapp'

urlpatterns = [
    path('', home, name='home'),

    path('accounts/', include('django.contrib.auth.urls')),
    path('logout/', logout_user, name='logout'),
    path('register/', register, name="register"),

    path('routerconfig/form', router_config_form, name='routerconfigform'),
    path('routerconfiglist/', router_config_list, name='routerconfiglist'),
    path('routerconfiglist/<int:router_config_id>/', router_config_details, name='routerconfig'),
    path('routerconfiglist/<int:router_config_id>/form/', router_config_edit_form, name='routerconfigedit'),
    path('routercurrentinfo/', router_current_info, name='routercurrentinfo'),
]