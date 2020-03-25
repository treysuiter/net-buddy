import sqlite3
from django.shortcuts import render, redirect, reverse
from netbuddyapp.models import RouterConfiguration, NetBuddyUser
from ..connection import Connection
from django.contrib.auth.decorators import login_required
from netmiko import ConnectHandler
from netbuddyapp.helper import get_device_obj, nb_exception
from ping3 import ping
import re

@login_required
def router_config_list(request):
    """
    Handles listing user's saved router config on My Configs;
    Handles saving new router configs
    """

    #List all of the user's configs

    if request.method == 'GET':
        
        all_router_configs = RouterConfiguration.objects.filter(netbuddy_user_id=request.user.id)

        template = 'router/router_config_list.html'
        context = {
            'all_router_configs': all_router_configs
        }

        return render(request, template, context)

    #Posts new configs    

    elif request.method == 'POST':

        #regex to make sure file name has no special characters
    
        form_data = request.POST
        unique_filename_check = None

        try:
            unique_filename_check = RouterConfiguration.objects.get(filename=form_data['filename'])
        except Exception:
            pass
        
        if re.match("^[A-Za-z0-9_-]*$", form_data['filename']) and unique_filename_check is None:
            current_user = request.user
            current_netbuddy_user = NetBuddyUser.objects.get(user_id=current_user.id)
            

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

            #Exception if conn.send_command throws error
            except Exception as exception:

                return nb_exception(request, exception)
        
        #Filename was already used
        elif unique_filename_check is not None:
            template = 'router/router_config_form.html'
            context = {'bad_file_name': 'Filename must be unique.'}

            return render(request, template, context)

        #Filename had special characters
        else:
            template = 'router/router_config_form.html'
            context = {'bad_file_name': 'Filename can only contain letters, numbers, dashes or underscores.'}

            return render(request, template, context)
        
# Original sql query

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