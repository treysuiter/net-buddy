from django.shortcuts import render
from ping3 import ping
from netbuddyapp.models import NetBuddyUser

def home(request):

    if request.method == 'GET' and request.user.id:

        current_user = request.user
        current_netbuddy_user = NetBuddyUser.objects.get(user_id=current_user.id)

        router_ping_info = ping(current_netbuddy_user.current_router_ip)

        if current_netbuddy_user.tftp_ip is not None:
            tftp_ping_info = ping(current_netbuddy_user.tftp_ip)
        else:
            tftp_ping_info = None


        template = 'home.html'
        context = {'router_ping_info': router_ping_info, 'tftp_ping_info': tftp_ping_info,'current_netbuddy_user': current_netbuddy_user}

        return render(request, template, context)

    elif request.method == 'GET':

        template = 'home.html'
        context = {}

        return render(request, template, context)