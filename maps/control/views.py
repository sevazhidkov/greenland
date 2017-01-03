from django.shortcuts import render


def create_map(request):
    if request.method == 'GET':
         return render(request, 'maps/control/add.html')
