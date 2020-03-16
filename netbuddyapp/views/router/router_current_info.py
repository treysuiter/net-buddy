from django.shortcuts import render
from netmiko import ConnectHandler
from netbuddyapp.models import NetBuddyUser

def router_current_info(request):

    """
    Handles current router running-config readout on Current Configuration page
    """

    current_user = request.user
    current_netbuddy_user = NetBuddyUser.objects.get(user_id=current_user.id)
	
    if request.method == 'GET':
        try:
            device = {}
            device['device_type'] = 'cisco_ios'
            device['ip'] = f"{current_netbuddy_user.current_router_ip}"
            device['username'] = f"{current_netbuddy_user.ssh_username}"
            device['password'] = f"{current_netbuddy_user.ssh_password}"
            conn = ConnectHandler(**device)
            
            prompt_output = conn.find_prompt()
            uptime_output = conn.send_command("show version | i uptime")
            showrun_output = conn.send_command("show run")
            conn.disconnect()

            template = 'router/router_current_info.html'
            context = {'prompt_output': prompt_output, 'uptime_output': uptime_output, 'showrun_output': showrun_output }

            return render(request, template, context)

        except Exception as exception:

            error_text='Uh oh, looks like something went wrong. Check and see is your device is running, connected, and configured properly.'
            template = 'router/router_current_info.html'
            context = {'error_text': error_text, 'exception': exception}

            return render(request, template, context)

