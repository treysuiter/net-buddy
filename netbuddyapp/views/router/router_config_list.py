import sqlite3
from django.shortcuts import render, redirect, reverse
from netbuddyapp.models import RouterConfiguration, NetBuddyUser
from ..connection import Connection
from django.contrib.auth.decorators import login_required
from netmiko import ConnectHandler
from netbuddyapp.helper import get_device_obj, nb_exception
from ping3 import ping

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
            # config_string="",
            netbuddy_user_id=current_user.id
        )

        #Netmiko commands to save new running_config
        
        try:
            conn = ConnectHandler(**get_device_obj(request))

            new_config.config_string = conn.send_command("show run")
            
            if current_netbuddy_user.tftp_ip:
                tftp_ping_check = ping(current_netbuddy_user.tftp_ip)
                if tftp_ping_check is not None:
                    conn.send_command(f"copy running-config tftp://{current_netbuddy_user.tftp_ip}/{form_data['filename']}")

            conn.disconnect()

            # and then save to the db
            new_config.save()
            return redirect(reverse('netbuddyapp:routerconfiglist'))

        except Exception as exception:

            return nb_exception(request, exception)

            # error_text='Uh oh, looks like something went wrong. Check and see is your device is running, connected, and configured properly.'
            # template = 'router/router_current_info.html'
            # context = {'error_text': error_text, 'exception': exception}

            # return render(request, template, context)

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
