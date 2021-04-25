from django.http import JsonResponse
from django.shortcuts import render

# Create your views here.
from rest_framework.parsers import JSONParser

from loginapp.models import Users
from parkapp.models import Parking_floor, Users_car
from loginapp.serializers import UsersSerializer
from parkapp.serializers import Parking_floorSerializer, Users_carSerializer


def loginpage(request):
    return render(request,'login/loginpage.html')

def testpage(request):

    return render(request,'login/testpage.html')


def joinpage(request):

    return render(request,'login/joinpage.html')

def parkjoin(request):

    return render(request,'login/parkjoin.html')
def reservation(request):

    return render(request,'login/reservation.html')


def loginimpl(request):
    id = request.POST['id']
    pwd = request.POST['pwd']
    try:
        usered = Users.objects.get(u_id=id)
        parking_floor = Parking_floor.objects.filter(u_id=id)
        if pwd == usered.u_pwd:
            request.session['suser'] = id
            if parking_floor:
                pass
            else:
                parking_floor = ""
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

def joinimpl(request):
    id = request.POST['id']
    pwd = request.POST['pwd']
    name = request.POST['name']
    age = request.POST['age']
    gender = request.POST['gender']
    email = request.POST['email']

    try:
        data = Users(u_id=id,u_gender=gender,u_pwd=pwd,u_name=name,u_age=age,u_email=email)
        data.save()
        usered = Users.objects.get(u_id=id)
        parking_floor = Parking_floor.objects.filter(u_id=id)
        print("회원가입성공")
        request.session['suser'] = id
        if parking_floor:
            pass
        else:
            parking_floor = ""
        context = {
            'users' : usered,
            'login' : 'success',
            'parking_floor' : parking_floor
        }
    except:
        context = {
            'login' : 'fail'
        }
        return render(request,'login/joinpage.html',context)
    return render(request,'park/parkpage.html',context)

def loginAndroid(request):
    if request.method == 'POST': # 안드로이드에서 post방식으로 보내오면
        data = JSONParser().parse(request) # json형태로 파서
        print(1)
        id = data['id'] #id라는 이름으로 보내진 값 추출
        print(2)
        obj = Users.objects.get(u_id=id) # 아이디에 맞는 데이터베이스 내용 셀렉트
        # 패스워드비교
        if data['password'] == obj.u_pwd: #패스워드도 맞을경우
            serializer = UsersSerializer(obj)
            print("장고에서 확인중...")
            return JsonResponse(serializer.data,safe=False, json_dumps_params={'ensure_ascii':False})
        else:
            return JsonResponse("fail",safe=False, json_dumps_params={'ensure_ascii':False})

def ParkingAndroid(request):
    if request.method == 'POST': # 안드로이드에서 post방식으로 보내오면
        data = JSONParser().parse(request) # json형태로 파서
        id = data['id'] #id라는 이름으로 보내진 값 추출
        parking_floor = Parking_floor.objects.filter(u_id=id) #id에 딸린 내용 가져오기
        serializer = Parking_floorSerializer(parking_floor, many=True) #json형태로 만들기
        print("장고에서 확인중...")
        print(serializer.data)
        return JsonResponse(serializer.data,safe=False, json_dumps_params={'ensure_ascii':False})
    else:
        return JsonResponse("fail",safe=False, json_dumps_params={'ensure_ascii':False})

def UsersCarAndroid(request):
    if request.method == 'POST': # 안드로이드에서 post방식으로 보내오면
        data = JSONParser().parse(request) # json형태로 파서
        id = data['id'] #id라는 이름으로 보내진 값 추출
        users_car = Users_car.objects.filter(u_id=id) #id에 딸린 내용 가져오기
        serializer = Users_carSerializer(users_car, many=True) #json형태로 만들기
        print("장고에서 확인중...")
        print(serializer.data)
        return JsonResponse(serializer.data,safe=False, json_dumps_params={'ensure_ascii':False})
    else:
        return JsonResponse("fail",safe=False, json_dumps_params={'ensure_ascii':False})