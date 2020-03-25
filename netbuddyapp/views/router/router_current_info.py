from django.shortcuts import render
from netmiko import ConnectHandler
from netbuddyapp.models import NetBuddyUser
from netbuddyapp.helper import get_device_obj, nb_exception

def router_current_info(request):

    """
    Handles current router running-config readout on Current Configuration page
    """

    current_user = request.user
    current_netbuddy_user = NetBuddyUser.objects.get(user_id=current_user.id)
	
    if request.method == 'GET':
        try:
            conn = ConnectHandler(**get_device_obj(request))
            
            prompt_output = conn.find_prompt()
            uptime_output = conn.send_command("show version | i uptime")
            showrun_output = conn.send_command("show run")
            conn.disconnect()

            template = 'router/router_current_info.html'
            context = {'prompt_output': prompt_output, 'uptime_output': uptime_output, 'showrun_output': showrun_output }

            return render(request, template, context)

        except Exception as exception:

            return nb_exception(request, exception)