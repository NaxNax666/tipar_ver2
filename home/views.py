from django.http.response import HttpResponseRedirect
from django.shortcuts import render, redirect

from django.contrib.auth.models import User
from . models import *
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from . contract_buffer import Contracts
from web3 import Web3
from datetime import datetime
from . youmoney_module import popolny, check_payment, getamount
from time import sleep


def index(request):
    cars = Car.objects.all()
    return render(request, "index.html", {'cars':cars})

def customer_signup(request):
    if request.user.is_authenticated:
        return redirect("/")
    if request.method == "POST":
        username = request.POST['username']
        email = request.POST['email']
        first_name = request.POST['first_name']
        last_name = request.POST['last_name']
        password1 = request.POST['password1']
        password2 = request.POST['password2']
        phone = request.POST['phone']
        city = request.POST['city']

        if password1 != password2:
            return redirect("/customer_signup")

        user = User.objects.create_user(username=username, email=email, first_name=first_name, last_name=last_name, password=password1)
        user.save()
        try:
            location = Location.objects.get(city=city.lower())
        except:
            location = None
        if location is not None:
            customer = Customer(user=user, phone=phone, location=location, type="Customer")
        else:
            location = Location(city=city.lower())
            location.save()
            location = Location.objects.get(city=city.lower())
            customer = Customer(user=user, phone=phone, location=location, type="Customer")
        eth_inst = Contracts()
        acc=eth_inst.sign_up()
        addr = acc.address
        pk = Web3.to_hex(acc.key)
        etheraccountcustomer = EtherAccountCustomer(customer=user, address=addr, private_key=pk)
        etheraccountcustomer.save()
        customer.save()
        alert = True
        return render(request, "customer_signup.html", {'alert':alert})
    return render(request, "customer_signup.html")

def customer_login(request):
    if request.user.is_authenticated:
        return redirect("/")
    else:
        if request.method == "POST":
            username = request.POST['username']
            password = request.POST['password']
            user = authenticate(username=username, password=password)

            if user is not None:
                user1 = Customer.objects.get(user=user)
                if user1.type == "Customer":
                    login(request, user)
                    return redirect("/customer_homepage")
            else:
                alert = True
                return render(request, "customer_login.html", {'alert':alert})
    return render(request, "customer_login.html")

def car_dealer_signup(request):
    if request.method == "POST":
        username = request.POST['username']
        first_name = request.POST['first_name']
        last_name = request.POST['last_name']
        email = request.POST['email']
        city = request.POST['city']
        phone = request.POST['phone']
        password1 = request.POST['password1']
        password2 = request.POST['password2']

        if password1 != password2:
            return redirect('/car_dealer_signup')

        user = User.objects.create_user(username=username, email=email, first_name=first_name, last_name=last_name, password=password1)
        user.save()
        try:
            location = Location.objects.get(city = city.lower())
        except:
            location = None
        if location is not None:
            car_dealer = CarDealer(car_dealer=user, phone=phone, location=location, type="Car Dealer")
        else:
            location = Location(city = city.lower())
            location.save()
            location = Location.objects.get(city = city.lower())
            car_dealer = CarDealer(car_dealer = user, phone=phone, location=location, type="Car Dealer")
        Eth_inst = Contracts()
        acc=Eth_inst.sign_up()
        addr = acc.address
        pk = Web3.to_hex(acc.key)
        car_dealer.save()
        etheraccountcardealer = EtherAccountCarDealer(car_dealer = car_dealer, address = addr, private_key=pk)
        etheraccountcardealer.save()

        return render(request, "car_dealer_login.html")
    return render(request, "car_dealer_signup.html")

def car_dealer_login(request):
    if request.user.is_authenticated:
        return redirect("/")
    else:
        if request.method == "POST":
            username = request.POST['username']
            password = request.POST['password']
            user = authenticate(username=username, password=password)

            if user is not None:
                user1 = CarDealer.objects.get(car_dealer=user)
                if user1.type == "Car Dealer":
                    login(request, user)
                    return redirect("/all_cars")
                else:
                    alert = True
                    return render(request, "car_dealer_login.html", {"alert":alert})
    return render(request, "car_dealer_login.html")

def signout(request):
    logout(request)
    return redirect('/')

def add_car(request):
    if request.method == "POST":
        car_name = request.POST['car_name']
        city = request.POST['city']
        image = request.FILES['image']
        capacity = request.POST['capacity']
        rent = request.POST['rent']
        car_dealer = CarDealer.objects.get(car_dealer=request.user)
        try:
            location = Location.objects.get(city=city)
        except:
            location = None
        if location is not None:
            car = Car(name=car_name, car_dealer=car_dealer, location=location, capacity=capacity, image=image, rent=rent)
        else:
            location = Location(city=city)
            car = Car(name=car_name, car_dealer=car_dealer, location=location, capacity=capacity, image=image, rent=rent)
        car.save()
        alert = True
        return render(request, "add_car.html", {'alert':alert})
    return render(request, "add_car.html")

def all_cars(request):
    dealer = CarDealer.objects.filter(car_dealer=request.user).first()
    cars = Car.objects.filter(car_dealer=dealer)
    return render(request, "all_cars.html", {'cars':cars})

def edit_car(request, myid):
    car = Car.objects.filter(id=myid)[0]
    if request.method == "POST":
        car_name = request.POST['car_name']
        city = request.POST['city']
        capacity = request.POST['capacity']
        rent = request.POST['rent']

        car.name = car_name
        car.city = city
        car.capacity = capacity
        car.rent = rent
        car.save()

        try:
            image = request.FILES['image']
            car.image = image
            car.save()
        except:
            pass
        alert = True
        return render(request, "edit_car.html", {'alert':alert})
    return render(request, "edit_car.html", {'car':car})

def delete_car(request, myid):
    if not request.user.is_authenticated:
        return redirect("/car_dealer_login")
    car = Car.objects.filter(id=myid)
    car.delete()
    return redirect("/all_cars")

def customer_homepage(request):
    return render(request, "customer_homepage.html")

def search_results(request):
    city = request.POST['city']
    city = city.lower()
    vehicles_list = []
    location = Location.objects.filter(city = city)
    for a in location:
        cars = Car.objects.filter(location=a)
        for car in cars:
            if car.is_available == True:
                vehicle_dictionary = {'name':car.name, 'id':car.id, 'image':car.image.url, 'city':car.location.city,'capacity':car.capacity}
                vehicles_list.append(vehicle_dictionary)
    request.session['vehicles_list'] = vehicles_list
    return render(request, "search_results.html")

def car_rent(request):
    id = request.POST['id']
    car = Car.objects.get(id=id)
    cost_per_day = int(car.rent)
    return render(request, 'car_rent.html', {'car':car, 'cost_per_day':cost_per_day})

def order_details(request):
    car_id = request.POST['id']
    username = request.user
    user = User.objects.get(username=username)
    days = request.POST['days']
    car = Car.objects.get(id=car_id)
    if car.is_available:
        car_dealer = car.car_dealer
        seller_tb = EtherAccountCarDealer.objects.get(car_dealer = car_dealer)
        buyer_tb = EtherAccountCustomer.objects.get(customer = user)

        seller = {
        'private_key': seller_tb.private_key,
        'address': seller_tb.address,
        }
        buyer = {
            'private_key': buyer_tb.private_key,
            'address': buyer_tb.address,
        }
        rent = int(car.rent)*int(days)
        car_dealer.earnings += rent
        car_dealer.save()
        date_time = datetime.now().strftime("%Y-%m-%d")
        try:
            Eth_instance = Contracts()
            result_list = Eth_instance.start_rent(seller, buyer, int(car.rent), int(days), car)
            order = Order(car=car, car_dealer=car_dealer, user=user, rent=rent, days=days, smart_contract_address = result_list[1], start_date = date_time)
            order.save()
            tx_hash = result_list[0]
            tx_hist = TX_history(order=order, tx_hash=tx_hash)
            tx_hist.save()
        except:
            order = Order.objects.get(car=car, car_dealer=car_dealer, user=user, rent=rent, days=days, smart_contract_address = "", start_date="2022-01-01")


        car.is_available = False
        car.save()
        return render(request, "order_details.html", {'order':order})
    return render(request, "order_details.html")

def past_orders(request):
    all_orders = []
    user = User.objects.get(username=request.user)
    try:
        orders = Order.objects.filter(user=user)
    except:
        orders = None
    if orders is not None:
        for order in orders:
            if order.is_complete == False:
                order_dictionary = {'id':order.id, 'rent':order.rent, 'car':order.car, 'start_date': order.start_date, 'days':order.days, 'car_dealer':order.car_dealer, 'address':order.smart_contract_address}
                all_orders.append(order_dictionary)
    return render(request, "past_orders.html", {'all_orders':all_orders})

def delete_order(request, myid):
    order = Order.objects.filter(id=myid)
    order.delete()
    return redirect("/past_orders")

def all_orders(request):
    username = request.user
    user = User.objects.get(username=username)
    car_dealer = CarDealer.objects.get(car_dealer=user)
    orders = Order.objects.filter(car_dealer=car_dealer)
    all_orders = []
    for order in orders:
        if order.is_complete == False:
            all_orders.append(order)
    return render(request, "all_orders.html", {'all_orders':all_orders})

def complete_order(request):
    order_id = request.POST['id']
    order = Order.objects.get(id=order_id)
    car = order.car
    car_dealer = car.car_dealer
    seller_tb = EtherAccountCarDealer.objects.get(car_dealer=car_dealer)
    seller = {
        'private_key': seller_tb.private_key,
        'address': seller_tb.address,
    }
    Eth_instance = Contracts()
    tx_hash = Eth_instance.endRental(seller, order.smart_contract_address)

    order.is_complete = True
    order.save()
    tx_hist = TX_history(order = order, tx_hash = tx_hash)
    tx_hist.save()
    car.is_available = True
    car.save()
    return HttpResponseRedirect('/all_orders/')

def breake_order(request):
    order_id = request.POST['id']
    order = Order.objects.get(id=order_id)
    car = order.car
    st_date = order.start_date
    car_dealer = car.car_dealer
    seller_tb = EtherAccountCarDealer.objects.get(car_dealer=car_dealer)
    seller = {
        'private_key': seller_tb.private_key,
        'address': seller_tb.address,
    }
    curr_time = datetime.now()
    delta = curr_time - datetime.strptime(st_date, "%Y-%m-%d")
    summ_to_return = int(order.rent) - int(car.rent) * delta.days
    Eth_instance = Contracts()
    tx_hash = Eth_instance.breakRental(seller, order.smart_contract_address, summ_to_return)
    order.is_complete = True
    order.save()
    tx_hist = TX_history(order = order, tx_hash = tx_hash)
    tx_hist.save()
    car.is_available = True
    car.save()
    return HttpResponseRedirect('/all_orders/')

def earnings(request):
    username = request.user
    user = User.objects.get(username=username)
    car_dealer = CarDealer.objects.get(car_dealer=user)
    orders = Order.objects.filter(car_dealer=car_dealer)
    all_orders = []
    for order in orders:
        all_orders.append(order)
    return render(request, "earnings.html", {'amount':car_dealer.earnings, 'all_orders':all_orders})

def connect_metamask(request):
    return render(request, "mtmsk.html")

def getInform(request):
    eth_inst = Contracts()
    if not request.user.is_authenticated:
        return redirect("/")
    if request.method == "POST":
        tx_hash = request.POST["hash"]
        res = eth_inst.getreipt(tx_hash)
        return render(request, "result.html", {'res': res})
    username = request.user
    user = User.objects.get(username=username)
    try:
        car_dealer = CarDealer.objects.get(car_dealer=user)
        buff = EtherAccountCarDealer.objects.get(car_dealer=car_dealer)
    except:
        buff = EtherAccountCustomer.objects.get(customer = user)
    res = eth_inst.getbalance(buff.address)
    return render(request, "info.html", {'balance': res})

k=0
def payment(request):
    print("start")
    global k
    k+=1
    global buff_am
    eth_inst = Contracts()
    if not request.user.is_authenticated:
        return redirect("/")
    if request.method == "POST":
        amount = request.POST["amount"]
        buff_am=amount
        url_list = popolny(amount, request.user)
        return HttpResponseRedirect(url_list[0])
    username = request.user
    user = User.objects.get(username=username)
    try:
        car_dealer = CarDealer.objects.get(car_dealer=user)
        buff = EtherAccountCarDealer.objects.get(car_dealer=car_dealer)
        print('kk')

    except:
        buff = EtherAccountCustomer.objects.get(customer = user)
    if not check_payment(request.user):
        sleep(10)
        print(k)
        return redirect("/payment")
    get_amount = getamount(request.user)
    print(f'if out, \n {get_amount}')
    res = eth_inst.transfer(buff.address, get_amount)
    print('if after')
    return render(request, "success.html", {'hash': res})