from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from .router_config_details import get_router_config

#View for handling router config form for new router configs and editing existing router configs

@login_required
def router_config_form(request):

    """
    Form for new config
    """

    if request.method == 'GET':
        template = 'router/router_config_form.html'
        context = {}

        return render(request, template, context)


@login_required
def router_config_edit_form(request, router_config_id):

    """
    Form for editing config
    """

    if request.method == 'GET':
        router_config = get_router_config(router_config_id)

        template = 'router/router_config_form.html'
        context = {
            'router_config': router_config
        }
        return render(request, template, context)
