from django.shortcuts import redirect, render
from .models import *
from . import Checksum
from django.conf import settings
from django.http import HttpResponse
from django.views.decorators.csrf import csrf_exempt
from app.utils import VerifyPaytmResponse
import requests

# Create your views here.

def index(request):
    cat = Category.objects.all()
    data=Product.objects.all()
    
    return render(request,'index.html',{'cat':cat,'data':data})

def base(request):
    cat = Category.objects.all()

    return render(request,'base.html',{'cat':cat})

def signup(request):
    cat = Category.objects.all()
    if request.method == "POST":
        Fullname = request.POST['Fullname']
        Username = request.POST['Username']
        Email = request.POST['Email']
        Password = request.POST['Password']
        user = User(Fullname=Fullname,Username=Username,Email=Email,Password=Password)
        user.save()
        return redirect('login')
    return render(request,'signup.html',{'cat':cat})

def Login(request):
    cat = Category.objects.all()

    if request.method == "POST":
        Email = request.POST['Email']
        Password = request.POST['Password']
        user = User(Email=Email,Password=Password)
        if user:
            request.session['user']=Email
            return redirect('/')
    return render(request,'Login.html',{'cat':cat})

def product(request):
    cid=request.GET.get("cid")
    prod=Product.objects.filter(cname__id=cid)
    return render(request,'product.html',{'prod':prod})

def detail(request):
    cat = Category.objects.all()
    cid=request.GET.get("cid")
    prod = Product.objects.get(pk=cid)

    return render(request,'detail.html',{'prod':prod,'cat':cat})

def pluse(requist,id):
    r1 = Cart.objects.get(id=id)
    total = r1.Prodect.p_price
    print(total,"TTTTTTTTTTTTTTTTTTTt")
    r1.quantity+=1
    r1.subtotal = total * r1.quantity
    print(r1.subtotal,"ssssssssssss")
    r1.save()
    print(r1,"RRRRRRRRR")
    return redirect('/showcart')

def min(request,id):
    m1 = Cart.objects.get(id=id)
    total = m1.Prodect.p_price
    print(total,"price")
    m1.quantity-=1
    m1.subtotal = total*m1.quantity
    print(m1,"dsder") 
    m1.save()
    print(m1,"aaa")
    return redirect('/showcart')

def addtocart(request,id):
    cat = Category.objects.all()
    con={}
    if 'user' in request.session:
        user=request.session['user']
        user_info=User.objects.get(Email=user)
        prod=Product.objects.get(id=id)
        cartexist=Cart.objects.filter(Prodect__p_name=prod.p_name)
        qty=1
        if cartexist:
            return redirect('showcart')
        else:
            obj=Cart(Prodect=prod,User=user_info,quantity=qty,subtotal=prod.p_price)
            obj.save()
            return redirect('showcart')
        con['Cart']=Cart.objects.filter(User__Email=user_info)
        return render(request,'addtocart.html',{'cat':cat})
    else:
        return redirect('login')

def showcart(request):
    con={}
    con['cat'] = Category.objects.all()
    if 'user' in request.session:
        user=request.session['user']
        user_info=User.objects.get(Email=user)
        c1=Cart.objects.filter(User__id=user_info.id)
        list1=[]
        subtotal=0
        for i in c1:
            list1.append(i.Prodect.p_price)
            subtotal+=i.subtotal
        l1=sum(list1)
        con['Cart']=c1
        con['subtotal']=subtotal
        request.session['subtotal']=subtotal
    return render(request,'addtocart.html',con)

def Logout(request):
    if 'user' in request.session:
        del request.session['user']
    return redirect('/')

def addaddress(request):
    cat = Category.objects.all()

    if 'user' in request.session:
        if request.method == "POST":
            user=request.session['user']
            user_info=User.objects.get(Email=user)
            name = request.POST['name']
            address = request.POST['address']
            pno = request.POST['pno']
            country = request.POST['country']
            city = request.POST['city']
            state = request.POST['state']
            pincode = request.POST['pincode']
            user = Detail(user=user_info,name=name,address=address,pno=pno,contry=country,city=city,state=state,pincode=pincode)
            user.save()
    return render(request,"addaddress.html",{'cat':cat})

def checkout(request):
    con={}
    if 'user' in request.session:
        if request.method=='POST':
            user=request.session['user']
            user_info=User.objects.get(Email=user)
            det=Detail.objects.filter(user=user_info)
            choice_id=request.POST.get('choice')
            det_id=Detail.objects.get(id=choice_id)
            c1=Cart.objects.filter(User__id=user_info.id)
            list1=[]
            subtotal=0
            for i in c1:
                list1.append(i.Prodect.p_price)
                subtotal+=i.subtotal
                obj=Order(product=i.Prodect,det=det_id,user=user_info,qyantity=i.quantity,total=i.subtotal)
                obj.save()
                print(obj,"oooooooooooooooooooooooooooooo")
            c1.delete()
            return redirect('paybutton')
            l1=sum(list1)
            con['Cart']=c1
            con['subtotal']=subtotal
            con['det']=det
        else:
            user=request.session['user']
            user_info=User.objects.get(Email=user)
            det=Detail.objects.filter(user=user_info)
            c1=Cart.objects.filter(User__id=user_info.id)
            list1=[]
            subtotal=0
            for i in c1:
                list1.append(i.Prodect.p_price)
                subtotal+=i.subtotal
            l1=sum(list1)
            con['Cart']=c1
            con['subtotal']=subtotal
            con['det']=det
        return render(request,'chackout.html',con)
    return render(request,'chackout.html',con)

def paybutton(request):
    return HttpResponse("<h3><a href='http://localhost:8000/payment'><button>PayNow</button></html></h3>")


def payment(request):
    total=request.session['subtotal']
    order_id = Checksum.__id_generator__()
    bill_amount = str(total)
    data_dict = {
        'MID': settings.PAYTM_MERCHANT_ID,
        'INDUSTRY_TYPE_ID': settings.PAYTM_INDUSTRY_TYPE_ID,
        'WEBSITE': settings.PAYTM_WEBSITE,
        'CHANNEL_ID': settings.PAYTM_CHANNEL_ID,
        'CALLBACK_URL': settings.PAYTM_CALLBACK_URL,
        'MOBILE_NO': '7405505665',
        'EMAIL': 'dhaval.savalia6@gmail.com',
        'CUST_ID': '123123',
        'ORDER_ID':order_id,
        'TXN_AMOUNT': bill_amount,
    } # This data should ideally come from database
    data_dict['CHECKSUMHASH'] = Checksum.generate_checksum(data_dict, settings.PAYTM_MERCHANT_KEY)
    context = {
        'payment_url': settings.PAYTM_PAYMENT_GATEWAY_URL,
        'comany_name': settings.PAYTM_COMPANY_NAME,
        'data_dict': data_dict
    }
    return render(request, 'payment.html', context)
   

@csrf_exempt
def response(request):
    resp = VerifyPaytmResponse(request)
    if resp['verified']:
        # save success details to db; details in resp['paytm']
        return HttpResponse("<center><h1>Transaction Successful</h1><center>", status=200)
    else:
        # check what happened; details in resp['paytm']
        return HttpResponse("<center><h1>Transaction Failed</h1><center>", status=400)

def order(request):
    if 'user' in request.session:
        user=request.session['user']
        user_info=User.objects.get(Email=user)
        data=Order.objects.filter(user__Email=user)
    else:
        return redirect('login')
    return render(request,'order.html',{'data':data})