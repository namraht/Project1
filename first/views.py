from django.shortcuts import render

# Create your views here.
import urllib2
import json
import math
from rest_framework.parsers import JSONParser
from rest_framework.response import Response
from rest_framework.views import APIView
from django.contrib.auth import authenticate
from django.http import HttpResponse

from first.models import Repairer, Customer, AUser, Shop, Expertise, Favourites, CustomerRating, RepairerRating
from django.db.models import Avg, Max



class Register(APIView):
    """
    A view that can accept POST requests with JSON content.
    """
    parser_classes = (JSONParser,)

    def post(self, request, format=None):
        url="http://192.168.0.7:8000/register/"
        body_unicode = request.body.decode('utf-8')
        userdata = json.loads(body_unicode)

        category=userdata['category']
        uname = userdata['uname']
        fname = userdata['fname']
        lname = userdata['lname']
        password = userdata['password']
        email=userdata['email']
        #expertise=""
        secretque=userdata['secretque']
        secretans= userdata['secretans']
       # shop = ""
        phone=userdata['phoneno']
        cnic=userdata['cnic']
        lon=userdata['longitude']
        lat=userdata['latitude']

        if category == 'Repairer':
            expertise = userdata['expertise']
            shop = userdata['shop']
            try:
                maxId = Shop.objects.aggregate(Max('id'))
                if maxId == None:
                    no= 1
                elif maxId!=None:
                    no = maxId['id__max']+1

                shopp= Shop.objects.get(name=shop)

            except Shop.DoesNotExist:
                shopp=Shop(id=no,name=shop)
                shopp.save()
                shoppid=shopp
            else:
                shoppid=shopp
            repairer = Repairer.objects.create_user(email=email,password=password, fname=fname,lname=lname,uname=uname,phone=phone,secretque=secretque,secretans=secretans,cnic=cnic,lon=lon,lat=lat,shopid=shoppid)
            repairer.set_password(password)
            repairer.save();

            expList = expertise.split(',')
            print (expList)
            for exp in expList[:-1]:
                expertisse = Expertise(username=repairer, workCategory=exp)
                print (exp)
                expertisse.save()

            #expertisse=Expertise(username=repairer,workCategory=expertise)
            #expertisse.save()
        elif category=='Client':
            customer = Customer.objects.create_user(email=email, password=password, fname=fname, lname=lname,uname=uname, phone=phone, secretque=secretque, secretans=secretans,cnic=cnic,lon=lon,lat=lat)
            customer.set_password(password)
            customer.save();

        return Response({'received data': request.data})

class CheckUsername(APIView):
    parser_classes = (JSONParser,)

    def post(self, request, format=None):
        url = "http://192.168.0.7:8000/checkusername/"
        body_unicode = request.body.decode('utf-8')
        userdata = json.loads(body_unicode)


        uname = userdata['uname']
        try:
            user = AUser.objects.get(username=uname)
        except AUser.DoesNotExist:
            return Response(data={'message': False})  # return false as user does not exist
        else:
            return Response(data={'message': True})

class SecretQuesFromUsername(APIView):
    parser_classes = (JSONParser,)

    def post(self, request, format=None):
        url = "http://192.168.0.7:8000/getsecretqueans/"
        body_unicode = request.body.decode('utf-8')
        userdata = json.loads(body_unicode)

        uname = userdata['uname']
        try:
            user = Repairer.objects.get(username=uname)

        except Repairer.DoesNotExist:
            try:
                user = Customer.objects.get(username=uname)
            except Customer.DoesNotExist:
                return Response(data={'SecretQuestion': ''})  # return false as user does not exist
            else:
                secretQuestion = user.secretQuestion
                return Response(data={'SecretQuestion': secretQuestion})
        else:
            secretQuestion = user.secretQuestion
            return Response(data={'SecretQuestion': secretQuestion})

class MatchSecretAns(APIView):
    parser_classes = (JSONParser,)

    def post(self, request, format=None):
        url = "http://192.168.0.7:8000/matchsecretans/"
        body_unicode = request.body.decode('utf-8')
        userdata = json.loads(body_unicode)

        uname = userdata['uname']
        secretAns1=userdata['secretAns']
        try:
            user = Repairer.objects.get(username=uname)


        except Repairer.DoesNotExist:
            try:
                user = Customer.objects.get(username=uname)
            except Customer.DoesNotExist:
                return Response(data={'message': False})  # return false as user does not exist
            else:
                secretAns = user.secretAnswer
                if secretAns == secretAns1:
                    return Response(data={'message': True})
                else:
                    return Response(data={'message': False})

        else:
            secretAns = user.secretAnswer
            if secretAns == secretAns1:
                return Response(data={'message': True})
            else:
                return Response(data={'message': False})

class ChangePassword(APIView):
    parser_classes = (JSONParser,)

    def post(self, request, format=None):
        url = "http://192.168.0.7:8000/changepassword/"
        body_unicode = request.body.decode('utf-8')
        userdata = json.loads(body_unicode)

        uname = userdata['uname']
        password=userdata['password']
        try:
            user = AUser.objects.get(username=uname)


        except AUser.DoesNotExist:
            return Response(data={'message': False})  # return false as user does not exist

        else:
            user.password=password
            user.set_password(password)
            user.save()
            return Response(data={'message': True})
           
class GetProfile(APIView):
    parser_classes = (JSONParser,)

    def post(self, request, format=None):
        url = "http://192.168.0.7:8000/getProfile/"
        body_unicode = request.body.decode('utf-8')
        userdata = json.loads(body_unicode)
        uname = userdata['uname']
        fav=None
        revList=[]
        favList=[]
        expList=[]
        data = {}
        password = userdata['password']

        try:
            check = Repairer.objects.get(username=uname)
        except Repairer.DoesNotExist:
            try:
                check = Customer.objects.get(username=uname)
            except Customer.DoesNotExist:
                return Response(data={'message': False})  # return null as username does not exist
            else:
                user = authenticate(username=uname, password=password)
                if user is not None:
                    data['message']=True
                    data['uname'] = check.username
                    data['fname'] = check.first_name
                    data['lname'] = check.last_name
                    data['email'] = check.email
                    data['password'] = check.password
                    data['cnic'] = check.cnic
                    data['contactno']=check.contactNo
                    data['category']="Customer"
                    data['reviews']=[]
                    data['latitude']=check.latitude
                    data['longitude']=check.longitude
                    data['favourites']=[]

                    fav = Favourites.objects.filter(c_username__username=uname)
                    if(fav):
                        for i in fav:
                            favList.append(i.r_username)
                        data['favourites'] = favList

                    rev=CustomerRating.objects.filter(c_username__username=uname)
                    if(rev):
                        for i in rev:
                            revList.append(i.reviews)
                        data['reviews']=revList
                    avgRating=rev.aggregate(Avg('rating'))
                    data['avgRating']=avgRating['rating__avg']
                    return Response(data)  # return true as user exist
                else:
                    return Response(data={'message': False})  # return fasle as user does not exist
        else:
            user = authenticate(username=uname, password=password)
            if user is not None:
                data['message'] = True
                data['uname'] = check.username
                data['fname'] = check.first_name
                data['lname'] = check.last_name
                data['email'] = check.email
                data['password'] = check.password
                data['cnic'] = check.cnic
                data['contactno'] = check.contactNo
                data['category']="Repairer"
                data['latitude'] = check.latitude
                data['longitude'] = check.longitude
                data['reviews'] = []
                data['expertise']=[]
                exp=Expertise.objects.filter(username__username=uname)
                if(exp):
                    for i in exp:
                        expList.append(i.workCategory)
                    data['expertise'] = expList

                rev = RepairerRating.objects.filter(r_username__username=uname)
                if (rev):
                    for i in rev:
                        revList.append(i.reviews)
                    data['reviews'] = revList
                avgRating = rev.aggregate(Avg('rating'))
                data['avgRating'] = avgRating['rating__avg']
                shopId=check.shopid
                try:
                    shop=Shop.objects.get(id=shopId.id)
                except Shop.DoesNotExist:
                    data['shop'] =None
                else:
                    data['shop']=check.shopid.name
                return Response(data)  # return true as user exist
            else:
                return Response(data={'message': False})  # return fasle as user does not exist

class GetRepairersList(APIView):
    parser_classes = (JSONParser,)

    def post(self, request, format=None):
        url = "http://192.168.0.7:8000/getProfile/"
        body_unicode = request.body.decode('utf-8')
        info=json.loads(body_unicode)
        uname=info['uname']
        user = Customer.objects.get(username=uname)
        lat=user.latitude
        lon=user.longitude
        radius=info['radius']
        if (radius=='2 km'):
            radius=2
        category=info['category']
        r=radius*2
        r=r/2
        minLatitude = lat - r
        maxLatitude= lat + r
        minLongitude= (lon * 2) / 60 * (math.cos(math.radians(minLatitude)))
        maxLongitude= (lon * 2) / 60 * (math.cos(math.radians(maxLatitude)))
        repairerList=Repairer.objects.all()
        dictArray=[]
        dictObject={}
        for r in repairerList:
            rev = RepairerRating.objects.filter(r_username__username=r.username)
            avgRating = rev.aggregate(Avg('rating'))
            dictObject = {
                'username':r.username,
                'rating':avgRating['rating__avg'],
            }
            dictArray.append(dictObject)
     #       dictObject['username']=r.username
      #      rev = RepairerRating.objects.filter(r_username__username=r.username)
       #     avgRating = rev.aggregate(Avg('rating'))
        #    dictObject['rating']=avgRating
        data={}
        data['data']=dictArray
        return Response(data)

class GiveFavourites(APIView):
    parser_classes = (JSONParser,)

    def post(self, request, format=None):
        url = "http://192.168.0.7:8000/changepassword/"
        body_unicode = request.body.decode('utf-8')
        userdata = json.loads(body_unicode)

        uname = userdata['uname']
        try:
            repairerList = Favourites.objects.filter(c_username__username=uname)
            dictArray = []
            dictObject = {}
            for r in repairerList:
                rev = RepairerRating.objects.filter(r_username__username=r.r_username)
                avgRating = rev.aggregate(Avg('rating'))
                dictObject = {
                    'username': r.r_username,
                    'rating': avgRating['rating__avg'],
                }
                dictArray.append(dictObject)

            data = {}
            data['data'] = dictArray
            return Response(data)


        except Favourites.DoesNotExist:
            return Response(data={'message': False})  # return false as user does not exist

class DeleteFavourite(APIView):
    parser_classes = (JSONParser,)

    def post(self, request, format=None):
        url = "http://192.168.0.7:8000/changepassword/"
        body_unicode = request.body.decode('utf-8')
        userdata = json.loads(body_unicode)

        c_username = userdata['c_username']
        r_username=userdata['r_username']
        try:
            user = Favourites.objects.filter(c_username__username=c_username,r_username=r_username)
            user.delete()
            return Response(data={'message': True})

        except AUser.DoesNotExist:
            return Response(data={'message': False})  # return false as user does not exist

class GetRepairersListByUsername(APIView):
    parser_classes = (JSONParser,)

    def post(self, request, format=None):
        url = "http://192.168.0.7:8000/getProfile/"
        body_unicode = request.body.decode('utf-8')
        info=json.loads(body_unicode)
        rname=info['r_username']

        repairerList=Repairer.objects.filter(username__contains=rname)
        dictArray=[]
        dictObject={}
        for r in repairerList:
            rev = RepairerRating.objects.filter(r_username__username=r.username)

            avgRating = rev.aggregate(Avg('rating'))

            dictObject = {
                'username': r.username,
                'rating': avgRating['rating__avg'],
            }


            dictArray.append(dictObject)
        data={}
        data['data']=dictArray
        return Response(data)

class AddFavourite(APIView):
    parser_classes = (JSONParser,)

    def post(self, request, format=None):
        url = "http://192.168.0.7:8000/changepassword/"
        body_unicode = request.body.decode('utf-8')
        userdata = json.loads(body_unicode)

        c_username = userdata['c_username']
        try:
            client=Customer.objects.get(username=c_username)
        except Customer.DoesNotExist:
            return Response(data={'message': False})
        else:
            r_username = userdata['r_username']

            favourite = Favourites(c_username=client,r_username=r_username)
            favourite.save()
            return Response(data={'message': True})

class ShowRepairerProfile(APIView):
    parser_classes = (JSONParser,)

    def post(self, request, format=None):
        url = "http://192.168.0.7:8000/getProfile/"
        body_unicode = request.body.decode('utf-8')
        userdata = json.loads(body_unicode)
        cname=userdata['c_username']
        rname = userdata['r_username']
        fav=None
        revList=[]
        clientList=[]
        rateList=[]
        favList=[]
        expList=[]
        data = {}
        try:
            check = Repairer.objects.get(username=rname)
        except Repairer.DoesNotExist:
            return Response(data)

        else:
            data['message'] = True
            data['uname'] = check.username
            data['fname'] = check.first_name
            data['lname'] = check.last_name
            data['email'] = check.email
            data['password'] = check.password
            data['cnic'] = check.cnic
            data['contactno'] = check.contactNo
            data['category'] = "Repairer"
            data['latitude'] = check.latitude
            data['longitude'] = check.longitude
            data['reviews'] = [""]
            data['expertise'] = [""]
            data['clientList'] = [""]
            exp = Expertise.objects.filter(username__username=rname)
            if (exp):
                for i in exp:
                    expList.append(i.workCategory)
                data['expertise'] = expList

            rev = RepairerRating.objects.filter(r_username__username=rname)
            if (rev):
                for i in rev:
                    revList.append(i.reviews)
                    rateList.append(i.rating)
                    clientList.append(i.c_username)
                data['reviews'] = revList
                data['ratings'] = rateList
                data['clientList'] = clientList
            avgRating = rev.aggregate(Avg('rating'))
            data['avgRating'] = avgRating['rating__avg']
            shopId = check.shopid
            try:
                shop = Shop.objects.get(id=shopId.id)
            except Shop.DoesNotExist:
                data['shop'] = None
            else:
                data['shop'] = check.shopid.name
            isFav=Favourites.objects.filter(c_username__username=cname,r_username=rname)
            if isFav.exists():
                data['isFav']=True
            else:
                data['isFav']=False

            return Response(data)  # return true as user exist

class SearchRepairerResult(APIView):
    parser_classes = (JSONParser,)

    def post(self, request, format=None):
        url = "http://192.168.0.7:8000/SearchRepairerResult/"
        body_unicode = request.body.decode('utf-8')
        userdata = json.loads(body_unicode)
        category=userdata['expertise']

        try:
            repairerList = Repairer.objects.all()
            expertise = Expertise.objects.filter(workCategory__contains=category)
            rating = []
            expList = []
            expertiseList = []
            data = {}
            dictArray = []
            ratingList=[]

            if expertise:
                for r in repairerList:
                    exp = Expertise.objects.filter(username__username__contains=r.username,workCategory__contains=category)
                    expList.append(exp.values('username__username'))
                    expertiseList.append(exp.values('username__username'))


                if expList:
                    data['users'] = expertiseList
                    while len(expList) > 0:
                        rev = RepairerRating.objects.filter(r_username__username=expList.pop(0))
                        if rev:
                            avgRating = rev.aggregate(Avg('rating'))
                            rating = avgRating['rating__avg']
                            ratingList.append(round(rating,1))
                        else:
                            rating = 'NoRating'
                            ratingList.append(rating)

                    data['avgRating'] = ratingList
                    data['message'] = True
                    return Response(data)
            else:
                return Response(data={'message': False})  # return false as user does not exist

        except Exception:
            return Response(data={'message': False})  # return null as user does not exist

class GetRepairersListByExpertise(APIView):
    parser_classes = (JSONParser,)

    def post(self, request, format=None):
        url = "http://192.168.0.7:8000/getProfile/"
        body_unicode = request.body.decode('utf-8')
        info=json.loads(body_unicode)
        expertise=info['expertise']
        try:
            repairerList=Expertise.objects.filter(workCategory__contains=expertise)
            dictArray=[]
            dictObject={}
            for r in repairerList:
                rev = RepairerRating.objects.filter(r_username__username=r.username)
                avgRating = rev.aggregate(Avg('rating'))
                dictObject = {
                    'username': r.username.username,
                    'rating': avgRating['rating__avg'],
                }
                dictArray.append(dictObject)
            data={}
            data['data']=dictArray
        except Exception:
            data['data']=[]
        return Response(data)
		


class EditCustomerProfile(APIView):
    """
    A view that can accept POST requests with JSON content.
    """
    parser_classes = (JSONParser,)
    def post(self, request, format=None):
        body_unicode = request.body.decode('utf-8')
        userdata = json.loads(body_unicode)

        unamePrevious = userdata['unamePrevious']
        uname = userdata['uname']
        fname = userdata['fname']
        lname = userdata['lname']
        password = userdata['password']
        email = userdata['email']
        phone = userdata['phoneno']
        lon = userdata['longitude']
        lat = userdata['latitude']
        try:
            user = Customer.objects.get(username=unamePrevious)
            if user:
                user.username = uname
                user.first_name = fname
                user.last_name = lname
                user.email = email
                user.contactNo = phone
                user.longitude = lon
                user.latitude = lat
                user.password = password
                user.set_password(password)
                user.save()
                return Response(data={'message': True})

        except Customer.DoesNotExist:
            return Response(data={'message': False})  # return false as user does not exist

		


class EditRepairerProfile(APIView):
    parser_classes = (JSONParser,)
    def post(self, request, format=None):
        body_unicode = request.body.decode('utf-8')
        userdata = json.loads(body_unicode)

        unamePrevious = userdata['unamePrevious']
        uname = userdata['uname']
        fname = userdata['fname']
        lname = userdata['lname']
        shop = userdata['shop']
        password = userdata['password']
        email = userdata['email']
        phone = userdata['phoneno']
        lon = userdata['longitude']
        lat = userdata['latitude']
        try:
            user = Repairer.objects.get(username=unamePrevious)
            if user:
                user.username = uname
                user.first_name = fname
                user.last_name = lname
                user.email = email
                user.contactNo = phone
                user.longitude = lon
                user.latitude = lat
                user.password = password
                user.set_password(password)

                try:
                    maxId = Shop.objects.aggregate(Max('id'))
                    if maxId == None:
                        no = 1
                    elif maxId != None:
                        no = maxId['id__max'] + 1

                    shopp = Shop.objects.get(name=shop)
                except Shop.DoesNotExist:
                    shopp = Shop(id=no, name=shop)
                    shopp.save()
                    shoppid = shopp
                else:
                    shoppid = shopp

                user.shopid = shoppid
                user.save()

                return Response(data={'message': True})

        except Repairer.DoesNotExist:
            return Response(data={'message': False})  # return false as user does not exist


class AddDelExpertise(APIView):
    """
    A view that can accept POST requests with JSON content.
    """
    parser_classes = (JSONParser,)
    def post(self, request, format=None):
        body_unicode = request.body.decode('utf-8')
        userdata = json.loads(body_unicode)
        expertise = userdata['expertise']
        r_username=userdata['r_username']
        try:
            repairer=Repairer.objects.get(username=r_username)
            expOld=Expertise.objects.filter(username=repairer)
            expOld.delete()
            expList = expertise.split(',')
            print (expList)
            for exp in expList[:-1]:
                expertisse = Expertise(username=repairer, workCategory=exp)
                print (exp)
                expertisse.save()
            return Response(data={'message': True})
        except Repairer.DoesNotExist:
            return Response(data={'message': False})

class GiveExpertise(APIView):
    """
    A view that can accept POST requests with JSON content.
    """
    parser_classes = (JSONParser,)
    def post(self, request, format=None):
        body_unicode = request.body.decode('utf-8')
        userdata = json.loads(body_unicode)
        r_username = userdata['r_username']
        data = {}
        try:
            repairer=Repairer.objects.get(username=r_username)
            exp=Expertise.objects.filter(username=repairer)
            dictArray = []
            for e in exp:
                dictArray.append(e.workCategory)

            data['data']=dictArray
         #   data['expertise']=dictArray

            return Response(data)
        except Repairer.DoesNotExist:
            return Response(data)

'''
def signup(request):
    unamePrevious = 'g'
    uname = 'g'
    fname = 'g'
    lname = 'g'
    password = 'g'
    email = 'g@gmail.com'
    shop = 'RepairHub'
    phone = '123'
    lon = 74.356913
    lat = 31.554735

    try:
        user = Repairer.objects.get(username=unamePrevious)
        if user:
            user.username = uname
            user.first_name = fname
            user.last_name = lname
            user.email = email
            user.contactNo = phone
            user.longitude = lon
            user.latitude = lat
            user.password = password
            user.set_password(password)

            try:
                maxId = Shop.objects.aggregate(Max('id'))
                if maxId == None:
                    no= 1
                elif maxId!=None:
                    no = maxId['id__max']+1

                shopp= Shop.objects.get(name=shop)
            except Shop.DoesNotExist:
                shopp=Shop(id=no,name=shop)
                shopp.save()
                shoppid=shopp
            else:
                shoppid=shopp

            user.shopid=shoppid
            user.save()

            return HttpResponse("Data Saved")

    except Repairer.DoesNotExist:
        return HttpResponse("Data not Saved")

'''