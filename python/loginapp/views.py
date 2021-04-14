from django.shortcuts import render

# Create your views here.

def loginpage(request):
    return render(request,'login/loginpage.html')

def joinpage(request):
    return render(request,'join/joinpage.html')