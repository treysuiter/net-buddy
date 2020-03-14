import sqlite3
from django.urls import reverse
from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from netbuddyapp.models import RouterConfiguration, NetBuddyUser
from ..connection import Connection
from netmiko import ConnectHandler


def get_router_config(router_config_id):
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
    if request.method == 'GET':
        router_config = get_router_config(router_config_id)
        template_name = 'router/router_config_details.html'
        return render(request, template_name, {'router_config': router_config})

    elif request.method == 'POST':

        current_user = request.user
        current_netbuddy_user = NetBuddyUser.objects.get(user_id=current_user.id)
        router_config_to_load = RouterConfiguration.objects.get(pk=router_config_id)

        form_data = request.POST

        if (
            "actual_method" in form_data
            and form_data["actual_method"] == "LOAD_CONFIG"
        ):
            device = {}
            device['device_type'] = 'cisco_ios'
            device['ip'] = f"{current_netbuddy_user.current_router_ip}"
            device['username'] = f"{current_netbuddy_user.ssh_username}"
            device['password'] = f"{current_netbuddy_user.ssh_password}"
            conn = ConnectHandler(**device)

            conn.send_command(f"copy tftp://172.16.1.5/{router_config_to_load.filename} running-config")

            return redirect(reverse('netbuddyapp:routerconfiglist'))


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
