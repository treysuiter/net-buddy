from django.contrib.auth.decorators import login_required
from django.shortcuts import render
from netmiko import ConnectHandler
from netbuddyapp.models import NetBuddyUser
from netbuddyapp.helper import get_device_obj

@login_required
def router_commands(request):

    form_data = request.GET

    if request.method == 'GET':

        if (
            "actual_method" in form_data
            and form_data["actual_method"] == "SHOW_IP_INTERFACES_BRIEF"
        ):
            try:
                conn = ConnectHandler(**get_device_obj(request))
                output = conn.send_command('show ip interface brief')
                template = 'router/router_commands.html'
                context = {
                    'output': output
                }
                conn.disconnect()
                return render(request, template, context)

            except Exception as exception:

                error_text='Uh oh, looks like something went wrong. Check and see is your device is running, connected, and configured properly.'
                template = 'router/router_current_info.html'
                context = {'error_text': error_text, 'exception': exception}

                return render(request, template, context)

        if (
            "actual_method" in form_data
            and form_data["actual_method"] == "SHOW_IP_ROUTE"
        ):
            try:
                conn = ConnectHandler(**get_device_obj(request))
                output = conn.send_command('show ip route')
                template = 'router/router_commands.html'
                context = {
                    'output': output
                }
                conn.disconnect()
                return render(request, template, context)

            except Exception as exception:

                error_text='Uh oh, looks like something went wrong. Check and see is your device is running, connected, and configured properly.'
                template = 'router/router_current_info.html'
                context = {'error_text': error_text, 'exception': exception}

                return render(request, template, context)

        if (
            "actual_method" in form_data
            and form_data["actual_method"] == "SHOW_VERSION"
        ):
            try:
                conn = ConnectHandler(**get_device_obj(request))
                output = conn.send_command('show version')
                template = 'router/router_commands.html'
                context = {
                    'output': output
                }
                conn.disconnect()
                return render(request, template, context)

            except Exception as exception:

                error_text='Uh oh, looks like something went wrong. Check and see is your device is running, connected, and configured properly.'
                template = 'router/router_current_info.html'
                context = {'error_text': error_text, 'exception': exception}

                return render(request, template, context)           

        if (
            "actual_method" in form_data
            and form_data["actual_method"] == "SHOW_IP_PROTOCOLS"
        ):
            try:
                conn = ConnectHandler(**get_device_obj(request))
                output = conn.send_command('show ip protocols')
                template = 'router/router_commands.html'
                context = {
                    'output': output
                }
                conn.disconnect()
                return render(request, template, context)

            except Exception as exception:

                error_text='Uh oh, looks like something went wrong. Check and see is your device is running, connected, and configured properly.'
                template = 'router/router_current_info.html'
                context = {'error_text': error_text, 'exception': exception}

                return render(request, template, context)    

        else:
            
            template = 'router/router_commands.html'
            context = {
            }

            return render(request, template, context)