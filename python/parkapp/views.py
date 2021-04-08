from django.shortcuts import render

# Create your views here.

def parkpage(request):
    return render(request,'park/parkpage.html')