from django.shortcuts import render, redirect
from django.http import HttpResponse
from . models import product, Contract, Order, OrderUpdate, User
from math import ceil
import json
from django.contrib import messages
from django.contrib.auth.models import User, auth
from django.contrib.auth import authenticate, login, logout

# Create your views here.

def index(request):
    #products = product.objects.all()
    #n = len(products)
    #nSlides= n//4 + ceil((n/4) - (n//4))
    #prams = {'no_of_slides': nSlides, 'range': range(nSlides), 'product': products}

    #allProds=[[products, range(1, (nSlides)), nSlides],[products, range(1, (nSlides)), nSlides]]
    #prams={'allProds':allProds }

    allProds = []
    catprods = product.objects.values('category', 'id')
    cats = {item['category'] for item in catprods}
    for cat in cats:
        prod = product.objects.filter(category=cat)
        n = len(prod)
        nSlides = n // 4 + ceil((n / 4) - (n // 4))
        allProds.append([prod, range(1, nSlides), nSlides])  

    prams = {'allProds': allProds}
    return render(request, "shop/index.html", prams)

def home(request):
    allProds = []
    catprods = product.objects.values('category', 'id')
    cats = {item['category'] for item in catprods}
    for cat in cats:
        prod = product.objects.filter(category=cat)
        n = len(prod)
        nSlides = n // 4 + ceil((n / 4) - (n // 4))
        allProds.append([prod, range(1, nSlides), nSlides])  

    prams = {'allProds': allProds}
    return render(request, "shop/index.html", prams)

def allprod(request, category):
    Category = product.objects.filter(category = category)
    return render(request, "shop/allProd.html", {'category':Category})

def searchMatch(queryy, item):
    if queryy in item.desc.lower() or queryy in item.product_name.lower() or queryy in item.category.lower():
        return True
    else:
        return False

def search(request):
    query= request.GET.get('search')
    queryy = query.casefold()
    allProds = []
    catprods = product.objects.values('category', 'id')
    cats = {item['category'] for item in catprods}
    for cat in cats:
        prodtemp = product.objects.filter(category=cat)
        prod=[item for item in prodtemp if searchMatch(queryy, item)]
        n = len(prod)
        nSlides = n // 4 + ceil((n / 4) - (n // 4))
        if len(prod) != 0:
            allProds.append([prod, range(1, nSlides), nSlides])
    params = {'allProds': allProds, "msg": ""}
    if len(allProds) == 0 or len(query)<4:
        params = {'msg': "Please make sure to enter relevant search query"}
    return render(request, 'shop/search.html', params)


def about(request):
    return render(request, "shop/about.html")

def contract(request):
    thank = False
    if request.method == "POST":
        name = request.POST.get('name', '')
        email = request.POST.get('email', '')
        phone = request.POST.get('phone', '')
        desc = request.POST.get('desc', '')
        contract = Contract(name=name, email=email, phone=phone, desc=desc)
        contract.save()

        thank = True

    return render(request, "shop/contract.html", {'thank': thank})

def tracker(request):
    if request.method=="POST":
        orderId = request.POST.get('orderId', '')
        email = request.POST.get('email', '')
        try:
            order = Order.objects.filter(order_id=orderId, email=email)
            if len(order)>0:
                update = OrderUpdate.objects.filter(order_id=orderId)
                updates = []
                for item in update:
                    updates.append({'text': item.update_desc, 'time': item.timestamp})
                    response = json.dumps({"status":"success", "updates": updates, "itemsJson": order[0].items_json}, default=str)
                return HttpResponse(response)
            else:
                return HttpResponse('{"status":"noitem"}')
        except Exception as e:
            return HttpResponse('{"status":"error"}')

    return render(request, 'shop/tracker.html')



def productview(request, myid):
    Product = product.objects.filter(id = myid)
    return render(request, "shop/productview.html", {'product':Product[0]})


def checkout(request):
    if request.method=="POST":
        items_json = request.POST.get('itemsJson', '')
        name = request.POST.get('name', '')
        amount = request.POST.get('amount', '')
        email = request.POST.get('email', '')
        address = request.POST.get('address1', '') + "   " + request.POST.get('address2', '')
        city = request.POST.get('city', '')
        state = request.POST.get('state', '')
        zip_code = request.POST.get('zip_code', '')
        phone = request.POST.get('phone1', '') + "   " + request.POST.get('phone2', '')
        order = Order(items_json=items_json, name=name, email=email, address=address, city=city,
                       state=state, zip_code=zip_code, phone=phone, amount=amount)
        order.save()

        update = OrderUpdate(order_id=order.order_id, update_desc="The order has been placed")
        update.save()

        thank = True
        id = order.order_id
        return render(request, 'shop/checkout.html', {'thank':thank, 'id': id})
    return render(request, "shop/checkout.html")



def register(request):
    if request.method == 'POST':
        first_name = request.POST['first_name']
        last_name = request.POST['last_name']
        email = request.POST['email']
        username = request.POST['username']
        password1 = request.POST['password1']
        password2 = request.POST['password2']

        if len(username)<10:
            messages.error(request, " Your user name must be under 10 characters")
            return redirect('home')

        if not username.isalnum():
            messages.error(request, " User name should only contain letters and numbers")
            return redirect('home')
        if (password1!= password2):
             messages.error(request, " Passwords do not match")
             return redirect('home')

        myuser = User.objects.create_user(username, email, password1)
        myuser.first_name= first_name
        myuser.last_name= last_name
        myuser.save()
        messages.success(request, " Your account has been successfully created")
        return redirect('login')
       
    return render(request, 'shop/register.html') 
        

def login(request):
    if request.method=="POST":
        # Get the post parameters
        loginusername=request.POST['loginusername']
        loginpassword=request.POST['loginpassword']

        user=authenticate(username= loginusername, password= loginpassword)

        if user is not None:
            auth.login(request, user)
            messages.success(request, "Successfully Logged In")
            return redirect("home")
        else:
            messages.error(request, "Invalid credentials! Please try again")
            return redirect("login")
    else:
       return render(request, 'shop/login.html') 

def logout(request):
    auth.logout(request)
    messages.success(request, "Successfully Logged Out")
    return redirect('home')

