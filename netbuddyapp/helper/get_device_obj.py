
from netbuddyapp.models import NetBuddyUser

def get_device_obj(request):

    """
    creates device object to be used for ConnectHander instantiating
    """
    current_user = request.user
    current_netbuddy_user = NetBuddyUser.objects.get(user_id=current_user.id)
    device = {}
    device['device_type'] = 'cisco_ios'
    device['ip'] = f"{current_netbuddy_user.current_router_ip}"
    device['username'] = f"{current_netbuddy_user.ssh_username}"
    device['password'] = f"{current_netbuddy_user.ssh_password}"

    return device