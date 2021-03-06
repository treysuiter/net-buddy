from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User

#Form to for NetbuddyUser model properties

class RegisterForm(UserCreationForm):

    """
    Form to extend Django's registration
    """
    current_router_ip = forms.CharField(max_length=55)
    current_vlan_ip = forms.CharField(max_length=55, required=False, help_text='(Optional)')
    tftp_ip = forms.CharField(max_length=55, required=False, help_text='(Optional)')
    ssh_username = forms.CharField(max_length=55)
    ssh_password = forms.CharField(max_length=55)

    class Meta:
        model = User
        fields = ('username', 'current_router_ip', 'current_vlan_ip', 'tftp_ip', 'ssh_username', 'ssh_password','password1', 'password2', )