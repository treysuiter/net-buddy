import sqlite3
from django.urls import reverse
from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from netbuddyapp.models import RouterConfiguration, NetBuddyUser
from ..connection import Connection
from netmiko import ConnectHandler
from netbuddyapp.helper import get_device_obj, nb_exception
from ping3 import ping


def get_router_config(router_config_id):
    """
    Returns router config
    """


    #SQL Example

    # with sqlite3.connect(Connection.db_path) as conn:
    #     conn.row_factory = model_factory(Book)
    #     db_cursor = conn.cursor()

    #     db_cursor.execute("""
    #     SELECT
    #         b.id,
    #         b.title,
    #         b.isbn,
    #         b.author,
    #         b.year,
    #         b.librarian_id,
    #         b.location_id
    #     FROM libraryapp_book b
    #     WHERE b.id = ?
    #     """, (book_id,))

    #     return db_cursor.fetchone()

    return RouterConfiguration.objects.get(pk=router_config_id)


@login_required
def router_config_details(request, router_config_id):

    """
    Will render router config details page when router config title are clicked on My Configs; 
    Handles loading saved router configs;
    Handles deleting router configs;
    Handles edit of router config descriptions
    """

    if request.method == 'GET':

        current_user = request.user
        current_netbuddy_user = NetBuddyUser.objects.get(user_id=current_user.id)
        
        try:
            router_config = get_router_config(router_config_id)
            template_name = 'router/router_config_details.html'
        except Exception:
            return redirect(reverse('netbuddyapp:routerconfiglist'))

        if router_config.netbuddy_user_id == request.user.id:
            return render(request, template_name, {'router_config': router_config, 'current_netbuddy_user': current_netbuddy_user})
        else:
            return redirect(reverse('netbuddyapp:routerconfiglist'))

    elif request.method == 'POST':

        current_user = request.user
        current_netbuddy_user = NetBuddyUser.objects.get(user_id=current_user.id)
        router_config_to_load = RouterConfiguration.objects.get(pk=router_config_id)

        form_data = request.POST

        if (
            "actual_method" in form_data
            and form_data["actual_method"] == "TFTP_LOAD_CONFIG"
        ):
            
            tftp_ping_check = ping(current_netbuddy_user.tftp_ip)

            if tftp_ping_check is not None:

                #Netmiko commands to load a saved running-config
                try:
                    conn = ConnectHandler(**get_device_obj(request))

                    output = conn.send_command_timing(f"copy tftp://{current_netbuddy_user.tftp_ip}/{router_config_to_load.filename} running-config")

                    if "Error opening" and "(No such file or directory)" in output:

                        return nb_exception(request, "File not found on TFTP server")

                    conn.disconnect()

                    return redirect(reverse('netbuddyapp:routercurrentinfo'))

                except Exception as exception:

                    # error_text='Uh oh, looks like something went wrong. Check and see is your device is running, connected, and configured properly.'
                    # template = 'router/router_current_info.html'
                    # context = {'error_text': error_text, 'exception': exception}

                    return nb_exception(request, exception)

            else:

                return nb_exception(request, "TFTP server is not online")

        if (
            "actual_method" in form_data
            and form_data["actual_method"] == "GLOBAL_LOAD_CONFIG"
        ):

            #Netmiko commands to load a saved running-config
            try:
                conn = ConnectHandler(**get_device_obj(request))

                # conn.send_command('conf term')
                test_string = router_config_to_load.config_string

                result = test_string.find('version')
                print(result, 'this is where version is')
                conn.send_command_timing('conf term')
                output = conn.send_command_timing(f'{router_config_to_load.config_string}')
                conn.disconnect()

                return redirect(reverse('netbuddyapp:routercurrentinfo'))

            except Exception as exception:

                # error_text='Uh oh, looks like something went wrong. Check and see is your device is running, connected, and configured properly.'
                # template = 'router/router_current_info.html'
                # context = {'error_text': error_text, 'exception': exception}

                return nb_exception(request, exception)


        if (
            "actual_method" in form_data
            and form_data["actual_method"] == "DELETE"
        ):

            router_config = RouterConfiguration.objects.get(
                pk=router_config_id)
            router_config.delete()

            return redirect(reverse('netbuddyapp:routerconfiglist'))

        if (
            "actual_method" in form_data
            and form_data["actual_method"] == "PUT"
        ):

            #SQL Example

            # with sqlite3.connect(Connection.db_path) as conn:
            #     db_cursor = conn.cursor()

            #     db_cursor.execute("""
            #     UPDATE libraryapp_book
            #     SET title = ?,
            #         author = ?,
            #         isbn = ?,
            #         year = ?,
            #         location_id = ?
            #     WHERE id = ?
            #     """,
            #     (
            #         form_data['title'], form_data['author'],
            #         form_data['isbn'], form_data['year_published'],
            #         form_data["location"], book_id,
            #     ))

            # # retrieve it first:
            config_to_update = RouterConfiguration.objects.get(pk=router_config_id)

            # # Reassign a property's value
            config_to_update.description = form_data['description']

            # # Save the change to the db
            config_to_update.save()

            return redirect(reverse('netbuddyapp:routerconfiglist'))
