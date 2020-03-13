from django.shortcuts import render
from django.contrib.auth.decorators import login_required

@login_required
def router_config_form(request):
    if request.method == 'GET':
        template = 'router/router_config_form.html'
        context = {}

        return render(request, template, context)