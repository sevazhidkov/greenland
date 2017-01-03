from django.shortcuts import redirect
from maps.models import LatLngBounds, MapArea


def add_map(request):
    print(request.FILES)
    display_bounds = LatLngBounds()
    display_bounds.east = float(request.POST['display_east'])
    display_bounds.north = float(request.POST['display_north'])
    display_bounds.south = float(request.POST['display_south'])
    display_bounds.west = float(request.POST['display_west'])
    display_bounds.save()

    contour_bounds = LatLngBounds()
    contour_bounds.east = float(request.POST['contour_east'])
    contour_bounds.north = float(request.POST['contour_north'])
    contour_bounds.south = float(request.POST['contour_south'])
    contour_bounds.west = float(request.POST['contour_west'])
    contour_bounds.save()

    map_area = MapArea()
    map_area.display_area = display_bounds
    map_area.contour_map_reference = contour_bounds
    print(len(list(request.FILES['contour_map_image'].chunks())))
    map_area.contour_map_image = list(request.FILES['contour_map_image'].chunks())[0]
    map_area.save()

    return redirect('/admin/maps/maparea/')
