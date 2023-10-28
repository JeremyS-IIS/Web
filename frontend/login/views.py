from django.shortcuts import render, HttpResponse

def login_page(request):
    return HttpResponse("Hello world from login!!")