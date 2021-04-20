from django.shortcuts import render

# Create your views here.


def adminpage(request):
    return render(request,'admin/adminpage.html')

def park_adminpage(request):
    u_id = request.session['suser']
    try:
        parking = Parking.objects.get(u_id=u_id)
        context = {
            "parking": parking
        }
        print(parking)
        return render(request,'admin/park_adminpage.html',context)
    except:
        return render(request,'admin/park_adminpage.html')

def car_infopage(request):
    u_id = request.session['suser']

    return render(request,'admin/car_infopage.html')

def data_infopage(request):
    u_id = request.session['suser']

    return render(request,'admin/data_infopage.html')

def park_adminUpdate(request):
    u_id = request.session['suser']

    return render(request,'admin/park_adminUpdate.html')