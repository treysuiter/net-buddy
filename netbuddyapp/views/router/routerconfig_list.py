import sqlite3
from django.shortcuts import render
from netbuddyapp.models import RouterConfiguration
from ..connection import Connection
from django.contrib.auth.decorators import login_required

@login_required
def router_config_list(request):
    if request.method == 'GET':
        with sqlite3.connect(Connection.db_path) as conn:
            conn.row_factory = sqlite3.Row
            db_cursor = conn.cursor()

            db_cursor.execute("""
            select
                r.id,
                r.filename,
                r.config_string,
                r.description,
                r.created_at,
                r.netbuddy_user_id
            from netbuddyapp_routerconfiguration r
            """)

            all_router_configs = []
            dataset = db_cursor.fetchall()

            for row in dataset:
                router_config = RouterConfiguration()
                router_config.id = row['id']
                router_config.filename = row['filename']
                router_config.config_string = row['config_string']
                router_config.description = row['description']
                router_config.created_at = row['created_at']
                router_config.netbuddy_user_id = row['netbuddy_user_id']

                all_router_configs.append(router_config)

        template = 'router/router_config_list.html'
        context = {
            'all_router_configs': all_router_configs
        }

        return render(request, template, context)