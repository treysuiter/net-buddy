import sqlite3
from django.shortcuts import render, redirect, reverse
from netbuddyapp.models import RouterConfiguration, NetBuddyUser
from ..connection import Connection
from django.contrib.auth.decorators import login_required
from netmiko import ConnectHandler


@login_required
def router_config_list(request):
    """
    Handles listing user's saved router config on My Configs;
    Handles saving new router configs
    """
    if request.method == 'GET':
        
        all_router_configs = RouterConfiguration.objects.filter(netbuddy_user_id=request.user.id)

        template = 'router/router_config_list.html'
        context = {
            'all_router_configs': all_router_configs
        }

        return render(request, template, context)

    elif request.method == 'POST':

        current_user = request.user
        current_netbuddy_user = NetBuddyUser.objects.get(user_id=current_user.id)
        form_data = request.POST

        new_config = RouterConfiguration(
            filename=form_data['filename'],
            description=form_data['description'],
            netbuddy_user_id=current_user.id
        )

        #Netmiko commands to save new running_config
        
        try:
            device = {}
            device['device_type'] = 'cisco_ios'
            device['ip'] = f"{current_netbuddy_user.current_router_ip}"
            device['username'] = f"{current_netbuddy_user.ssh_username}"
            device['password'] = f"{current_netbuddy_user.ssh_password}"
            conn = ConnectHandler(**device)

            conn.send_command(f"copy running-config tftp://172.16.1.5/{form_data['filename']}")
            conn.disconnect()

            # and then save to the db
            new_config.save()
            return redirect(reverse('netbuddyapp:routerconfiglist'))

        except Exception as exception:

            error_text='Uh oh, looks like something went wrong. Check and see is your device is running, connected, and configured properly.'
            template = 'router/router_current_info.html'
            context = {'error_text': error_text, 'exception': exception}

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
