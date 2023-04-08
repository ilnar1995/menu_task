from django.shortcuts import render

# Create your views here.
from django.shortcuts import render
from .models import ModelMixin, Menu


def main(request):
    menu_instances = Menu.objects.all()
    context = {'all_menu': menu_instances}

    return render(request, 'menu/main.html', context)

def menu_view(request, menu_slug, p):
    context = {'menu_slug': menu_slug, 'path_list': p.split('/')}

    return render(request, 'menu/body.html', context)

def main_view(request, menu_slug):
    context = {'menu_slug': menu_slug}

    return render(request, 'menu/body.html', context)
