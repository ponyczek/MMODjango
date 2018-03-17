from django.shortcuts import render

# Create your views here.
def adventure(request):
    return render(request, 'dashboard/adventure.html')
