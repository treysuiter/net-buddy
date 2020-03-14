from django.shortcuts import render
from netmiko import ConnectHandler
from netbuddyapp.models import NetBuddyUser

def router_current_info(request):

    current_user = request.user
    current_netbuddy_user = NetBuddyUser.objects.get(user_id=current_user.id)
	
    if request.method == 'GET':
        device = {}
        device['device_type'] = 'cisco_ios'
        device['ip'] = f"{current_netbuddy_user.current_router_ip}"
        device['username'] = f"{current_netbuddy_user.ssh_username}"
        device['password'] = f"{current_netbuddy_user.ssh_password}"
        conn = ConnectHandler(**device)
        
        prompt_output = conn.find_prompt()
        uptime_output = conn.send_command("show version | i uptime")
        showrun_output = conn.send_command("show run")

        template = 'router/router_current_info.html'
        context = {'prompt_output': prompt_output, 'uptime_output': uptime_output, 'showrun_output': showrun_output }

        return render(request, template, context)