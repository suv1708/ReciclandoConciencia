from django.shortcuts import render

# Create your views here.

def home(request):
    return render(request, 'core/home.html')



def advices(request):
    return render(request, 'core/advices.html')


def gallery(request):
    return render(request, 'core/gallery.html')

def about(request):
    return render(request, 'core/about.html')


