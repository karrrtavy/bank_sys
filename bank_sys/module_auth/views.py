from django.shortcuts import render, redirect

# Create your views here.
def register(request):
    return render(request, 'module_auth\sugn_up.html')

def login(request):
    return render(request, 'module_auth\sign_in.html')