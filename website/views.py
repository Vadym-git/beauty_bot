from django.shortcuts import render, HttpResponse, HttpResponseRedirect
from django.urls import reverse
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.models import User
import time
from beauty.models import Business, ServiceType, City, Counties
from service_bot.settings import BASE_DIR
from .forms import BusinessForm, ServiceTypeForm
import json


# Create your views here.

def index_view(request):
    return render(request, 'website/index.html')


def edit_service(request, id):
    if not request.user.is_authenticated:
        return HttpResponseRedirect(reverse(login_view))
    data = ServiceType.objects.get(pk=id)
    if request.POST:
        form = ServiceTypeForm(request.POST, instance=data)
        if form.is_valid():
            data.save()
            return HttpResponseRedirect(reverse(services_view))
    return render(request, 'website/edit-service.html', context={
        'service_data': ServiceTypeForm(instance=data)})


def delete_service(request, s_id):
    try:
        service = ServiceType.objects.get(id=s_id)
        if service.owner.owner.id == request.user.id:
            service.delete()
    except Exception as es:
        pass
    return HttpResponseRedirect(reverse(services_view))


def services_view(request):
    if not request.user.is_authenticated:
        return HttpResponseRedirect(reverse(login_view))
    if request.POST:
        form = ServiceTypeForm(request.POST)
        if form.is_valid():
            name = form.cleaned_data['name']
            price = form.cleaned_data['price']
            description = form.cleaned_data['description']
            owner = Business.objects.get(owner=request.user)
            ServiceType(name=name, price=price, owner=owner, description=description).save()
            return HttpResponseRedirect(reverse(services_view))
    services = ServiceType.objects.filter(owner=Business.objects.get(owner=request.user)).order_by('-id')
    return render(request, 'website/services.html', context={'service_data': ServiceTypeForm, 'services': services})


def user_account(request):
    if not request.user.is_authenticated:
        return HttpResponseRedirect(reverse(login_view))
    try:
        account_object = Business.objects.get(owner=request.user)
    except Business.DoesNotExist:
        account_object = Business(owner=request.user)
        account_object.save()
    if request.POST:
        form = BusinessForm(request.POST)
        if form.is_valid():
            account_object.name = form.cleaned_data['name'].lower()
            account_object.city = form.cleaned_data['city']
            account_object.type_of_business = form.cleaned_data['type_of_business']
            account_object.county = form.cleaned_data['county']
            account_object.about = form.cleaned_data['about']
            account_object.email = form.cleaned_data['email']
            try:
                account_object.phone = form.cleaned_data['phone'].lower()
            except AttributeError:
                account_object.phone = form.cleaned_data['phone']
            try:
                account_object.telegram = form.cleaned_data['telegram'].lower()
            except AttributeError:
                account_object.telegram = form.cleaned_data['telegram']
            try:
                account_object.insta = form.cleaned_data['insta'].lower()
            except AttributeError:
                account_object.insta = form.cleaned_data['insta']
            account_object.save()
            return HttpResponseRedirect(reverse(user_account))
    return render(request, 'website/account.html',
                  context={'service_data': BusinessForm(instance=account_object)})


def registration_view(request):
    if request.user.is_authenticated:
        return HttpResponseRedirect(reverse(user_account))
    if request.POST:
        try:
            email = request.POST['email']
            password = request.POST['password']
            repassword = request.POST['repassword']
            policy = request.POST['policy']
        except KeyError:
            return render(request, 'website/registration.html', context={'error': 'Something went wrong'})
        if password != repassword:
            return render(request, 'website/registration.html',
                          context={'error': 'Паролі не співпадають'})
        try:
            user = User.objects.get(email=email)
        except User.DoesNotExist:
            user = User.objects.create_user(round(time.time() * 10000), email, password, )
            user.is_active = True
            user.save()
            return HttpResponseRedirect(reverse(login_view))

        #  если юзер с таким имейлом существует
        return render(request, 'website/registration.html',
                      context={'error': 'Ви не можете бути зареєстровані з цією імейл адресою!'})
    return render(request, 'website/registration.html')


def login_view(request):
    if request.user.is_authenticated:
        return HttpResponseRedirect(reverse(user_account))
    if request.POST:
        try:
            email = request.POST['email']
            password = request.POST['password']
        except KeyError:
            return render(request, 'website/login.html', context={'error': 'Something went wrong'})
        try:
            request_user = User.objects.get(email=email)
            user = authenticate(username=request_user.username, password=password)
        except User.DoesNotExist:
            user = None
        if user:
            login(request, user)
            request.session.set_expiry(3600)
            return HttpResponseRedirect(reverse(user_account))
        else:
            return render(request, 'website/login.html', context={'error': 'Невірний імейл чи пароль'})
    return render(request, 'website/login.html')


def policy(request):
    return render(request, 'website/policy.html')


def logout_view(request):
    logout(request)
    return HttpResponseRedirect(reverse(index_view))


def add_cities(request):
    if not request.user.is_superuser:
        return HttpResponseRedirect(reverse(index_view))
    with open(BASE_DIR / '../cities.json') as f:
        data = json.load(f)
        for county in data:
            try:
                print(county)
                county = Counties.objects.get(name=county)
                if county:
                    cities = data[county.name]
                    for city in cities:
                        if 'environs' in city:
                            continue
                        if len(city) > 32:
                            continue
                        try:
                            city = City.objects.get(name=city)
                        except City.DoesNotExist:
                            ncity = City()
                            ncity.name = city
                            ncity.county = county
                            ncity.save()
                        except City.MultipleObjectsReturned:
                            pass
            except Counties.DoesNotExist:
                ncounty = Counties()
                ncounty.name = county
                ncounty.save()
                for city in data[county]:
                    if 'environs' in city:
                        continue
                    ncity = City()
                    ncity.name = city
                    ncity.county = ncounty
                    ncity.save()
    return HttpResponse('Success', status=200)


def get_cities(request, county: str):
    cities = City.objects.filter(county=county).distinct().order_by('name')
    cities = [[i.id, i.name] for i in cities]
    return HttpResponse(json.dumps(cities))
