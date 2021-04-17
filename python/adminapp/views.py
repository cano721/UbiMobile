from django.shortcuts import render

# Create your views here.

def adminpage(request):
    return render(request,'admin/adminpage.html')

def park_adminpage(request):
    return render(request,'admin/park_adminpage.html')