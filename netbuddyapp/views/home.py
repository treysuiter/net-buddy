from django.shortcuts import render
from netmiko import ConnectHandler

def home(request):
	
    if request.method == 'GET':
        device = {}
        device['device_type'] = 'cisco_ios'
        device['ip'] = '172.16.1.1'
        device['username'] = 'admin'
        device['password'] = 'adminpass1'
        conn = ConnectHandler(**device)
        output = conn.send_command("show version | i uptime")
        template = 'home.html'
        context = {'output': output}

        return render(request, template, context)