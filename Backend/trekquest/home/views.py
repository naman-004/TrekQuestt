from django.shortcuts import render

# Create your views here.

def resregister(request):
    return render(request, 'customer-registration.html')

def reslogin(request):
    return render(request, 'customer-login.html')

