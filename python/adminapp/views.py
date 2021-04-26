from datetime import date, timedelta

from django.http import JsonResponse
from django.shortcuts import render

# Create your views here.
from adminapp.models import Parking
from loginapp.models import Users
from parkapp.models import Users_car, Users_car_ac


def adminpage(request):
    return render(request,'admin/adminpage.html')

def park_adminpage(request):
    u_id = request.session['suser']
    try:
        parking = Parking.objects.filter(u_id=u_id)
        context = {
            'parking': parking
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


def graph1(request):
    teen = Users.objects.filter(u_age__range = (10,20)).count()
    twenty = Users.objects.filter(u_age__range = (20,30)).count()
    thirty = Users.objects.filter(u_age__range = (30,40)).count()
    forty = Users.objects.filter(u_age__range = (40,50)).count()
    fifty = Users.objects.filter(u_age__range = (50,60)).count()
    sixty = Users.objects.filter(u_age__range = (60,70)).count()
    old = Users.objects.filter(u_age__range = (70,150)).count()
    sumage = teen + twenty + thirty + forty + fifty + sixty +old

    datas = [{
        'name': '회원수',
        'data': [
            ['10대 '+str(teen/sumage*100)+'%', teen],
            ['20대 '+str(twenty/sumage*100)+'%', twenty],
            ['30대 '+str(thirty/sumage*100)+'%', thirty],
            ['40대 '+str(forty/sumage*100)+'%', forty],
            ['50대 '+str(fifty/sumage*100)+'%', fifty],
            ['60대 '+str(sixty/sumage*100)+'%', sixty],
            ['60대이상 '+str(old/sumage*100)+'%', old],
        ]
    }]
    context = {
        'datas': datas
    }
    return JsonResponse(context)


def graph2(request):

    man = Users.objects.filter(u_gender="남자").count()
    woman = Users.objects.filter(u_gender="여자").count()
    sum = man + woman

    datas = [{
        'name': '회원수',
        'data': [
            ['남자 ' + str(man / sum * 100) + '%', man],
            ['여자 ' + str(woman / sum * 100) + '%', woman],
        ]
    }]
    context = {
        'datas': datas
    }
    return JsonResponse(context)


def graph3(request):
    users_car = Users_car.objects.values('uc_model')
    datas = []
    numbers = []
    for r in users_car:
        number = Users_car.objects.filter(uc_model=r['uc_model']).count()
        if not [r['uc_model'],number] in datas:
            datas.append([r['uc_model'],number])
            numbers.append(number)
    context = {
        'datas': datas,
        'numbers' : numbers
    }
    return JsonResponse(context)

def graph4(request):
    datas = Users_car_ac.objects.filter(uca_pulse__range = (1,60))
    print(datas)
    datas2 = Users_car_ac.objects.all()
    context = {
        'datas': datas,
    }
    return JsonResponse(context)