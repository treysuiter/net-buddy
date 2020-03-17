from django.contrib.auth.decorators import login_required
from django.shortcuts import render
from netmiko import ConnectHandler
from netbuddyapp.models import NetBuddyUser

@login_required
def router_commands(request):

    form_data = request.GET
    current_user = request.user
    current_netbuddy_user = NetBuddyUser.objects.get(user_id=current_user.id)
    device = {}
    device['device_type'] = 'cisco_ios'
    device['ip'] = f"{current_netbuddy_user.current_router_ip}"
    device['username'] = f"{current_netbuddy_user.ssh_username}"
    device['password'] = f"{current_netbuddy_user.ssh_password}"

    if request.method == 'GET':


        if (
            "actual_method" in form_data
            and form_data["actual_method"] == "SHOW_IP_INTERFACES_BRIEF"
        ):
            conn = ConnectHandler(**device)
            output = conn.send_command('show ip interface brief')
            template = 'router/router_commands.html'
            context = {
                'output': output
            }

            return render(request, template, context)

        else:
            
            template = 'router/router_commands.html'
            context = {
            }

            return render(request, template, context)