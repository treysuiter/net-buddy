from django.contrib.auth import login, authenticate
from django.contrib.auth.forms import UserCreationForm
from django.shortcuts import render, redirect

from netbuddyapp.forms.register_form import RegisterForm

def register(request):
    if request.method == 'POST':
        form = RegisterForm(request.POST)
        if form.is_valid():
            user = form.save()
            user.netbuddyuser.current_router_ip = form.cleaned_data.get('current_router_ip')
            user.netbuddyuser.current_vlan_ip = form.cleaned_data.get('current_vlan_ip')
            user.netbuddyuser.ssh_username = form.cleaned_data.get('ssh_username')
            user.netbuddyuser.ssh_password = form.cleaned_data.get('ssh_password')
            user.save()
            raw_password = form.cleaned_data.get('password1')
            user = authenticate(username=user.username, password=raw_password)
            login(request, user)
            return redirect('netbuddyapp:routerconfiglist')
    else:
        form = RegisterForm()
    return render(request, 'registration/register.html', {'form': form})