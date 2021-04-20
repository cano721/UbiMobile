from django.shortcuts import render

# Create your views here.


def parkpage(request):
    parking_floor = Parking_floor.objects.get()
    context = {
        'parking_floor' : parking_floor
    }
    return render(request,'park/parkpage.html',context)