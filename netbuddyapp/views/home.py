from django.shortcuts import render

def home(request):
    if request.method == 'GET':
        template = 'home.html'
        context = {}

        return render(request, template, context)