from django.shortcuts import render
from .models import Product,Contact,Order,OrderUpdate
from math import ceil
import json
from django.http import HttpResponse
from django.conf import settings
from django.core.mail import send_mail
from django.http import HttpResponse


# Create your views here.
def index(request):
    # prod = Product.objects.all()
    # n = len(prod)
    # slides = n//4 + ceil((n/4) + (n//4))
    allProd = []
    category = Product.objects.values('category','id')
    catprod = {item['category'] for item in category}
    for cat in catprod:
        product = Product.objects.filter(category=cat)
        n = len(product)
        slides = n//4 + ceil((n/4) + (n//4))
        allProd.append([product,range(1,slides),slides])
   
    params = {'allProd': allProd}
    return render(request,'AqeelShop/index.html',params)

def SearchQuery(query,item):
    if query in item.product_name or query in item.category:
        return True
    else:
        return False

def search(request):
    query = request.GET.get('search')
    allProd = []
    category = Product.objects.values('category','id')
    catprod = {item['category'] for item in category}
    for cat in catprod:
        producttemp = Product.objects.filter(category=cat)
        product = [item for item in producttemp if SearchQuery(query,item)]
        n = len(product)

        slides = n//4 + ceil((n/4) + (n//4))
        if len(product)!= 0:
            allProd.append([product,range(1,slides),slides])
    params = {'allProd': allProd}
    if len(allProd) == 0 or len(query)<4:
            params = {'allProd': allProd,'msg': "Please make sure to enter relevant search query"}
    return render(request,'AqeelShop/search.html',params)

def about(request):
    return render(request,'AqeelShop/about.html')

def contact(request):

    if request.method == "POST":
        name = request.POST.get('name','')
        email = [request.POST.get('email','')]
        phone = request.POST.get('phone','')
        desc = request.POST.get('desc','')
        contact = Contact(name = name, email = email, phone = phone,desc = desc)
        contact.save()
        from_email = settings.EMAIL_HOST_USER
        
        try:
            # Send email
            send_mail(
                'Thank You for Your Submission',
                desc,
                from_email,
                email,
                fail_silently=False,  # Set to True if you don't want to raise exceptions
            )
            return HttpResponse('Email sent successfully!')
        except Exception as e:
            return HttpResponse('An error occurred while sending the email: ' + str(e))
    
    return render(request,'AqeelShop/contact.html')

def tracker(request):
    if request.method =="POST":
        orderId = request.POST.get('orderId', '')
        email = request.POST.get('email', '')
        try:
            order = Order.objects.filter(order_id = orderId, email = email)
            if len(order) > 0:
                update = OrderUpdate.objects.filter(order_id = orderId)
                updates = []
                for item in update:
                    updates.append({'text': item.update_desc, 'time': item.timestamp})
                    response = json.dumps({"status": "Success", "updates": updates,"itemJson" :order[0].item_json}, default=str)
                return HttpResponse(response)
            else:
                return HttpResponse('{"status": "No Item"}')
        except Exception as e:
            return HttpResponse('{"status": "Error"}')
    return render(request,'AqeelShop/tracker.html')

def checkout(request):
    if request.method=="POST":
        item_json = request.POST.get('item_json', '')
        name = request.POST.get('name', '')
        amount = request.POST.get('amount', '')
        email = request.POST.get('email', '')
        address = request.POST.get('address1', '') + " " + request.POST.get('address2', '')
        city = request.POST.get('city', '')
        state = request.POST.get('state', '')
        zip_code = request.POST.get('zip_code', '')
        phone = request.POST.get('phone', '')

        order = Order(item_json = item_json, name = name, email = email, address = address, city = city, state = state, zipcode = zip_code, phone = phone, amount = amount)
        order.save()
        update = OrderUpdate(order_id = order.order_id,update_desc = "Your Order has been placed")
        update.save()
        thank = True
        id = order.order_id
        return render(request, 'AqeelShop/checkout.html', {'thank':thank, 'id':id})
    return render(request, 'AqeelShop/checkout.html')
def prodviews(request,id):
    #Fetch the product using ID
    product = Product.objects.filter(id=id)
    return render(request,'AqeelShop/productview.html',{'product':product[0]})
