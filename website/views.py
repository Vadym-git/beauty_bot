from django.shortcuts import render, HttpResponse, HttpResponseRedirect
from django.urls import reverse
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.models import User
import time
from beauty.models import Business, ServiceType
from .forms import BusinessForm, ServiceTypeForm


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
    services = ServiceType.objects.filter(owner=Business.objects.get(owner=request.user)).order_by('-id')
    return render(request, 'website/services.html', context={'service_data': ServiceTypeForm, 'services': services})


def user_account(request):
    if not request.user.is_authenticated:
        return HttpResponseRedirect(reverse(login_view))
    account_object = Business.objects.get(owner=request.user.id)
    if request.POST:
        form = BusinessForm(request.POST, instance=account_object)
        if form.is_valid():
            name = form.cleaned_data['name'].lower()
            city = form.cleaned_data['city'].lower()
            account_object.name = name
            account_object.city = city
            account_object.save()
            return HttpResponseRedirect(reverse(user_account))
    return render(request, 'website/account.html',
                  context={'service_data': BusinessForm(instance=account_object), 'error': 'error'})


def registration_view(request):
    if request.user.is_authenticated:
        return HttpResponseRedirect(reverse(user_account))
    if request.POST:
        try:
            email = request.POST['email']
            password = request.POST['password']
            repassword = request.POST['repassword']
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
            service = Business(owner=user)
            service.save()
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


def logout_view(request):
    logout(request)
    return HttpResponseRedirect(reverse(index_view))
