from django.shortcuts import HttpResponse

def home2(request):
    return HttpResponse("<h1>Demo home2</h1>")


