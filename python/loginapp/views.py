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
        print(1)
        usered = Users.objects.get(u_id=id)
        print(2)
        parking_floor = Parking_floor.objects.all()
        print(3)
        if pwd == usered.u_pwd:
            print(4)
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
