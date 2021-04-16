from django.shortcuts import render

# Create your views here.
from frame.loginapp.login_userdb import UsersDb
from frame.parkapp.parking_userdb import ParkDb


def loginpage(request):
    return render(request,'login/loginpage.html')

def joinpage(request):

    return render(request,'login/joinpage.html')

def loginimpl(request):
    id = request.POST['id']
    pwd = request.POST['pwd']
    context = { }
    try:
        users = UsersDb().selectid(id)
        parking_floor = ParkDb().select()
        if pwd == users.u_pwd:
            request.session['suser'] = id
            context = {
                'users' : users,
                'login' : 'success',
                'parking_floor' : parking_floor
            }
        else:
            raise Exception
    except:
        context = {
            'login' : 'fail'
        }
        return render(request,'park/parkpage.html',context)
    return render(request,'park/parkpage.html',context)
