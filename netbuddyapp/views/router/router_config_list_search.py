import sqlite3
from django.shortcuts import render
from netbuddyapp.models import RouterConfiguration, NetBuddyUser
from ..connection import Connection
from django.contrib.auth.decorators import login_required
from django.db.models import Q


@login_required
def router_config_list_search(request):
    """
    Handles listing user's saved router config on My Configs;
    Handles saving new router configs
    """
    if request.method == 'GET':

        form_data = request.GET

        all_router_configs = RouterConfiguration.objects.filter(Q(description__icontains=f"{form_data['searchfield']}") | Q(filename__icontains=f"{form_data['searchfield']}"))
        template = 'router/router_config_list.html'
        context = {
            'all_router_configs': all_router_configs
        }

        return render(request, template, context)

        # Original slq query

        # current_user = request.user
        # form_data = request.POST

        # with sqlite3.connect(Connection.db_path) as conn:
        #     db_cursor = conn.cursor()

        #     db_cursor.execute("""
        #     INSERT INTO netbuddyapp_routerconfiguration
        #     (
        #         filename, description, netbuddy_user_id, created_at
        #     )
        #     VALUES (?, ?, ?, ?)
        #     """,
        #     (form_data['filename'], form_data['description'],
        #         current_user.id, 'placeholder'))

        # return redirect(reverse('netbuddyapp:routerconfiglist'))
