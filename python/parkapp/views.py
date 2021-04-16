from django.shortcuts import render

# Create your views here.
from frame.parkapp.parking_userdb import UsersDb


def parkpage(request):
    parking_floor = UsersDb().select()

    context = {
        'parking_floor' : parking_floor
    }
    return render(request,'park/parkpage.html',context)