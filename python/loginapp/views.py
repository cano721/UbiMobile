from django.shortcuts import render

# Create your views here.


def loginpage(request):
    return render(request,'login/loginpage.html')

def joinpage(request):

    return render(request,'login/joinpage.html')

def loginimpl(request):
    id = request.POST['id']
    pwd = request.POST['pwd']
    try:
        users = Users.objects.get(u_id,id)
        parking_floor = Parking_floor.objects.get()
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
