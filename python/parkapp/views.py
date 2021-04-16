from django.shortcuts import render

# Create your views here.
from frame.parkapp.parking_userdb import ParkDb


def parkpage(request):
    parking_floor = ParkDb().select()

    context = {
        'parking_floor' : parking_floor
    }
    return render(request,'park/parkpage.html',context)