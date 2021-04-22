from django.shortcuts import render

# Create your views here.
from parkapp.models import Parking_floor


def parkpage(request):
    id = request.session['suser']
    parking_floor = Parking_floor.objects.filter(u_id=id)
    # 조인 기능을 써야함

    context = {
        'parking_floor' : parking_floor
    }
    return render(request,'park/parkpage.html',context)