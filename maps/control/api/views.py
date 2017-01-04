from django.shortcuts import redirect

from maps import api


def add_map(request):
    api.views.create_map_area(request, form=True)
    return redirect('/admin/maps/maparea/')
