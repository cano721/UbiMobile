from django.shortcuts import render

# Create your views here.
from frame.loginapp.login_userdb import UsersDb


def loginpage(request):
    return render(request,'login/loginpage.html')

def joinpage(request):

    return render(request,'login/joinpage.html')

def loginimpl(request):
    id = request.post['id']
    pwd = request.post['pwd']
    context = { }
    try:
        users = UsersDb().selectid(id)
        if pwd == users.u_pwd:
            request.session['suser'] = id
            context = {
                'users' : users,
                'login' : 'success'
            }
    except:
        context = {
            'login' : 'fail'
        }
        return render(request,'park/parkpage.html',context)
    return render(request,'park/parkpage.html',context)
