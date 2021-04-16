from django.shortcuts import render

# Create your views here.

def loginpage(request):
    return render(request,'login/loginpage.html')

def joinpage(request):

    return render(request,'login/joinpage.html')

def loginimpl(request):
    id = request.post['id']
    pwd = request.post['pwd']
    context = {  }
    return render(request,'park/parkpage.html',context)