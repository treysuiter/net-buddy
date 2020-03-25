import sqlite3
from django.shortcuts import render
from netbuddyapp.models import RouterConfiguration, NetBuddyUser
from ..connection import Connection
from django.contrib.auth.decorators import login_required
from django.db.models import Q


@login_required
def router_config_list_search(request):
    """
    Handles search for router configs.
    """
    if request.method == 'GET':

        form_data = request.GET

        all_router_configs = RouterConfiguration.objects.filter(Q(netbuddy_user_id=request.user.id) & (Q(description__icontains=f"{form_data['searchfield']}") | Q(filename__icontains=f"{form_data['searchfield']}")))
        template = 'router/router_config_list.html'
        context = {
            'all_router_configs': all_router_configs
        }

        return render(request, template, context)