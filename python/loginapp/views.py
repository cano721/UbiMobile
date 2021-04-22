from django.shortcuts import render

# Create your views here.
from loginapp.models import Users
from parkapp.models import Parking_floor
from loginapp.serializers import UsersSerializer


def loginpage(request):
    return render(request,'login/loginpage.html')

def joinpage(request):

    return render(request,'login/joinpage.html')

def loginimpl(request):
    id = request.POST['id']
    pwd = request.POST['pwd']
    try:
        usered = Users.objects.get(u_id=id)
        parking_floor = Parking_floor.objects.filter(u_id=id)
        if pwd == usered.u_pwd:
            request.session['suser'] = id
            context = {
                'users' : usered,
                'login' : 'success',
                'parking_floor' : parking_floor
            }
        else:
            raise Exception
    except:
        context = {
            'login' : 'fail'
        }

        return render(request,'login/loginpage.html',context)
    return render(request,'park/parkpage.html',context)
