from django.shortcuts import render

def nb_exception(request, exception):

    """
    Exception message if SSH connection could not be made with Netmiko
    """

    error_text='Uh oh, looks like something went wrong. Check and see is your device is running, connected, and configured properly.'
    template = 'router/router_current_info.html'
    context = {'error_text': error_text, 'exception': exception}

    return render(request, template, context)