from django.shortcuts import render
from ping3 import ping
from netbuddyapp.models import NetBuddyUser

def home(request):

    if request.method == 'GET' and request.user.id:

        current_user = request.user
        current_netbuddy_user = NetBuddyUser.objects.get(user_id=current_user.id)

        ping_info = ping(current_netbuddy_user.current_router_ip)

        template = 'home.html'
        context = {'ping_info': ping_info, 'current_router_ip': current_netbuddy_user.current_router_ip}

        return render(request, template, context)

    elif request.method == 'GET':

        template = 'home.html'
        context = {}

        return render(request, template, context)