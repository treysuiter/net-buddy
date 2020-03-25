from django.urls import reverse
from django.shortcuts import redirect
from django.contrib.auth import logout

def logout_user(request):
    """
    Handles logout
    """
    logout(request)
    return redirect(reverse('netbuddyapp:home'))