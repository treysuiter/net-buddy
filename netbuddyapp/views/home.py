# from django.shortcuts import render
# from netmiko import ConnectHandler

# file_name = 'nss_net_config'

# copy_to_tftp = f'copy running-config tftp://172.16.1.5/{file_name}'
# copy_from_tftp = f'copy tftp://172.16.1.5/{file_name} running-config'
# show_uptime = "show version | i uptime"
# show_run = "show run"

# def home(request):
	
#     if request.method == 'GET':
#         device = {}
#         device['device_type'] = 'cisco_ios'
#         device['ip'] = '172.16.1.1'
#         device['username'] = 'admin'
#         device['password'] = 'adminpass1'
#         conn = ConnectHandler(**device)

#         #change variable here
#         output = conn.send_command(show_run)

#         template = 'home.html'
#         context = {'output': output}

#         return render(request, template, context)

from django.shortcuts import render

def home(request):
    if request.method == 'GET':
        template = 'home.html'
        context = {}

        return render(request, template, context)