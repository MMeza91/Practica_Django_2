from django.shortcuts import render

# Create your views here.
def home(request):
    return render(request,"home.html",{})

def test(request, variable):
    return render(request,"test.html",{"variable": variable })